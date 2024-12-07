//! A minimal RaBitQ implementation for top-1 retrieval.

use core::f32;
use std::sync::atomic::{AtomicU64, Ordering};

use faer::row::from_slice as row_from_slice;
use faer::{Col, Mat, MatRef, Row};
use rand::distributions::Distribution;
use rand_distr::StandardNormal;

use crate::distance::squared_euclidean;

const DEFAULT_X_DOT_PRODUCT: f32 = 0.8;
const EPSILON: f32 = 1.9;
pub(crate) const THETA_LOG_DIM: usize = 4;
const SCALAR: f32 = 1.0 / ((1 << THETA_LOG_DIM) as f32 - 1.0);

/// Factor struct to store the metadata for centroids.
#[derive(Debug, Clone, Copy, Default)]
#[repr(C)]
pub struct Factor {
    /// ip
    pub factor_ip: f32,
    /// ppc
    pub factor_ppc: f32,
    /// error bound
    pub error_bound: f32,
    /// (x - c) ** 2
    pub center_distance_square: f32,
}

impl Factor {
    #[allow(dead_code)]
    fn into_vec(self) -> Vec<f32> {
        vec![
            self.factor_ip,
            self.factor_ppc,
            self.error_bound,
            self.center_distance_square,
        ]
    }
}

impl From<Vec<f32>> for Factor {
    fn from(f32s: Vec<f32>) -> Self {
        assert_eq!(f32s.len(), 4);
        Self {
            factor_ip: f32s[0],
            factor_ppc: f32s[1],
            error_bound: f32s[2],
            center_distance_square: f32s[3],
        }
    }
}

/// Convert the vector to binary format and store in a u64 vector.
#[inline]
pub fn vector_binarize_u64(vec: &[f32]) -> Vec<u64> {
    let mut binary = vec![0u64; vec.len().div_ceil(64)];
    for (i, &v) in vec.iter().enumerate() {
        if v > 0.0 {
            binary[i / 64] |= 1 << (i % 64);
        }
    }
    binary
}

/// Convert the vector to +1/-1 format.
#[inline]
pub fn vector_binarize_one(vec: &[f32]) -> Col<f32> {
    Col::from_fn(vec.len(), |i| if vec[i] > 0.0 { 1.0 } else { -1.0 })
}

/// Project the vector to the orthogonal matrix.
#[inline]
pub fn project(vec: &[f32], orthogonal: &MatRef<f32>) -> Col<f32> {
    #[cfg(any(target_arch = "x86_64", target_arch = "x86"))]
    {
        if is_x86_feature_detected!("avx2") {
            Col::from_fn(orthogonal.ncols(), |i| unsafe {
                crate::simd::dot_product(
                    vec,
                    orthogonal
                        .col(i)
                        .try_as_slice()
                        .expect("failed to get orthogonal slice"),
                )
            })
        } else {
            (row_from_slice(vec) * orthogonal).transpose().to_owned()
        }
    }
    #[cfg(not(any(target_arch = "x86_64", target_arch = "x86")))]
    {
        (row_from_slice(vec) * orthogonal).transpose().to_owned()
    }
}

// Get the min/max value of the residual of two vectors.
fn min_max_raw(res: &mut [f32], x: &[f32], y: &[f32]) -> (f32, f32) {
    let mut min = f32::MAX;
    let mut max = f32::MIN;
    for i in 0..res.len() {
        res[i] = x[i] - y[i];
        if res[i] < min {
            min = res[i];
        }
        if res[i] > max {
            max = res[i];
        }
    }
    (min, max)
}

/// Interface of `min_max_residual`: get the min/max value of the residual of two vectors.
#[inline]
pub fn min_max_residual(res: &mut [f32], x: &[f32], y: &[f32]) -> (f32, f32) {
    #[cfg(any(target_arch = "x86_64", target_arch = "x86"))]
    {
        if is_x86_feature_detected!("avx") {
            unsafe { crate::simd::min_max_residual(res, x, y) }
        } else {
            min_max_raw(res, x, y)
        }
    }
    #[cfg(not(any(target_arch = "x86_64", target_arch = "x86")))]
    {
        min_max_raw(res, x, y)
    }
}

// Quantize the query residual vector.
fn scalar_quantize_raw(
    quantized: &mut [u8],
    vec: &[f32],
    lower_bound: f32,
    multiplier: f32,
) -> u32 {
    let mut sum = 0u32;
    for i in 0..quantized.len() {
        let q = ((vec[i] - lower_bound) * multiplier).round() as u8;
        quantized[i] = q;
        sum += q as u32;
    }
    sum
}

/// Interface of `scalar_quantize`: scale vector to u8.
#[inline]
pub fn scalar_quantize(
    quantized: &mut [u8],
    vec: &[f32],
    lower_bound: f32,
    multiplier: f32,
) -> u32 {
    #[cfg(any(target_arch = "x86_64", target_arch = "x86"))]
    {
        if is_x86_feature_detected!("avx2") {
            unsafe { crate::simd::scalar_quantize(quantized, vec, lower_bound, multiplier) }
        } else {
            scalar_quantize_raw(quantized, vec, lower_bound, multiplier)
        }
    }
    #[cfg(not(any(target_arch = "x86_64", target_arch = "x86")))]
    {
        scalar_quantize_raw(quantized, vec, lower_bound, multiplier)
    }
}

