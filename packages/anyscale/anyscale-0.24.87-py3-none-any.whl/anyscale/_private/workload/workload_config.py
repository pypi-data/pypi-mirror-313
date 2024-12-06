from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from anyscale._private.models import ImageURI, ModelBase
from anyscale.compute_config.models import ComputeConfig


@dataclass(frozen=True)
class WorkloadConfig(ModelBase):
    name: Optional[str] = field(
        default=None, metadata={"docstring": "Should be overwritten by subclass."}
    )

    def _validate_name(self, name: Optional[str]):
        if name is not None and not isinstance(name, str):
            raise TypeError("'name' must be a string.")

    image_uri: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "URI of an existing image. Exclusive with `containerfile`."
        },
    )

    def _validate_image_uri(self, image_uri: Optional[str]):
        if image_uri is not None and not isinstance(image_uri, str):
            raise TypeError(f"'image_uri' must be an str but it is {type(image_uri)}.")
        if image_uri is not None:
            ImageURI.from_str(image_uri)

    containerfile: Optional[str] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "The file path to a containerfile that will be built into an image before running the workload. Exclusive with `image_uri`."
        },
    )

    def _validate_containerfile(self, containerfile: Optional[str]):
        if containerfile is not None and not isinstance(containerfile, str):
            raise TypeError("'containerfile' must be a string.")

    compute_config: Union[ComputeConfig, Dict, str, None] = field(
        default=None,
        metadata={
            "docstring": "The name of an existing registered compute config or an inlined ComputeConfig object."
        },
    )

    def _validate_compute_config(
        self, compute_config: Union[ComputeConfig, Dict, str, None]
    ) -> Union[None, str, ComputeConfig]:
        if compute_config is None or isinstance(compute_config, str):
            return compute_config

        if isinstance(compute_config, dict):
            compute_config = ComputeConfig.from_dict(compute_config)
        if not isinstance(compute_config, ComputeConfig):
            raise TypeError(
                "'compute_config' must be a string, ComputeConfig, or corresponding dict"
            )

        return compute_config

    working_dir: Optional[str] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "Directory that will be used as the working directory for the application. If a local directory is provided, it will be uploaded to cloud storage automatically. When running inside a workspace, this defaults to the current working directory ('.')."
        },
    )

    def _validate_working_dir(self, working_dir: Optional[str]):
        if working_dir is not None and not isinstance(working_dir, str):
            raise TypeError("'working_dir' must be a string.")

    excludes: Optional[List[str]] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "A list of file path globs that will be excluded when uploading local files for `working_dir`."
        },
    )

    def _validate_excludes(self, excludes: Optional[List[str]]):
        if excludes is not None and (
            not isinstance(excludes, list)
            or not all(isinstance(e, str) for e in excludes)
        ):
            raise TypeError("'excludes' must be a list of strings.")

    requirements: Optional[Union[str, List[str]]] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "A list of pip requirements or a path to a `requirements.txt` file for the workload. When running inside a workspace, this defaults to the workspace-tracked requirements."
        },
    )

    def _validate_requirements(self, requirements: Optional[Union[str, List[str]]]):
        if requirements is None or isinstance(requirements, str):
            return

        if not isinstance(requirements, list) or not all(
            isinstance(r, str) for r in requirements
        ):
            raise TypeError(
                "'requirements' must be a string (file path) or list of strings."
            )

    env_vars: Optional[Dict[str, str]] = field(
        default=None,
        repr=True,
        metadata={
            "docstring": "A dictionary of environment variables that will be set for the workload."
        },
    )

    def _validate_env_vars(self, env_vars: Optional[Dict[str, str]]):
        if env_vars is not None and (
            not isinstance(env_vars, dict)
            or not all(
                isinstance(k, str) and isinstance(v, str) for k, v in env_vars.items()
            )
        ):
            raise TypeError("'env_vars' must be a Dict[str, str].")

    py_modules: Optional[List[str]] = field(
        default=None,
        repr=True,
        metadata={
            "docstring": "A list of local directories or remote URIs that will be uploaded and added to the Python path."
        },
    )

    def _validate_py_modules(self, py_modules: Optional[List[str]]):
        if py_modules is not None and (
            not isinstance(py_modules, list)
            or not all(isinstance(m, str) for m in py_modules)
        ):
            raise TypeError("'py_modules' must be a list of strings.")

    cloud: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "The Anyscale Cloud to run this workload on. If not provided, the organization default will be used (or, if running in a workspace, the cloud of the workspace)."
        },
    )

    def _validate_cloud(self, cloud: Optional[str]):
        if cloud is not None and not isinstance(cloud, str):
            raise TypeError("'cloud' must be a string.")

    project: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "The project for the workload. If not provided, the default project for the cloud will be used (or, if running in a workspace, the project of the workspace)."
        },
    )

    def _validate_project(self, project: Optional[str]):
        if project is not None and not isinstance(project, str):
            raise TypeError("'project' must be a string.")

    registry_login_secret: Optional[str] = field(
        default=None,
        repr=False,
        metadata={
            "docstring": "A name or identifier of the secret containing credentials to authenticate to the docker registry hosting the image. "
            "This can only be used when 'image_uri' is specified and the image is not hosted on Anyscale."
        },
    )

    def _validate_registry_login_secret(self, registry_login_secret: Optional[str]):
        if registry_login_secret is not None and not isinstance(
            registry_login_secret, str
        ):
            raise TypeError("'registry_login_secret' must be a string.")

    ray_version: Optional[str] = field(
        default=None,
        metadata={
            "docstring": "The Ray version (X.Y.Z) specified for this image specified by either an image URI or a containerfile. If not provided, the latest Ray version will be used."
        },
    )

    def _validate_ray_version(self, ray_version: Optional[str]):
        if ray_version is not None and not isinstance(ray_version, str):
            raise TypeError("'ray_version' must be a string.")
        if ray_version:
            vs = ray_version.split(".")
            if len(vs) != 3:
                raise ValueError(
                    f"Invalid Ray version format: {ray_version}. Must be in the format 'X.Y.Z'."
                )
