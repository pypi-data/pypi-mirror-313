"""
COLMAP plugin
"""

from __future__ import annotations
import numpy
import typing
from . import cost_functions
from . import manifold
from . import pyceres

__all__: list[str] = [
    "AbsolutePoseEstimationOptions",
    "AbsolutePoseRefinementOptions",
    "BACovariance",
    "BACovarianceOptions",
    "BACovarianceOptionsParams",
    "BundleAdjuster",
    "BundleAdjustmentConfig",
    "BundleAdjustmentOptions",
    "COLMAP_build",
    "COLMAP_version",
    "Camera",
    "CameraMode",
    "CameraModelId",
    "CopyType",
    "Correspondence",
    "CorrespondenceGraph",
    "Database",
    "DatabaseCache",
    "DatabaseTransaction",
    "DelaunayMeshingOptions",
    "Device",
    "EstimateTriangulationOptions",
    "ExhaustiveMatchingOptions",
    "ExhaustivePairGenerator",
    "ExperimentalPoseParam",
    "Image",
    "ImageAlignmentError",
    "ImagePairStat",
    "ImagePairsMatchingOptions",
    "ImageReaderOptions",
    "ImageSelectionMethod",
    "ImportedPairGenerator",
    "IncrementalMapper",
    "IncrementalMapperCallback",
    "IncrementalMapperOptions",
    "IncrementalMapperStatus",
    "IncrementalPipeline",
    "IncrementalPipelineOptions",
    "IncrementalTriangulator",
    "IncrementalTriangulatorOptions",
    "ListPoint2D",
    "LocalBundleAdjustmentReport",
    "LossFunctionType",
    "MapCameraIdToCamera",
    "MapImageIdToImage",
    "MapPoint3DIdToPoint3D",
    "Normalization",
    "ObservationManager",
    "PairGenerator",
    "Point2D",
    "Point3D",
    "PoissonMeshingOptions",
    "PosePrior",
    "PosePriorBundleAdjustmentOptions",
    "PosePriorCoordinateSystem",
    "RANSACOptions",
    "Reconstruction",
    "ReconstructionManager",
    "Rigid3d",
    "Rotation3d",
    "SequentialMatchingOptions",
    "SequentialPairGenerator",
    "Sift",
    "SiftExtractionOptions",
    "SiftMatchingOptions",
    "Sim3d",
    "SpatialMatchingOptions",
    "SpatialPairGenerator",
    "StereoFusionOptions",
    "SyntheticDatasetMatchConfig",
    "SyntheticDatasetOptions",
    "Timer",
    "Track",
    "TrackElement",
    "TriangulationResidualType",
    "TwoViewGeometry",
    "TwoViewGeometryConfiguration",
    "TwoViewGeometryOptions",
    "UndistortCameraOptions",
    "VocabTreeMatchingOptions",
    "VocabTreePairGenerator",
    "absolute_pose_estimation",
    "align_reconstruction_to_locations",
    "align_reconstructions_via_points",
    "align_reconstructions_via_proj_centers",
    "align_reconstructions_via_reprojections",
    "bundle_adjustment",
    "compare_reconstructions",
    "compute_squared_sampson_error",
    "create_default_bundle_adjuster",
    "create_pose_prior_bundle_adjuster",
    "essential_matrix_estimation",
    "essential_matrix_from_pose",
    "estimate_absolute_pose",
    "estimate_and_refine_absolute_pose",
    "estimate_and_refine_generalized_absolute_pose",
    "estimate_ba_covariance",
    "estimate_calibrated_two_view_geometry",
    "estimate_essential_matrix",
    "estimate_fundamental_matrix",
    "estimate_homography_matrix",
    "estimate_sim3d",
    "estimate_sim3d_robust",
    "estimate_triangulation",
    "estimate_two_view_geometry",
    "estimate_two_view_geometry_pose",
    "extract_features",
    "fundamental_matrix_estimation",
    "has_cuda",
    "homography_decomposition",
    "homography_matrix_estimation",
    "import_images",
    "incremental_mapping",
    "infer_camera_from_image",
    "logging",
    "match_exhaustive",
    "match_sequential",
    "match_spatial",
    "match_vocabtree",
    "ostream",
    "poisson_meshing",
    "pose_from_homography_matrix",
    "refine_absolute_pose",
    "rig_absolute_pose_estimation",
    "set_random_seed",
    "stereo_fusion",
    "synthesize_dataset",
    "triangulate_points",
    "undistort_images",
    "verify_matches",
]
M = typing.TypeVar("M", bound=int)
N = typing.TypeVar("N", bound=int)

class AbsolutePoseEstimationOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> AbsolutePoseEstimationOptions: ...
    def __deepcopy__(self, arg0: dict) -> AbsolutePoseEstimationOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def estimate_focal_length(self) -> bool:
        """
        (bool, default: False)
        """
    @estimate_focal_length.setter
    def estimate_focal_length(self, arg0: bool) -> None: ...
    @property
    def ransac(self) -> RANSACOptions:
        """
        (RANSACOptions, default: RANSACOptions(max_error=12.0, min_inlier_ratio=0.1, confidence=0.99999, dyn_num_trials_multiplier=3.0, min_num_trials=100, max_num_trials=10000))
        """
    @ransac.setter
    def ransac(self, arg0: RANSACOptions) -> None: ...

class AbsolutePoseRefinementOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> AbsolutePoseRefinementOptions: ...
    def __deepcopy__(self, arg0: dict) -> AbsolutePoseRefinementOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def gradient_tolerance(self) -> float:
        """
        (float, default: 1.0)
        """
    @gradient_tolerance.setter
    def gradient_tolerance(self, arg0: float) -> None: ...
    @property
    def loss_function_scale(self) -> float:
        """
        (float, default: 1.0)
        """
    @loss_function_scale.setter
    def loss_function_scale(self, arg0: float) -> None: ...
    @property
    def max_num_iterations(self) -> int:
        """
        (int, default: 100)
        """
    @max_num_iterations.setter
    def max_num_iterations(self, arg0: int) -> None: ...
    @property
    def print_summary(self) -> bool:
        """
        (bool, default: False)
        """
    @print_summary.setter
    def print_summary(self, arg0: bool) -> None: ...
    @property
    def refine_extra_params(self) -> bool:
        """
        (bool, default: False)
        """
    @refine_extra_params.setter
    def refine_extra_params(self, arg0: bool) -> None: ...
    @property
    def refine_focal_length(self) -> bool:
        """
        (bool, default: False)
        """
    @refine_focal_length.setter
    def refine_focal_length(self, arg0: bool) -> None: ...

class BACovariance:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def get_cam1_from_cam2_cov(
        self, image_id1: int, image_id2: int
    ) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]] | None:
        """
        Tangent space covariance in the order [rotation, translation]. If some dimensions are kept constant, the respective rows/columns are omitted. Returns null if image not a variable in the problem.
        """
    def get_cam_from_world_cov(
        self, image_id: int
    ) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]] | None:
        """
        Tangent space covariance in the order [rotation, translation]. If some dimensions are kept constant, the respective rows/columns are omitted. Returns null if image not a variable in the problem.
        """
    def get_other_params_cov(
        self, param: float
    ) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]] | None:
        """
        Tangent space covariance for any variable parameter block in the problem. If some dimensions are kept constant, the respective rows/columns are omitted. Returns null if parameter block not a variable in the problem.
        """
    def get_point_cov(
        self, image_id: int
    ) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float64]] | None:
        """
        Covariance for 3D points, conditioned on all other variables set constant. If some dimensions are kept constant, the respective rows/columns are omitted. Returns null if 3D point not a variable in the problem.
        """

class BACovarianceOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> BACovarianceOptions: ...
    def __deepcopy__(self, arg0: dict) -> BACovarianceOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def damping(self) -> float:
        """
        Damping factor for the Hessian in the Schur complement solver. Enables to robustly deal with poorly conditioned parameters. (float, default: 1e-08)
        """
    @damping.setter
    def damping(self, arg0: float) -> None: ...
    @property
    def experimental_custom_poses(self) -> list[ExperimentalPoseParam]:
        """
        WARNING: This option will be removed in a future release, use at your own risk. For custom bundle adjustment problems, this enables to specify a custom set of pose parameter blocks to consider. Note that these pose blocks must not necessarily be part of the reconstruction but they must follow the standard requirement for applying the Schur complement trick. (list, default: [])
        """
    @experimental_custom_poses.setter
    def experimental_custom_poses(
        self, arg0: list[ExperimentalPoseParam]
    ) -> None: ...
    @property
    def params(self) -> BACovarianceOptionsParams:
        """
        For which parameters to compute the covariance. (BACovarianceOptionsParams, default: BACovarianceOptionsParams.ALL)
        """
    @params.setter
    def params(self, arg0: BACovarianceOptionsParams) -> None: ...

class BACovarianceOptionsParams:
    """
    Members:

      POSES

      POINTS

      POSES_AND_POINTS

      ALL
    """

    ALL: typing.ClassVar[
        BACovarianceOptionsParams
    ]  # value = <BACovarianceOptionsParams.ALL: 3>
    POINTS: typing.ClassVar[
        BACovarianceOptionsParams
    ]  # value = <BACovarianceOptionsParams.POINTS: 1>
    POSES: typing.ClassVar[
        BACovarianceOptionsParams
    ]  # value = <BACovarianceOptionsParams.POSES: 0>
    POSES_AND_POINTS: typing.ClassVar[
        BACovarianceOptionsParams
    ]  # value = <BACovarianceOptionsParams.POSES_AND_POINTS: 2>
    __members__: typing.ClassVar[
        dict[str, BACovarianceOptionsParams]
    ]  # value = {'POSES': <BACovarianceOptionsParams.POSES: 0>, 'POINTS': <BACovarianceOptionsParams.POINTS: 1>, 'POSES_AND_POINTS': <BACovarianceOptionsParams.POSES_AND_POINTS: 2>, 'ALL': <BACovarianceOptionsParams.ALL: 3>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class BundleAdjuster:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(
        self, options: BundleAdjustmentOptions, config: BundleAdjustmentConfig
    ) -> None: ...
    def solve(self) -> pyceres.SolverSummary: ...
    @property
    def config(self) -> BundleAdjustmentConfig: ...
    @property
    def options(self) -> BundleAdjustmentOptions: ...
    @property
    def problem(self): ...

class BundleAdjustmentConfig:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> BundleAdjustmentConfig: ...
    def __deepcopy__(self, arg0: dict) -> BundleAdjustmentConfig: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def add_constant_point(self, point3D_id: int) -> None: ...
    def add_image(self, image_id: int) -> None: ...
    def add_variable_point(self, point3D_id: int) -> None: ...
    def constant_cam_positions(self, image_id: int) -> list[int]: ...
    def has_constant_cam_intrinsics(self, camera_id: int) -> bool: ...
    def has_constant_cam_pose(self, image_id: int) -> bool: ...
    def has_constant_cam_positions(self, image_id: int) -> bool: ...
    def has_constant_point(self, point3D_id: int) -> bool: ...
    def has_image(self, image_id: int) -> bool: ...
    def has_point(self, point3D_id: int) -> bool: ...
    def has_variable_point(self, point3D_id: int) -> bool: ...
    def mergedict(self, arg0: dict) -> None: ...
    def num_constant_cam_intrinsics(self) -> int: ...
    def num_constant_cam_poses(self) -> int: ...
    def num_constant_cam_positions(self) -> int: ...
    def num_constant_points(self) -> int: ...
    def num_images(self) -> int: ...
    def num_points(self) -> int: ...
    def num_residuals(self, reconstruction: Reconstruction) -> int: ...
    def num_variable_points(self) -> int: ...
    def remove_constant_point(self, point3D_id: int) -> None: ...
    def remove_image(self, image_id: int) -> None: ...
    def remove_variable_cam_positions(self, image_id: int) -> None: ...
    def remove_variable_point(self, point3D_id: int) -> None: ...
    def set_constant_cam_intrinsics(self, camera_id: int) -> None: ...
    def set_constant_cam_pose(self, image_id: int) -> None: ...
    def set_constant_cam_positions(
        self, image_id: int, idxs: list[int]
    ) -> None: ...
    def set_variable_cam_intrinsics(self, camera_id: int) -> None: ...
    def set_variable_cam_pose(self, image_id: int) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def constant_cam_poses(self) -> set[int]:
        """
        (set, default: set())
        """
    @property
    def constant_intrinsics(self) -> set[int]:
        """
        (set, default: set())
        """
    @property
    def constant_point3D_ids(self) -> set[int]:
        """
        (set, default: set())
        """
    @property
    def image_ids(self) -> set[int]:
        """
        (set, default: set())
        """
    @property
    def variable_point3D_ids(self) -> set[int]:
        """
        (set, default: set())
        """

class BundleAdjustmentOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> BundleAdjustmentOptions: ...
    def __deepcopy__(self, arg0: dict) -> BundleAdjustmentOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def create_loss_function(self): ...
    def create_solver_options(
        self, config: BundleAdjustmentConfig, problem
    ) -> pyceres.SolverOptions: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def gpu_index(self) -> str:
        """
        Which GPU to use for solving the problem. (str, default: -1)
        """
    @gpu_index.setter
    def gpu_index(self, arg0: str) -> None: ...
    @property
    def loss_function_scale(self) -> float:
        """
        Scaling factor determines residual at which robustification takes place. (float, default: 1.0)
        """
    @loss_function_scale.setter
    def loss_function_scale(self, arg0: float) -> None: ...
    @property
    def loss_function_type(self) -> LossFunctionType:
        """
        Loss function types: Trivial (non-robust) and Cauchy (robust) loss. (LossFunctionType, default: LossFunctionType.TRIVIAL)
        """
    @loss_function_type.setter
    def loss_function_type(self, arg0: LossFunctionType) -> None: ...
    @property
    def max_num_images_direct_dense_cpu_solver(self) -> int:
        """
        Threshold to switch between direct, sparse, and iterative solvers. (int, default: 50)
        """
    @max_num_images_direct_dense_cpu_solver.setter
    def max_num_images_direct_dense_cpu_solver(self, arg0: int) -> None: ...
    @property
    def max_num_images_direct_dense_gpu_solver(self) -> int:
        """
        Threshold to switch between direct, sparse, and iterative solvers. (int, default: 200)
        """
    @max_num_images_direct_dense_gpu_solver.setter
    def max_num_images_direct_dense_gpu_solver(self, arg0: int) -> None: ...
    @property
    def max_num_images_direct_sparse_cpu_solver(self) -> int:
        """
        Threshold to switch between direct, sparse, and iterative solvers. (int, default: 1000)
        """
    @max_num_images_direct_sparse_cpu_solver.setter
    def max_num_images_direct_sparse_cpu_solver(self, arg0: int) -> None: ...
    @property
    def max_num_images_direct_sparse_gpu_solver(self) -> int:
        """
        Threshold to switch between direct, sparse, and iterative solvers. (int, default: 4000)
        """
    @max_num_images_direct_sparse_gpu_solver.setter
    def max_num_images_direct_sparse_gpu_solver(self, arg0: int) -> None: ...
    @property
    def min_num_images_gpu_solver(self) -> int:
        """
        Minimum number of images to use the GPU solver. (int, default: 50)
        """
    @min_num_images_gpu_solver.setter
    def min_num_images_gpu_solver(self, arg0: int) -> None: ...
    @property
    def min_num_residuals_for_cpu_multi_threading(self) -> int:
        """
        Minimum number of residuals to enable multi-threading. Note that single-threaded is typically better for small bundle adjustment problems due to the overhead of threading. (int, default: 50000)
        """
    @min_num_residuals_for_cpu_multi_threading.setter
    def min_num_residuals_for_cpu_multi_threading(self, arg0: int) -> None: ...
    @property
    def print_summary(self) -> bool:
        """
        Whether to print a final summary. (bool, default: True)
        """
    @print_summary.setter
    def print_summary(self, arg0: bool) -> None: ...
    @property
    def refine_extra_params(self) -> bool:
        """
        Whether to refine the extra parameter group. (bool, default: True)
        """
    @refine_extra_params.setter
    def refine_extra_params(self, arg0: bool) -> None: ...
    @property
    def refine_extrinsics(self) -> bool:
        """
        Whether to refine the extrinsic parameter group. (bool, default: True)
        """
    @refine_extrinsics.setter
    def refine_extrinsics(self, arg0: bool) -> None: ...
    @property
    def refine_focal_length(self) -> bool:
        """
        Whether to refine the focal length parameter group. (bool, default: True)
        """
    @refine_focal_length.setter
    def refine_focal_length(self, arg0: bool) -> None: ...
    @property
    def refine_principal_point(self) -> bool:
        """
        Whether to refine the principal point parameter group. (bool, default: False)
        """
    @refine_principal_point.setter
    def refine_principal_point(self, arg0: bool) -> None: ...
    @property
    def solver_options(self) -> pyceres.SolverOptions:
        """
        Options for the Ceres solver. Using this member requires having PyCeres installed. (SolverOptions, default: SolverOptions(minimizer_type=MinimizerType.TRUST_REGION, line_search_direction_type=LineSearchDirectionType.LBFGS, line_search_type=LineSearchType.WOLFE, nonlinear_conjugate_gradient_type=NonlinearConjugateGradientType.FLETCHER_REEVES, max_lbfgs_rank=20, use_approximate_eigenvalue_bfgs_scaling=False, line_search_interpolation_type=LineSearchInterpolationType.CUBIC, min_line_search_step_size=1e-09, line_search_sufficient_function_decrease=0.0001, max_line_search_step_contraction=0.001, min_line_search_step_contraction=0.6, max_num_line_search_step_size_iterations=20, max_num_line_search_direction_restarts=5, line_search_sufficient_curvature_decrease=0.9, max_line_search_step_expansion=10.0, trust_region_strategy_type=TrustRegionStrategyType.LEVENBERG_MARQUARDT, dogleg_type=DoglegType.TRADITIONAL_DOGLEG, use_nonmonotonic_steps=False, max_consecutive_nonmonotonic_steps=10, max_num_iterations=100, max_solver_time_in_seconds=1000000000.0, num_threads=-1, initial_trust_region_radius=10000.0, max_trust_region_radius=1e+16, min_trust_region_radius=1e-32, min_relative_decrease=0.001, min_lm_diagonal=1e-06, max_lm_diagonal=1e+32, max_num_consecutive_invalid_steps=10, function_tolerance=0.0, gradient_tolerance=0.0001, parameter_tolerance=0.0, linear_solver_type=LinearSolverType.SPARSE_NORMAL_CHOLESKY, preconditioner_type=PreconditionerType.JACOBI, visibility_clustering_type=VisibilityClusteringType.CANONICAL_VIEWS, dense_linear_algebra_library_type=DenseLinearAlgebraLibraryType.EIGEN, sparse_linear_algebra_library_type=SparseLinearAlgebraLibraryType.SUITE_SPARSE, use_explicit_schur_complement=False, dynamic_sparsity=False, use_inner_iterations=False, inner_iteration_tolerance=0.001, min_linear_solver_iterations=0, max_linear_solver_iterations=200, eta=0.1, jacobi_scaling=True, logging_type=LoggingType.SILENT, minimizer_progress_to_stdout=False, trust_region_problem_dump_directory='/tmp', trust_region_problem_dump_format_type=DumpFormatType.TEXTFILE, check_gradients=False, gradient_check_relative_precision=1e-08, gradient_check_numeric_derivative_relative_step_size=1e-06, update_state_every_iteration=False))
        """
    @solver_options.setter
    def solver_options(self, arg0: pyceres.SolverOptions) -> None: ...
    @property
    def use_gpu(self) -> bool:
        """
        Whether to use Ceres' CUDA linear algebra library, if available. (bool, default: False)
        """
    @use_gpu.setter
    def use_gpu(self, arg0: bool) -> None: ...

