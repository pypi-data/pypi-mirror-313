import os
import warnings
from collections import OrderedDict
from pickle import load as pickle_load
from typing import Any, Callable, Dict, List, Literal, Optional, Type, Union, get_args

from truefoundry.common.utils import (
    get_python_version_major_minor,
    list_pip_packages_installed,
)
from truefoundry.ml.autogen.client import SerializationFormat
from truefoundry.ml.autogen.entities import artifacts as autogen_artifacts
from truefoundry.ml.enums import ModelFramework
from truefoundry.ml.log_types.artifacts.utils import (
    get_single_file_path_if_only_one_in_directory,
    to_unix_path,
)
from truefoundry.pydantic_v1 import BaseModel, Field

# Map serialization format to corresponding pip packages
SERIALIZATION_FORMAT_TO_PACKAGES_NAME_MAP = {
    SerializationFormat.JOBLIB: ["joblib"],
    SerializationFormat.CLOUDPICKLE: ["cloudpickle"],
}


class _SerializationFormatLoaderRegistry:
    def __init__(self):
        # An OrderedDict is used to maintain the order of loaders based on priority
        # The loaders are added in the following order:
        #     1. joblib (if available)
        #     2. cloudpickle (if available)
        #     3. pickle (default fallback)
        # This ensures that when looking up a loader, it follows the correct loading priority.
        self._loader_map: Dict[SerializationFormat, Callable[[bytes], object]] = (
            OrderedDict()
        )
        try:
            from joblib import load as joblib_load

            self._loader_map[SerializationFormat.JOBLIB] = joblib_load
        except ImportError:
            pass

        try:
            from cloudpickle import load as cloudpickle_load

            self._loader_map[SerializationFormat.CLOUDPICKLE] = cloudpickle_load
        except ImportError:
            pass

        # Add pickle loader as a fallback
        self._loader_map[SerializationFormat.PICKLE] = pickle_load

    def get_loader_map(self) -> Dict[SerializationFormat, Callable[[bytes], object]]:
        return self._loader_map


_serialization_format_loader_registry = _SerializationFormatLoaderRegistry()


class FastAIFramework(autogen_artifacts.FastAIFramework):
    """FastAI model Framework"""

    type: Literal["fastai"] = "fastai"


class GluonFramework(autogen_artifacts.GluonFramework):
    """Gluon model Framework"""

    type: Literal["gluon"] = "gluon"


class H2OFramework(autogen_artifacts.H2OFramework):
    """H2O model Framework"""

    type: Literal["h2o"] = "h2o"


class KerasFramework(autogen_artifacts.KerasFramework):
    """Keras model Framework"""

    type: Literal["keras"] = "keras"


class LightGBMFramework(autogen_artifacts.LightGBMFramework):
    """LightGBM model Framework"""

    type: Literal["lightgbm"] = "lightgbm"


class ONNXFramework(autogen_artifacts.ONNXFramework):
    """ONNX model Framework"""

    type: Literal["onnx"] = "onnx"


class PaddleFramework(autogen_artifacts.PaddleFramework):
    """Paddle model Framework"""

    type: Literal["paddle"] = "paddle"


class PyTorchFramework(autogen_artifacts.PyTorchFramework):
    """PyTorch model Framework"""

    type: Literal["pytorch"] = "pytorch"


class SklearnFramework(autogen_artifacts.SklearnFramework):
    """Sklearn model Framework"""

    type: Literal["sklearn"] = "sklearn"


class SpaCyFramework(autogen_artifacts.SpaCyFramework):
    """SpaCy model Framework"""

    type: Literal["spacy"] = "spacy"


class StatsModelsFramework(autogen_artifacts.StatsModelsFramework):
    """StatsModels model Framework"""

    type: Literal["statsmodels"] = "statsmodels"


class TensorFlowFramework(autogen_artifacts.TensorFlowFramework):
    """TensorFlow model Framework"""

    type: Literal["tensorflow"] = "tensorflow"


class TransformersFramework(autogen_artifacts.TransformersFramework):
    """Transformers model Framework"""

    type: Literal["transformers"] = "transformers"


class XGBoostFramework(autogen_artifacts.XGBoostFramework):
    """XGBoost model Framework"""

    type: Literal["xgboost"] = "xgboost"


# Union of all the model frameworks


ModelFrameworkType = Union[
    FastAIFramework,
    GluonFramework,
    H2OFramework,
    KerasFramework,
    LightGBMFramework,
    ONNXFramework,
    PaddleFramework,
    PyTorchFramework,
    SklearnFramework,
    SpaCyFramework,
    StatsModelsFramework,
    TensorFlowFramework,
    TransformersFramework,
    XGBoostFramework,
]