/// Convert the vector to binary format (one value to multiple bits) and store in a u64 vector.
#[inline]
fn vector_binarize_query_raw(vec: &[u8], binary: &mut [u64]) {
    let length = vec.len();
    for j in 0..THETA_LOG_DIM {
        for i in 0..length {
            binary[(i + j * length) / 64] |= (((vec[i] >> j) & 1) as u64) << (i % 64);
        }
    }
}

/// Interface of `vector_binarize_query`
#[inline]
pub fn vector_binarize_query(vec: &[u8], binary: &mut [u64]) {
    #[cfg(any(target_arch = "x86_64", target_arch = "x86"))]
    {
        if is_x86_feature_detected!("avx2") {
            unsafe {
                crate::simd::vector_binarize_query(vec, binary);
            }
        } else {
            vector_binarize_query_raw(vec, binary);
        }
    }
    #[cfg(not(any(target_arch = "x86_64", target_arch = "x86")))]
    {
        vector_binarize_query_raw(vec, binary);
    }
}

/// Calculate the dot product of two binary vectors.
#[inline]
fn binary_dot_product(x: &[u64], y: &[u64]) -> u32 {
    let mut res = 0;
    for i in 0..x.len() {
        res += (x[i] & y[i]).count_ones();
    }
    res
}

/// Calculate the dot product of two binary vectors with different lengths.
///
/// The length of `y` should be `x.len() * THETA_LOG_DIM`.
#[inline]
pub fn asymmetric_binary_dot_product(x: &[u64], y: &[u64]) -> u32 {
    let mut res = 0;
    let length = x.len();
    let mut y_slice = y;
    for i in 0..THETA_LOG_DIM {
        res += {
            #[cfg(any(target_arch = "x86_64", target_arch = "x86"))]
            {
                if is_x86_feature_detected!("avx2") {
                    unsafe { crate::simd::binary_dot_product(x, y_slice) << i }
                } else {
                    binary_dot_product(x, y_slice) << i
                }
            }
            #[cfg(not(any(target_arch = "x86_64", target_arch = "x86")))]
            {
                binary_dot_product(x, y_slice) << i
            }
        };
        y_slice = &y_slice[length..];
    }
    res
}

#[derive(Debug, Default)]
struct Metrics {
    pub rough: AtomicU64,
    pub precise: AtomicU64,
}

impl Metrics {
    pub fn update(&self, rough: u64, precise: u64) {
        self.rough.fetch_add(rough, Ordering::Relaxed);
        self.precise.fetch_add(precise, Ordering::Relaxed);
    }

    pub fn fetch(&self) -> (u64, u64) {
        (
            self.rough.load(Ordering::Relaxed),
            self.precise.load(Ordering::Relaxed),
        )
    }
}

/// RaBitQ struct for top-1 retrieval.
pub struct RaBitQ {
    centroids: Mat<f32>,
    mean: Row<f32>,
    orthogonal: Mat<f32>,
    factors: Vec<Factor>,
    binary_vec: Vec<u64>,
    idx: Vec<usize>,
    dim: usize,
    metrics: Metrics,
}