class Camera:
    focal_length: float
    focal_length_x: float
    focal_length_y: float
    principal_point_x: float
    principal_point_y: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    @staticmethod
    def create(
        camera_id: int,
        model: CameraModelId,
        focal_length: float,
        width: int,
        height: int,
    ) -> Camera: ...
    def __copy__(self) -> Camera: ...
    def __deepcopy__(self, arg0: dict) -> Camera: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def calibration_matrix(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[3]], numpy.dtype[numpy.float64]
    ]:
        """
        Compute calibration matrix from params.
        """
    @typing.overload
    def cam_from_img(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[2], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> numpy.ndarray[
        tuple[typing.Literal[2], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]:
        """
        Project point in image plane to world / infinity.
        """
    @typing.overload
    def cam_from_img(
        self,
        arg0: numpy.ndarray[
            tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
        ],
    ) -> numpy.ndarray[tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]]:
        """
        Project list of points in image plane to world / infinity.
        """
    @typing.overload
    def cam_from_img(
        self, arg0: ListPoint2D
    ) -> numpy.ndarray[tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]]:
        """
        Project list of points in image plane to world / infinity.
        """
    def cam_from_img_threshold(self, arg0: float) -> float:
        """
        Convert pixel threshold in image plane to world space.
        """
    def extra_params_idxs(self) -> list[int]:
        """
        Indices of extra parameters in params property.
        """
    def focal_length_idxs(self) -> list[int]:
        """
        Indices of focal length parameters in params property.
        """
    def has_bogus_params(self, arg0: float, arg1: float, arg2: float) -> bool:
        """
        Check whether camera has bogus parameters.
        """
    @typing.overload
    def img_from_cam(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[2], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> numpy.ndarray[
        tuple[typing.Literal[2], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]:
        """
        Project point from world / infinity to image plane.
        """
    @typing.overload
    def img_from_cam(
        self,
        arg0: numpy.ndarray[
            tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
        ],
    ) -> numpy.ndarray[tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]]:
        """
        Project list of points from world / infinity to image plane.
        """
    @typing.overload
    def img_from_cam(
        self,
        arg0: numpy.ndarray[
            tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]
        ],
    ) -> typing.Any:
        """
        Project list of points from world / infinity to image plane.
        """
    @typing.overload
    def img_from_cam(
        self, arg0: ListPoint2D
    ) -> numpy.ndarray[tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]]:
        """
        Project list of points from world / infinity to image plane.
        """
    def mean_focal_length(self) -> float: ...
    def mergedict(self, arg0: dict) -> None: ...
    def params_to_string(self) -> str:
        """
        Concatenate parameters as comma-separated list.
        """
    def principal_point_idxs(self) -> list[int]:
        """
        Indices of principal point parameters in params property.
        """
    @typing.overload
    def rescale(self, arg0: int, arg1: int) -> None:
        """
        Rescale camera dimensions to (width_height) and accordingly the focal length and
        and the principal point.
        """
    @typing.overload
    def rescale(self, arg0: float) -> None:
        """
        Rescale camera dimensions by given factor and accordingly the focal length and
        and the principal point.
        """
    def set_params_from_string(self, arg0: str) -> bool:
        """
        Set camera parameters from comma-separated list.
        """
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    def verify_params(self) -> bool:
        """
        Check whether parameters are valid, i.e. the parameter vector has
        the correct dimensions that match the specified camera model.
        """
    @property
    def camera_id(self) -> int:
        """
        Unique identifier of the camera. (int, default: 4294967295)
        """
    @camera_id.setter
    def camera_id(self, arg0: int) -> None: ...
    @property
    def has_prior_focal_length(self) -> bool:
        """
        (bool, default: False)
        """
    @has_prior_focal_length.setter
    def has_prior_focal_length(self, arg0: bool) -> None: ...
    @property
    def height(self) -> int:
        """
        Height of camera sensor. (int, default: 0)
        """
    @height.setter
    def height(self, arg0: int) -> None: ...
    @property
    def model(self) -> CameraModelId:
        """
        Camera model. (CameraModelId, default: CameraModelId.INVALID)
        """
    @model.setter
    def model(self, arg0: CameraModelId) -> None: ...
    @property
    def params(
        self,
    ) -> numpy.ndarray[tuple[M, typing.Literal[1]], numpy.dtype[numpy.float64]]:
        """
        Camera parameters. (ndarray, default: [])
        """
    @params.setter
    def params(self, arg1: list[float]) -> None: ...
    @property
    def params_info(self) -> str:
        """
        Get human-readable information about the parameter vector ordering.
        """
    @property
    def width(self) -> int:
        """
        Width of camera sensor. (int, default: 0)
        """
    @width.setter
    def width(self, arg0: int) -> None: ...

class CameraMode:
    """
    Members:

      AUTO

      SINGLE

      PER_FOLDER

      PER_IMAGE
    """

    AUTO: typing.ClassVar[CameraMode]  # value = <CameraMode.AUTO: 0>
    PER_FOLDER: typing.ClassVar[
        CameraMode
    ]  # value = <CameraMode.PER_FOLDER: 2>
    PER_IMAGE: typing.ClassVar[CameraMode]  # value = <CameraMode.PER_IMAGE: 3>
    SINGLE: typing.ClassVar[CameraMode]  # value = <CameraMode.SINGLE: 1>
    __members__: typing.ClassVar[
        dict[str, CameraMode]
    ]  # value = {'AUTO': <CameraMode.AUTO: 0>, 'SINGLE': <CameraMode.SINGLE: 1>, 'PER_FOLDER': <CameraMode.PER_FOLDER: 2>, 'PER_IMAGE': <CameraMode.PER_IMAGE: 3>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class CameraModelId:
    """
    Members:

      INVALID

      SIMPLE_PINHOLE

      PINHOLE

      SIMPLE_RADIAL

      SIMPLE_RADIAL_FISHEYE

      RADIAL

      RADIAL_FISHEYE

      OPENCV

      OPENCV_FISHEYE

      FULL_OPENCV

      FOV

      THIN_PRISM_FISHEYE

      RAD_TAN_THIN_PRISM_FISHEYE
    """

    FOV: typing.ClassVar[CameraModelId]  # value = <CameraModelId.FOV: 7>
    FULL_OPENCV: typing.ClassVar[
        CameraModelId
    ]  # value = <CameraModelId.FULL_OPENCV: 6>
    INVALID: typing.ClassVar[
        CameraModelId
    ]  # value = <CameraModelId.INVALID: -1>
    OPENCV: typing.ClassVar[CameraModelId]  # value = <CameraModelId.OPENCV: 4>
    OPENCV_FISHEYE: typing.ClassVar[
        CameraModelId
    ]  # value = <CameraModelId.OPENCV_FISHEYE: 5>
    PINHOLE: typing.ClassVar[
        CameraModelId
    ]  # value = <CameraModelId.PINHOLE: 1>
    RADIAL: typing.ClassVar[CameraModelId]  # value = <CameraModelId.RADIAL: 3>
    RADIAL_FISHEYE: typing.ClassVar[
        CameraModelId
    ]  # value = <CameraModelId.RADIAL_FISHEYE: 9>
    RAD_TAN_THIN_PRISM_FISHEYE: typing.ClassVar[
        CameraModelId
    ]  # value = <CameraModelId.RAD_TAN_THIN_PRISM_FISHEYE: 11>
    SIMPLE_PINHOLE: typing.ClassVar[
        CameraModelId
    ]  # value = <CameraModelId.SIMPLE_PINHOLE: 0>
    SIMPLE_RADIAL: typing.ClassVar[
        CameraModelId
    ]  # value = <CameraModelId.SIMPLE_RADIAL: 2>
    SIMPLE_RADIAL_FISHEYE: typing.ClassVar[
        CameraModelId
    ]  # value = <CameraModelId.SIMPLE_RADIAL_FISHEYE: 8>
    THIN_PRISM_FISHEYE: typing.ClassVar[
        CameraModelId
    ]  # value = <CameraModelId.THIN_PRISM_FISHEYE: 10>
    __members__: typing.ClassVar[
        dict[str, CameraModelId]
    ]  # value = {'INVALID': <CameraModelId.INVALID: -1>, 'SIMPLE_PINHOLE': <CameraModelId.SIMPLE_PINHOLE: 0>, 'PINHOLE': <CameraModelId.PINHOLE: 1>, 'SIMPLE_RADIAL': <CameraModelId.SIMPLE_RADIAL: 2>, 'SIMPLE_RADIAL_FISHEYE': <CameraModelId.SIMPLE_RADIAL_FISHEYE: 8>, 'RADIAL': <CameraModelId.RADIAL: 3>, 'RADIAL_FISHEYE': <CameraModelId.RADIAL_FISHEYE: 9>, 'OPENCV': <CameraModelId.OPENCV: 4>, 'OPENCV_FISHEYE': <CameraModelId.OPENCV_FISHEYE: 5>, 'FULL_OPENCV': <CameraModelId.FULL_OPENCV: 6>, 'FOV': <CameraModelId.FOV: 7>, 'THIN_PRISM_FISHEYE': <CameraModelId.THIN_PRISM_FISHEYE: 10>, 'RAD_TAN_THIN_PRISM_FISHEYE': <CameraModelId.RAD_TAN_THIN_PRISM_FISHEYE: 11>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class CopyType:
    """
    Members:

      copy

      softlink

      hardlink
    """

    __members__: typing.ClassVar[
        dict[str, CopyType]
    ]  # value = {'copy': <CopyType.copy: 0>, 'softlink': <CopyType.softlink: 2>, 'hardlink': <CopyType.hardlink: 1>}
    copy: typing.ClassVar[CopyType]  # value = <CopyType.copy: 0>
    hardlink: typing.ClassVar[CopyType]  # value = <CopyType.hardlink: 1>
    softlink: typing.ClassVar[CopyType]  # value = <CopyType.softlink: 2>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class Correspondence:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> Correspondence: ...
    def __deepcopy__(self, arg0: dict) -> Correspondence: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, image_id: int, point2D_idx: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def image_id(self) -> int:
        """
        (int, default: 4294967295)
        """
    @image_id.setter
    def image_id(self, arg0: int) -> None: ...
    @property
    def point2D_idx(self) -> int:
        """
        (int, default: 4294967295)
        """
    @point2D_idx.setter
    def point2D_idx(self, arg0: int) -> None: ...

class CorrespondenceGraph:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> CorrespondenceGraph: ...
    def __deepcopy__(self, arg0: dict) -> CorrespondenceGraph: ...
    def __init__(self) -> None: ...
    def __repr__(self) -> str: ...
    def add_correspondences(
        self,
        image_id1: int,
        image_id2: int,
        correspondences: numpy.ndarray[
            tuple[M, typing.Literal[2]], numpy.dtype[numpy.uint32]
        ],
    ) -> None: ...
    def add_image(self, image_id: int, num_points2D: int) -> None: ...
    def exists_image(self, image_id: int) -> bool: ...
    def extract_correspondences(
        self, image_id: int, point2D_idx: int
    ) -> list[Correspondence]: ...
    def extract_transitive_correspondences(
        self, image_id: int, point2D_idx: int, transitivity: int
    ) -> list[Correspondence]: ...
    def finalize(self) -> None: ...
    def find_correspondences_between_images(
        self, image_id1: int, image_id2: int
    ) -> numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.uint32]
    ]: ...
    def has_correspondences(self, image_id: int, point2D_idx: int) -> bool: ...
    def is_two_view_observation(
        self, image_id: int, point2D_idx: int
    ) -> bool: ...
    def num_correspondences_between_all_images(self) -> dict[int, int]: ...
    def num_correspondences_between_images(
        self, image_id1: int, image_id2: int
    ) -> int: ...
    def num_correspondences_for_image(self, image_id: int) -> int: ...
    def num_image_pairs(self) -> int: ...
    def num_images(self) -> int: ...
    def num_observations_for_image(self, image_id: int) -> int: ...

class Database:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    @staticmethod
    def image_pair_to_pair_id(image_id1: int, image_id2: int) -> int: ...
    @staticmethod
    def merge(
        database1: Database, database2: Database, merged_database: Database
    ) -> None: ...
    @staticmethod
    def pair_id_to_image_pair(pair_id: int) -> tuple[int, int]: ...
    @staticmethod
    def swap_image_pair(image_id1: int, image_id2: int) -> bool: ...
    def __enter__(self) -> Database: ...
    def __exit__(self, *args) -> None: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, path: str) -> None: ...
    def clear_all_tables(self) -> None: ...
    def clear_cameras(self) -> None: ...
    def clear_descriptors(self) -> None: ...
    def clear_images(self) -> None: ...
    def clear_keypoints(self) -> None: ...
    def clear_matches(self) -> None: ...
    def clear_pose_priors(self) -> None: ...
    def clear_two_view_geometries(self) -> None: ...
    def close(self) -> None: ...
    def delete_inlier_matches(self, image_id1: int, image_id2: int) -> None: ...
    def delete_matches(self, image_id1: int, image_id2: int) -> None: ...
    def exists_camera(self, camera_id: int) -> bool: ...
    def exists_descriptors(self, image_id: int) -> bool: ...
    @typing.overload
    def exists_image(self, image_id: int) -> bool: ...
    @typing.overload
    def exists_image(self, name: str) -> bool: ...
    def exists_inlier_matches(self, image_id1: int, image_id2: int) -> bool: ...
    def exists_keypoints(self, image_id: int) -> bool: ...
    def exists_matches(self, image_id1: int, image_id2: int) -> bool: ...
    def exists_pose_prior(self, image_id: int) -> bool: ...
    def num_descriptors_for_image(self, image_id: int) -> int: ...
    def num_keypoints_for_image(self, image_id: int) -> int: ...
    def open(self, path: str) -> None: ...
    def read_all_cameras(self) -> list[Camera]: ...
    def read_all_images(self) -> list[Image]: ...
    def read_all_matches(
        self,
    ) -> tuple[
        list[int],
        list[
            numpy.ndarray[
                tuple[M, typing.Literal[2]], numpy.dtype[numpy.uint32]
            ]
        ],
    ]: ...
    def read_camera(self, camera_id: int) -> Camera: ...
    def read_descriptors(
        self, image_id: int
    ) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.uint8]]: ...
    @typing.overload
    def read_image(self, image_id: int) -> Image: ...
    @typing.overload
    def read_image(self, name: str) -> Image: ...
    def read_keypoints(
        self, image_id: int
    ) -> numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float32]]: ...
    def read_matches(
        self, image_id1: int, image_id2: int
    ) -> numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.uint32]
    ]: ...
    def read_pose_prior(self, image_id: int) -> PosePrior: ...
    def read_two_view_geometries(
        self,
    ) -> tuple[list[int], list[TwoViewGeometry]]: ...
    def read_two_view_geometry(
        self, image_id1: int, image_id2: int
    ) -> TwoViewGeometry: ...
    def read_two_view_geometry_num_inliers(
        self,
    ) -> tuple[list[int], list[int]]: ...
    def update_camera(self, camera: Camera) -> None: ...
    def update_image(self, image: Image) -> None: ...
    def write_camera(
        self, camera: Camera, use_camera_id: bool = False
    ) -> int: ...
    def write_descriptors(
        self,
        image_id: int,
        descriptors: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.uint8]],
    ) -> None: ...
    def write_image(self, image: Image, use_image_id: bool = False) -> int: ...
    def write_keypoints(
        self,
        image_id: int,
        keypoints: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float32]],
    ) -> None: ...
    def write_matches(
        self,
        image_id1: int,
        image_id2: int,
        matches: numpy.ndarray[
            tuple[M, typing.Literal[2]], numpy.dtype[numpy.uint32]
        ],
    ) -> None: ...
    def write_pose_prior(
        self, image_id: int, pose_prior: PosePrior
    ) -> None: ...
    def write_two_view_geometry(
        self, image_id1: int, image_id2: int, two_view_geometry: TwoViewGeometry
    ) -> None: ...
    @property
    def num_cameras(self) -> int: ...
    @property
    def num_descriptors(self) -> int: ...
    @property
    def num_images(self) -> int: ...
    @property
    def num_inlier_matches(self) -> int: ...
    @property
    def num_keypoints(self) -> int: ...
    @property
    def num_matched_image_pairs(self) -> int: ...
    @property
    def num_matches(self) -> int: ...
    @property
    def num_pose_priors(self) -> int: ...
    @property
    def num_verified_image_pairs(self) -> int: ...

class DatabaseCache:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    @staticmethod
    def create(
        database: Database,
        min_num_matches: int,
        ignore_watermarks: bool,
        image_names: set[str],
    ) -> DatabaseCache: ...
    def __init__(self) -> None: ...
    def exists_camera(self, camera_id: int) -> bool: ...
    def exists_image(self, image_id: int) -> bool: ...
    def find_image_with_name(self, name: str) -> Image: ...
    def num_cameras(self) -> int: ...
    def num_images(self) -> int: ...
    @property
    def cameras(self) -> dict[int, Camera]: ...
    @property
    def correspondence_graph(self) -> CorrespondenceGraph: ...
    @property
    def images(self) -> dict[int, Image]: ...

class DatabaseTransaction:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __enter__(self) -> None: ...
    def __exit__(self, *args) -> None: ...
    def __init__(self, database: Database) -> None: ...

class DelaunayMeshingOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> DelaunayMeshingOptions: ...
    def __deepcopy__(self, arg0: dict) -> DelaunayMeshingOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def distance_sigma_factor(self) -> float:
        """
        The factor that is applied to the computed distance sigma, which isautomatically computed as the 25th percentile of edge lengths. A highervalue will increase the smoothness of the surface. (float, default: 1.0)
        """
    @distance_sigma_factor.setter
    def distance_sigma_factor(self, arg0: float) -> None: ...
    @property
    def max_depth_dist(self) -> float:
        """
        Maximum relative depth difference between input point and a vertex of anexisting cell in the Delaunay triangulation, otherwise a new vertex iscreated in the triangulation. (float, default: 0.05)
        """
    @max_depth_dist.setter
    def max_depth_dist(self, arg0: float) -> None: ...
    @property
    def max_proj_dist(self) -> float:
        """
        Unify input points into one cell in the Delaunay triangulation that fallwithin a reprojected radius of the given pixels. (float, default: 20.0)
        """
    @max_proj_dist.setter
    def max_proj_dist(self, arg0: float) -> None: ...
    @property
    def max_side_length_factor(self) -> float:
        """
        Filtering thresholds for outlier surface mesh faces. If the longest side ofa mesh face (longest out of 3) exceeds the side lengths of all faces at acertain percentile by the given factor, then it is considered an outliermesh face and discarded. (float, default: 25.0)
        """
    @max_side_length_factor.setter
    def max_side_length_factor(self, arg0: float) -> None: ...
    @property
    def max_side_length_percentile(self) -> float:
        """
        Filtering thresholds for outlier surface mesh faces. If the longest side ofa mesh face (longest out of 3) exceeds the side lengths of all faces at acertain percentile by the given factor, then it is considered an outliermesh face and discarded. (float, default: 95.0)
        """
    @max_side_length_percentile.setter
    def max_side_length_percentile(self, arg0: float) -> None: ...
    @property
    def num_threads(self) -> int:
        """
        The number of threads to use for reconstruction. Default is all threads. (int, default: -1)
        """
    @num_threads.setter
    def num_threads(self, arg0: int) -> None: ...
    @property
    def quality_regularization(self) -> float:
        """
        A higher quality regularization leads to a smoother surface. (float, default: 1.0)
        """
    @quality_regularization.setter
    def quality_regularization(self, arg0: float) -> None: ...
    @property
    def visibility_sigma(self) -> float:
        """
        The standard deviation of wrt. the number of images seen by each point.Increasing this value decreases the influence of points seen in few images. (float, default: 3.0)
        """
    @visibility_sigma.setter
    def visibility_sigma(self, arg0: float) -> None: ...

