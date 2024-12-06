from argparse import ArgumentParser
from time import perf_counter
from struct import unpack, pack

from faiss import Kmeans
from sklearn.cluster import MiniBatchKMeans
import numpy as np


def build_arg_parser():
    parser = ArgumentParser()
    parser.add_argument("--n_clusters", "-n", type=int, default=4096)
    parser.add_argument("--max_iter", "-m", type=int, default=25)
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--input", "-i", type=str, required=True)
    parser.add_argument("--output", "-o", type=str, required=True)
    parser.add_argument(
        "--library", "-l", type=str, default="faiss", choices=["faiss", "sklearn"]
    )
    return parser


def read_vec(filepath: str, vec_type: np.dtype = np.float32):
    """Read vectors from a file. Support `fvecs`, `ivecs` and `bvecs` format.
    Args:
        filepath: The path of the file.
        vec_type: The type of the vectors.
    """
    size = np.dtype(vec_type).itemsize
    with open(filepath, "rb") as f:
        vecs = []
        while True:
            try:
                buf = f.read(4)
                if len(buf) == 0:
                    break
                dim = unpack("<i", buf)[0]
                vecs.append(np.frombuffer(f.read(dim * size), dtype=vec_type))
            except Exception as err:
                print(err)
                break
    return np.array(vecs)


def write_vec(filepath: str, vecs: np.ndarray, vec_type: np.dtype = np.float32):
    """Write vectors to a file. Support `fvecs`, `ivecs` and `bvecs` format."""
    with open(filepath, "wb") as f:
        for vec in vecs.astype(vec_type):
            f.write(pack("<i", len(vec)))
            f.write(vec.tobytes())


def faiss_cluster(args):
    vecs = read_vec(args.input)
    dim = vecs.shape[1]
    kmeans = Kmeans(dim, args.n_clusters, niter=args.max_iter, verbose=args.verbose)
    t_start = perf_counter()
    kmeans.train(vecs)
    print(f"faiss k-means training time: {perf_counter() - t_start:.6f}s")
    write_vec(args.output, kmeans.centroids)


def sklearn_cluster(args):
    vecs = read_vec(args.input)
    kmeans = MiniBatchKMeans(
        n_clusters=args.n_clusters, max_iter=args.max_iter, verbose=args.verbose
    )
    t_start = perf_counter()
    kmeans.fit(vecs)
    print(
        f"scikit-learn k-means training + assign time: {perf_counter() - t_start:.6f}s"
    )
    write_vec(args.output, kmeans.cluster_centers_)


if __name__ == "__main__":
    args = build_arg_parser().parse_args()
    print(args)
    if args.library == "faiss":
        faiss_cluster(args)
    else:
        sklearn_cluster(args)
