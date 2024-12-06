from collections.abc import Callable, Mapping, Sequence
import enum
from typing import Optional

import sgl


class AccessType(enum.Enum):
    none = 0

    read = 1

    write = 2

    readwrite = 3

class CallContext(sgl.Object):
    def __init__(self, device: sgl.Device, call_shape: Shape) -> None:
        """N/A"""

    @property
    def device(self) -> sgl.Device:
        """N/A"""

    @property
    def call_shape(self) -> Shape:
        """N/A"""

class CallMode(enum.Enum):
    prim = 0

    bwds = 1

    fwds = 2

class NativeBoundCallRuntime(sgl.Object):
    def __init__(self) -> None:
        """N/A"""

    @property
    def args(self) -> list[NativeBoundVariableRuntime]:
        """N/A"""

    @args.setter
    def args(self, arg: Sequence[NativeBoundVariableRuntime], /) -> None: ...

    @property
    def kwargs(self) -> dict[str, NativeBoundVariableRuntime]:
        """N/A"""

    @kwargs.setter
    def kwargs(self, arg: Mapping[str, NativeBoundVariableRuntime], /) -> None: ...

    def find_kwarg(self, arg: str, /) -> NativeBoundVariableRuntime:
        """N/A"""

    def calculate_call_shape(self, arg0: int, arg1: list, arg2: dict, /) -> Shape:
        """N/A"""

    def write_calldata_pre_dispatch(self, arg0: CallContext, arg1: dict, arg2: list, arg3: dict, /) -> None:
        """N/A"""

    def read_call_data_post_dispatch(self, arg0: CallContext, arg1: dict, arg2: list, arg3: dict, /) -> None:
        """N/A"""

class NativeBoundVariableRuntime(sgl.Object):
    def __init__(self) -> None:
        """N/A"""

    @property
    def access(self) -> tuple[AccessType, AccessType]:
        """N/A"""

    @access.setter
    def access(self, arg: tuple[AccessType, AccessType], /) -> None: ...

    @property
    def transform(self) -> Shape:
        """N/A"""

    @transform.setter
    def transform(self, arg: Shape, /) -> None: ...

    @property
    def python_type(self) -> NativeType:
        """N/A"""

    @python_type.setter
    def python_type(self, arg: NativeType, /) -> None: ...

    @property
    def shape(self) -> Shape:
        """N/A"""

    @shape.setter
    def shape(self, arg: Shape, /) -> None: ...

    @property
    def variable_name(self) -> str:
        """N/A"""

    @variable_name.setter
    def variable_name(self, arg: str, /) -> None: ...

    @property
    def children(self) -> Optional[dict[str, NativeBoundVariableRuntime]]:
        """N/A"""

    @children.setter
    def children(self, arg: Mapping[str, NativeBoundVariableRuntime], /) -> None: ...

    def populate_call_shape(self, arg0: Sequence[int], arg1: object, /) -> None:
        """N/A"""

    def write_call_data_pre_dispatch(self, arg0: CallContext, arg1: dict, arg2: object, /) -> None:
        """N/A"""

    def read_call_data_post_dispatch(self, arg0: CallContext, arg1: dict, arg2: object, /) -> None:
        """N/A"""

    def read_output(self, arg0: CallContext, arg1: object, /) -> object:
        """N/A"""

class NativeCallData(sgl.Object):
    def __init__(self) -> None:
        """N/A"""

    @property
    def device(self) -> sgl.Device:
        """N/A"""

    @device.setter
    def device(self, arg: sgl.Device, /) -> None: ...

    @property
    def kernel(self) -> sgl.ComputeKernel:
        """N/A"""

    @kernel.setter
    def kernel(self, arg: sgl.ComputeKernel, /) -> None: ...

    @property
    def call_dimensionality(self) -> int:
        """N/A"""

    @call_dimensionality.setter
    def call_dimensionality(self, arg: int, /) -> None: ...

    @property
    def runtime(self) -> NativeBoundCallRuntime:
        """N/A"""

    @runtime.setter
    def runtime(self, arg: NativeBoundCallRuntime, /) -> None: ...

    @property
    def vars(self) -> dict:
        """N/A"""

    @vars.setter
    def vars(self, arg: dict, /) -> None: ...

    @property
    def call_mode(self) -> CallMode:
        """N/A"""

    @call_mode.setter
    def call_mode(self, arg: CallMode, /) -> None: ...

    @property
    def last_call_shape(self) -> Shape:
        """N/A"""

    def add_before_dispatch_hook(self, arg: Callable[[dict], None], /) -> None:
        """N/A"""

    def add_after_dispatch_hook(self, arg: Callable[[dict], None], /) -> None:
        """N/A"""

    def call(self, *args, **kwargs) -> object:
        """N/A"""

    def append_to(self, command_buffer: sgl.CommandBuffer, *args, **kwargs) -> object:
        """N/A"""

class NativeType(sgl.Object):
    def __init__(self) -> None:
        """N/A"""

    @property
    def name(self) -> str:
        """N/A"""

    @name.setter
    def name(self, arg: str, /) -> None: ...

    @property
    def element_type(self) -> NativeType:
        """N/A"""

    @element_type.setter
    def element_type(self, arg: Optional[NativeType]) -> None: ...

    @property
    def concrete_shape(self) -> Shape:
        """N/A"""

    @concrete_shape.setter
    def concrete_shape(self, arg: Shape, /) -> None: ...

    def get_byte_size(self, arg: object, /) -> int:
        """N/A"""

    def get_container_shape(self, arg: object, /) -> Shape:
        """N/A"""

    def get_shape(self, value: Optional[object] = None) -> Shape:
        """N/A"""

    def create_calldata(self, arg0: CallContext, arg1: NativeBoundVariableRuntime, arg2: object, /) -> object:
        """N/A"""

    def read_calldata(self, arg0: CallContext, arg1: NativeBoundVariableRuntime, arg2: object, arg3: object, /) -> None:
        """N/A"""

    def create_output(self, arg0: CallContext, arg1: NativeBoundVariableRuntime, /) -> object:
        """N/A"""

    def read_output(self, arg0: CallContext, arg1: NativeBoundVariableRuntime, arg2: object, /) -> object:
        """N/A"""

class Shape:
    def __init__(self, *args) -> None:
        """N/A"""

    def __add__(self, arg: Shape, /) -> Shape:
        """N/A"""

    def __getitem__(self, index: int) -> int:
        """N/A"""

    def __len__(self) -> int:
        """N/A"""

    @property
    def valid(self) -> bool:
        """N/A"""

    @property
    def concrete(self) -> bool:
        """N/A"""

    def as_tuple(self) -> tuple:
        """N/A"""

    def as_list(self) -> list[int]:
        """N/A"""

    def __repr__(self) -> str:
        """N/A"""

    def __str__(self) -> str:
        """N/A"""

    def __eq__(self, arg: object, /) -> bool:
        """N/A"""

def hash_signature(value_to_id: Callable[[object], str], *args, **kwargs) -> str:
    """N/A"""