class Device:
    """
    Members:

      auto

      cpu

      cuda
    """

    __members__: typing.ClassVar[
        dict[str, Device]
    ]  # value = {'auto': <Device.auto: -1>, 'cpu': <Device.cpu: 0>, 'cuda': <Device.cuda: 1>}
    auto: typing.ClassVar[Device]  # value = <Device.auto: -1>
    cpu: typing.ClassVar[Device]  # value = <Device.cpu: 0>
    cuda: typing.ClassVar[Device]  # value = <Device.cuda: 1>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class EstimateTriangulationOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> EstimateTriangulationOptions: ...
    def __deepcopy__(self, arg0: dict) -> EstimateTriangulationOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def min_tri_angle(self) -> float:
        """
        Minimum triangulation angle in radians. (float, default: 0.0)
        """
    @min_tri_angle.setter
    def min_tri_angle(self, arg0: float) -> None: ...
    @property
    def ransac(self) -> RANSACOptions:
        """
        RANSAC options. (RANSACOptions, default: RANSACOptions(max_error=0.03490658503988659, min_inlier_ratio=0.02, confidence=0.9999, dyn_num_trials_multiplier=3.0, min_num_trials=0, max_num_trials=10000))
        """
    @ransac.setter
    def ransac(self, arg0: RANSACOptions) -> None: ...
    @property
    def residual_type(self) -> TriangulationResidualType:
        """
        Employed residual type. (TriangulationResidualType, default: TriangulationResidualType.ANGULAR_ERROR)
        """
    @residual_type.setter
    def residual_type(self, arg0: TriangulationResidualType) -> None: ...

class ExhaustiveMatchingOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> ExhaustiveMatchingOptions: ...
    def __deepcopy__(self, arg0: dict) -> ExhaustiveMatchingOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def block_size(self) -> int:
        """
        (int, default: 50)
        """
    @block_size.setter
    def block_size(self, arg0: int) -> None: ...

class ExhaustivePairGenerator(PairGenerator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(
        self, options: ExhaustiveMatchingOptions, database: Database
    ) -> None: ...

class ExperimentalPoseParam:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> ExperimentalPoseParam: ...
    def __deepcopy__(self, arg0: dict) -> ExperimentalPoseParam: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def image_id(self) -> int:
        """
        (int, default: 4294967295)
        """
    @image_id.setter
    def image_id(self, arg0: int) -> None: ...
    @property
    def qvec(self) -> float:
        """
        (NoneType, default: None)
        """
    @qvec.setter
    def qvec(self, arg0: float) -> None: ...
    @property
    def tvec(self) -> float:
        """
        (NoneType, default: None)
        """
    @tvec.setter
    def tvec(self, arg0: float) -> None: ...

class Image:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> Image: ...
    def __deepcopy__(self, arg0: dict) -> Image: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        name: str = "",
        points2D: ListPoint2D = ...,
        cam_from_world: Rigid3d | None = None,
        camera_id: int = 4294967295,
        id: int = 4294967295,
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        name: str = "",
        keypoints: numpy.ndarray[
            tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
        ] = ...,
        cam_from_world: Rigid3d | None = ...,
        camera_id: int = 4294967295,
        id: int = 4294967295,
    ) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def get_observation_point2D_idxs(self) -> list[int]:
        """
        Get the indices of 2D points that observe a 3D point.
        """
    def get_observation_points2D(self) -> ListPoint2D:
        """
        Get the 2D points that observe a 3D point.
        """
    def has_camera_id(self) -> bool:
        """
        Check whether identifier of camera has been set.
        """
    def has_camera_ptr(self) -> bool:
        """
        Check whether the camera pointer has been set.
        """
    def has_point3D(self, point3D_id: int) -> bool:
        """
        Check whether one of the image points is part of a 3D point track.
        """
    def mergedict(self, arg0: dict) -> None: ...
    def num_points2D(self) -> int:
        """
        Get the number of image points (keypoints).
        """
    def point2D(self, point2D_idx: int) -> Point2D:
        """
        Direct accessor for a point2D.
        """
    def project_point(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> (
        numpy.ndarray[
            tuple[typing.Literal[2], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ]
        | None
    ):
        """
        Project 3D point onto the image
        """
    def projection_center(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]:
        """
        Extract the projection center in world space.
        """
    def reset_camera_ptr(self) -> None:
        """
        Make the camera pointer a nullptr.
        """
    def reset_point3D_for_point2D(self, point2D_idx: int) -> None:
        """
        Set the point as not triangulated, i.e. it is not part of a 3D point track
        """
    def reset_pose(self) -> None:
        """
        Invalidate the pose of the image.
        """
    def set_point3D_for_point2D(
        self, point2D_Idx: int, point3D_id: int
    ) -> None:
        """
        Set the point as triangulated, i.e. it is part of a 3D point track.
        """
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    def viewing_direction(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]:
        """
        Extract the viewing direction of the image.
        """
    @property
    def cam_from_world(self) -> Rigid3d | None:
        """
        The pose of the image, defined as the transformation from world to camera space. None if the image is not registered. (NoneType, default: None)
        """
    @cam_from_world.setter
    def cam_from_world(self, arg1: Rigid3d | None) -> None: ...
    @property
    def camera(self) -> Camera | None:
        """
        The address of the camera (NoneType, default: None)
        """
    @camera.setter
    def camera(self, arg1: Camera) -> None: ...
    @property
    def camera_id(self) -> int:
        """
        Unique identifier of the camera. (int, default: 4294967295)
        """
    @camera_id.setter
    def camera_id(self, arg1: int) -> None: ...
    @property
    def has_pose(self) -> bool:
        """
        Whether the image has a valid pose. (bool, default: False)
        """
    @property
    def image_id(self) -> int:
        """
        Unique identifier of the image. (int, default: 4294967295)
        """
    @image_id.setter
    def image_id(self, arg1: int) -> None: ...
    @property
    def name(self) -> str:
        """
        Name of the image. (str, default: )
        """
    @name.setter
    def name(self, arg1: str) -> None: ...
    @property
    def num_points3D(self) -> int:
        """
        Get the number of triangulations, i.e. the number of points that
        are part of a 3D point track. (int, default: 0)
        """
    @property
    def points2D(self) -> ListPoint2D:
        """
        Array of Points2D (=keypoints). (ListPoint2D, default: ListPoint2D[])
        """
    @points2D.setter
    def points2D(self, arg1: ListPoint2D) -> None: ...

class ImageAlignmentError:
    image_name: str
    proj_center_error: float
    rotation_error_deg: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self) -> None: ...

class ImagePairStat:
    num_total_corrs: int
    num_tri_corrs: int
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self) -> None: ...

class ImagePairsMatchingOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> ImagePairsMatchingOptions: ...
    def __deepcopy__(self, arg0: dict) -> ImagePairsMatchingOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def block_size(self) -> int:
        """
        Number of image pairs to match in one batch. (int, default: 1225)
        """
    @block_size.setter
    def block_size(self, arg0: int) -> None: ...
    @property
    def match_list_path(self) -> str:
        """
        Path to the file with the matches. (str, default: )
        """
    @match_list_path.setter
    def match_list_path(self, arg0: str) -> None: ...

class ImageReaderOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> ImageReaderOptions: ...
    def __deepcopy__(self, arg0: dict) -> ImageReaderOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def camera_mask_path(self) -> str:
        """
        Optional path to an image file specifying a mask for all images. No features will be extracted in regions where the mask is black (pixel intensity value 0 in grayscale) (str, default: )
        """
    @camera_mask_path.setter
    def camera_mask_path(self, arg0: str) -> None: ...
    @property
    def camera_model(self) -> str:
        """
        Name of the camera model. (str, default: SIMPLE_RADIAL)
        """
    @camera_model.setter
    def camera_model(self, arg0: str) -> None: ...
    @property
    def camera_params(self) -> str:
        """
        Manual specification of camera parameters. If empty, camera parameters will be extracted from EXIF, i.e. principal point and focal length. (str, default: )
        """
    @camera_params.setter
    def camera_params(self, arg0: str) -> None: ...
    @property
    def default_focal_length_factor(self) -> float:
        """
        If camera parameters are not specified manually and the image does not have focal length EXIF information, the focal length is set to the value `default_focal_length_factor * max(width, height)`. (float, default: 1.2)
        """
    @default_focal_length_factor.setter
    def default_focal_length_factor(self, arg0: float) -> None: ...
    @property
    def existing_camera_id(self) -> int:
        """
        Whether to explicitly use an existing camera for all images. Note that in this case the specified camera model and parameters are ignored. (int, default: -1)
        """
    @existing_camera_id.setter
    def existing_camera_id(self, arg0: int) -> None: ...
    @property
    def mask_path(self) -> str:
        """
        Optional root path to folder which contains imagemasks. For a given image, the corresponding maskmust have the same sub-path below this root as theimage has below image_path. The filename must beequal, aside from the added extension .png. For example, for an image image_path/abc/012.jpg,the mask would be mask_path/abc/012.jpg.png. Nofeatures will be extracted in regions where themask image is black (pixel intensity value 0 ingrayscale). (str, default: )
        """
    @mask_path.setter
    def mask_path(self, arg0: str) -> None: ...

class ImageSelectionMethod:
    """
    Members:

      MAX_VISIBLE_POINTS_NUM

      MAX_VISIBLE_POINTS_RATIO

      MIN_UNCERTAINTY
    """

    MAX_VISIBLE_POINTS_NUM: typing.ClassVar[
        ImageSelectionMethod
    ]  # value = <ImageSelectionMethod.MAX_VISIBLE_POINTS_NUM: 0>
    MAX_VISIBLE_POINTS_RATIO: typing.ClassVar[
        ImageSelectionMethod
    ]  # value = <ImageSelectionMethod.MAX_VISIBLE_POINTS_RATIO: 1>
    MIN_UNCERTAINTY: typing.ClassVar[
        ImageSelectionMethod
    ]  # value = <ImageSelectionMethod.MIN_UNCERTAINTY: 2>
    __members__: typing.ClassVar[
        dict[str, ImageSelectionMethod]
    ]  # value = {'MAX_VISIBLE_POINTS_NUM': <ImageSelectionMethod.MAX_VISIBLE_POINTS_NUM: 0>, 'MAX_VISIBLE_POINTS_RATIO': <ImageSelectionMethod.MAX_VISIBLE_POINTS_RATIO: 1>, 'MIN_UNCERTAINTY': <ImageSelectionMethod.MIN_UNCERTAINTY: 2>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class ImportedPairGenerator(PairGenerator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(
        self, options: ImagePairsMatchingOptions, database: Database
    ) -> None: ...

class IncrementalMapper:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self, arg0: DatabaseCache) -> None: ...
    def adjust_global_bundle(
        self,
        options: IncrementalMapperOptions,
        ba_options: BundleAdjustmentOptions,
    ) -> bool: ...
    def adjust_local_bundle(
        self,
        options: IncrementalMapperOptions,
        ba_options: BundleAdjustmentOptions,
        tri_options: IncrementalTriangulatorOptions,
        image_id: int,
        point3D_ids: set[int],
    ) -> LocalBundleAdjustmentReport: ...
    def begin_reconstruction(self, reconstruction: Reconstruction) -> None: ...
    def clear_modified_points3D(self) -> None: ...
    def complete_and_merge_tracks(
        self, tri_options: IncrementalTriangulatorOptions
    ) -> int: ...
    def complete_tracks(
        self, tri_options: IncrementalTriangulatorOptions
    ) -> int: ...
    def end_reconstruction(self, discard: bool) -> None: ...
    def estimate_initial_two_view_geometry(
        self, options: IncrementalMapperOptions, image_id1: int, image_id2: int
    ) -> TwoViewGeometry | None: ...
    def filter_images(self, options: IncrementalMapperOptions) -> int: ...
    def filter_points(self, options: IncrementalMapperOptions) -> int: ...
    def find_initial_image_pair(
        self, options: IncrementalMapperOptions, image_id1: int, image_id2: int
    ) -> tuple[int, int] | None: ...
    def find_local_bundle(
        self, options: IncrementalMapperOptions, image_id: int
    ) -> list[int]: ...
    def find_next_images(
        self, options: IncrementalMapperOptions
    ) -> list[int]: ...
    def get_modified_points3D(self) -> set[int]: ...
    def iterative_global_refinement(
        self,
        max_num_refinements: int,
        max_refinement_change: float,
        options: IncrementalMapperOptions,
        ba_options: BundleAdjustmentOptions,
        tri_options: IncrementalTriangulatorOptions,
        normalize_reconstruction: bool = True,
    ) -> None: ...
    def iterative_local_refinement(
        self,
        max_num_refinements: int,
        max_refinement_change: float,
        options: IncrementalMapperOptions,
        ba_options: BundleAdjustmentOptions,
        tri_options: IncrementalTriangulatorOptions,
        image_id: int,
    ) -> None: ...
    def merge_tracks(
        self, tri_options: IncrementalTriangulatorOptions
    ) -> int: ...
    def num_shared_reg_images(self) -> int: ...
    def num_total_reg_images(self) -> int: ...
    def register_initial_image_pair(
        self,
        options: IncrementalMapperOptions,
        two_view_geometry: TwoViewGeometry,
        image_id1: int,
        image_id2: int,
    ) -> None: ...
    def register_next_image(
        self, options: IncrementalMapperOptions, image_id: int
    ) -> bool: ...
    def retriangulate(
        self, tri_options: IncrementalTriangulatorOptions
    ) -> int: ...
    def triangulate_image(
        self, tri_options: IncrementalTriangulatorOptions, image_id: int
    ) -> int: ...
    @property
    def existing_image_ids(self) -> set[int]: ...
    @property
    def filtered_images(self) -> set[int]: ...
    @property
    def num_reg_images_per_camera(self) -> dict[int, int]: ...
    @property
    def observation_manager(self) -> ObservationManager: ...
    @property
    def reconstruction(self) -> Reconstruction: ...
    @property
    def triangulator(self) -> IncrementalTriangulator: ...

class IncrementalMapperCallback:
    """
    Members:

      INITIAL_IMAGE_PAIR_REG_CALLBACK

      NEXT_IMAGE_REG_CALLBACK

      LAST_IMAGE_REG_CALLBACK
    """

    INITIAL_IMAGE_PAIR_REG_CALLBACK: typing.ClassVar[
        IncrementalMapperCallback
    ]  # value = <IncrementalMapperCallback.INITIAL_IMAGE_PAIR_REG_CALLBACK: 0>
    LAST_IMAGE_REG_CALLBACK: typing.ClassVar[
        IncrementalMapperCallback
    ]  # value = <IncrementalMapperCallback.LAST_IMAGE_REG_CALLBACK: 2>
    NEXT_IMAGE_REG_CALLBACK: typing.ClassVar[
        IncrementalMapperCallback
    ]  # value = <IncrementalMapperCallback.NEXT_IMAGE_REG_CALLBACK: 1>
    __members__: typing.ClassVar[
        dict[str, IncrementalMapperCallback]
    ]  # value = {'INITIAL_IMAGE_PAIR_REG_CALLBACK': <IncrementalMapperCallback.INITIAL_IMAGE_PAIR_REG_CALLBACK: 0>, 'NEXT_IMAGE_REG_CALLBACK': <IncrementalMapperCallback.NEXT_IMAGE_REG_CALLBACK: 1>, 'LAST_IMAGE_REG_CALLBACK': <IncrementalMapperCallback.LAST_IMAGE_REG_CALLBACK: 2>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class IncrementalMapperOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> IncrementalMapperOptions: ...
    def __deepcopy__(self, arg0: dict) -> IncrementalMapperOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def abs_pose_max_error(self) -> float:
        """
        Maximum reprojection error in absolute pose estimation. (float, default: 12.0)
        """
    @abs_pose_max_error.setter
    def abs_pose_max_error(self, arg0: float) -> None: ...
    @property
    def abs_pose_min_inlier_ratio(self) -> float:
        """
        Minimum inlier ratio in absolute pose estimation. (float, default: 0.25)
        """
    @abs_pose_min_inlier_ratio.setter
    def abs_pose_min_inlier_ratio(self, arg0: float) -> None: ...
    @property
    def abs_pose_min_num_inliers(self) -> int:
        """
        Minimum number of inliers in absolute pose estimation. (int, default: 30)
        """
    @abs_pose_min_num_inliers.setter
    def abs_pose_min_num_inliers(self, arg0: int) -> None: ...
    @property
    def abs_pose_refine_extra_params(self) -> bool:
        """
        Whether to estimate the extra parameters in absolute pose estimation. (bool, default: True)
        """
    @abs_pose_refine_extra_params.setter
    def abs_pose_refine_extra_params(self, arg0: bool) -> None: ...
    @property
    def abs_pose_refine_focal_length(self) -> bool:
        """
        Whether to estimate the focal length in absolute pose estimation. (bool, default: True)
        """
    @abs_pose_refine_focal_length.setter
    def abs_pose_refine_focal_length(self, arg0: bool) -> None: ...
    @property
    def filter_max_reproj_error(self) -> float:
        """
        Maximum reprojection error in pixels for observations. (float, default: 4.0)
        """
    @filter_max_reproj_error.setter
    def filter_max_reproj_error(self, arg0: float) -> None: ...
    @property
    def filter_min_tri_angle(self) -> float:
        """
        Minimum triangulation angle in degrees for stable 3D points. (float, default: 1.5)
        """
    @filter_min_tri_angle.setter
    def filter_min_tri_angle(self, arg0: float) -> None: ...
    @property
    def fix_existing_images(self) -> bool:
        """
        If reconstruction is provided as input, fix the existing image poses. (bool, default: False)
        """
    @fix_existing_images.setter
    def fix_existing_images(self, arg0: bool) -> None: ...
    @property
    def image_selection_method(self) -> ImageSelectionMethod:
        """
        Method to find and select next best image to register. (ImageSelectionMethod, default: ImageSelectionMethod.MIN_UNCERTAINTY)
        """
    @image_selection_method.setter
    def image_selection_method(self, arg0: ImageSelectionMethod) -> None: ...
    @property
    def init_max_error(self) -> float:
        """
        Maximum error in pixels for two-view geometry estimation for initial image pair. (float, default: 4.0)
        """
    @init_max_error.setter
    def init_max_error(self, arg0: float) -> None: ...
    @property
    def init_max_forward_motion(self) -> float:
        """
        Maximum forward motion for initial image pair. (float, default: 0.95)
        """
    @init_max_forward_motion.setter
    def init_max_forward_motion(self, arg0: float) -> None: ...
    @property
    def init_max_reg_trials(self) -> int:
        """
        Maximum number of trials to use an image for initialization. (int, default: 2)
        """
    @init_max_reg_trials.setter
    def init_max_reg_trials(self, arg0: int) -> None: ...
    @property
    def init_min_num_inliers(self) -> int:
        """
        Minimum number of inliers for initial image pair. (int, default: 100)
        """
    @init_min_num_inliers.setter
    def init_min_num_inliers(self, arg0: int) -> None: ...
    @property
    def init_min_tri_angle(self) -> float:
        """
        Minimum triangulation angle for initial image pair. (float, default: 16.0)
        """
    @init_min_tri_angle.setter
    def init_min_tri_angle(self, arg0: float) -> None: ...
    @property
    def local_ba_min_tri_angle(self) -> float:
        """
        Minimum triangulation for images to be chosen in local bundle adjustment. (float, default: 6.0)
        """
    @local_ba_min_tri_angle.setter
    def local_ba_min_tri_angle(self, arg0: float) -> None: ...
    @property
    def local_ba_num_images(self) -> int:
        """
        Number of images to optimize in local bundle adjustment. (int, default: 6)
        """
    @local_ba_num_images.setter
    def local_ba_num_images(self, arg0: int) -> None: ...
    @property
    def max_extra_param(self) -> float:
        """
        The threshold used to filter and ignore images with degenerate intrinsics. (float, default: 1.0)
        """
    @max_extra_param.setter
    def max_extra_param(self, arg0: float) -> None: ...
    @property
    def max_focal_length_ratio(self) -> float:
        """
        The threshold used to filter and ignore images with degenerate intrinsics. (float, default: 10.0)
        """
    @max_focal_length_ratio.setter
    def max_focal_length_ratio(self, arg0: float) -> None: ...
    @property
    def max_reg_trials(self) -> int:
        """
        Maximum number of trials to register an image. (int, default: 3)
        """
    @max_reg_trials.setter
    def max_reg_trials(self, arg0: int) -> None: ...
    @property
    def min_focal_length_ratio(self) -> float:
        """
        The threshold used to filter and ignore images with degenerate intrinsics. (float, default: 0.1)
        """
    @min_focal_length_ratio.setter
    def min_focal_length_ratio(self, arg0: float) -> None: ...
    @property
    def num_threads(self) -> int:
        """
        Number of threads. (int, default: -1)
        """
    @num_threads.setter
    def num_threads(self, arg0: int) -> None: ...