impl RaBitQ {
    /// Create a new RaBitQ instance.
    pub fn new(centroids: &[f32], dim: usize) -> Self {
        // init
        let num = centroids.len() / dim;
        let dim_pad = dim.div_ceil(64) * 64;
        let centroids_mat = Mat::from_fn(num, dim_pad, |i, j| match j < dim {
            true => centroids[i * dim + j],
            false => 0.0,
        });
        let dim_sqrt = (dim_pad as f32).sqrt();

        // orthogonal matrix
        let mut rng = rand::thread_rng();
        let random: Mat<f32> =
            Mat::from_fn(dim_pad, dim_pad, |_, _| StandardNormal.sample(&mut rng));
        let orthogonal = random.qr().compute_q();
        // let orthogonal = Mat::identity(dim_pad, dim_pad);

        let projected = &centroids_mat * &orthogonal;
        let mut factors = vec![Factor::default(); num];
        let mut xc_distances = vec![0.0; num];
        let mut x_dot_product = vec![0.0; num];
        let mut binary_vec = Vec::with_capacity(num);
        let mut signed_vec = Vec::with_capacity(num);
        let mut mean = Row::zeros(dim_pad);
        for v in projected.row_iter() {
            mean += v;
        }
        mean.iter_mut().for_each(|v| *v /= num as f32);

        // factors
        for (i, p) in projected.row_iter().enumerate() {
            let xc = p - &mean;
            xc_distances[i] = xc.norm_l2();
            factors[i].center_distance_square = xc_distances[i].powi(2);
            binary_vec.push(vector_binarize_u64(xc.as_slice()));
            signed_vec.push(vector_binarize_one(xc.as_slice()));
            let norm = xc_distances[i] * dim_sqrt;
            x_dot_product[i] = match norm.is_normal() {
                true => &xc * &signed_vec[i] / norm,
                false => DEFAULT_X_DOT_PRODUCT,
            };
        }

        let error_base = 2.0 * EPSILON / (dim_pad as f32 - 1.0).sqrt();
        let one_vec: Row<f32> = Row::ones(dim_pad);
        for i in 0..num {
            let xc_over_ip = xc_distances[i] / x_dot_product[i];
            let factor = &mut factors[i];
            factor.error_bound =
                error_base * (xc_over_ip * xc_over_ip - factor.center_distance_square).sqrt();
            factor.factor_ip = -2.0 / dim_sqrt * xc_over_ip;
            factor.factor_ppc = factor.factor_ip * (&one_vec * &signed_vec[i]);
        }

        // sort by distances
        let mut idx = xc_distances.iter().enumerate().collect::<Vec<_>>();
        idx.sort_by(|&x, &y| x.1.partial_cmp(y.1).unwrap());
        let idx = idx.into_iter().map(|(i, _)| i).collect::<Vec<_>>();
        let binary_vec = idx.iter().flat_map(|&i| binary_vec[i].clone()).collect();
        let factors: Vec<Factor> = idx.iter().map(|&i| factors[i]).collect();
        let centroids_col_based = Mat::from_fn(num, dim_pad, |i, j| centroids_mat.read(idx[i], j))
            .transpose()
            .to_owned();

        RaBitQ {
            centroids: centroids_col_based,
            orthogonal,
            mean,
            binary_vec,
            factors,
            idx,
            dim: dim_pad,
            metrics: Metrics::default(),
        }
    }

    /// Retrieve the top-1 index.
    pub fn retrieve_top_one(&self, query: &[f32]) -> usize {
        assert_eq!(self.dim, query.len().div_ceil(64) * 64);
        let mut query_pad = query.to_vec();
        if self.dim > query.len() {
            query_pad.extend_from_slice(&vec![0.0; self.dim - query.len()]);
        }

        let projected = project(&query_pad, &self.orthogonal.as_ref());
        let mut rough_distances = Vec::with_capacity(self.centroids.nrows());
        let mut quantized = vec![0u8; self.dim];
        let mut binary = vec![0u64; (self.dim * THETA_LOG_DIM).div_ceil(64)];
        let mut residual = vec![0.0; self.dim];
        let yc_distance = squared_euclidean(projected.as_slice(), self.mean.as_slice());

        let (lower_bound, upper_bound) =
            min_max_residual(&mut residual, projected.as_slice(), self.mean.as_slice());
        let delta = (upper_bound - lower_bound) * SCALAR;
        let one_over_delta = delta.recip();
        let scalar_sum = scalar_quantize(&mut quantized, &residual, lower_bound, one_over_delta);
        vector_binarize_query(&quantized, &mut binary);
        self.calculate_rough_distance(
            yc_distance,
            &binary,
            lower_bound,
            scalar_sum as f32,
            delta,
            &mut rough_distances,
        );
        self.rank(&rough_distances, &query_pad)
    }

    fn calculate_rough_distance(
        &self,
        yc_distance_square: f32,
        y_binary_vec: &[u64],
        lower_bound: f32,
        scalar_sum: f32,
        delta: f32,
        rough_distances: &mut Vec<(f32, usize)>,
    ) {
        let dist_sqrt = yc_distance_square.sqrt();
        let offset = y_binary_vec.len() / THETA_LOG_DIM;
        for &i in self.idx.iter() {
            let factor = &self.factors[i];
            rough_distances.push((
                (factor.center_distance_square
                    + yc_distance_square
                    + lower_bound * factor.factor_ppc
                    + (2.0
                        * asymmetric_binary_dot_product(
                            &self.binary_vec[i * offset..(i + 1) * offset],
                            y_binary_vec,
                        ) as f32
                        - scalar_sum)
                        * factor.factor_ip
                        * delta
                    - factor.error_bound * dist_sqrt),
                i,
            ));
        }
    }

    fn rank(&self, rough_distances: &[(f32, usize)], query: &[f32]) -> usize {
        let mut threshold = f32::MAX;
        let mut min_index = 0;
        let mut count = 0;
        for &(rough, i) in rough_distances.iter() {
            if rough < threshold {
                count += 1;
                let accurate = squared_euclidean(
                    self.centroids
                        .col(i)
                        .try_as_slice()
                        .expect("failed to get centroids slice"),
                    query,
                );
                if accurate < threshold {
                    threshold = accurate;
                    min_index = self.idx[i];
                }
            }
        }
        self.metrics.update(rough_distances.len() as u64, count);

        min_index
    }

    /// Get the rough/precise metrics.
    pub fn get_metrics(&self) -> (u64, u64) {
        self.metrics.fetch()
    }
}
