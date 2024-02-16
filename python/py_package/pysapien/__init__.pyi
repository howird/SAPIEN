from __future__ import annotations
import jax
import numpy
import torch
import typing
from . import internal_renderer
from . import math
from . import physx
from . import render
from . import simsense
__all__ = ['Component', 'CudaArray', 'Device', 'Entity', 'Pose', 'Profiler', 'Scene', 'System', 'internal_renderer', 'math', 'physx', 'profile', 'render', 'set_log_level', 'simsense']
_T = typing.TypeVar("_T", Component)
class Component:
    entity_pose: Pose
    name: str
    pose: Pose
    def __init__(self) -> None:
        ...
    def disable(self) -> None:
        """
        disable the component
        """
    def enable(self) -> None:
        """
        enable the component
        """
    def get_entity(self) -> Entity:
        ...
    def get_entity_pose(self) -> Pose:
        ...
    def get_name(self) -> str:
        ...
    def get_pose(self) -> Pose:
        ...
    def set_entity_pose(self, arg0: Pose) -> None:
        ...
    def set_name(self, arg0: str) -> None:
        ...
    def set_pose(self, arg0: Pose) -> None:
        ...
    @property
    def entity(self) -> Entity:
        ...
    @property
    def is_enabled(self) -> bool:
        ...
class CudaArray:
    def __init__(self, arg0: typing.Any) -> None:
        ...
    def dlpack(self) -> typing.Any:
        ...
    def jax(self) -> jax.Array:
        ...
    def torch(self) -> torch.Tensor:
        ...
    @property
    def __cuda_array_interface__(self) -> dict:
        ...
    @property
    def cuda_id(self) -> int:
        ...
    @property
    def ptr(self) -> int:
        ...
    @property
    def shape(self) -> list[int]:
        ...
    @property
    def strides(self) -> list[int]:
        ...
    @property
    def typstr(self) -> str:
        ...
class Device:
    def __init__(self, alias: str) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def can_present(self) -> bool:
        ...
    def can_render(self) -> bool:
        ...
    def is_cpu(self) -> bool:
        ...
    def is_cuda(self) -> bool:
        ...
    @property
    def cuda_id(self) -> int:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def pci_string(self) -> str | None:
        ...
class Entity:
    name: str
    pose: Pose
    def __init__(self) -> None:
        ...
    def add_component(self, component: Component) -> Entity:
        ...
    def add_to_scene(self, scene: Scene) -> Entity:
        ...
    def find_component_by_type(self, cls: type[_T]) -> _T:
        ...
    def get_components(self) -> list[Component]:
        ...
    def get_global_id(self) -> int:
        ...
    def get_name(self) -> str:
        ...
    def get_per_scene_id(self) -> int:
        ...
    def get_pose(self) -> Pose:
        ...
    def get_scene(self) -> Scene:
        ...
    def remove_component(self, component: Component) -> None:
        ...
    @typing.overload
    def remove_from_scene(self) -> None:
        ...
    @typing.overload
    def remove_from_scene(self) -> None:
        ...
    def set_name(self, arg0: str) -> None:
        ...
    def set_pose(self, arg0: Pose) -> None:
        ...
    @property
    def components(self) -> list[Component]:
        ...
    @property
    def global_id(self) -> int:
        ...
    @property
    def per_scene_id(self) -> int:
        ...
    @property
    def scene(self) -> Scene:
        ...
class Pose:
    p: numpy.ndarray[typing.Literal[3], numpy.dtype[numpy.float32]]
    q: numpy.ndarray[typing.Literal[4], numpy.dtype[numpy.float32]]
    rpy: numpy.ndarray[typing.Literal[3], numpy.dtype[numpy.float32]]
    def __getstate__(self) -> tuple:
        ...
    @typing.overload
    def __init__(self, p: numpy.ndarray[typing.Literal[3], numpy.dtype[numpy.float32]] | list[float] | tuple = ..., q: numpy.ndarray[typing.Literal[4], numpy.dtype[numpy.float32]] | list[float] | tuple = ...) -> None:
        ...
    @typing.overload
    def __init__(self, arg0: numpy.ndarray[tuple[typing.Literal[4], typing.Literal[4]], numpy.dtype[numpy.float32]] | list | tuple) -> None:
        ...
    def __mul__(self, arg0: Pose) -> Pose:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
    def get_p(self) -> numpy.ndarray[typing.Literal[3], numpy.dtype[numpy.float32]]:
        ...
    def get_q(self) -> numpy.ndarray[typing.Literal[4], numpy.dtype[numpy.float32]]:
        ...
    def get_rpy(self) -> numpy.ndarray[typing.Literal[3], numpy.dtype[numpy.float32]]:
        ...
    def inv(self) -> Pose:
        ...
    def set_p(self, p: numpy.ndarray[typing.Literal[3], numpy.dtype[numpy.float32]] | list[float] | tuple) -> None:
        ...
    def set_q(self, q: numpy.ndarray[typing.Literal[4], numpy.dtype[numpy.float32]] | list[float] | tuple) -> None:
        ...
    def set_rpy(self, arg0: numpy.ndarray[typing.Literal[3], numpy.dtype[numpy.float32]] | list[float] | tuple) -> None:
        ...
    def to_transformation_matrix(self) -> numpy.ndarray[tuple[typing.Literal[4], typing.Literal[4]], numpy.dtype[numpy.float32]]:
        ...
class Profiler:
    def __call__(self, arg0: typing.Callable) -> typing.Callable:
        ...
    def __enter__(self) -> None:
        ...
    def __exit__(self, arg0: type | None, arg1: typing.Any | None, arg2: typing.Any | None) -> None:
        ...
    def __init__(self, arg0: str) -> None:
        ...
class Scene:
    def __init__(self, systems: list[System]) -> None:
        ...
    def add_entity(self, arg0: Entity) -> None:
        ...
    def add_system(self, arg0: System) -> None:
        ...
    def clear(self) -> None:
        ...
    def get_entities(self) -> list[Entity]:
        ...
    def get_id(self) -> int:
        ...
    def get_physx_system(self) -> physx.PhysxSystem:
        ...
    def get_render_system(self) -> render.RenderSystem:
        ...
    def get_system(self, name: str) -> System:
        ...
    def pack_poses(self) -> bytes:
        ...
    def remove_entity(self, entity: Entity) -> None:
        ...
    def unpack_poses(self, data: bytes) -> None:
        ...
    @property
    def entities(self) -> list[Entity]:
        ...
    @property
    def id(self) -> int:
        ...
    @property
    def physx_system(self) -> physx.PhysxSystem:
        ...
    @property
    def render_system(self) -> render.RenderSystem:
        ...
class System:
    def __init__(self) -> None:
        ...
    def step(self) -> None:
        ...
@typing.overload
def profile(arg0: str) -> Profiler:
    ...
@typing.overload
def profile(arg0: typing.Callable) -> typing.Callable:
    ...
def set_log_level(level: str) -> None:
    ...