class IncrementalMapperStatus:
    """
    Members:

      NO_INITIAL_PAIR

      BAD_INITIAL_PAIR

      SUCCESS

      INTERRUPTED
    """

    BAD_INITIAL_PAIR: typing.ClassVar[
        IncrementalMapperStatus
    ]  # value = <IncrementalMapperStatus.BAD_INITIAL_PAIR: 1>
    INTERRUPTED: typing.ClassVar[
        IncrementalMapperStatus
    ]  # value = <IncrementalMapperStatus.INTERRUPTED: 3>
    NO_INITIAL_PAIR: typing.ClassVar[
        IncrementalMapperStatus
    ]  # value = <IncrementalMapperStatus.NO_INITIAL_PAIR: 0>
    SUCCESS: typing.ClassVar[
        IncrementalMapperStatus
    ]  # value = <IncrementalMapperStatus.SUCCESS: 2>
    __members__: typing.ClassVar[
        dict[str, IncrementalMapperStatus]
    ]  # value = {'NO_INITIAL_PAIR': <IncrementalMapperStatus.NO_INITIAL_PAIR: 0>, 'BAD_INITIAL_PAIR': <IncrementalMapperStatus.BAD_INITIAL_PAIR: 1>, 'SUCCESS': <IncrementalMapperStatus.SUCCESS: 2>, 'INTERRUPTED': <IncrementalMapperStatus.INTERRUPTED: 3>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class IncrementalPipeline:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(
        self,
        options: IncrementalPipelineOptions,
        image_path: str,
        database_path: str,
        reconstruction_manager: ReconstructionManager,
    ) -> None: ...
    def add_callback(
        self, id: int, func: typing.Callable[[], None]
    ) -> None: ...
    def callback(self, id: int) -> None: ...
    def check_run_global_refinement(
        self,
        reconstruction: Reconstruction,
        ba_prev_num_reg_images: int,
        ba_prev_num_points: int,
    ) -> bool: ...
    def initialize_reconstruction(
        self,
        core_mapper: IncrementalMapper,
        mapper_options: IncrementalMapperOptions,
        reconstruction: Reconstruction,
    ) -> IncrementalMapperStatus: ...
    def load_database(self) -> bool: ...
    def reconstruct(self, mapper_options: IncrementalMapperOptions) -> None: ...
    def reconstruct_sub_model(
        self,
        core_mapper: IncrementalMapper,
        mapper_options: IncrementalMapperOptions,
        reconstruction: Reconstruction,
    ) -> IncrementalMapperStatus: ...
    def run(self) -> None: ...
    @property
    def database_cache(self) -> DatabaseCache: ...
    @property
    def database_path(self) -> str: ...
    @property
    def image_path(self) -> str: ...
    @property
    def options(self) -> IncrementalPipelineOptions: ...
    @property
    def reconstruction_manager(self) -> ReconstructionManager: ...

class IncrementalPipelineOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> IncrementalPipelineOptions: ...
    def __deepcopy__(self, arg0: dict) -> IncrementalPipelineOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def get_global_bundle_adjustment(self) -> BundleAdjustmentOptions: ...
    def get_local_bundle_adjustment(self) -> BundleAdjustmentOptions: ...
    def get_mapper(self) -> IncrementalMapperOptions: ...
    def get_triangulation(self) -> IncrementalTriangulatorOptions: ...
    def is_initial_pair_provided(self) -> bool: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def ba_global_function_tolerance(self) -> float:
        """
        Ceres solver function tolerance for global bundle adjustment. (float, default: 0.0)
        """
    @ba_global_function_tolerance.setter
    def ba_global_function_tolerance(self, arg0: float) -> None: ...
    @property
    def ba_global_images_freq(self) -> int:
        """
        The growth rates after which to perform global bundle adjustment. (int, default: 500)
        """
    @ba_global_images_freq.setter
    def ba_global_images_freq(self, arg0: int) -> None: ...
    @property
    def ba_global_images_ratio(self) -> float:
        """
        The growth rates after which to perform global bundle adjustment. (float, default: 1.1)
        """
    @ba_global_images_ratio.setter
    def ba_global_images_ratio(self, arg0: float) -> None: ...
    @property
    def ba_global_max_num_iterations(self) -> int:
        """
        The maximum number of global bundle adjustment iterations. (int, default: 50)
        """
    @ba_global_max_num_iterations.setter
    def ba_global_max_num_iterations(self, arg0: int) -> None: ...
    @property
    def ba_global_max_refinement_change(self) -> float:
        """
        The thresholds for iterative bundle adjustment refinements. (float, default: 0.0005)
        """
    @ba_global_max_refinement_change.setter
    def ba_global_max_refinement_change(self, arg0: float) -> None: ...
    @property
    def ba_global_max_refinements(self) -> int:
        """
        The thresholds for iterative bundle adjustment refinements. (int, default: 5)
        """
    @ba_global_max_refinements.setter
    def ba_global_max_refinements(self, arg0: int) -> None: ...
    @property
    def ba_global_points_freq(self) -> int:
        """
        The growth rates after which to perform global bundle adjustment. (int, default: 250000)
        """
    @ba_global_points_freq.setter
    def ba_global_points_freq(self, arg0: int) -> None: ...
    @property
    def ba_global_points_ratio(self) -> float:
        """
        The growth rates after which to perform global bundle adjustment. (float, default: 1.1)
        """
    @ba_global_points_ratio.setter
    def ba_global_points_ratio(self, arg0: float) -> None: ...
    @property
    def ba_local_function_tolerance(self) -> float:
        """
        Ceres solver function tolerance for local bundle adjustment. (float, default: 0.0)
        """
    @ba_local_function_tolerance.setter
    def ba_local_function_tolerance(self, arg0: float) -> None: ...
    @property
    def ba_local_max_num_iterations(self) -> int:
        """
        The maximum number of local bundle adjustment iterations. (int, default: 25)
        """
    @ba_local_max_num_iterations.setter
    def ba_local_max_num_iterations(self, arg0: int) -> None: ...
    @property
    def ba_local_max_refinement_change(self) -> float:
        """
        The thresholds for iterative bundle adjustment refinements. (float, default: 0.001)
        """
    @ba_local_max_refinement_change.setter
    def ba_local_max_refinement_change(self, arg0: float) -> None: ...
    @property
    def ba_local_max_refinements(self) -> int:
        """
        The thresholds for iterative bundle adjustment refinements. (int, default: 2)
        """
    @ba_local_max_refinements.setter
    def ba_local_max_refinements(self, arg0: int) -> None: ...
    @property
    def ba_local_num_images(self) -> int:
        """
        The number of images to optimize in local bundle adjustment. (int, default: 6)
        """
    @ba_local_num_images.setter
    def ba_local_num_images(self, arg0: int) -> None: ...
    @property
    def ba_min_num_residuals_for_cpu_multi_threading(self) -> int:
        """
        The minimum number of residuals per bundle adjustment problem to enable multi-threading solving of the problems. (int, default: 50000)
        """
    @ba_min_num_residuals_for_cpu_multi_threading.setter
    def ba_min_num_residuals_for_cpu_multi_threading(
        self, arg0: int
    ) -> None: ...
    @property
    def ba_refine_extra_params(self) -> bool:
        """
        Which intrinsic parameters to optimize during the reconstruction. (bool, default: True)
        """
    @ba_refine_extra_params.setter
    def ba_refine_extra_params(self, arg0: bool) -> None: ...
    @property
    def ba_refine_focal_length(self) -> bool:
        """
        Which intrinsic parameters to optimize during the reconstruction. (bool, default: True)
        """
    @ba_refine_focal_length.setter
    def ba_refine_focal_length(self, arg0: bool) -> None: ...
    @property
    def ba_refine_principal_point(self) -> bool:
        """
        Which intrinsic parameters to optimize during the reconstruction. (bool, default: False)
        """
    @ba_refine_principal_point.setter
    def ba_refine_principal_point(self, arg0: bool) -> None: ...
    @property
    def extract_colors(self) -> bool:
        """
        Whether to extract colors for reconstructed points. (bool, default: True)
        """
    @extract_colors.setter
    def extract_colors(self, arg0: bool) -> None: ...
    @property
    def fix_existing_images(self) -> bool:
        """
        If reconstruction is provided as input, fix the existing image poses. (bool, default: False)
        """
    @fix_existing_images.setter
    def fix_existing_images(self, arg0: bool) -> None: ...
    @property
    def ignore_watermarks(self) -> bool:
        """
        Whether to ignore the inlier matches of watermark image pairs. (bool, default: False)
        """
    @ignore_watermarks.setter
    def ignore_watermarks(self, arg0: bool) -> None: ...
    @property
    def image_names(self) -> set[str]:
        """
        Which images to reconstruct. If no images are specified, all images will be reconstructed by default. (set, default: set())
        """
    @image_names.setter
    def image_names(self, arg0: set[str]) -> None: ...
    @property
    def init_image_id1(self) -> int:
        """
        The image identifier of the first image used to initialize the reconstruction. (int, default: -1)
        """
    @init_image_id1.setter
    def init_image_id1(self, arg0: int) -> None: ...
    @property
    def init_image_id2(self) -> int:
        """
        The image identifier of the second image used to initialize the reconstruction. Determined automatically if left unspecified. (int, default: -1)
        """
    @init_image_id2.setter
    def init_image_id2(self, arg0: int) -> None: ...
    @property
    def init_num_trials(self) -> int:
        """
        The number of trials to initialize the reconstruction. (int, default: 200)
        """
    @init_num_trials.setter
    def init_num_trials(self, arg0: int) -> None: ...
    @property
    def mapper(self) -> IncrementalMapperOptions:
        """
        Options of the IncrementalMapper. (IncrementalMapperOptions, default: IncrementalMapperOptions(init_min_num_inliers=100, init_max_error=4.0, init_max_forward_motion=0.95, init_min_tri_angle=16.0, init_max_reg_trials=2, abs_pose_max_error=12.0, abs_pose_min_num_inliers=30, abs_pose_min_inlier_ratio=0.25, abs_pose_refine_focal_length=True, abs_pose_refine_extra_params=True, local_ba_num_images=6, local_ba_min_tri_angle=6.0, min_focal_length_ratio=0.1, max_focal_length_ratio=10.0, max_extra_param=1.0, filter_max_reproj_error=4.0, filter_min_tri_angle=1.5, max_reg_trials=3, fix_existing_images=False, num_threads=-1, image_selection_method=ImageSelectionMethod.MIN_UNCERTAINTY))
        """
    @mapper.setter
    def mapper(self, arg0: IncrementalMapperOptions) -> None: ...
    @property
    def max_extra_param(self) -> float:
        """
        The threshold used to filter and ignore images with degenerate intrinsics. (float, default: 1.0)
        """
    @max_extra_param.setter
    def max_extra_param(self, arg0: float) -> None: ...
    @property
    def max_focal_length_ratio(self) -> float:
        """
        The threshold used to filter and ignore images with degenerate intrinsics. (float, default: 10.0)
        """
    @max_focal_length_ratio.setter
    def max_focal_length_ratio(self, arg0: float) -> None: ...
    @property
    def max_model_overlap(self) -> int:
        """
        The maximum number of overlapping images between sub-models. If the current sub-models shares more than this number of images with another model, then the reconstruction is stopped. (int, default: 20)
        """
    @max_model_overlap.setter
    def max_model_overlap(self, arg0: int) -> None: ...
    @property
    def max_num_models(self) -> int:
        """
        The number of sub-models to reconstruct. (int, default: 50)
        """
    @max_num_models.setter
    def max_num_models(self, arg0: int) -> None: ...
    @property
    def min_focal_length_ratio(self) -> float:
        """
        The threshold used to filter and ignore images with degenerate intrinsics. (float, default: 0.1)
        """
    @min_focal_length_ratio.setter
    def min_focal_length_ratio(self, arg0: float) -> None: ...
    @property
    def min_model_size(self) -> int:
        """
        The minimum number of registered images of a sub-model, otherwise the sub-model is discarded. Note that the first sub-model is always kept independent of size. (int, default: 10)
        """
    @min_model_size.setter
    def min_model_size(self, arg0: int) -> None: ...
    @property
    def min_num_matches(self) -> int:
        """
        The minimum number of matches for inlier matches to be considered. (int, default: 15)
        """
    @min_num_matches.setter
    def min_num_matches(self, arg0: int) -> None: ...
    @property
    def multiple_models(self) -> bool:
        """
        Whether to reconstruct multiple sub-models. (bool, default: True)
        """
    @multiple_models.setter
    def multiple_models(self, arg0: bool) -> None: ...
    @property
    def num_threads(self) -> int:
        """
        The number of threads to use during reconstruction. (int, default: -1)
        """
    @num_threads.setter
    def num_threads(self, arg0: int) -> None: ...
    @property
    def snapshot_images_freq(self) -> int:
        """
        Frequency of registered images according to which reconstruction snapshots will be saved. (int, default: 0)
        """
    @snapshot_images_freq.setter
    def snapshot_images_freq(self, arg0: int) -> None: ...
    @property
    def snapshot_path(self) -> str:
        """
        Path to a folder in which reconstruction snapshots will be saved during incremental reconstruction. (str, default: )
        """
    @snapshot_path.setter
    def snapshot_path(self, arg0: str) -> None: ...
    @property
    def triangulation(self) -> IncrementalTriangulatorOptions:
        """
        Options of the IncrementalTriangulator. (IncrementalTriangulatorOptions, default: IncrementalTriangulatorOptions(max_transitivity=1, create_max_angle_error=2.0, continue_max_angle_error=2.0, merge_max_reproj_error=4.0, complete_max_reproj_error=4.0, complete_max_transitivity=5, re_max_angle_error=5.0, re_min_ratio=0.2, re_max_trials=1, min_angle=1.5, ignore_two_view_tracks=True, min_focal_length_ratio=0.1, max_focal_length_ratio=10.0, max_extra_param=1.0))
        """
    @triangulation.setter
    def triangulation(self, arg0: IncrementalTriangulatorOptions) -> None: ...

