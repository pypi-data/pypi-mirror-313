import json
import grpc
import importlib.util
import importlib.metadata
import pkg_resources
from packaging.requirements import Requirement
from typing import Callable, List, Optional
import traceback
from profiles_rudderstack.model import BaseModelType
from profiles_rudderstack.recipe import PyNativeRecipe
from profiles_rudderstack.material import WhtMaterial, WhtFolder
from profiles_rudderstack.utils import RefManager
from profiles_rudderstack.project import WhtProject
from profiles_rudderstack.logger import Logger
import profiles_rudderstack.tunnel.tunnel_pb2 as tunnel
from profiles_rudderstack.tunnel.tunnel_pb2_grpc import PythonServiceServicer, WhtServiceStub

PYTHON_DISTRIBUTION = "profiles-rudderstack"


class PythonRpcService(PythonServiceServicer):
    def __init__(self, go_rpc: WhtServiceStub, current_supported_schema_version: int, pb_version: str):
        self.logger = Logger("PythonRpcService")
        self.ref_manager = RefManager()
        self.current_supported_schema_version = current_supported_schema_version
        self.pb_version = pb_version
        self.gorpc = go_rpc

    def __register_model_type(self, package: str, project: WhtProject):
        requirement = Requirement(package)
        # special case to skip registering Python distribution as it's not a pynative model type
        if requirement.name == PYTHON_DISTRIBUTION:
            return None

        module = importlib.import_module(requirement.name)
        try:
            registerFunc: Callable[[WhtProject], None] = getattr(
                module, "register_extensions")
        except AttributeError:
            # register_extensions is not found in the package
            # the package is not a pynative model type
            return None

        registerFunc(project)
        return None

    def RegisterPackages(self, request: tunnel.RegisterPackagesRequest, context: grpc.ServicerContext):
        """Register packages and their model types. Called from NewWhtProject"""
        try:
            not_installed: List[str] = []
            packages = set(request.packages)
            for package in packages:
                # special case to skip checking PYTHON_DISTRIBUTION version, as that is handled by pb
                if Requirement(package).name == PYTHON_DISTRIBUTION:
                    continue

                try:
                    pkg_resources.require(package)
                except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict) as e:
                    self.logger.error(traceback.format_exc(limit=1))
                    not_installed.append(package)

            if not_installed:
                error_message = "The following package(s) are not installed or their version is not correct: {}.".format(
                    ", ".join(not_installed))
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(error_message)
                return tunnel.RegisterPackagesResponse()

            project = WhtProject(request.project_id, request.base_proj_ref, self.current_supported_schema_version,
                                 self.pb_version, self.ref_manager, self.gorpc)
            for package in packages:
                err = self.__register_model_type(package, project)
                if err is not None:
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    context.set_details(f"while registering {package}: " + err)
                    return tunnel.RegisterPackagesResponse()

            return tunnel.RegisterPackagesResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc(limit=1)
            context.set_details(tb)
            return tunnel.RegisterPackagesResponse()

    def GetPackageVersion(self, request: tunnel.GetPackageVersionRequest, context: grpc.ServicerContext):
        model_type_ref = self.ref_manager.get_object(
            request.project_id, request.model_type)
        if model_type_ref is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("model type not found")
            return tunnel.GetPackageVersionResponse()

        package = model_type_ref["package"]
        version = importlib.metadata.version(package)
        return tunnel.GetPackageVersionResponse(version=version)

    def ModelFactory(self, request: tunnel.ModelFactoryRequest, context: grpc.ServicerContext):
        try:
            model_type_ref = self.ref_manager.get_object(
                request.project_id, request.model_type)
            if model_type_ref is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("model type not found")
                return tunnel.ModelFactoryResponse()

            build_spec = json.loads(request.build_spec)
            parent_folder = WhtFolder(request.project_id, request.parent_folder_ref)
            wht_model_ref, py_model_ref = model_type_ref["factory_func"](
                request.base_proj_ref, request.model_name, build_spec, parent_folder)
            return tunnel.ModelFactoryResponse(wht_model_ref=wht_model_ref, python_model_ref=py_model_ref)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
            return tunnel.ModelFactoryResponse()

    # Model methods

    def GetMaterialRecipe(self, request: tunnel.GetMaterialRecipeRequest, context: grpc.ServicerContext):
        model: Optional[BaseModelType] = self.ref_manager.get_object(
            request.project_id, request.py_model_ref)
        if model is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("get metaerial recipe: model not found")
            return tunnel.GetMaterialRecipeResponse()

        try:
            recipe = model.get_material_recipe()
            recipe_ref = self.ref_manager.create_ref(
                request.project_id, recipe)
            return tunnel.GetMaterialRecipeResponse(py_recipe_ref=recipe_ref)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
            return tunnel.GetMaterialRecipeResponse()

    def DescribeRecipe(self, request: tunnel.DescribeRecipeRequest, context: grpc.ServicerContext):
        recipe: Optional[PyNativeRecipe] = self.ref_manager.get_object(
            request.project_id, request.py_recipe_ref)
        if recipe is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("describe recipe: recipe not found")
            return tunnel.DescribeRecipeResponse()

        try:
            this = WhtMaterial(request.project_id,
                               request.material_ref, "compile")
            description, extension = recipe.describe(this)
            return tunnel.DescribeRecipeResponse(description=description, extension=extension)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
            return tunnel.DescribeRecipeResponse()

    def RegisterDependencies(self, request: tunnel.RegisterDependenciesRequest, context: grpc.ServicerContext):
        """Prepare the material for execution in dry run mode. In this mode, we discover dependencies. Anything called with de_ref is considered a dependency. However, the recipe is not supposed to be actually executed. warehouse is not supposed to be hit for discovering dependencies."""
        recipe: Optional[PyNativeRecipe] = self.ref_manager.get_object(
            request.project_id, request.py_recipe_ref)
        if recipe is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("prepare recipe: recipe not found")
            return tunnel.RegisterDependenciesResponse()

        try:
            this = WhtMaterial(request.project_id,
                               request.material_ref, "compile")
            recipe.register_dependencies(this)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
        return tunnel.RegisterDependenciesResponse()

    def Execute(self, request: tunnel.ExecuteRequest, context: grpc.ServicerContext):
        """Prepare the recipe if necessary, and execute the recipe to create the material. In this call, it is safe to assume that dependent materials have already been executed."""
        recipe: Optional[PyNativeRecipe] = self.ref_manager.get_object(
            request.project_id, request.py_recipe_ref)
        if recipe is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("recipe not found")
            return tunnel.ExecuteResponse()

        try:
            this = WhtMaterial(request.project_id, request.material_ref, "run")
            recipe.execute(this)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
        return tunnel.ExecuteResponse()

    def GetRecipeHash(self, request: tunnel.GetRecipeHashRequest, context: grpc.ServicerContext):
        recipe: Optional[PyNativeRecipe] = self.ref_manager.get_object(
            request.project_id, request.py_recipe_ref)
        if recipe is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("recipe not found")
            return tunnel.GetRecipeHashResponse()

        try:
            hash = recipe.hash()
            return tunnel.GetRecipeHashResponse(hash=hash)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
            return tunnel.GetRecipeHashResponse()

    def Validate(self, request: tunnel.ValidateRequest, context: grpc.ServicerContext):
        model: Optional[BaseModelType] = self.ref_manager.get_object(
            request.project_id, request.py_model_ref)
        if model is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("model not found")
            return tunnel.ValidateResponse()

        try:
            isValid, reason = model.validate()
            return tunnel.ValidateResponse(valid=isValid, reason=reason)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
            return tunnel.ValidateResponse()

    def DeleteProjectRefs(self, request: tunnel.DeleteProjectRefsRequest, context: grpc.ServicerContext):
        self.ref_manager.delete_refs(request.project_id)
        WhtMaterial._wht_ctx_store.remove_context(request.project_id)
        return tunnel.DeleteProjectRefsResponse()
    # Ping

    def Ping(self, request, context: grpc.ServicerContext):
        return tunnel.PingResponse(message="ready")