class _ModelFramework(BaseModel):
    __root__: ModelFrameworkType = Field(discriminator="type")

    @classmethod
    def to_model_framework_type(
        cls,
        framework: Optional[Union[str, ModelFramework, "ModelFrameworkType"]] = None,
    ) -> Optional["ModelFrameworkType"]:
        """
        Converts a ModelFramework or string representation to a ModelFrameworkType object.

        Args:
            framework (Optional[Union[str, ModelFramework, ModelFrameworkType]]): ModelFrameworkType or equivalent input.
                Supported frameworks can be found in `truefoundry.ml.enums.ModelFramework`.
                May be `None` if the framework is unknown or unsupported.
                **Deprecated**: Prefer passing a `ModelFrameworkType` instance.

        Returns:
            ModelFrameworkType corresponding to the input, or None if the input is None.
        """
        if framework is None:
            return None

        # Issue a deprecation warning for str and ModelFramework types
        if isinstance(framework, (str, ModelFramework)):
            warnings.warn(
                "Passing a string or ModelFramework Enum is deprecated. Please use a ModelFrameworkType object.",
                DeprecationWarning,
                stacklevel=2,
            )

        # Convert string to ModelFramework
        if isinstance(framework, str):
            framework = ModelFramework(framework)

        # Convert ModelFramework to ModelFrameworkType
        if isinstance(framework, ModelFramework):
            if framework == ModelFramework.UNKNOWN:
                return None
            return cls.parse_obj({"type": framework.value}).__root__

        # Directly return if already a ModelFrameworkType
        if isinstance(framework, get_args(ModelFrameworkType)):
            return framework

        raise ValueError(
            "framework must be a string, ModelFramework enum, or ModelFrameworkType object"
        )

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[ModelFrameworkType]:
        """Create an instance of ModelFramework from a dict"""
        if obj is None:
            return None

        return cls.parse_obj(obj).__root__


# Mapping of model frameworks to pip packages
_MODEL_FRAMEWORK_TO_PIP_PACKAGES: Dict[Type[ModelFrameworkType], List[str]] = {
    SklearnFramework: ["scikit-learn", "numpy", "pandas"],
    XGBoostFramework: ["xgboost", "numpy", "pandas"],
}


def _get_required_framework_pip_packages(framework: "ModelFrameworkType") -> List[str]:
    """
    Fetches the pip packages required for a given model framework.

    Args:
        framework ("ModelFrameworkType"): The model framework for which to fetch the pip packages.

    Returns:
        List[str]: The list of pip packages required for the given model framework.
                  If no packages are found for the framework type, returns an empty list.
    """
    return _MODEL_FRAMEWORK_TO_PIP_PACKAGES.get(framework.__class__, [])


def _detect_model_serialization_format(
    model_file_path: str,
) -> Optional[SerializationFormat]:
    """
    The function will attempt to load the model using each framework's loader and return the first successful one.

    Args:
        model_file_path (str): The path to the file to be loaded.

    Returns:
        Optional[SerializationFormat]: The serialization format if successfully loaded, None otherwise.
    """
    # Attempt to load the model using each framework
    for (
        serialization_format,
        loader,
    ) in _serialization_format_loader_registry.get_loader_map().items():
        try:
            with open(model_file_path, "rb") as f:
                loader(f)
            return serialization_format
        except Exception:
            continue
    return None


def _fetch_framework_specific_pip_packages(
    framework: "ModelFrameworkType",
) -> List[str]:
    """
    Fetch the pip packages required for the given framework, including any dependencies
    related to the framework's serialization format.

    Args:
        framework: The framework object (e.g., SklearnFramework, XGBoostFramework).

    Returns:
        List[str]: A list of pip packages for the given framework and environment,
                   including any dependencies based on the serialization format
                   (e.g., ['numpy==1.19.5', ...]).
    """
    framework_package_names = _get_required_framework_pip_packages(framework=framework)

    # Add serialization format dependencies if applicable
    if isinstance(framework, (SklearnFramework, XGBoostFramework)):
        framework_package_names.extend(
            SERIALIZATION_FORMAT_TO_PACKAGES_NAME_MAP.get(
                framework.serialization_format, []
            )
        )
    return [
        f"{package.name}=={package.version}"
        for package in list_pip_packages_installed(
            filter_package_names=framework_package_names
        )
    ]