class IncrementalTriangulator:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> IncrementalTriangulator: ...
    def __deepcopy__(self, arg0: dict) -> IncrementalTriangulator: ...
    def __init__(
        self,
        correspondence_graph: CorrespondenceGraph,
        reconstruction: Reconstruction,
        observation_manager: ObservationManager = None,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def add_modified_point3D(self, point3D_id: int) -> None: ...
    def clear_modified_points3D(self) -> None: ...
    def complete_all_tracks(
        self, options: IncrementalTriangulatorOptions
    ) -> int: ...
    def complete_image(
        self, options: IncrementalTriangulatorOptions, image_id: int
    ) -> int: ...
    def complete_tracks(
        self, options: IncrementalTriangulatorOptions, point3D_ids: set[int]
    ) -> int: ...
    def merge_all_tracks(
        self, options: IncrementalTriangulatorOptions
    ) -> int: ...
    def merge_tracks(
        self, options: IncrementalTriangulatorOptions, point3D_ids: set[int]
    ) -> int: ...
    def retriangulate(self, options: IncrementalTriangulatorOptions) -> int: ...
    def triangulate_image(
        self, options: IncrementalTriangulatorOptions, image_id: int
    ) -> int: ...

class IncrementalTriangulatorOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> IncrementalTriangulatorOptions: ...
    def __deepcopy__(self, arg0: dict) -> IncrementalTriangulatorOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def complete_max_reproj_error(self) -> float:
        """
        Maximum reprojection error to complete an existing triangulation. (float, default: 4.0)
        """
    @complete_max_reproj_error.setter
    def complete_max_reproj_error(self, arg0: float) -> None: ...
    @property
    def complete_max_transitivity(self) -> int:
        """
        Maximum transitivity for track completion. (int, default: 5)
        """
    @complete_max_transitivity.setter
    def complete_max_transitivity(self, arg0: int) -> None: ...
    @property
    def continue_max_angle_error(self) -> float:
        """
        Maximum angular error to continue existing triangulations. (float, default: 2.0)
        """
    @continue_max_angle_error.setter
    def continue_max_angle_error(self, arg0: float) -> None: ...
    @property
    def create_max_angle_error(self) -> float:
        """
        Maximum angular error to create new triangulations. (float, default: 2.0)
        """
    @create_max_angle_error.setter
    def create_max_angle_error(self, arg0: float) -> None: ...
    @property
    def ignore_two_view_tracks(self) -> bool:
        """
        Whether to ignore two-view tracks. (bool, default: True)
        """
    @ignore_two_view_tracks.setter
    def ignore_two_view_tracks(self, arg0: bool) -> None: ...
    @property
    def max_extra_param(self) -> float:
        """
        The threshold used to filter and ignore images with degenerate intrinsics. (float, default: 1.0)
        """
    @max_extra_param.setter
    def max_extra_param(self, arg0: float) -> None: ...
    @property
    def max_focal_length_ratio(self) -> float:
        """
        The threshold used to filter and ignore images with degenerate intrinsics. (float, default: 10.0)
        """
    @max_focal_length_ratio.setter
    def max_focal_length_ratio(self, arg0: float) -> None: ...
    @property
    def max_transitivity(self) -> int:
        """
        Maximum transitivity to search for correspondences. (int, default: 1)
        """
    @max_transitivity.setter
    def max_transitivity(self, arg0: int) -> None: ...
    @property
    def merge_max_reproj_error(self) -> float:
        """
        Maximum reprojection error in pixels to merge triangulations. (float, default: 4.0)
        """
    @merge_max_reproj_error.setter
    def merge_max_reproj_error(self, arg0: float) -> None: ...
    @property
    def min_angle(self) -> float:
        """
        Minimum pairwise triangulation angle for a stable triangulation. (float, default: 1.5)
        """
    @min_angle.setter
    def min_angle(self, arg0: float) -> None: ...
    @property
    def min_focal_length_ratio(self) -> float:
        """
        The threshold used to filter and ignore images with degenerate intrinsics. (float, default: 0.1)
        """
    @min_focal_length_ratio.setter
    def min_focal_length_ratio(self, arg0: float) -> None: ...
    @property
    def re_max_angle_error(self) -> float:
        """
        Maximum angular error to re-triangulate under-reconstructed image pairs. (float, default: 5.0)
        """
    @re_max_angle_error.setter
    def re_max_angle_error(self, arg0: float) -> None: ...
    @property
    def re_max_trials(self) -> int:
        """
        Maximum number of trials to re-triangulate an image pair. (int, default: 1)
        """
    @re_max_trials.setter
    def re_max_trials(self, arg0: int) -> None: ...
    @property
    def re_min_ratio(self) -> float:
        """
        Minimum ratio of common triangulations between an image pair over the number of correspondences between that image pair to be considered as under-reconstructed. (float, default: 0.2)
        """
    @re_min_ratio.setter
    def re_min_ratio(self, arg0: float) -> None: ...

class ListPoint2D:
    __hash__: typing.ClassVar[None] = None  # type: ignore
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __bool__(self) -> bool:
        """
        Check whether the list is nonempty
        """
    def __contains__(self, x: Point2D) -> bool:
        """
        Return true the container contains ``x``
        """
    @typing.overload
    def __delitem__(self, arg0: int) -> None:
        """
        Delete the list elements at index ``i``
        """
    @typing.overload
    def __delitem__(self, arg0: slice) -> None:
        """
        Delete list elements using a slice object
        """
    def __eq__(self, other: object) -> bool: ...
    @typing.overload
    def __getitem__(self, s: slice) -> ListPoint2D:
        """
        Retrieve list elements using a slice object
        """
    @typing.overload
    def __getitem__(self, arg0: int) -> Point2D: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: ListPoint2D) -> None:
        """
        Copy constructor
        """
    @typing.overload
    def __init__(self, arg0: typing.Iterable) -> None: ...
    def __iter__(self) -> typing.Iterator[Point2D]: ...
    def __len__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this list.
        """
    @typing.overload
    def __setitem__(self, arg0: int, arg1: Point2D) -> None: ...
    @typing.overload
    def __setitem__(self, arg0: slice, arg1: ListPoint2D) -> None:
        """
        Assign list elements using a slice object
        """
    def append(self, x: Point2D) -> None:
        """
        Add an item to the end of the list
        """
    def clear(self) -> None:
        """
        Clear the contents
        """
    def count(self, x: Point2D) -> int:
        """
        Return the number of times ``x`` appears in the list
        """
    @typing.overload
    def extend(self, L: ListPoint2D) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    @typing.overload
    def extend(self, L: typing.Iterable) -> None:
        """
        Extend the list by appending all the items in the given list
        """
    def insert(self, i: int, x: Point2D) -> None:
        """
        Insert an item at a given position.
        """
    @typing.overload
    def pop(self) -> Point2D:
        """
        Remove and return the last item
        """
    @typing.overload
    def pop(self, i: int) -> Point2D:
        """
        Remove and return the item at index ``i``
        """
    def remove(self, x: Point2D) -> None:
        """
        Remove the first item from the list whose value is x. It is an error if there is no such item.
        """

class LocalBundleAdjustmentReport:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> LocalBundleAdjustmentReport: ...
    def __deepcopy__(self, arg0: dict) -> LocalBundleAdjustmentReport: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def num_adjusted_observations(self) -> int:
        """
        (int, default: 0)
        """
    @num_adjusted_observations.setter
    def num_adjusted_observations(self, arg0: int) -> None: ...
    @property
    def num_completed_observations(self) -> int:
        """
        (int, default: 0)
        """
    @num_completed_observations.setter
    def num_completed_observations(self, arg0: int) -> None: ...
    @property
    def num_filtered_observations(self) -> int:
        """
        (int, default: 0)
        """
    @num_filtered_observations.setter
    def num_filtered_observations(self, arg0: int) -> None: ...
    @property
    def num_merged_observations(self) -> int:
        """
        (int, default: 0)
        """
    @num_merged_observations.setter
    def num_merged_observations(self, arg0: int) -> None: ...

class LossFunctionType:
    """
    Members:

      TRIVIAL

      SOFT_L1

      CAUCHY
    """

    CAUCHY: typing.ClassVar[
        LossFunctionType
    ]  # value = <LossFunctionType.CAUCHY: 2>
    SOFT_L1: typing.ClassVar[
        LossFunctionType
    ]  # value = <LossFunctionType.SOFT_L1: 1>
    TRIVIAL: typing.ClassVar[
        LossFunctionType
    ]  # value = <LossFunctionType.TRIVIAL: 0>
    __members__: typing.ClassVar[
        dict[str, LossFunctionType]
    ]  # value = {'TRIVIAL': <LossFunctionType.TRIVIAL: 0>, 'SOFT_L1': <LossFunctionType.SOFT_L1: 1>, 'CAUCHY': <LossFunctionType.CAUCHY: 2>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class MapCameraIdToCamera:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: int) -> bool: ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool: ...
    def __delitem__(self, arg0: int) -> None: ...
    def __getitem__(self, arg0: int) -> Camera: ...
    def __init__(self) -> None: ...
    def __iter__(self) -> typing.Iterator[int]: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this map.
        """
    def __setitem__(self, arg0: int, arg1: Camera) -> None: ...
    def items(self) -> typing.ItemsView: ...
    def keys(self) -> typing.KeysView: ...
    def values(self) -> typing.ValuesView: ...

