from typing import Any, Callable, Literal, Optional, Tuple, Union

from numpy.typing import ArrayLike
import numpy as np

from sarus_data_spec.dataspec_validator.signature import (
    SarusParameter,
    SarusSignature,
    SarusSignatureValue,
)

from ..external_op import ExternalOpImplementation

try:
    from sklearn import cluster
    from sklearn.base import BaseEstimator
except ModuleNotFoundError:
    BaseEstimator = Any


class sk_birch(ExternalOpImplementation):
    _transform_id = "sklearn.SK_BIRCH"
    _signature = SarusSignature(
        SarusParameter(
            name="threshold",
            annotation=float,
            default=0.5,
        ),
        SarusParameter(
            name="branching_factor",
            annotation=int,
            default=50,
        ),
        SarusParameter(
            name="n_clusters",
            annotation=Optional[Union[int, BaseEstimator]],
            default=3,
        ),
        SarusParameter(
            name="compute_labels",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=True,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return cluster.Birch(**kwargs)


class sk_dbscan(ExternalOpImplementation):
    _transform_id = "sklearn.SK_DBSCAN"
    _signature = SarusSignature(
        SarusParameter(
            name="eps",
            annotation=float,
            default=0.5,
        ),
        SarusParameter(
            name="min_samples",
            annotation=int,
            default=5,
        ),
        SarusParameter(
            name="metric",
            annotation=Union[str, Callable],
            default="euclidean",
        ),
        SarusParameter(
            name="metric_params",
            annotation=Optional[dict],
            default=None,
        ),
        SarusParameter(
            name="algorithm",
            annotation=Literal["auto", "ball_tree", "kd_tree", "brute"],
            default="auto",
        ),
        SarusParameter(
            name="leaf_size",
            annotation=int,
            default=30,
        ),
        SarusParameter(
            name="p",
            annotation=Optional[float],
            default=None,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return cluster.DBSCAN(**kwargs)


class sk_feature_agglomeration(ExternalOpImplementation):
    _transform_id = "sklearn.SK_FEATURE_AGGLOMERATION"
    _signature = SarusSignature(
        SarusParameter(
            name="n_clusters",
            annotation=Optional[int],
            default=2,
        ),
        SarusParameter(
            name="affinity",
            annotation=Union[str, Callable],
            default="euclidean",
        ),
        SarusParameter(
            name="metric",
            annotation=Optional[Union[str, Callable]],
            default=None,
        ),
        SarusParameter(
            name="memory",
            annotation=Optional[Union[str, Any]],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="connectivity",
            annotation=Optional[Union[ArrayLike, Callable]],
            default=None,
        ),
        SarusParameter(
            name="compute_full_tree",
            annotation=Union[Literal["auto"], bool],
            default="auto",
        ),
        SarusParameter(
            name="linkage",
            annotation=Literal["ward", "complete", "average", "single"],
            default="ward",
        ),
        SarusParameter(
            name="pooling_func",
            annotation=Callable,
            default=np.mean,
        ),
        SarusParameter(
            name="distance_threshold",
            annotation=Optional[float],
            default=None,
        ),
        SarusParameter(
            name="compute_distances",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return cluster.FeatureAgglomeration(**kwargs)


class sk_kmeans(ExternalOpImplementation):
    _transform_id = "sklearn.SK_KMEANS"
    _signature = SarusSignature(
        SarusParameter(
            name="n_clusters",
            annotation=int,
            default=8,
        ),
        SarusParameter(
            name="init",
            annotation=Union[
                Literal["k-means++", "random"], Callable, ArrayLike
            ],
            default="k-means++",
        ),
        SarusParameter(
            name="n_init",
            annotation=Union[Literal["auto"], int],
            default=10,
        ),
        SarusParameter(
            name="max_iter",
            annotation=int,
            default=300,
        ),
        SarusParameter(
            name="tol",
            annotation=float,
            default=1e-4,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
        SarusParameter(
            name="copy_x",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="algorithm",
            annotation=Literal["lloyd", "elkan", "auto", "full"],
            default="lloyd",
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return cluster.KMeans(**kwargs)


class sk_minibatch_kmeans(ExternalOpImplementation):
    _transform_id = "sklearn.SK_MINIBATCH_KMEANS"
    _signature = SarusSignature(
        SarusParameter(
            name="n_clusters",
            annotation=int,
            default=8,
        ),
        SarusParameter(
            name="init",
            annotation=Union[
                Literal["k-means++", "random"], Callable, ArrayLike
            ],
            default="k-means++",
        ),
        SarusParameter(
            name="max_iter",
            annotation=int,
            default=100,
        ),
        SarusParameter(
            name="batch_size",
            annotation=int,
            default=1024,
        ),
        SarusParameter(
            name="verbose",
            annotation=int,
            default=0,
        ),
        SarusParameter(
            name="compute_labels",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
        SarusParameter(
            name="tol",
            annotation=float,
            default=0.0,
        ),
        SarusParameter(
            name="max_no_improvement",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="init_size",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="n_init",
            annotation=Union[Literal["auto"], int],
            default=3,
        ),
        SarusParameter(
            name="reassignment_ratio",
            annotation=float,
            default=0.01,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return cluster.MiniBatchKMeans(**kwargs)


class sk_mean_shift(ExternalOpImplementation):
    _transform_id = "sklearn.SK_MEAN_SHIFT"
    _signature = SarusSignature(
        SarusParameter(
            name="bandwidth",
            annotation=float,
            default=None,
        ),
        SarusParameter(
            name="seeds",
            annotation=Optional[ArrayLike],
            default=None,
        ),
        SarusParameter(
            name="bin_seeding",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="min_bin_freq",
            annotation=int,
            default=1,
        ),
        SarusParameter(
            name="cluster_all",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="max_iter",
            annotation=int,
            default=300,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return cluster.MeanShift(**kwargs)


class sk_optics(ExternalOpImplementation):
    _transform_id = "sklearn.SK_OPTICS"
    _signature = SarusSignature(
        SarusParameter(
            name="min_samples",
            annotation=Union[int, float],
            default=5,
        ),
        SarusParameter(
            name="max_eps",
            annotation=float,
            default=np.inf,
        ),
        SarusParameter(
            name="metric",
            annotation=Union[
                Literal[
                    "cityblock",
                    "cosine",
                    "euclidean",
                    "l1",
                    "l2",
                    "manhattan",
                    "braycurtis",
                    "canberra",
                    "chebyshev",
                    "correlation",
                    "dice",
                    "hamming",
                    "jaccard",
                    "kulsinski",
                    "mahalanobis",
                    "minkowski",
                    "rogerstanimoto",
                    "russellrao",
                    "seuclidean",
                    "sokalmichener",
                    "sokalsneath",
                    "sqeuclidean",
                    "yule",
                ],
                Callable,
            ],
            default="minkowski",
        ),
        SarusParameter(
            name="p",
            annotation=float,
            default=2,
        ),
        SarusParameter(
            name="metric_params",
            annotation=Optional[dict],
            default=None,
        ),
        SarusParameter(
            name="cluster_method",
            annotation=Literal["xi", "dbscan"],
            default="xi",
        ),
        SarusParameter(
            name="eps",
            annotation=Optional[float],
            default=None,
        ),
        SarusParameter(
            name="xi",
            annotation=float,
            default=0.5,
        ),
        SarusParameter(
            name="predecessor_correction",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="min_cluster_size",
            annotation=Optional[Union[float, int]],
            default=None,
        ),
        SarusParameter(
            name="algorithm",
            annotation=Literal["auto", "ball_tree", "kd_tree", "brute"],
            default="auto",
        ),
        SarusParameter(
            name="leaf_size",
            annotation=int,
            default=30,
        ),
        SarusParameter(
            name="memory",
            annotation=Optional[Union[str, Any]],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
            predicate=lambda x: x is None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return cluster.OPTICS(**kwargs)


class sk_spectral_clustering(ExternalOpImplementation):
    _transform_id = "sklearn.SK_SPECTRAL_CLUSTERING"
    _signature = SarusSignature(
        SarusParameter(
            name="n_clusters",
            annotation=int,
            default=8,
        ),
        SarusParameter(
            name="eigen_solver",
            annotation=Optional[Literal["arpack", "lobpcg", "amg"]],
            default=None,
        ),
        SarusParameter(
            name="n_components",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
        SarusParameter(
            name="n_init",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="gamma",
            annotation=float,
            default=1.0,
        ),
        SarusParameter(
            name="affinity",
            annotation=Union[
                Literal[
                    "rbf",
                    "nearest_neighbors",
                    "precomputed",
                    "precomputed_nearest_neighbors",
                ],
                Callable,
            ],
            default="rbf",
        ),
        SarusParameter(
            name="n_neighbors",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="eigen_tol",
            annotation=Union[float, Literal["auto"]],
            default="auto",
        ),
        SarusParameter(
            name="assign_labels",
            annotation=Literal["kmeans", "discretize", "cluster_qr"],
            default="kmeans",
        ),
        SarusParameter(
            name="degree",
            annotation=int,
            default=3,
        ),
        SarusParameter(
            name="coef0",
            annotation=float,
            default=1.0,
        ),
        SarusParameter(
            name="kernel_params",
            annotation=Optional[dict],
            default=None,
        ),
        SarusParameter(
            name="n_jobs",
            annotation=Optional[int],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="verbose",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return cluster.SpectralClustering(**kwargs)


class sk_spectral_biclustering(ExternalOpImplementation):
    _transform_id = "sklearn.SK_SPECTRAL_BICLUSTERING"
    _signature = SarusSignature(
        SarusParameter(
            name="n_clusters",
            annotation=Union[int, Tuple[int, int]],
            default=3,
        ),
        SarusParameter(
            name="method",
            annotation=Literal["bistochastic", "scale", "log"],
            default="bistochastic",
        ),
        SarusParameter(
            name="n_components",
            annotation=int,
            default=6,
        ),
        SarusParameter(
            name="n_best",
            annotation=int,
            default=3,
        ),
        SarusParameter(
            name="svd_method",
            annotation=Literal["randomized", "arpack"],
            default="randomized",
        ),
        SarusParameter(
            name="n_svd_vecs",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="mini_batch",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="init",
            annotation=Union[Literal["k-means++", "random"], np.ndarray],
            default="k-means++",
        ),
        SarusParameter(
            name="n_init",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return cluster.SpectralBiclustering(**kwargs)


class sk_spectral_coclustering(ExternalOpImplementation):
    _transform_id = "sklearn.SK_SPECTRAL_COCLUSTERING"
    _signature = SarusSignature(
        SarusParameter(
            name="n_clusters",
            annotation=int,
            default=3,
        ),
        SarusParameter(
            name="svd_method",
            annotation=Literal["randomized", "arpack"],
            default="randomized",
        ),
        SarusParameter(
            name="n_svd_vecs",
            annotation=Optional[int],
            default=None,
        ),
        SarusParameter(
            name="mini_batch",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="init",
            annotation=Union[Literal["k-means++", "random"], np.ndarray],
            default="k-means++",
        ),
        SarusParameter(
            name="n_init",
            annotation=int,
            default=10,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return cluster.SpectralCoclustering(**kwargs)


class sk_affinity_propagation(ExternalOpImplementation):
    _transform_id = "sklearn.SK_AFFINITY_PROPAGATION"
    _signature = SarusSignature(
        SarusParameter(
            name="damping",
            annotation=float,
            default=0.5,
        ),
        SarusParameter(
            name="max_iter",
            annotation=int,
            default=200,
        ),
        SarusParameter(
            name="convergence_iter",
            annotation=int,
            default=15,
        ),
        SarusParameter(
            name="copy",
            annotation=bool,
            default=True,
        ),
        SarusParameter(
            name="preference",
            annotation=Optional[Union[ArrayLike, float]],
            default=None,
        ),
        SarusParameter(
            name="affinity",
            annotation=Literal["euclidean", "precomputed"],
            default="euclidean",
        ),
        SarusParameter(
            name="verbose",
            annotation=bool,
            default=False,
        ),
        SarusParameter(
            name="random_state",
            annotation=Optional[Union[int, np.random.RandomState]],
            default=None,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return cluster.AffinityPropagation(**kwargs)


class sk_agglomerative_clustering(ExternalOpImplementation):
    _transform_id = "sklearn.SK_AGGLOMERATIVE_CLUSTERING"
    _signature = SarusSignature(
        SarusParameter(
            name="n_clusters",
            annotation=Optional[int],
            default=2,
        ),
        SarusParameter(
            name="affinity",
            annotation=Union[Literal["euclidean", "precomputed"], Callable],
            default="euclidean",
        ),
        SarusParameter(
            name="metric",
            annotation=Optional[
                Union[
                    Literal[
                        "euclidean",
                        "l1",
                        "l2",
                        "manhattan",
                        "cosine",
                        "precomputed",
                    ],
                    Callable,
                ]
            ],
            default=None,
        ),
        SarusParameter(
            name="memory",
            annotation=Optional[Union[str, Any]],
            default=None,
            predicate=lambda x: x is None,
        ),
        SarusParameter(
            name="connectivity",
            annotation=Optional[Union[ArrayLike, Callable]],
            default=None,
        ),
        SarusParameter(
            name="compute_full_tree",
            annotation=Union[Literal["auto"], bool],
            default="auto",
        ),
        SarusParameter(
            name="linkage",
            annotation=Literal["ward", "complete", "average", "single"],
            default="ward",
        ),
        SarusParameter(
            name="distance_threshold",
            annotation=Optional[float],
            default=None,
        ),
        SarusParameter(
            name="compute_distances",
            annotation=bool,
            default=False,
        ),
    )

    def call(self, signature: SarusSignatureValue) -> Any:
        kwargs = signature.collect_kwargs()
        return cluster.AgglomerativeClustering(**kwargs)