def auto_update_environment_details(
    environment: autogen_artifacts.ModelVersionEnvironment,
    framework: Optional[ModelFrameworkType],
):
    """
    Auto fetch the environment details if not provided, based on the provided environment and framework.

    Args:
        environment: The environment object that holds environment details like python_version and pip_packages.
        framework: The framework object (e.g., SklearnFramework, XGBoostFramework) that may affect pip_package fetching.
    """
    # Auto fetch python_version if not provided
    if not environment.python_version:
        environment.python_version = get_python_version_major_minor()

    # Framework-specific pip_package handling
    if framework and not environment.pip_packages:
        environment.pip_packages = _fetch_framework_specific_pip_packages(framework)


def _validate_and_get_absolute_model_filepath(
    model_file_or_folder: str,
    model_filepath: Optional[str] = None,
) -> Optional[str]:
    # If no model_filepath is set, resolve it from the directory
    if not model_filepath:
        # If model_filepath is not set, resolve it based on these cases:
        #    - Case 1: model_file_or_folder/model.joblib -> model.joblib
        #    - Case 2: model_file_or_folder/folder/model.joblib -> folder/model.joblib
        #    - Case 3: model_file_or_folder/folder/model.joblib, model_file_or_folder/config.json -> None
        return get_single_file_path_if_only_one_in_directory(model_file_or_folder)

    # If model_filepath is already set, validate and resolve it:
    #    - Case 1: Resolve the absolute file path of the model file relative to the provided directory.
    #        Example: If model_file_or_folder is '/root/models' and model_filepath is 'model.joblib',
    #                 the resolved model file path would be '/root/models/model.joblib'. Validate it.
    #
    #    - Case 2: If model_filepath is a relative path, resolve it to an absolute path based on the provided directory.
    #        Example: If model_file_or_folder is '/root/models' and model_filepath is 'subfolder/model.joblib',
    #                 the resolved path would be '/root/models/subfolder/model.joblib'. Validate it.
    #
    #    - Case 3: Verify that the resolved model file exists and is a valid file.
    #        Example: If the resolved path is '/root/models/model.joblib', check if the file exists.
    #                 If it does not exist, raise a FileNotFoundError.
    #
    #    - Case 4: Ensure the resolved model file is located within the specified directory or is the directory itself.
    #        Example: If the resolved path is '/root/models/model.joblib' and model_file_or_folder is '/root/models',
    #                 the resolved path is valid. If the file lies outside '/root/models', raise a ValueError.
    #

    # If model_filepath is set, Resolve the absolute path of the model file (It can be a relative path or absolute path)
    model_dir = (
        os.path.dirname(model_file_or_folder)
        if os.path.isfile(model_file_or_folder)
        else model_file_or_folder
    )
    absolute_model_filepath = os.path.abspath(os.path.join(model_dir, model_filepath))

    # Validate if resolve valid is within the provided directory or is the same as it
    if not (
        absolute_model_filepath == model_file_or_folder
        or absolute_model_filepath.startswith(model_file_or_folder + os.sep)
    ):
        raise ValueError(
            f"model_filepath '{model_filepath}' must be relative to "
            f"{model_file_or_folder}. Resolved path '{absolute_model_filepath}' is invalid."
        )

    if not os.path.isfile(absolute_model_filepath):
        raise FileNotFoundError(f"Model file not found: {absolute_model_filepath}")

    return absolute_model_filepath


def _validate_and_resolve_model_filepath(
    model_file_or_folder: str,
    model_filepath: Optional[str] = None,
) -> Optional[str]:
    absolute_model_filepath = _validate_and_get_absolute_model_filepath(
        model_file_or_folder=model_file_or_folder, model_filepath=model_filepath
    )
    if absolute_model_filepath:
        return to_unix_path(
            os.path.relpath(absolute_model_filepath, model_file_or_folder)
            if os.path.isdir(model_file_or_folder)
            else os.path.basename(absolute_model_filepath)
        )


def auto_update_model_framework_details(
    framework: "ModelFrameworkType", model_file_or_folder: str
):
    """
    Auto update the model framework details based on the provided model file or folder path.

    Args:
        framework: The framework object (e.g., SklearnFramework, XGBoostFramework) to update.
        model_file_or_folder: The path to the model file or folder.
    """

    # Ensure the model file or folder path is an absolute path
    model_file_or_folder = os.path.abspath(model_file_or_folder)

    if isinstance(framework, (SklearnFramework, XGBoostFramework)):
        framework.model_filepath = _validate_and_resolve_model_filepath(
            model_file_or_folder=model_file_or_folder,
            model_filepath=framework.model_filepath,
        )
        if framework.model_filepath:
            absolute_model_filepath = (
                model_file_or_folder
                if os.path.isfile(model_file_or_folder)
                else os.path.join(model_file_or_folder, framework.model_filepath)
            )
            framework.serialization_format = (
                framework.serialization_format
                or _detect_model_serialization_format(
                    model_file_path=absolute_model_filepath
                )
            )