class MapImageIdToImage:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: int) -> bool: ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool: ...
    def __delitem__(self, arg0: int) -> None: ...
    def __getitem__(self, arg0: int) -> Image: ...
    def __init__(self) -> None: ...
    def __iter__(self) -> typing.Iterator[int]: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this map.
        """
    def __setitem__(self, arg0: int, arg1: Image) -> None: ...
    def items(self) -> typing.ItemsView: ...
    def keys(self) -> typing.KeysView: ...
    def values(self) -> typing.ValuesView: ...

class MapPoint3DIdToPoint3D:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __bool__(self) -> bool:
        """
        Check whether the map is nonempty
        """
    @typing.overload
    def __contains__(self, arg0: int) -> bool: ...
    @typing.overload
    def __contains__(self, arg0: typing.Any) -> bool: ...
    def __delitem__(self, arg0: int) -> None: ...
    def __getitem__(self, arg0: int) -> Point3D: ...
    def __init__(self) -> None: ...
    def __iter__(self) -> typing.Iterator[int]: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str:
        """
        Return the canonical string representation of this map.
        """
    def __setitem__(self, arg0: int, arg1: Point3D) -> None: ...
    def items(self) -> typing.ItemsView: ...
    def keys(self) -> typing.KeysView: ...
    def values(self) -> typing.ValuesView: ...

class Normalization:
    """
    Members:

      L1_ROOT : L1-normalizes each descriptor followed by element-wise square rooting. This normalization is usually better than standard L2-normalization. See 'Three things everyone should know to improve object retrieval', Relja Arandjelovic and Andrew Zisserman, CVPR 2012.

      L2 : Each vector is L2-normalized.
    """

    L1_ROOT: typing.ClassVar[
        Normalization
    ]  # value = <Normalization.L1_ROOT: 0>
    L2: typing.ClassVar[Normalization]  # value = <Normalization.L2: 1>
    __members__: typing.ClassVar[
        dict[str, Normalization]
    ]  # value = {'L1_ROOT': <Normalization.L1_ROOT: 0>, 'L2': <Normalization.L2: 1>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class ObservationManager:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(
        self,
        reconstruction: Reconstruction,
        correspondence_graph: CorrespondenceGraph = None,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def add_observation(
        self, point3D_id: int, track_element: TrackElement
    ) -> None:
        """
        Add observation to existing 3D point.
        """
    def add_point3D(
        self,
        xyz: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
        track: Track,
        color: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.uint8],
        ] = ...,
    ) -> int:
        """
        Add new 3D object, and return its unique ID.
        """
    def decrement_correspondence_has_point3D(
        self, image_id: int, point2D_idx: int
    ) -> None:
        """
        Indicate that another image has a point that is not triangulated any more and has a correspondence to this image point. This assumesthat `IncrementCorrespondenceHasPoint3D` was called for the sameimage point and correspondence before.
        """
    def delete_observation(self, image_id: int, point2D_idx: int) -> None:
        """
        Delete one observation from an image and the corresponding 3D point. Note that this deletes the entire 3D point, if the track has two elements prior to calling this method.
        """
    def delete_point3D(self, point3D_id: int) -> None:
        """
        Delete a 3D point, and all its references in the observed images.
        """
    def deregister_image(self, image_id: int) -> None:
        """
        De-register an existing image, and all its references.
        """
    def filter_all_points3D(
        self, max_reproj_error: float, min_tri_angle: float
    ) -> int:
        """
        Filter 3D points with large reprojection error, negative depth, orinsufficient triangulation angle. Return the number of filtered observations.
        """
    def filter_images(
        self,
        min_focal_length_ratio: float,
        max_focal_length_ratio: float,
        max_extra_param: float,
    ) -> list[int]:
        """
        Filter images without observations or bogus camera parameters.Return the identifiers of the filtered images.
        """
    def filter_observations_with_negative_depth(self) -> int:
        """
        Filter observations that have negative depth. Return the number of filtered observations.
        """
    def filter_points3D(
        self,
        max_reproj_error: float,
        min_tri_angle: float,
        point3D_ids: set[int],
    ) -> int:
        """
        Filter 3D points with large reprojection error, negative depth, orinsufficient triangulation angle. Return the number of filtered observations.
        """
    def filter_points3D_in_images(
        self, max_reproj_error: float, min_tri_angle: float, image_ids: set[int]
    ) -> int:
        """
        Filter 3D points with large reprojection error, negative depth, orinsufficient triangulation angle. Return the number of filtered observations.
        """
    def increment_correspondence_has_point3D(
        self, image_id: int, point2D_idx: int
    ) -> None:
        """
        Indicate that another image has a point that is triangulated and has a correspondence to this image point.
        """
    def merge_points3D(self, point3D_id1: int, point3D_id2: int) -> int:
        """
        Merge two 3D points and return new identifier of new 3D point.The location of the merged 3D point is a weighted average of the two original 3D point's locations according to their track lengths.
        """
    def num_correspondences(self, image_id: int) -> int:
        """
        Number of correspondences for all image points.
        """
    def num_observations(self, image_id: int) -> int:
        """
        Number of observations, i.e. the number of image points thathave at least one correspondence to another image.
        """
    def num_visible_points3D(self, image_id: int) -> int:
        """
        Get the number of observations that see a triangulated point, i.e. the number of image points that have at least one correspondence toa triangulated point in another image.
        """
    def point3D_visibility_score(self, image_id: int) -> int:
        """
        Get the score of triangulated observations. In contrast to`NumVisiblePoints3D`, this score also captures the distributionof triangulated observations in the image. This is useful to select the next best image in incremental reconstruction, because amore uniform distribution of observations results in more robust registration.
        """
    @property
    def image_pairs(self) -> dict[int, ImagePairStat]: ...

class PairGenerator:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def all_pairs(self) -> list[tuple[int, int]]: ...
    def has_finished(self) -> bool: ...
    def next(self) -> list[tuple[int, int]]: ...
    def reset(self) -> None: ...

class Point2D:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> Point2D: ...
    def __deepcopy__(self, arg0: dict) -> Point2D: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        xy: numpy.ndarray[
            tuple[typing.Literal[2], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
        point3D_id: int = 18446744073709551615,
    ) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def has_point3D(self) -> bool: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def point3D_id(self) -> int:
        """
        (int, default: 18446744073709551615)
        """
    @point3D_id.setter
    def point3D_id(self, arg0: int) -> None: ...
    @property
    def xy(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[2], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]:
        """
        (ndarray, default: [0. 0.])
        """
    @xy.setter
    def xy(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[2], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...

class Point3D:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> Point3D: ...
    def __deepcopy__(self, arg0: dict) -> Point3D: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def color(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.uint8]
    ]:
        """
        (ndarray, default: [0 0 0])
        """
    @color.setter
    def color(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.uint8],
        ],
    ) -> None: ...
    @property
    def error(self) -> float:
        """
        (float, default: -1.0)
        """
    @error.setter
    def error(self, arg0: float) -> None: ...
    @property
    def track(self) -> Track:
        """
        (Track, default: Track(elements=[]))
        """
    @track.setter
    def track(self, arg0: Track) -> None: ...
    @property
    def xyz(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]:
        """
        (ndarray, default: [0. 0. 0.])
        """
    @xyz.setter
    def xyz(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...

class PoissonMeshingOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> PoissonMeshingOptions: ...
    def __deepcopy__(self, arg0: dict) -> PoissonMeshingOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def color(self) -> float:
        """
        If specified, the reconstruction code assumes that the input is equippedwith colors and will extrapolate the color values to the vertices of thereconstructed mesh. The floating point value specifies the relativeimportance of finer color estimates over lower ones. (float, default: 32.0)
        """
    @color.setter
    def color(self, arg0: float) -> None: ...
    @property
    def depth(self) -> int:
        """
        This integer is the maximum depth of the tree that will be used for surfacereconstruction. Running at depth d corresponds to solving on a voxel gridwhose resolution is no larger than 2^d x 2^d x 2^d. Note that since thereconstructor adapts the octree to the sampling density, the specifiedreconstruction depth is only an upper bound. (int, default: 13)
        """
    @depth.setter
    def depth(self, arg0: int) -> None: ...
    @property
    def num_threads(self) -> int:
        """
        The number of threads used for the Poisson reconstruction. (int, default: -1)
        """
    @num_threads.setter
    def num_threads(self, arg0: int) -> None: ...
    @property
    def point_weight(self) -> float:
        """
        This floating point value specifies the importance that interpolation ofthe point samples is given in the formulation of the screened Poissonequation. The results of the original (unscreened) Poisson Reconstructioncan be obtained by setting this value to 0. (float, default: 1.0)
        """
    @point_weight.setter
    def point_weight(self, arg0: float) -> None: ...
    @property
    def trim(self) -> float:
        """
        This floating point values specifies the value for mesh trimming. Thesubset of the mesh with signal value less than the trim value is discarded. (float, default: 10.0)
        """
    @trim.setter
    def trim(self, arg0: float) -> None: ...

class PosePrior:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> PosePrior: ...
    def __deepcopy__(self, arg0: dict) -> PosePrior: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
        arg1: PosePriorCoordinateSystem,
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
        arg1: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[3]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
        arg1: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[3]],
            numpy.dtype[numpy.float64],
        ],
        arg2: PosePriorCoordinateSystem,
    ) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def is_covariance_valid(self) -> bool: ...
    def is_valid(self) -> bool: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def coordinate_system(self) -> PosePriorCoordinateSystem:
        """
        (PosePriorCoordinateSystem, default: PosePriorCoordinateSystem.UNDEFINED)
        """
    @coordinate_system.setter
    def coordinate_system(self, arg0: PosePriorCoordinateSystem) -> None: ...
    @property
    def position(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]:
        """
        (ndarray, default: [nan nan nan])
        """
    @position.setter
    def position(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...
    @property
    def position_covariance(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[3]], numpy.dtype[numpy.float64]
    ]:
        """
        (ndarray, default: [[nan nan nan]
        [nan nan nan]
        [nan nan nan]])
        """
    @position_covariance.setter
    def position_covariance(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[3]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...

class PosePriorBundleAdjustmentOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> PosePriorBundleAdjustmentOptions: ...
    def __deepcopy__(self, arg0: dict) -> PosePriorBundleAdjustmentOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def prior_position_loss_scale(self) -> float:
        """
        Threshold on the residual for the robust loss (chi2 for 3DOF at 95% = 7.815). (float, default: 7.815)
        """
    @prior_position_loss_scale.setter
    def prior_position_loss_scale(self, arg0: float) -> None: ...
    @property
    def ransac_max_error(self) -> float:
        """
        Maximum RANSAC error for Sim3 alignment. (float, default: 0.0)
        """
    @ransac_max_error.setter
    def ransac_max_error(self, arg0: float) -> None: ...
    @property
    def use_robust_loss_on_prior_position(self) -> bool:
        """
        Whether to use a robust loss on prior locations. (bool, default: False)
        """
    @use_robust_loss_on_prior_position.setter
    def use_robust_loss_on_prior_position(self, arg0: bool) -> None: ...

class PosePriorCoordinateSystem:
    """
    Members:

      UNDEFINED

      WGS84

      CARTESIAN
    """

    CARTESIAN: typing.ClassVar[
        PosePriorCoordinateSystem
    ]  # value = <PosePriorCoordinateSystem.CARTESIAN: 1>
    UNDEFINED: typing.ClassVar[
        PosePriorCoordinateSystem
    ]  # value = <PosePriorCoordinateSystem.UNDEFINED: -1>
    WGS84: typing.ClassVar[
        PosePriorCoordinateSystem
    ]  # value = <PosePriorCoordinateSystem.WGS84: 0>
    __members__: typing.ClassVar[
        dict[str, PosePriorCoordinateSystem]
    ]  # value = {'UNDEFINED': <PosePriorCoordinateSystem.UNDEFINED: -1>, 'WGS84': <PosePriorCoordinateSystem.WGS84: 0>, 'CARTESIAN': <PosePriorCoordinateSystem.CARTESIAN: 1>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class RANSACOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> RANSACOptions: ...
    def __deepcopy__(self, arg0: dict) -> RANSACOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def confidence(self) -> float:
        """
        (float, default: 0.9999)
        """
    @confidence.setter
    def confidence(self, arg0: float) -> None: ...
    @property
    def dyn_num_trials_multiplier(self) -> float:
        """
        (float, default: 3.0)
        """
    @dyn_num_trials_multiplier.setter
    def dyn_num_trials_multiplier(self, arg0: float) -> None: ...
    @property
    def max_error(self) -> float:
        """
        (float, default: 4.0)
        """
    @max_error.setter
    def max_error(self, arg0: float) -> None: ...
    @property
    def max_num_trials(self) -> int:
        """
        (int, default: 100000)
        """
    @max_num_trials.setter
    def max_num_trials(self, arg0: int) -> None: ...
    @property
    def min_inlier_ratio(self) -> float:
        """
        (float, default: 0.01)
        """
    @min_inlier_ratio.setter
    def min_inlier_ratio(self, arg0: float) -> None: ...
    @property
    def min_num_trials(self) -> int:
        """
        (int, default: 1000)
        """
    @min_num_trials.setter
    def min_num_trials(self, arg0: int) -> None: ...

class Reconstruction:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> Reconstruction: ...
    def __deepcopy__(self, arg0: dict) -> Reconstruction: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: Reconstruction) -> None: ...
    @typing.overload
    def __init__(self, path: str) -> None: ...
    def __repr__(self) -> str: ...
    def add_camera(self, camera: Camera) -> None:
        """
        Add new camera. There is only one camera per image, while multiple images might be taken by the same camera.
        """
    def add_image(self, image: Image) -> None:
        """
        Add new image. Its camera must have been added before. If its camera object is unset, it will be automatically populated from the added cameras.
        """
    def add_observation(
        self, point3D_id: int, track_element: TrackElement
    ) -> None:
        """
        Add observation to existing 3D point.
        """
    def add_point3D(
        self,
        xyz: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
        track: Track,
        color: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.uint8],
        ] = ...,
    ) -> int:
        """
        Add new 3D object, and return its unique ID.
        """
    def camera(self, camera_id: int) -> Camera:
        """
        Direct accessor for a camera.
        """
    def check(self) -> None:
        """
        Check if current reconstruction is well formed.
        """
    def compute_bounding_box(
        self, p0: float = 0.0, p1: float = 1.0
    ) -> tuple[
        numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
        numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ]: ...
    def compute_mean_observations_per_reg_image(self) -> float: ...
    def compute_mean_reprojection_error(self) -> float: ...
    def compute_mean_track_length(self) -> float: ...
    def compute_num_observations(self) -> int: ...
    def create_image_dirs(self, path: str) -> None:
        """
        Create all image sub-directories in the given path.
        """
    def crop(
        self,
        bbox: tuple[
            numpy.ndarray[
                tuple[typing.Literal[3], typing.Literal[1]],
                numpy.dtype[numpy.float64],
            ],
            numpy.ndarray[
                tuple[typing.Literal[3], typing.Literal[1]],
                numpy.dtype[numpy.float64],
            ],
        ],
    ) -> Reconstruction: ...
    def delete_observation(self, image_id: int, point2D_idx: int) -> None:
        """
        Delete one observation from an image and the corresponding 3D point. Note that this deletes the entire 3D point, if the track has two elements prior to calling this method.
        """
    def delete_point3D(self, point3D_id: int) -> None:
        """
        Delete a 3D point, and all its references in the observed images.
        """
    def deregister_image(self, image_id: int) -> None:
        """
        De-register an existing image, and all its references.
        """
    def exists_camera(self, camera_id: int) -> bool: ...
    def exists_image(self, image_id: int) -> bool: ...
    def exists_point3D(self, point3D_id: int) -> bool: ...
    def export_PLY(self, output_path: str) -> None:
        """
        Export 3D points to PLY format (.ply).
        """
    def extract_colors_for_all_images(self, path: str) -> None:
        """
        Extract colors for all 3D points by computing the mean color of all images.
        """
    def extract_colors_for_image(self, image_id: int, path: str) -> bool:
        """
        Extract colors for 3D points of given image. Colors will be extracted only for 3D points which are completely black. Return True if the image could be read at the given path.
        """
    def find_common_reg_image_ids(
        self, other: Reconstruction
    ) -> list[tuple[int, int]]:
        """
        Find images that are both present in this and the given reconstruction.
        """
    def find_image_with_name(self, name: str) -> Image:
        """
        Find image with matching name. Returns None if no match is found.
        """
    def image(self, image_id: int) -> Image:
        """
        Direct accessor for an image.
        """
    def import_PLY(self, path: str) -> None:
        """
        Import from PLY format. Note that these import functions areonly intended for visualization of data and usable for reconstruction.
        """
    def is_image_registered(self, image_id: int) -> bool:
        """
        Check if image is registered.
        """
    def merge_points3D(self, point3D_id1: int, point3D_id2: int) -> int:
        """
        Merge two 3D points and return new identifier of new 3D point.The location of the merged 3D point is a weighted average of the two original 3D point's locations according to their track lengths.
        """
    def normalize(
        self,
        fixed_scale: bool = False,
        extent: float = 10.0,
        p0: float = 0.1,
        p1: float = 0.9,
        use_images: bool = True,
    ) -> Sim3d:
        """
        Normalize scene by scaling and translation to avoid degeneratevisualization after bundle adjustment and to improve numericalstability of algorithms.

        Translates scene such that the mean of the camera centers or pointlocations are at the origin of the coordinate system.

        Scales scene such that the minimum and maximum camera centers are at the given `extent`, whereas `p0` and `p1` determine the minimum and maximum percentiles of the camera centers considered.
        """
    def num_cameras(self) -> int: ...
    def num_images(self) -> int: ...
    def num_points3D(self) -> int: ...
    def num_reg_images(self) -> int: ...
    def point3D(self, point3D_id: int) -> Point3D:
        """
        Direct accessor for a Point3D.
        """
    def point3D_ids(self) -> set[int]: ...
    def read(self, path: str) -> None:
        """
        Read reconstruction in COLMAP format. Prefer binary.
        """
    def read_binary(self, path: str) -> None: ...
    def read_text(self, path: str) -> None: ...
    def reg_image_ids(self) -> set[int]: ...
    def register_image(self, image_id: int) -> None:
        """
        Register an existing image.
        """
    def summary(self) -> str: ...
    def tear_down(self) -> None: ...
    def transform(self, new_from_old_world: Sim3d) -> None:
        """
        Apply the 3D similarity transformation to all images and points.
        """
    def update_point_3d_errors(self) -> None: ...
    def write(self, output_dir: str) -> None:
        """
        Write reconstruction in COLMAP binary format.
        """
    def write_binary(self, path: str) -> None: ...
    def write_text(self, path: str) -> None: ...
    @property
    def cameras(self) -> MapCameraIdToCamera: ...
    @property
    def images(self) -> MapImageIdToImage: ...
    @property
    def points3D(self) -> MapPoint3DIdToPoint3D: ...

class ReconstructionManager:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self) -> None: ...
    def add(self) -> int: ...
    def clear(self) -> None: ...
    def delete(self, idx: int) -> None: ...
    def get(self, idx: int) -> Reconstruction: ...
    def read(self, path: str) -> int: ...
    def size(self) -> int: ...
    def write(self, path: str) -> None: ...

class Rigid3d:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    @staticmethod
    def interpolate(
        cam_from_world1: Rigid3d, cam_from_world2: Rigid3d, t: float
    ) -> Rigid3d: ...
    def __copy__(self) -> Rigid3d: ...
    def __deepcopy__(self, arg0: dict) -> Rigid3d: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        arg0: Rotation3d,
        arg1: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[4]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    @typing.overload
    def __mul__(self, arg0: Rigid3d) -> Rigid3d: ...
    @typing.overload
    def __mul__(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]: ...
    @typing.overload
    def __mul__(
        self,
        arg0: numpy.ndarray[
            tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]
        ],
    ) -> numpy.ndarray[
        tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]
    ]: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def adjoint(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[6], typing.Literal[6]], numpy.dtype[numpy.float64]
    ]: ...
    def get_covariance_for_inverse(
        self,
        covar: numpy.ndarray[
            tuple[typing.Literal[6], typing.Literal[6]],
            numpy.dtype[numpy.float64],
        ],
    ) -> numpy.ndarray[
        tuple[typing.Literal[6], typing.Literal[6]], numpy.dtype[numpy.float64]
    ]: ...
    def inverse(self) -> Rigid3d: ...
    def matrix(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[4]], numpy.dtype[numpy.float64]
    ]: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def rotation(self) -> Rotation3d:
        """
        (Rotation3d, default: Rotation3d(xyzw=[0, 0, 0, 1]))
        """
    @rotation.setter
    def rotation(self, arg0: Rotation3d) -> None: ...
    @property
    def translation(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]:
        """
        (ndarray, default: [0. 0. 0.])
        """
    @translation.setter
    def translation(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...

class Rotation3d:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> Rotation3d: ...
    def __deepcopy__(self, arg0: dict) -> Rotation3d: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        xyzw: numpy.ndarray[
            tuple[typing.Literal[4], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None:
        """
        Quaternion in [x,y,z,w] format.
        """
    @typing.overload
    def __init__(
        self,
        rotmat: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[3]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None:
        """
        3x3 rotation matrix.
        """
    @typing.overload
    def __init__(
        self,
        axis_angle: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None:
        """
        Axis-angle 3D vector.
        """
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    @typing.overload
    def __mul__(self, arg0: Rotation3d) -> Rotation3d: ...
    @typing.overload
    def __mul__(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]: ...
    @typing.overload
    def __mul__(
        self,
        arg0: numpy.ndarray[
            tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]
        ],
    ) -> numpy.ndarray[
        tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]
    ]: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def angle(self) -> float: ...
    def angle_to(self, other: Rotation3d) -> float: ...
    def inverse(self) -> Rotation3d: ...
    def matrix(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[3]], numpy.dtype[numpy.float64]
    ]: ...
    def mergedict(self, arg0: dict) -> None: ...
    def norm(self) -> float: ...
    def normalize(self) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def quat(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[4], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]:
        """
        Quaternion in [x,y,z,w] format. (ndarray, default: [0. 0. 0. 1.])
        """
    @quat.setter
    def quat(
        self,
        arg1: numpy.ndarray[
            tuple[typing.Literal[4], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...

class SequentialMatchingOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> SequentialMatchingOptions: ...
    def __deepcopy__(self, arg0: dict) -> SequentialMatchingOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    def vocab_tree_options(self) -> VocabTreeMatchingOptions: ...
    @property
    def loop_detection(self) -> bool:
        """
        Loop detection is invoked every `loop_detection_period` images. (bool, default: False)
        """
    @loop_detection.setter
    def loop_detection(self, arg0: bool) -> None: ...
    @property
    def loop_detection_max_num_features(self) -> int:
        """
        The maximum number of features to use for indexing an image. If an image has more features, only the largest-scale features will be indexed. (int, default: -1)
        """
    @loop_detection_max_num_features.setter
    def loop_detection_max_num_features(self, arg0: int) -> None: ...
    @property
    def loop_detection_num_checks(self) -> int:
        """
        Number of nearest-neighbor checks to use in retrieval. (int, default: 256)
        """
    @loop_detection_num_checks.setter
    def loop_detection_num_checks(self, arg0: int) -> None: ...
    @property
    def loop_detection_num_images(self) -> int:
        """
        The number of images to retrieve in loop detection. This number should be significantly bigger than the sequential matching overlap. (int, default: 50)
        """
    @loop_detection_num_images.setter
    def loop_detection_num_images(self, arg0: int) -> None: ...
    @property
    def loop_detection_num_images_after_verification(self) -> int:
        """
        How many images to return after spatial verification. Set to 0 to turn off spatial verification. (int, default: 0)
        """
    @loop_detection_num_images_after_verification.setter
    def loop_detection_num_images_after_verification(
        self, arg0: int
    ) -> None: ...
    @property
    def loop_detection_num_nearest_neighbors(self) -> int:
        """
        Number of nearest neighbors to retrieve per query feature. (int, default: 1)
        """
    @loop_detection_num_nearest_neighbors.setter
    def loop_detection_num_nearest_neighbors(self, arg0: int) -> None: ...
    @property
    def overlap(self) -> int:
        """
        Number of overlapping image pairs. (int, default: 10)
        """
    @overlap.setter
    def overlap(self, arg0: int) -> None: ...
    @property
    def quadratic_overlap(self) -> bool:
        """
        Whether to match images against their quadratic neighbors. (bool, default: True)
        """
    @quadratic_overlap.setter
    def quadratic_overlap(self, arg0: bool) -> None: ...
    @property
    def vocab_tree_path(self) -> str:
        """
        Path to the vocabulary tree. (str, default: )
        """
    @vocab_tree_path.setter
    def vocab_tree_path(self, arg0: str) -> None: ...

class SequentialPairGenerator(PairGenerator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(
        self, options: SequentialMatchingOptions, database: Database
    ) -> None: ...

class Sift:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(
        self,
        options: SiftExtractionOptions | None = None,
        device: Device = Device.auto,
    ) -> None: ...
    @typing.overload
    def extract(
        self, image: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.uint8]]
    ) -> tuple[
        numpy.ndarray[tuple[M, typing.Literal[4]], numpy.dtype[numpy.float32]],
        numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float32]],
    ]: ...
    @typing.overload
    def extract(
        self, image: numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float32]]
    ) -> tuple[
        numpy.ndarray[tuple[M, typing.Literal[4]], numpy.dtype[numpy.float32]],
        numpy.ndarray[tuple[M, N], numpy.dtype[numpy.float32]],
    ]: ...
    @property
    def device(self) -> Device: ...
    @property
    def options(self) -> SiftExtractionOptions: ...

class SiftExtractionOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> SiftExtractionOptions: ...
    def __deepcopy__(self, arg0: dict) -> SiftExtractionOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def darkness_adaptivity(self) -> bool:
        """
        Whether to adapt the feature detection depending on the image darkness. only available on GPU. (bool, default: False)
        """
    @darkness_adaptivity.setter
    def darkness_adaptivity(self, arg0: bool) -> None: ...
    @property
    def domain_size_pooling(self) -> bool:
        """
        "Domain-Size Pooling in Local Descriptors and NetworkArchitectures", J. Dong and S. Soatto, CVPR 2015 (bool, default: False)
        """
    @domain_size_pooling.setter
    def domain_size_pooling(self, arg0: bool) -> None: ...
    @property
    def dsp_max_scale(self) -> float:
        """
        (float, default: 3.0)
        """
    @dsp_max_scale.setter
    def dsp_max_scale(self, arg0: float) -> None: ...
    @property
    def dsp_min_scale(self) -> float:
        """
        (float, default: 0.16666666666666666)
        """
    @dsp_min_scale.setter
    def dsp_min_scale(self, arg0: float) -> None: ...
    @property
    def dsp_num_scales(self) -> int:
        """
        (int, default: 10)
        """
    @dsp_num_scales.setter
    def dsp_num_scales(self, arg0: int) -> None: ...
    @property
    def edge_threshold(self) -> float:
        """
        Edge threshold for detection. (float, default: 10.0)
        """
    @edge_threshold.setter
    def edge_threshold(self, arg0: float) -> None: ...
    @property
    def estimate_affine_shape(self) -> bool:
        """
        Estimate affine shape of SIFT features in the form of oriented ellipses as opposed to original SIFT which estimates oriented disks. (bool, default: False)
        """
    @estimate_affine_shape.setter
    def estimate_affine_shape(self, arg0: bool) -> None: ...
    @property
    def first_octave(self) -> int:
        """
        First octave in the pyramid, i.e. -1 upsamples the image by one level. (int, default: -1)
        """
    @first_octave.setter
    def first_octave(self, arg0: int) -> None: ...
    @property
    def gpu_index(self) -> str:
        """
        Index of the GPU used for feature matching. For multi-GPU matching, you should separate multiple GPU indices by comma, e.g., '0,1,2,3'. (str, default: -1)
        """
    @gpu_index.setter
    def gpu_index(self, arg0: str) -> None: ...
    @property
    def max_image_size(self) -> int:
        """
        Maximum image size, otherwise image will be down-scaled. (int, default: 3200)
        """
    @max_image_size.setter
    def max_image_size(self, arg0: int) -> None: ...
    @property
    def max_num_features(self) -> int:
        """
        Maximum number of features to detect, keeping larger-scale features. (int, default: 8192)
        """
    @max_num_features.setter
    def max_num_features(self, arg0: int) -> None: ...
    @property
    def max_num_orientations(self) -> int:
        """
        Maximum number of orientations per keypoint if not estimate_affine_shape. (int, default: 2)
        """
    @max_num_orientations.setter
    def max_num_orientations(self, arg0: int) -> None: ...
    @property
    def normalization(self) -> Normalization:
        """
        L1_ROOT or L2 descriptor normalization (Normalization, default: Normalization.L1_ROOT)
        """
    @normalization.setter
    def normalization(self, arg0: Normalization) -> None: ...
    @property
    def num_octaves(self) -> int:
        """
        (int, default: 4)
        """
    @num_octaves.setter
    def num_octaves(self, arg0: int) -> None: ...
    @property
    def num_threads(self) -> int:
        """
        Number of threads for feature matching and geometric verification. (int, default: -1)
        """
    @num_threads.setter
    def num_threads(self, arg0: int) -> None: ...
    @property
    def octave_resolution(self) -> int:
        """
        Number of levels per octave. (int, default: 3)
        """
    @octave_resolution.setter
    def octave_resolution(self, arg0: int) -> None: ...
    @property
    def peak_threshold(self) -> float:
        """
        Peak threshold for detection. (float, default: 0.006666666666666667)
        """
    @peak_threshold.setter
    def peak_threshold(self, arg0: float) -> None: ...
    @property
    def upright(self) -> bool:
        """
        Fix the orientation to 0 for upright features (bool, default: False)
        """
    @upright.setter
    def upright(self, arg0: bool) -> None: ...

class SiftMatchingOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> SiftMatchingOptions: ...
    def __deepcopy__(self, arg0: dict) -> SiftMatchingOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def cross_check(self) -> bool:
        """
        Whether to enable cross checking in matching. (bool, default: True)
        """
    @cross_check.setter
    def cross_check(self, arg0: bool) -> None: ...
    @property
    def gpu_index(self) -> str:
        """
        Index of the GPU used for feature matching. For multi-GPU matching, you should separate multiple GPU indices by comma, e.g., "0,1,2,3". (str, default: -1)
        """
    @gpu_index.setter
    def gpu_index(self, arg0: str) -> None: ...
    @property
    def guided_matching(self) -> bool:
        """
        Whether to perform guided matching, if geometric verification succeeds. (bool, default: False)
        """
    @guided_matching.setter
    def guided_matching(self, arg0: bool) -> None: ...
    @property
    def max_distance(self) -> float:
        """
        Maximum distance to best match. (float, default: 0.7)
        """
    @max_distance.setter
    def max_distance(self, arg0: float) -> None: ...
    @property
    def max_num_matches(self) -> int:
        """
        Maximum number of matches. (int, default: 32768)
        """
    @max_num_matches.setter
    def max_num_matches(self, arg0: int) -> None: ...
    @property
    def max_ratio(self) -> float:
        """
        Maximum distance ratio between first and second best match. (float, default: 0.8)
        """
    @max_ratio.setter
    def max_ratio(self, arg0: float) -> None: ...
    @property
    def num_threads(self) -> int:
        """
        (int, default: -1)
        """
    @num_threads.setter
    def num_threads(self, arg0: int) -> None: ...

class Sim3d:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> Sim3d: ...
    def __deepcopy__(self, arg0: dict) -> Sim3d: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(
        self,
        arg0: float,
        arg1: Rotation3d,
        arg2: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...
    @typing.overload
    def __init__(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[4]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    @typing.overload
    def __mul__(self, arg0: Sim3d) -> Sim3d: ...
    @typing.overload
    def __mul__(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]: ...
    @typing.overload
    def __mul__(
        self,
        arg0: numpy.ndarray[
            tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]
        ],
    ) -> numpy.ndarray[
        tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]
    ]: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def inverse(self) -> Sim3d: ...
    def matrix(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[4]], numpy.dtype[numpy.float64]
    ]: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    def transform_camera_world(self, cam_from_world: Rigid3d) -> Rigid3d: ...
    @property
    def rotation(self) -> Rotation3d:
        """
        (Rotation3d, default: Rotation3d(xyzw=[0, 0, 0, 1]))
        """
    @rotation.setter
    def rotation(self, arg0: Rotation3d) -> None: ...
    @property
    def scale(self) -> numpy.ndarray[typing.Any, numpy.dtype[typing.Any]]:
        """
        (ndarray, default: 1.0)
        """
    @scale.setter
    def scale(self, arg1: float) -> None: ...
    @property
    def translation(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[1]], numpy.dtype[numpy.float64]
    ]:
        """
        (ndarray, default: [0. 0. 0.])
        """
    @translation.setter
    def translation(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...

class SpatialMatchingOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> SpatialMatchingOptions: ...
    def __deepcopy__(self, arg0: dict) -> SpatialMatchingOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def ignore_z(self) -> bool:
        """
        Whether to ignore the Z-component of the location prior. (bool, default: True)
        """
    @ignore_z.setter
    def ignore_z(self, arg0: bool) -> None: ...
    @property
    def max_distance(self) -> float:
        """
        The maximum distance between the query and nearest neighbor [meters]. (float, default: 100.0)
        """
    @max_distance.setter
    def max_distance(self, arg0: float) -> None: ...
    @property
    def max_num_neighbors(self) -> int:
        """
        The maximum number of nearest neighbors to match. (int, default: 50)
        """
    @max_num_neighbors.setter
    def max_num_neighbors(self, arg0: int) -> None: ...
    @property
    def num_threads(self) -> int:
        """
        (int, default: -1)
        """
    @num_threads.setter
    def num_threads(self, arg0: int) -> None: ...

class SpatialPairGenerator(PairGenerator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(
        self, options: SpatialMatchingOptions, database: Database
    ) -> None: ...

class StereoFusionOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> StereoFusionOptions: ...
    def __deepcopy__(self, arg0: dict) -> StereoFusionOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def bounding_box(
        self,
    ) -> tuple[
        numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float32],
        ],
        numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[1]],
            numpy.dtype[numpy.float32],
        ],
    ]:
        """
        Bounding box Tuple[min, max] (tuple, default: (array([-3.4028235e+38, -3.4028235e+38, -3.4028235e+38], dtype=float32), array([3.4028235e+38, 3.4028235e+38, 3.4028235e+38], dtype=float32)))
        """
    @bounding_box.setter
    def bounding_box(
        self,
        arg0: tuple[
            numpy.ndarray[
                tuple[typing.Literal[3], typing.Literal[1]],
                numpy.dtype[numpy.float32],
            ],
            numpy.ndarray[
                tuple[typing.Literal[3], typing.Literal[1]],
                numpy.dtype[numpy.float32],
            ],
        ],
    ) -> None: ...
    @property
    def cache_size(self) -> float:
        """
        Cache size in gigabytes for fusion. (float, default: 32.0)
        """
    @cache_size.setter
    def cache_size(self, arg0: float) -> None: ...
    @property
    def check_num_images(self) -> int:
        """
        Number of overlapping images to transitively check for fusing points. (int, default: 50)
        """
    @check_num_images.setter
    def check_num_images(self, arg0: int) -> None: ...
    @property
    def mask_path(self) -> str:
        """
        Path for PNG masks. Same format expected as ImageReaderOptions. (str, default: )
        """
    @mask_path.setter
    def mask_path(self, arg0: str) -> None: ...
    @property
    def max_depth_error(self) -> float:
        """
        Maximum relative difference between measured and projected depth. (float, default: 0.009999999776482582)
        """
    @max_depth_error.setter
    def max_depth_error(self, arg0: float) -> None: ...
    @property
    def max_image_size(self) -> int:
        """
        Maximum image size in either dimension. (int, default: -1)
        """
    @max_image_size.setter
    def max_image_size(self, arg0: int) -> None: ...
    @property
    def max_normal_error(self) -> float:
        """
        Maximum angular difference in degrees of normals of pixels to be fused. (float, default: 10.0)
        """
    @max_normal_error.setter
    def max_normal_error(self, arg0: float) -> None: ...
    @property
    def max_num_pixels(self) -> int:
        """
        Maximum number of pixels to fuse into a single point. (int, default: 10000)
        """
    @max_num_pixels.setter
    def max_num_pixels(self, arg0: int) -> None: ...
    @property
    def max_reproj_error(self) -> float:
        """
        Maximum relative difference between measured and projected pixel. (float, default: 2.0)
        """
    @max_reproj_error.setter
    def max_reproj_error(self, arg0: float) -> None: ...
    @property
    def max_traversal_depth(self) -> int:
        """
        Maximum depth in consistency graph traversal. (int, default: 100)
        """
    @max_traversal_depth.setter
    def max_traversal_depth(self, arg0: int) -> None: ...
    @property
    def min_num_pixels(self) -> int:
        """
        Minimum number of fused pixels to produce a point. (int, default: 5)
        """
    @min_num_pixels.setter
    def min_num_pixels(self, arg0: int) -> None: ...
    @property
    def num_threads(self) -> int:
        """
        The number of threads to use during fusion. (int, default: -1)
        """
    @num_threads.setter
    def num_threads(self, arg0: int) -> None: ...
    @property
    def use_cache(self) -> bool:
        """
        Flag indicating whether to use LRU cache or pre-load all data (bool, default: False)
        """
    @use_cache.setter
    def use_cache(self, arg0: bool) -> None: ...

class SyntheticDatasetMatchConfig:
    """
    Members:

      EXHAUSTIVE

      CHAINED
    """

    CHAINED: typing.ClassVar[
        SyntheticDatasetMatchConfig
    ]  # value = <SyntheticDatasetMatchConfig.CHAINED: 2>
    EXHAUSTIVE: typing.ClassVar[
        SyntheticDatasetMatchConfig
    ]  # value = <SyntheticDatasetMatchConfig.EXHAUSTIVE: 1>
    __members__: typing.ClassVar[
        dict[str, SyntheticDatasetMatchConfig]
    ]  # value = {'EXHAUSTIVE': <SyntheticDatasetMatchConfig.EXHAUSTIVE: 1>, 'CHAINED': <SyntheticDatasetMatchConfig.CHAINED: 2>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class SyntheticDatasetOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> SyntheticDatasetOptions: ...
    def __deepcopy__(self, arg0: dict) -> SyntheticDatasetOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def camera_height(self) -> int:
        """
        (int, default: 768)
        """
    @camera_height.setter
    def camera_height(self, arg0: int) -> None: ...
    @property
    def camera_model_id(self) -> CameraModelId:
        """
        (CameraModelId, default: CameraModelId.SIMPLE_RADIAL)
        """
    @camera_model_id.setter
    def camera_model_id(self, arg0: CameraModelId) -> None: ...
    @property
    def camera_params(self) -> list[float]:
        """
        (list, default: [1280.0, 512.0, 384.0, 0.05])
        """
    @camera_params.setter
    def camera_params(self, arg0: list[float]) -> None: ...
    @property
    def camera_width(self) -> int:
        """
        (int, default: 1024)
        """
    @camera_width.setter
    def camera_width(self, arg0: int) -> None: ...
    @property
    def match_config(self) -> SyntheticDatasetMatchConfig:
        """
        (SyntheticDatasetMatchConfig, default: SyntheticDatasetMatchConfig.EXHAUSTIVE)
        """
    @match_config.setter
    def match_config(self, arg0: SyntheticDatasetMatchConfig) -> None: ...
    @property
    def num_cameras(self) -> int:
        """
        (int, default: 2)
        """
    @num_cameras.setter
    def num_cameras(self, arg0: int) -> None: ...
    @property
    def num_images(self) -> int:
        """
        (int, default: 10)
        """
    @num_images.setter
    def num_images(self, arg0: int) -> None: ...
    @property
    def num_points2D_without_point3D(self) -> int:
        """
        (int, default: 10)
        """
    @num_points2D_without_point3D.setter
    def num_points2D_without_point3D(self, arg0: int) -> None: ...
    @property
    def num_points3D(self) -> int:
        """
        (int, default: 100)
        """
    @num_points3D.setter
    def num_points3D(self, arg0: int) -> None: ...
    @property
    def point2D_stddev(self) -> float:
        """
        (float, default: 0.0)
        """
    @point2D_stddev.setter
    def point2D_stddev(self, arg0: float) -> None: ...
    @property
    def prior_position_stddev(self) -> float:
        """
        (float, default: 1.5)
        """
    @prior_position_stddev.setter
    def prior_position_stddev(self, arg0: float) -> None: ...
    @property
    def use_geographic_coords_prior(self) -> bool:
        """
        (bool, default: False)
        """
    @use_geographic_coords_prior.setter
    def use_geographic_coords_prior(self, arg0: bool) -> None: ...
    @property
    def use_prior_position(self) -> bool:
        """
        (bool, default: False)
        """
    @use_prior_position.setter
    def use_prior_position(self, arg0: bool) -> None: ...

class Timer:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(self) -> None: ...
    def elapsed_hours(self) -> float: ...
    def elapsed_micro_seconds(self) -> float: ...
    def elapsed_minutes(self) -> float: ...
    def elapsed_seconds(self) -> float: ...
    def pause(self) -> None: ...
    def print_hours(self) -> None: ...
    def print_minutes(self) -> None: ...
    def print_seconds(self) -> None: ...
    def reset(self) -> None: ...
    def restart(self) -> None: ...
    def resume(self) -> None: ...
    def start(self) -> None: ...

class Track:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> Track: ...
    def __deepcopy__(self, arg0: dict) -> Track: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: list[TrackElement]) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    @typing.overload
    def add_element(self, image_id: int, point2D_idx: int) -> None:
        """
        Add an observation to the track.
        """
    @typing.overload
    def add_element(self, element: TrackElement) -> None: ...
    def add_elements(self, elements: list[TrackElement]) -> None:
        """
        Add multiple elements.
        """
    @typing.overload
    def delete_element(self, image_id: int, point2D_idx: int) -> None:
        """
        Delete observation from track.
        """
    @typing.overload
    def delete_element(self, index: int) -> None:
        """
        Remove TrackElement at index.
        """
    def length(self) -> int:
        """
        Track Length.
        """
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def elements(self) -> list[TrackElement]:
        """
        (list, default: [])
        """
    @elements.setter
    def elements(self, arg1: list[TrackElement]) -> None: ...

class TrackElement:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> TrackElement: ...
    def __deepcopy__(self, arg0: dict) -> TrackElement: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: int, arg1: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def image_id(self) -> int:
        """
        (int, default: 4294967295)
        """
    @image_id.setter
    def image_id(self, arg0: int) -> None: ...
    @property
    def point2D_idx(self) -> int:
        """
        (int, default: 4294967295)
        """
    @point2D_idx.setter
    def point2D_idx(self, arg0: int) -> None: ...

class TriangulationResidualType:
    """
    Members:

      ANGULAR_ERROR

      REPROJECTION_ERROR
    """

    ANGULAR_ERROR: typing.ClassVar[
        TriangulationResidualType
    ]  # value = <TriangulationResidualType.ANGULAR_ERROR: 0>
    REPROJECTION_ERROR: typing.ClassVar[
        TriangulationResidualType
    ]  # value = <TriangulationResidualType.REPROJECTION_ERROR: 1>
    __members__: typing.ClassVar[
        dict[str, TriangulationResidualType]
    ]  # value = {'ANGULAR_ERROR': <TriangulationResidualType.ANGULAR_ERROR: 0>, 'REPROJECTION_ERROR': <TriangulationResidualType.REPROJECTION_ERROR: 1>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    @typing.overload
    def __init__(self, value: int) -> None: ...
    @typing.overload
    def __init__(self, arg0: str) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class TwoViewGeometry:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> TwoViewGeometry: ...
    def __deepcopy__(self, arg0: dict) -> TwoViewGeometry: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def invert(self) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def E(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[3]], numpy.dtype[numpy.float64]
    ]:
        """
        (ndarray, default: [[0. 0. 0.]
        [0. 0. 0.]
        [0. 0. 0.]])
        """
    @E.setter
    def E(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[3]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...
    @property
    def F(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[3]], numpy.dtype[numpy.float64]
    ]:
        """
        (ndarray, default: [[0. 0. 0.]
        [0. 0. 0.]
        [0. 0. 0.]])
        """
    @F.setter
    def F(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[3]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...
    @property
    def H(
        self,
    ) -> numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[3]], numpy.dtype[numpy.float64]
    ]:
        """
        (ndarray, default: [[0. 0. 0.]
        [0. 0. 0.]
        [0. 0. 0.]])
        """
    @H.setter
    def H(
        self,
        arg0: numpy.ndarray[
            tuple[typing.Literal[3], typing.Literal[3]],
            numpy.dtype[numpy.float64],
        ],
    ) -> None: ...
    @property
    def cam2_from_cam1(self) -> Rigid3d:
        """
        (Rigid3d, default: Rigid3d(rotation_xyzw=[0, 0, 0, 1], translation=[0, 0, 0]))
        """
    @cam2_from_cam1.setter
    def cam2_from_cam1(self, arg0: Rigid3d) -> None: ...
    @property
    def config(self) -> int:
        """
        (int, default: 0)
        """
    @config.setter
    def config(self, arg0: int) -> None: ...
    @property
    def inlier_matches(
        self,
    ) -> numpy.ndarray[tuple[M, typing.Literal[2]], numpy.dtype[numpy.uint32]]:
        """
        (ndarray, default: [])
        """
    @inlier_matches.setter
    def inlier_matches(
        self,
        arg1: numpy.ndarray[
            tuple[M, typing.Literal[2]], numpy.dtype[numpy.uint32]
        ],
    ) -> None: ...
    @property
    def tri_angle(self) -> float:
        """
        (float, default: -1.0)
        """
    @tri_angle.setter
    def tri_angle(self, arg0: float) -> None: ...

class TwoViewGeometryConfiguration:
    """
    Members:

      UNDEFINED

      DEGENERATE

      CALIBRATED

      UNCALIBRATED

      PLANAR

      PANORAMIC

      PLANAR_OR_PANORAMIC

      WATERMARK

      MULTIPLE
    """

    CALIBRATED: typing.ClassVar[
        TwoViewGeometryConfiguration
    ]  # value = <TwoViewGeometryConfiguration.CALIBRATED: 2>
    DEGENERATE: typing.ClassVar[
        TwoViewGeometryConfiguration
    ]  # value = <TwoViewGeometryConfiguration.DEGENERATE: 1>
    MULTIPLE: typing.ClassVar[
        TwoViewGeometryConfiguration
    ]  # value = <TwoViewGeometryConfiguration.MULTIPLE: 8>
    PANORAMIC: typing.ClassVar[
        TwoViewGeometryConfiguration
    ]  # value = <TwoViewGeometryConfiguration.PANORAMIC: 5>
    PLANAR: typing.ClassVar[
        TwoViewGeometryConfiguration
    ]  # value = <TwoViewGeometryConfiguration.PLANAR: 4>
    PLANAR_OR_PANORAMIC: typing.ClassVar[
        TwoViewGeometryConfiguration
    ]  # value = <TwoViewGeometryConfiguration.PLANAR_OR_PANORAMIC: 6>
    UNCALIBRATED: typing.ClassVar[
        TwoViewGeometryConfiguration
    ]  # value = <TwoViewGeometryConfiguration.UNCALIBRATED: 3>
    UNDEFINED: typing.ClassVar[
        TwoViewGeometryConfiguration
    ]  # value = <TwoViewGeometryConfiguration.UNDEFINED: 0>
    WATERMARK: typing.ClassVar[
        TwoViewGeometryConfiguration
    ]  # value = <TwoViewGeometryConfiguration.WATERMARK: 7>
    __members__: typing.ClassVar[
        dict[str, TwoViewGeometryConfiguration]
    ]  # value = {'UNDEFINED': <TwoViewGeometryConfiguration.UNDEFINED: 0>, 'DEGENERATE': <TwoViewGeometryConfiguration.DEGENERATE: 1>, 'CALIBRATED': <TwoViewGeometryConfiguration.CALIBRATED: 2>, 'UNCALIBRATED': <TwoViewGeometryConfiguration.UNCALIBRATED: 3>, 'PLANAR': <TwoViewGeometryConfiguration.PLANAR: 4>, 'PANORAMIC': <TwoViewGeometryConfiguration.PANORAMIC: 5>, 'PLANAR_OR_PANORAMIC': <TwoViewGeometryConfiguration.PLANAR_OR_PANORAMIC: 6>, 'WATERMARK': <TwoViewGeometryConfiguration.WATERMARK: 7>, 'MULTIPLE': <TwoViewGeometryConfiguration.MULTIPLE: 8>}
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __eq__(self, other: typing.Any) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: typing.Any) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    def __str__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class TwoViewGeometryOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> TwoViewGeometryOptions: ...
    def __deepcopy__(self, arg0: dict) -> TwoViewGeometryOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def compute_relative_pose(self) -> bool:
        """
        (bool, default: False)
        """
    @compute_relative_pose.setter
    def compute_relative_pose(self, arg0: bool) -> None: ...
    @property
    def detect_watermark(self) -> bool:
        """
        (bool, default: True)
        """
    @detect_watermark.setter
    def detect_watermark(self, arg0: bool) -> None: ...
    @property
    def force_H_use(self) -> bool:
        """
        (bool, default: False)
        """
    @force_H_use.setter
    def force_H_use(self, arg0: bool) -> None: ...
    @property
    def max_H_inlier_ratio(self) -> float:
        """
        (float, default: 0.8)
        """
    @max_H_inlier_ratio.setter
    def max_H_inlier_ratio(self, arg0: float) -> None: ...
    @property
    def min_E_F_inlier_ratio(self) -> float:
        """
        (float, default: 0.95)
        """
    @min_E_F_inlier_ratio.setter
    def min_E_F_inlier_ratio(self, arg0: float) -> None: ...
    @property
    def min_num_inliers(self) -> int:
        """
        (int, default: 15)
        """
    @min_num_inliers.setter
    def min_num_inliers(self, arg0: int) -> None: ...
    @property
    def multiple_ignore_watermark(self) -> bool:
        """
        (bool, default: True)
        """
    @multiple_ignore_watermark.setter
    def multiple_ignore_watermark(self, arg0: bool) -> None: ...
    @property
    def multiple_models(self) -> bool:
        """
        (bool, default: False)
        """
    @multiple_models.setter
    def multiple_models(self, arg0: bool) -> None: ...
    @property
    def ransac(self) -> RANSACOptions:
        """
        (RANSACOptions, default: RANSACOptions(max_error=4.0, min_inlier_ratio=0.25, confidence=0.999, dyn_num_trials_multiplier=3.0, min_num_trials=100, max_num_trials=10000))
        """
    @ransac.setter
    def ransac(self, arg0: RANSACOptions) -> None: ...
    @property
    def watermark_border_size(self) -> float:
        """
        (float, default: 0.1)
        """
    @watermark_border_size.setter
    def watermark_border_size(self, arg0: float) -> None: ...
    @property
    def watermark_min_inlier_ratio(self) -> float:
        """
        (float, default: 0.7)
        """
    @watermark_min_inlier_ratio.setter
    def watermark_min_inlier_ratio(self, arg0: float) -> None: ...

class UndistortCameraOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> UndistortCameraOptions: ...
    def __deepcopy__(self, arg0: dict) -> UndistortCameraOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def blank_pixels(self) -> float:
        """
        The amount of blank pixels in the undistorted image in the range [0, 1]. (float, default: 0.0)
        """
    @blank_pixels.setter
    def blank_pixels(self, arg0: float) -> None: ...
    @property
    def max_image_size(self) -> int:
        """
        Maximum image size in terms of width or height of the undistorted camera. (int, default: -1)
        """
    @max_image_size.setter
    def max_image_size(self, arg0: int) -> None: ...
    @property
    def max_scale(self) -> float:
        """
        Maximum scale change of camera used to satisfy the blank pixel constraint. (float, default: 2.0)
        """
    @max_scale.setter
    def max_scale(self, arg0: float) -> None: ...
    @property
    def min_scale(self) -> float:
        """
        Minimum scale change of camera used to satisfy the blank pixel constraint. (float, default: 0.2)
        """
    @min_scale.setter
    def min_scale(self, arg0: float) -> None: ...
    @property
    def roi_max_x(self) -> float:
        """
        (float, default: 1.0)
        """
    @roi_max_x.setter
    def roi_max_x(self, arg0: float) -> None: ...
    @property
    def roi_max_y(self) -> float:
        """
        (float, default: 1.0)
        """
    @roi_max_y.setter
    def roi_max_y(self, arg0: float) -> None: ...
    @property
    def roi_min_x(self) -> float:
        """
        (float, default: 0.0)
        """
    @roi_min_x.setter
    def roi_min_x(self, arg0: float) -> None: ...
    @property
    def roi_min_y(self) -> float:
        """
        (float, default: 0.0)
        """
    @roi_min_y.setter
    def roi_min_y(self, arg0: float) -> None: ...

class VocabTreeMatchingOptions:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __copy__(self) -> VocabTreeMatchingOptions: ...
    def __deepcopy__(self, arg0: dict) -> VocabTreeMatchingOptions: ...
    def __getstate__(self) -> dict: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: dict) -> None: ...
    @typing.overload
    def __init__(self, **kwargs) -> None: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, arg0: dict) -> None: ...
    def check(self) -> None: ...
    def mergedict(self, arg0: dict) -> None: ...
    def summary(self, write_type: bool = False) -> str: ...
    def todict(self, recursive: bool = True) -> dict: ...
    @property
    def match_list_path(self) -> str:
        """
        Optional path to file with specific image names to match. (str, default: )
        """
    @match_list_path.setter
    def match_list_path(self, arg0: str) -> None: ...
    @property
    def max_num_features(self) -> int:
        """
        The maximum number of features to use for indexing an image. (int, default: -1)
        """
    @max_num_features.setter
    def max_num_features(self, arg0: int) -> None: ...
    @property
    def num_checks(self) -> int:
        """
        Number of nearest-neighbor checks to use in retrieval. (int, default: 256)
        """
    @num_checks.setter
    def num_checks(self, arg0: int) -> None: ...
    @property
    def num_images(self) -> int:
        """
        Number of images to retrieve for each query image. (int, default: 100)
        """
    @num_images.setter
    def num_images(self, arg0: int) -> None: ...
    @property
    def num_images_after_verification(self) -> int:
        """
        How many images to return after spatial verification. Set to 0 to turn off spatial verification. (int, default: 0)
        """
    @num_images_after_verification.setter
    def num_images_after_verification(self, arg0: int) -> None: ...
    @property
    def num_nearest_neighbors(self) -> int:
        """
        Number of nearest neighbors to retrieve per query feature. (int, default: 5)
        """
    @num_nearest_neighbors.setter
    def num_nearest_neighbors(self, arg0: int) -> None: ...
    @property
    def num_threads(self) -> int:
        """
        (int, default: -1)
        """
    @num_threads.setter
    def num_threads(self, arg0: int) -> None: ...
    @property
    def vocab_tree_path(self) -> str:
        """
        Path to the vocabulary tree. (str, default: )
        """
    @vocab_tree_path.setter
    def vocab_tree_path(self, arg0: str) -> None: ...

class VocabTreePairGenerator(PairGenerator):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __init__(
        self,
        options: VocabTreeMatchingOptions,
        database: Database,
        query_image_ids: list[int] = [],
    ) -> None: ...

class logging:
    class Level:
        """
        Members:

          INFO

          WARNING

          ERROR

          FATAL
        """

        ERROR: typing.ClassVar[logging.Level]  # value = <Level.ERROR: 2>
        FATAL: typing.ClassVar[logging.Level]  # value = <Level.FATAL: 3>
        INFO: typing.ClassVar[logging.Level]  # value = <Level.INFO: 0>
        WARNING: typing.ClassVar[logging.Level]  # value = <Level.WARNING: 1>
        __members__: typing.ClassVar[
            dict[str, logging.Level]
        ]  # value = {'INFO': <Level.INFO: 0>, 'WARNING': <Level.WARNING: 1>, 'ERROR': <Level.ERROR: 2>, 'FATAL': <Level.FATAL: 3>}
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs): ...
        def __eq__(self, other: typing.Any) -> bool: ...
        def __getstate__(self) -> int: ...
        def __hash__(self) -> int: ...
        def __index__(self) -> int: ...
        def __init__(self, value: int) -> None: ...
        def __int__(self) -> int: ...
        def __ne__(self, other: typing.Any) -> bool: ...
        def __repr__(self) -> str: ...
        def __setstate__(self, state: int) -> None: ...
        def __str__(self) -> str: ...
        @property
        def name(self) -> str: ...
        @property
        def value(self) -> int: ...

    ERROR: typing.ClassVar[logging.Level]  # value = <Level.ERROR: 2>
    FATAL: typing.ClassVar[logging.Level]  # value = <Level.FATAL: 3>
    INFO: typing.ClassVar[logging.Level]  # value = <Level.INFO: 0>
    WARNING: typing.ClassVar[logging.Level]  # value = <Level.WARNING: 1>
    alsologtostderr: typing.ClassVar[bool] = True
    log_dir: typing.ClassVar[str] = ""
    logtostderr: typing.ClassVar[bool] = False
    minloglevel: typing.ClassVar[int] = 0
    stderrthreshold: typing.ClassVar[int] = 2
    verbose_level: typing.ClassVar[int] = 0
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    @staticmethod
    def error(message: str) -> None: ...
    @staticmethod
    def fatal(message: str) -> None: ...
    @staticmethod
    def info(message: str) -> None: ...
    @staticmethod
    def set_log_destination(level: logging.Level, path: str) -> None: ...
    @staticmethod
    def verbose(level: int, message: str) -> None: ...
    @staticmethod
    def warning(message: str) -> None: ...

class ostream:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs): ...
    def __enter__(self) -> None: ...
    def __exit__(self, *args) -> None: ...
    def __init__(self, stdout: bool = True, stderr: bool = True) -> None: ...

def absolute_pose_estimation(*args, **kwargs) -> typing.Any:
    """
    Deprecated, use ``estimate_and_refine_absolute_pose`` instead.
    """

def align_reconstruction_to_locations(
    src: Reconstruction,
    tgt_image_names: list[str],
    tgt_locations: numpy.ndarray[
        tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]
    ],
    min_common_images: int,
    ransac_options: RANSACOptions,
) -> Sim3d | None: ...
def align_reconstructions_via_points(
    src_reconstruction: Reconstruction,
    tgt_reconstruction: Reconstruction,
    min_common_observations: int = 3,
    max_error: float = 0.005,
    min_inlier_ratio: float = 0.9,
) -> Sim3d | None: ...
def align_reconstructions_via_proj_centers(
    src_reconstruction: Reconstruction,
    tgt_reconstruction: Reconstruction,
    max_proj_center_error: float,
) -> Sim3d | None: ...
def align_reconstructions_via_reprojections(
    src_reconstruction: Reconstruction,
    tgt_reconstruction: Reconstruction,
    min_inlier_observations: float = 0.3,
    max_reproj_error: float = 8.0,
) -> Sim3d | None: ...
def bundle_adjustment(
    reconstruction: Reconstruction,
    options: BundleAdjustmentOptions = BundleAdjustmentOptions(),
) -> None:
    """
    Jointly refine 3D points and camera poses
    """

def compare_reconstructions(
    reconstruction1: Reconstruction,
    reconstruction2: Reconstruction,
    alignment_error: str = "reprojection",
    min_inlier_observations: float = 0.3,
    max_reproj_error: float = 8.0,
    max_proj_center_error: float = 0.1,
) -> dict | None: ...
def compute_squared_sampson_error(
    points2D1: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    points2D2: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    E: numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[3]], numpy.dtype[numpy.float64]
    ],
) -> list[float]:
    """
    Calculate the squared Sampson error for a given essential or fundamental matrix.
    """

def create_default_bundle_adjuster(
    options: BundleAdjustmentOptions,
    config: BundleAdjustmentConfig,
    reconstruction: Reconstruction,
) -> BundleAdjuster: ...
def create_pose_prior_bundle_adjuster(
    options: BundleAdjustmentOptions,
    prior_options: PosePriorBundleAdjustmentOptions,
    config: BundleAdjustmentConfig,
    pose_priors: dict[int, PosePrior],
    reconstruction: Reconstruction,
) -> BundleAdjuster: ...
def essential_matrix_estimation(*args, **kwargs) -> typing.Any:
    """
    Deprecated, use ``estimate_essential_matrix`` instead.
    """

def essential_matrix_from_pose(
    cam2_from_cam1: Rigid3d,
) -> numpy.ndarray[
    tuple[typing.Literal[3], typing.Literal[3]], numpy.dtype[numpy.float64]
]:
    """
    Construct essential matrix from relative pose.
    """

def estimate_absolute_pose(
    points2D: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    points3D: numpy.ndarray[
        tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]
    ],
    camera: Camera,
    estimation_options: AbsolutePoseEstimationOptions = AbsolutePoseEstimationOptions(),
) -> dict | None:
    """
    Robustly estimate absolute pose using LO-RANSAC without non-linear refinement.
    """

def estimate_and_refine_absolute_pose(
    points2D: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    points3D: numpy.ndarray[
        tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]
    ],
    camera: Camera,
    estimation_options: AbsolutePoseEstimationOptions = AbsolutePoseEstimationOptions(),
    refinement_options: AbsolutePoseRefinementOptions = AbsolutePoseRefinementOptions(),
    return_covariance: bool = False,
) -> dict | None:
    """
    Robust absolute pose estimation with LO-RANSAC followed by non-linear refinement.
    """

def estimate_and_refine_generalized_absolute_pose(
    points2D: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    points3D: numpy.ndarray[
        tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]
    ],
    camera_idxs: list[int],
    cams_from_rig: list[Rigid3d],
    cameras: list[Camera],
    estimation_options: RANSACOptions = AbsolutePoseEstimationOptions().ransac,
    refinement_options: AbsolutePoseRefinementOptions = AbsolutePoseRefinementOptions(),
    return_covariance: bool = False,
) -> dict | None:
    """
    Robustly estimate generalized absolute pose using LO-RANSACfollowed by non-linear refinement.
    """

def estimate_ba_covariance(
    options: BACovarianceOptions,
    reconstruction: Reconstruction,
    bundle_adjuster: BundleAdjuster,
) -> BACovariance | None:
    """
    Computes covariances for the parameters in a bundle adjustment problem. It is important that the problem has a structure suitable for solving using the Schur complement trick. This is the case for the standard configuration of bundle adjustment problems, but be careful if you modify the underlying problem with custom residuals. Returns null if the estimation was not successful.
    """

def estimate_calibrated_two_view_geometry(
    camera1: Camera,
    points1: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    camera2: Camera,
    points2: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    matches: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.uint32]
    ] = None,
    options: TwoViewGeometryOptions = TwoViewGeometryOptions(),
) -> TwoViewGeometry: ...
def estimate_essential_matrix(
    points2D1: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    points2D2: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    camera1: Camera,
    camera2: Camera,
    estimation_options: RANSACOptions = RANSACOptions(),
) -> dict | None:
    """
    Robustly estimate essential matrix with LO-RANSAC and decompose it using the cheirality check.
    """

def estimate_fundamental_matrix(
    points2D1: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    points2D2: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    estimation_options: RANSACOptions = RANSACOptions(),
) -> dict | None:
    """
    Robustly estimate fundamental matrix with LO-RANSAC.
    """

def estimate_homography_matrix(
    points2D1: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    points2D2: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    estimation_options: RANSACOptions = RANSACOptions(),
) -> dict | None:
    """
    Robustly estimate homography matrix using LO-RANSAC.
    """

def estimate_sim3d(
    src: numpy.ndarray[tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]],
    tgt: numpy.ndarray[tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]],
) -> Sim3d | None:
    """
    Estimate the 3D similarity transform tgt_from_src.
    """

def estimate_sim3d_robust(
    src: numpy.ndarray[tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]],
    tgt: numpy.ndarray[tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]],
    estimation_options: RANSACOptions = RANSACOptions(),
) -> Sim3d | None:
    """
    Robustly estimate the 3D similarity transform tgt_from_src using LO-RANSAC.
    """

def estimate_triangulation(
    points: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    cams_from_world: list[Rigid3d],
    cameras: list[Camera],
    options: EstimateTriangulationOptions = EstimateTriangulationOptions(),
) -> dict | None:
    """
    Robustly estimate 3D point from observations in multiple views using LO-RANSAC
    """

def estimate_two_view_geometry(
    camera1: Camera,
    points1: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    camera2: Camera,
    points2: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    matches: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.uint32]
    ] = None,
    options: TwoViewGeometryOptions = TwoViewGeometryOptions(),
) -> TwoViewGeometry: ...
def estimate_two_view_geometry_pose(
    camera1: Camera,
    points1: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    camera2: Camera,
    points2: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    geometry: TwoViewGeometry,
) -> bool: ...
def extract_features(
    database_path: str,
    image_path: str,
    image_list: list[str] = [],
    camera_mode: CameraMode = CameraMode.AUTO,
    camera_model: str = "SIMPLE_RADIAL",
    reader_options: ImageReaderOptions = ImageReaderOptions(),
    sift_options: SiftExtractionOptions = SiftExtractionOptions(),
    device: Device = Device.auto,
) -> None:
    """
    Extract SIFT Features and write them to database
    """

def fundamental_matrix_estimation(*args, **kwargs) -> typing.Any:
    """
    Deprecated, use ``estimate_fundamental_matrix`` instead.
    """

def homography_decomposition(*args, **kwargs) -> typing.Any:
    """
    Deprecated, use ``pose_from_homography_matrix`` instead.
    """

def homography_matrix_estimation(*args, **kwargs) -> typing.Any:
    """
    Deprecated, use ``estimate_homography_matrix`` instead.
    """

def import_images(
    database_path: str,
    image_path: str,
    camera_mode: CameraMode = CameraMode.AUTO,
    image_list: list[str] = [],
    options: ImageReaderOptions = ImageReaderOptions(),
) -> None:
    """
    Import images into a database
    """

def incremental_mapping(
    database_path: str,
    image_path: str,
    output_path: str,
    options: IncrementalPipelineOptions = IncrementalPipelineOptions(),
    input_path: str = "",
    initial_image_pair_callback: typing.Callable[[], None] = None,
    next_image_callback: typing.Callable[[], None] = None,
) -> dict[int, Reconstruction]:
    """
    Recover 3D points and unknown camera poses
    """

def infer_camera_from_image(
    image_path: str, options: ImageReaderOptions = ImageReaderOptions()
) -> Camera:
    """
    Guess the camera parameters from the EXIF metadata
    """

def match_exhaustive(
    database_path: str,
    sift_options: SiftMatchingOptions = SiftMatchingOptions(),
    matching_options: ExhaustiveMatchingOptions = ExhaustiveMatchingOptions(),
    verification_options: TwoViewGeometryOptions = TwoViewGeometryOptions(),
    device: Device = Device.auto,
) -> None:
    """
    Exhaustive feature matching
    """

def match_sequential(
    database_path: str,
    sift_options: SiftMatchingOptions = SiftMatchingOptions(),
    matching_options: SequentialMatchingOptions = SequentialMatchingOptions(),
    verification_options: TwoViewGeometryOptions = TwoViewGeometryOptions(),
    device: Device = Device.auto,
) -> None:
    """
    Sequential feature matching
    """

def match_spatial(
    database_path: str,
    sift_options: SiftMatchingOptions = SiftMatchingOptions(),
    matching_options: SpatialMatchingOptions = SpatialMatchingOptions(),
    verification_options: TwoViewGeometryOptions = TwoViewGeometryOptions(),
    device: Device = Device.auto,
) -> None:
    """
    Spatial feature matching
    """

def match_vocabtree(
    database_path: str,
    sift_options: SiftMatchingOptions = SiftMatchingOptions(),
    matching_options: VocabTreeMatchingOptions = VocabTreeMatchingOptions(),
    verification_options: TwoViewGeometryOptions = TwoViewGeometryOptions(),
    device: Device = Device.auto,
) -> None:
    """
    Vocab tree feature matching
    """

def poisson_meshing(
    input_path: str,
    output_path: str,
    options: PoissonMeshingOptions = PoissonMeshingOptions(),
) -> None:
    """
    Perform Poisson surface reconstruction and return true if successful.
    """

def pose_from_homography_matrix(
    H: numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[3]], numpy.dtype[numpy.float64]
    ],
    K1: numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[3]], numpy.dtype[numpy.float64]
    ],
    K2: numpy.ndarray[
        tuple[typing.Literal[3], typing.Literal[3]], numpy.dtype[numpy.float64]
    ],
    points1: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    points2: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
) -> dict:
    """
    Recover the most probable pose from the given homography matrix using the cheirality check.
    """

def refine_absolute_pose(
    cam_from_world: Rigid3d,
    points2D: numpy.ndarray[
        tuple[M, typing.Literal[2]], numpy.dtype[numpy.float64]
    ],
    points3D: numpy.ndarray[
        tuple[M, typing.Literal[3]], numpy.dtype[numpy.float64]
    ],
    inlier_mask: numpy.ndarray[
        tuple[M, typing.Literal[1]], numpy.dtype[numpy.bool_]
    ],
    camera: Camera,
    refinement_options: AbsolutePoseRefinementOptions = AbsolutePoseRefinementOptions(),
    return_covariance: bool = False,
) -> dict | None:
    """
    Non-linear refinement of absolute pose.
    """

def rig_absolute_pose_estimation(*args, **kwargs) -> typing.Any:
    """
    Deprecated, use ``estimate_and_refine_generalized_absolute_pose`` instead.
    """

def set_random_seed(seed: int) -> None:
    """
    Initialize the PRNG with the given seed.
    """

def stereo_fusion(
    output_path: str,
    workspace_path: str,
    workspace_format: str = "COLMAP",
    pmvs_option_name: str = "option-all",
    input_type: str = "geometric",
    options: StereoFusionOptions = StereoFusionOptions(),
) -> Reconstruction:
    """
    Stereo Fusion
    """

def synthesize_dataset(
    options: SyntheticDatasetOptions, database: Database = None
) -> Reconstruction: ...
def triangulate_points(
    reconstruction: Reconstruction,
    database_path: str,
    image_path: str,
    output_path: str,
    clear_points: bool = True,
    options: IncrementalPipelineOptions = IncrementalPipelineOptions(),
    refine_intrinsics: bool = False,
) -> Reconstruction:
    """
    Triangulate 3D points from known camera poses
    """

def undistort_images(
    output_path: str,
    input_path: str,
    image_path: str,
    image_list: list[str] = [],
    output_type: str = "COLMAP",
    copy_policy: CopyType = CopyType.copy,
    num_patch_match_src_images: int = 20,
    undistort_options: UndistortCameraOptions = UndistortCameraOptions(),
) -> None:
    """
    Undistort images
    """

def verify_matches(
    database_path: str,
    pairs_path: str,
    options: TwoViewGeometryOptions = TwoViewGeometryOptions(),
) -> None:
    """
    Run geometric verification of the matches
    """

COLMAP_build: str = "Commit 682ea9a on 2024-12-06 without CUDA"
COLMAP_version: str = "COLMAP 3.11.1"
__ceres_version__: str = "2.1.0"
__version__: str = "3.11.1"
has_cuda: bool = False
