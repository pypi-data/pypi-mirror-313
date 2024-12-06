from collections.abc import Callable, Mapping, Sequence
import enum
import os
import pathlib
from typing import TypedDict, Union
from numpy.typing import NDArray
from typing import Annotated, TypeAlias, overload

from numpy.typing import ArrayLike

from . import (
    math as math,
    platform as platform,
    renderdoc as renderdoc,
    sgl_ext as sgl_ext,
    slangpy as slangpy,
    tev as tev,
    thread as thread,
    ui as ui
)
from .math import (
    bool1 as bool1,
    bool2 as bool2,
    bool3 as bool3,
    bool4 as bool4,
    float1 as float1,
    float16_t as float16_t,
    float16_t1 as float16_t1,
    float16_t2 as float16_t2,
    float16_t3 as float16_t3,
    float16_t4 as float16_t4,
    float2 as float2,
    float2x2 as float2x2,
    float2x4 as float2x4,
    float3 as float3,
    float3x3 as float3x3,
    float3x4 as float3x4,
    float4 as float4,
    float4x4 as float4x4,
    int1 as int1,
    int2 as int2,
    int3 as int3,
    int4 as int4,
    quatf as quatf,
    uint1 as uint1,
    uint2 as uint2,
    uint3 as uint3,
    uint4 as uint4
)
bool1param = Union[math.bool1, Sequence[bool]]
bool2param = Union[math.bool2, Sequence[bool]]
bool3param = Union[math.bool3, Sequence[bool]]
bool4param = Union[math.bool4, Sequence[bool]]
float1param = Union[math.float1, Sequence[float]]
float16_tparam = Union[math.float16_t, float]
float16_t1param = Union[math.float16_t1, Sequence[float16_t]]
float16_t2param = Union[math.float16_t2, Sequence[float16_t]]
float16_t3param = Union[math.float16_t3, Sequence[float16_t]]
float16_t4param = Union[math.float16_t4, Sequence[float16_t]]
float2param = Union[math.float2, Sequence[float]]
float2x2param = Union[math.float2x2, Sequence[float]]
float2x4param = Union[math.float2x4, Sequence[float]]
float3param = Union[math.float3, Sequence[float]]
float3x3param = Union[math.float3x3, Sequence[float]]
float3x4param = Union[math.float3x4, Sequence[float]]
float4param = Union[math.float4, Sequence[float]]
float4x4param = Union[math.float4x4, Sequence[float]]
int1param = Union[math.int1, Sequence[int]]
int2param = Union[math.int2, Sequence[int]]
int3param = Union[math.int3, Sequence[int]]
int4param = Union[math.int4, Sequence[int]]
quatfparam = Union[math.quatf, Sequence[float]]
uint1param = Union[math.uint1, Sequence[int]]
uint2param = Union[math.uint2, Sequence[int]]
uint3param = Union[math.uint3, Sequence[int]]
uint4param = Union[math.uint4, Sequence[int]]


class AccelerationStructure(DeviceResource):
    def kind(self) -> AccelerationStructureKind: ...

    @property
    def device_address(self) -> int: ...

class AccelerationStructureBuildDesc:
    pass

class AccelerationStructureBuildFlags(enum.IntFlag):
    none = 0

    allow_update = 1

    allow_compaction = 2

    prefer_fast_trace = 4

    prefer_fast_build = 8

    minimize_memory = 16

    perform_update = 32

class AccelerationStructureBuildInputs(AccelerationStructureBuildInputsBase):
    def __init__(self) -> None: ...

    @property
    def kind(self) -> AccelerationStructureKind: ...

    @kind.setter
    def kind(self, arg: AccelerationStructureKind, /) -> None: ...

    @property
    def flags(self) -> AccelerationStructureBuildFlags: ...

    @flags.setter
    def flags(self, arg: AccelerationStructureBuildFlags, /) -> None: ...

    @property
    def desc_count(self) -> int: ...

    @desc_count.setter
    def desc_count(self, arg: int, /) -> None: ...

    @property
    def instance_descs(self) -> int:
        """
        Array of `RayTracingInstanceDesc` values in device memory. Used when
        `kind` is `top_level`.
        """

    @instance_descs.setter
    def instance_descs(self, arg: int, /) -> None: ...

    @property
    def geometry_descs(self) -> list[RayTracingGeometryDesc]:
        """
        Array of `RayTracingGeometryDesc` values. Used when `kind` is
        `bottom_level`.
        """

    @geometry_descs.setter
    def geometry_descs(self, arg: Sequence[RayTracingGeometryDesc], /) -> None: ...

class AccelerationStructureBuildInputsBase:
    pass

class AccelerationStructureCopyMode(enum.Enum):
    clone = 0

    compact = 1

class AccelerationStructureKind(enum.Enum):
    top_level = 0

    bottom_level = 1

class AccelerationStructurePrebuildInfo:
    @property
    def result_data_max_size(self) -> int: ...

    @property
    def scratch_data_size(self) -> int: ...

    @property
    def update_scratch_data_size(self) -> int: ...

class AccelerationStructureQueryDesc:
    pass

class AdapterInfo:
    @property
    def name(self) -> str:
        """Descriptive name of the adapter."""

    @property
    def vendor_id(self) -> int:
        """
        Unique identifier for the vendor (only available for D3D12 and
        Vulkan).
        """

    @property
    def device_id(self) -> int:
        """
        Unique identifier for the physical device among devices from the
        vendor (only available for D3D12 and Vulkan).
        """

    @property
    def luid(self) -> list[int]:
        """Logically unique identifier of the adapter."""

    def __repr__(self) -> str: ...

class App(Object):
    @overload
    def __init__(self, arg: AppDescParam, /) -> None: ...

    @overload
    def __init__(self, device: Device | None = None) -> None: ...

    @property
    def device(self) -> Device: ...

    def run(self) -> None: ...

    def run_frame(self) -> None: ...

    def terminate(self) -> None: ...

class AppDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def device(self) -> Device:
        """
        Device to use for rendering. If not provided, a default device will be
        created.
        """

    @device.setter
    def device(self, arg: Device, /) -> None: ...

AppDescDict = TypedDict("AppDescDict", {
    "device": Device
}, total = False)

AppDescParam = Union[AppDesc, AppDescDict]

class AppWindow(Object):
    def __init__(self, app: App, width: int = 1920, height: int = 1280, title: str = 'sgl', mode: WindowMode = WindowMode.normal, resizable: bool = True, swapchain_format: Format = Format.bgra8_unorm_srgb, enable_vsync: bool = False) -> None: ...

    class RenderContext:
        @property
        def swapchain_image(self) -> Texture: ...

        @property
        def framebuffer(self) -> Framebuffer: ...

        @property
        def command_buffer(self) -> CommandBuffer: ...

    @property
    def device(self) -> Device: ...

    @property
    def screen(self) -> ui.Screen: ...

    def render(self, render_context: AppWindow.RenderContext) -> None: ...

    def on_resize(self, width: int, height: int) -> None: ...

    def on_keyboard_event(self, event: KeyboardEvent) -> None: ...

    def on_mouse_event(self, event: MouseEvent) -> None: ...

    def on_gamepad_event(self, event: GamepadEvent) -> None: ...

    def on_drop_files(self, files: Sequence[str]) -> None: ...

class AppWindowDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def width(self) -> int:
        """Width of the window in pixels."""

    @width.setter
    def width(self, arg: int, /) -> None: ...

    @property
    def height(self) -> int:
        """Height of the window in pixels."""

    @height.setter
    def height(self, arg: int, /) -> None: ...

    @property
    def title(self) -> str:
        """Title of the window."""

    @title.setter
    def title(self, arg: str, /) -> None: ...

    @property
    def mode(self) -> WindowMode:
        """Window mode."""

    @mode.setter
    def mode(self, arg: WindowMode, /) -> None: ...

    @property
    def resizable(self) -> bool:
        """Whether the window is resizable."""

    @resizable.setter
    def resizable(self, arg: bool, /) -> None: ...

    @property
    def swapchain_format(self) -> Format:
        """Format of the swapchain images."""

    @swapchain_format.setter
    def swapchain_format(self, arg: Format, /) -> None: ...

    @property
    def enable_vsync(self) -> bool:
        """Enable/disable vertical synchronization."""

    @enable_vsync.setter
    def enable_vsync(self, arg: bool, /) -> None: ...

AppWindowDescDict = TypedDict("AppWindowDescDict", {
    "width": int,
    "height": int,
    "title": str,
    "mode": WindowMode,
    "resizable": bool,
    "swapchain_format": Format,
    "enable_vsync": bool
}, total = False)

AppWindowDescParam = Union[AppWindowDesc, AppWindowDescDict]

class AspectBlendDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def src_factor(self) -> BlendFactor: ...

    @src_factor.setter
    def src_factor(self, arg: BlendFactor, /) -> None: ...

    @property
    def dst_factor(self) -> BlendFactor: ...

    @dst_factor.setter
    def dst_factor(self, arg: BlendFactor, /) -> None: ...

    @property
    def op(self) -> BlendOp: ...

    @op.setter
    def op(self, arg: BlendOp, /) -> None: ...

AspectBlendDescDict = TypedDict("AspectBlendDescDict", {
    "src_factor": BlendFactor,
    "dst_factor": BlendFactor,
    "op": BlendOp
}, total = False)

AspectBlendDescParam = Union[AspectBlendDesc, AspectBlendDescDict]

class BaseReflectionObject(Object):
    @property
    def is_valid(self) -> bool:
        """N/A"""

class Bitmap(Object):
    @overload
    def __init__(self, pixel_format: Bitmap.PixelFormat, component_type: Struct.Type, width: int, height: int, channel_count: int = 0, channel_names: Sequence[str] = []) -> None: ...

    @overload
    def __init__(self, data: Annotated[ArrayLike, dict(device='cpu')], pixel_format: Bitmap.PixelFormat | None = None, channel_names: Sequence[str] | None = None) -> None: ...

    @overload
    def __init__(self, path: str | os.PathLike) -> None: ...

    class PixelFormat(enum.Enum):
        y = 0

        ya = 1

        r = 2

        rg = 3

        rgb = 4

        rgba = 5

        multi_channel = 6

    ComponentType: TypeAlias = Struct.Type

    class FileFormat(enum.Enum):
        unknown = 0

        auto = 1

        png = 2

        jpg = 3

        bmp = 4

        tga = 5

        hdr = 6

        exr = 7

    @property
    def pixel_format(self) -> Bitmap.PixelFormat:
        """The pixel format."""

    @property
    def component_type(self) -> Struct.Type:
        """The component type."""

    @property
    def pixel_struct(self) -> Struct:
        """Struct describing the pixel layout."""

    @property
    def width(self) -> int:
        """The width of the bitmap in pixels."""

    @property
    def height(self) -> int:
        """The height of the bitmap in pixels."""

    @property
    def pixel_count(self) -> int:
        """The total number of pixels in the bitmap."""

    @property
    def channel_count(self) -> int:
        """The number of channels in the bitmap."""

    @property
    def channel_names(self) -> list[str]:
        """The names of the channels in the bitmap."""

    @property
    def srgb_gamma(self) -> bool:
        """True if the bitmap is in sRGB gamma space."""

    @srgb_gamma.setter
    def srgb_gamma(self, arg: bool, /) -> None: ...

    def has_alpha(self) -> bool:
        """Returns true if the bitmap has an alpha channel."""

    @property
    def bytes_per_pixel(self) -> int:
        """The number of bytes per pixel."""

    @property
    def buffer_size(self) -> int:
        """The total size of the bitmap in bytes."""

    def empty(self) -> bool:
        """True if bitmap is empty."""

    def clear(self) -> None:
        """Clears the bitmap to zeros."""

    def vflip(self) -> None:
        """Vertically flip the bitmap."""

    def split(self) -> list[tuple[str, Bitmap]]:
        """
        Split bitmap into multiple bitmaps, each containing the channels with
        the same prefix.

        For example, if the bitmap has channels `albedo.R`, `albedo.G`,
        `albedo.B`, `normal.R`, `normal.G`, `normal.B`, this function will
        return two bitmaps, one containing the channels `albedo.R`,
        `albedo.G`, `albedo.B` and the other containing the channels
        `normal.R`, `normal.G`, `normal.B`.

        Common pixel formats (e.g. `y`, `rgb`, `rgba`) are automatically
        detected and used for the split bitmaps.

        Any channels that do not have a prefix will be returned in the bitmap
        with the empty prefix.

        Returns:
            Returns a list of (prefix, bitmap) pairs.
        """

    def convert(self, pixel_format: Bitmap.PixelFormat | None = None, component_type: Struct.Type | None = None, srgb_gamma: bool | None = None) -> Bitmap: ...

    def write(self, path: str | os.PathLike, format: Bitmap.FileFormat = Bitmap.FileFormat.auto, quality: int = -1) -> None: ...

    def write_async(self, path: str | os.PathLike, format: Bitmap.FileFormat = Bitmap.FileFormat.auto, quality: int = -1) -> None: ...

    @staticmethod
    def read_multiple(paths: Sequence[str | os.PathLike], format: Bitmap.FileFormat = Bitmap.FileFormat.auto) -> list[Bitmap]:
        """
        Load a list of bitmaps from multiple paths. Uses multi-threading to
        load bitmaps in parallel.
        """

    def __eq__(self, arg: Bitmap, /) -> bool: ...

    def __ne__(self, arg: Bitmap, /) -> bool: ...

    @property
    def __array_interface__(self) -> object: ...

class BlendDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def targets(self) -> list[TargetBlendDesc]: ...

    @targets.setter
    def targets(self, arg: Sequence[TargetBlendDescParam], /) -> None: ...

    @property
    def alpha_to_coverage_enable(self) -> bool: ...

    @alpha_to_coverage_enable.setter
    def alpha_to_coverage_enable(self, arg: bool, /) -> None: ...

BlendDescDict = TypedDict("BlendDescDict", {
    "targets": Sequence[TargetBlendDescParam],
    "alpha_to_coverage_enable": bool
}, total = False)

BlendDescParam = Union[BlendDesc, BlendDescDict]

class BlendFactor(enum.Enum):
    zero = 0

    one = 1

    src_color = 2

    inv_src_color = 3

    src_alpha = 4

    inv_src_alpha = 5

    dest_alpha = 6

    inv_dest_alpha = 7

    dest_color = 8

    inv_dest_color = 9

    src_alpha_saturate = 10

    blend_color = 11

    inv_blend_color = 12

    secondary_src_color = 13

    inv_secondary_src_color = 14

    secondary_src_alpha = 15

    inv_secondary_src_alpha = 16

class BlendOp(enum.Enum):
    add = 0

    subtract = 1

    reverse_subtract = 2

    min = 3

    max = 4

class Buffer(Resource):
    @property
    def desc(self) -> BufferDesc: ...

    @property
    def size(self) -> int: ...

    @property
    def struct_size(self) -> int: ...

    @property
    def device_address(self) -> int: ...

    def get_srv(self, offset: int = 0, size: int = 18446744073709551615) -> ResourceView:
        """Get a shader resource view for a range of the buffer."""

    def get_uav(self, offset: int = 0, size: int = 18446744073709551615) -> ResourceView:
        """Get a unordered access view for a range of the buffer."""

    def to_numpy(self) -> NDArray: ...

    def from_numpy(self, data: ArrayLike) -> None: ...

    def to_torch(self, type: DataType = DataType.void, shape: Sequence[int] = [], strides: Sequence[int] = []) -> Annotated[ArrayLike, dict(device='cuda')]: ...

class BufferCursor(Object):
    """N/A"""

    @overload
    def __init__(self, element_layout: TypeLayoutReflection, size: int) -> None:
        """N/A"""

    @overload
    def __init__(self, element_layout: TypeLayoutReflection, buffer_resource: Buffer) -> None:
        """N/A"""

    @overload
    def __init__(self, element_layout: TypeLayoutReflection, buffer_resource: Buffer, element_count: int, first_element: int) -> None:
        """N/A"""

    @property
    def element_type_layout(self) -> TypeLayoutReflection:
        """N/A"""

    @property
    def element_type(self) -> TypeReflection:
        """N/A"""

    def find_element(self, index: int) -> BufferElementCursor:
        """N/A"""

    @property
    def element_count(self) -> int:
        """N/A"""

    @property
    def element_size(self) -> int:
        """N/A"""

    @property
    def size(self) -> int:
        """N/A"""

    @property
    def is_loaded(self) -> bool:
        """N/A"""

    def load(self) -> None:
        """N/A"""

    def apply(self) -> None:
        """N/A"""

    @property
    def resource(self) -> Buffer:
        """N/A"""

    def __getitem__(self, arg: int, /) -> BufferElementCursor: ...

    def __len__(self) -> int: ...

    def to_numpy(self) -> NDArray: ...

    def from_numpy(self, data: ArrayLike) -> None: ...

    def __dir__(self) -> list[str]: ...

    def __getattr__(self, arg: str, /) -> object: ...

class BufferDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def size(self) -> int:
        """Buffer size in bytes."""

    @size.setter
    def size(self, arg: int, /) -> None: ...

    @property
    def struct_size(self) -> int:
        """Struct size in bytes."""

    @struct_size.setter
    def struct_size(self, arg: int, /) -> None: ...

    @property
    def format(self) -> Format:
        """Buffer format. Used when creating typed buffer views."""

    @format.setter
    def format(self, arg: Format, /) -> None: ...

    @property
    def initial_state(self) -> ResourceState:
        """Initial resource state."""

    @initial_state.setter
    def initial_state(self, arg: ResourceState, /) -> None: ...

    @property
    def usage(self) -> ResourceUsage:
        """Resource usage flags."""

    @usage.setter
    def usage(self, arg: ResourceUsage, /) -> None: ...

    @property
    def memory_type(self) -> MemoryType:
        """Memory type."""

    @memory_type.setter
    def memory_type(self, arg: MemoryType, /) -> None: ...

    @property
    def debug_name(self) -> str:
        """Resource debug name."""

    @debug_name.setter
    def debug_name(self, arg: str, /) -> None: ...

BufferDescDict = TypedDict("BufferDescDict", {
    "size": int,
    "struct_size": int,
    "format": Format,
    "initial_state": ResourceState,
    "usage": ResourceUsage,
    "memory_type": MemoryType,
    "debug_name": str
}, total = False)

BufferDescParam = Union[BufferDesc, BufferDescDict]

class BufferElementCursor:
    """N/A"""

    @overload
    def set_data(self, data: Annotated[ArrayLike, dict(device='cpu')]) -> None:
        """N/A"""

    @overload
    def set_data(self, data: Annotated[ArrayLike, dict(device='cpu')]) -> None: ...

    def __dir__(self) -> list[str]: ...

    def __repr__(self) -> str: ...

    def is_valid(self) -> bool:
        """N/A"""

    def find_field(self, name: str) -> BufferElementCursor:
        """N/A"""

    def find_element(self, index: int) -> BufferElementCursor:
        """N/A"""

    def has_field(self, name: str) -> bool:
        """N/A"""

    def has_element(self, index: int) -> bool:
        """N/A"""

    @overload
    def __getitem__(self, arg: str, /) -> BufferElementCursor: ...

    @overload
    def __getitem__(self, arg: int, /) -> BufferElementCursor: ...

    def __getattr__(self, arg: str, /) -> BufferElementCursor: ...

    def read(self) -> object:
        """N/A"""

    def __setattr__(self, name: str, val: object) -> None:
        """N/A"""

    @overload
    def __setitem__(self, index: str, val: object) -> None:
        """N/A"""

    @overload
    def __setitem__(self, index: int, val: object) -> None:
        """N/A"""

    def write(self, val: object) -> None:
        """N/A"""

class BufferRange:
    def __init__(self) -> None: ...

    @property
    def offset(self) -> int:
        """N/A"""

    @property
    def size(self) -> int:
        """N/A"""

    def __repr__(self) -> str:
        """N/A"""

class CommandBuffer(DeviceResource):
    def open(self) -> None:
        r"""
        Open the command buffer for recording.

        No-op if command buffer is already open.

        \note Due to current limitations, only a single command buffer can be
        open at any given time.
        """

    def close(self) -> None:
        """
        Close the command buffer.

        No-op if command buffer is already closed.
        """

    def submit(self, queue: CommandQueueType = CommandQueueType.graphics) -> int:
        """
        Submit the command buffer to the device.

        The returned submission ID can be used to wait for the command buffer
        to complete.

        Parameter ``queue``:
            Command queue to submit to.

        Returns:
            Submission ID.
        """

    def write_timestamp(self, query_pool: QueryPool, index: int) -> None:
        """
        Write a timestamp.

        Parameter ``query_pool``:
            Query pool.

        Parameter ``index``:
            Index of the query.
        """

    def resolve_query(self, query_pool: QueryPool, index: int, count: int, buffer: Buffer, offset: int) -> None:
        """
        Resolve a list of queries and write the results to a buffer.

        Parameter ``query_pool``:
            Query pool.

        Parameter ``index``:
            Index of the first query.

        Parameter ``count``:
            Number of queries to resolve.

        Parameter ``buffer``:
            Destination buffer.

        Parameter ``offset``:
            Offset into the destination buffer.
        """

    @overload
    def set_resource_state(self, resource: Resource, new_state: ResourceState) -> bool:
        """
        Transition resource state of a resource and add a barrier if state has
        changed.

        Parameter ``resource``:
            Resource

        Parameter ``new_state``:
            New state

        Returns:
            True if barrier was recorded (i.e. state has changed).
        """

    @overload
    def set_resource_state(self, resource_view: ResourceView, new_state: ResourceState) -> bool:
        """
        Transition resource state of a resource and add a barrier if state has
        changed. For buffer views, this will set the resource state of the
        entire buffer. For texture views, this will set the resource state of
        all its sub-resources.

        Parameter ``resource_view``:
            Resource view

        Parameter ``new_state``:
            New state

        Returns:
            True if barrier was recorded (i.e. state has changed).
        """

    def set_buffer_state(self, buffer: Buffer, new_state: ResourceState) -> bool:
        """
        Transition resource state of a buffer and add a barrier if state has
        changed.

        Parameter ``buffer``:
            Buffer

        Parameter ``new_state``:
            New state

        Returns:
            True if barrier was recorded (i.e. state has changed).
        """

    def set_texture_state(self, texture: Texture, new_state: ResourceState) -> bool:
        """
        Transition resource state of a texture and add a barrier if state has
        changed.

        Parameter ``texture``:
            Texture

        Parameter ``new_state``:
            New state

        Returns:
            True if barrier was recorded (i.e. state has changed).
        """

    def uav_barrier(self, resource: Resource) -> None:
        """Insert a UAV barrier"""

    @overload
    def clear_resource_view(self, resource_view: ResourceView, clear_value: float4param) -> None: ...

    @overload
    def clear_resource_view(self, resource_view: ResourceView, clear_value: uint4param) -> None: ...

    @overload
    def clear_resource_view(self, resource_view: ResourceView, depth_value: float, stencil_value: int, clear_depth: bool, clear_stencil: bool) -> None: ...

    @overload
    def clear_texture(self, texture: Texture, clear_value: float4param) -> None: ...

    @overload
    def clear_texture(self, texture: Texture, clear_value: uint4param) -> None: ...

    def copy_resource(self, dst: Resource, src: Resource) -> None:
        """
        Copy an entire resource.

        Parameter ``dst``:
            Destination resource.

        Parameter ``src``:
            Source resource.
        """

    def copy_buffer_region(self, dst: Buffer, dst_offset: int, src: Buffer, src_offset: int, size: int) -> None:
        """
        Copy a buffer region.

        Parameter ``dst``:
            Destination buffer.

        Parameter ``dst_offset``:
            Destination offset in bytes.

        Parameter ``src``:
            Source buffer.

        Parameter ``src_offset``:
            Source offset in bytes.

        Parameter ``size``:
            Size in bytes.
        """

    def copy_texture_region(self, dst: Texture, dst_subresource: int, dst_offset: uint3param, src: Texture, src_subresource: int, src_offset: uint3param, extent: uint3param = ...) -> None:
        """
        Copy a texture region.

        Parameter ``dst``:
            Destination texture.

        Parameter ``dst_subresource``:
            Destination subresource index.

        Parameter ``dst_offset``:
            Destination offset in texels.

        Parameter ``src``:
            Source texture.

        Parameter ``src_subresource``:
            Source subresource index.

        Parameter ``src_offset``:
            Source offset in texels.

        Parameter ``extent``:
            Size in texels (-1 for maximum possible size).
        """

    @overload
    def blit(self, dst: ResourceView, src: ResourceView, filter: TextureFilteringMode = TextureFilteringMode.linear) -> None:
        """
        Blit a SRV to an RTV.

        Blits the full extent of the source texture to the destination
        texture.

        Parameter ``dst``:
            RTV of the destination texture.

        Parameter ``src``:
            SRV of the source texture.

        Parameter ``filter``:
            Filtering mode to use.
        """

    @overload
    def blit(self, dst: Texture, src: Texture, filter: TextureFilteringMode = TextureFilteringMode.linear) -> None:
        """
        Blit a texture to another texture.

        Blits the full extent of the source texture to the destination
        texture.

        Parameter ``dst``:
            Destination texture.

        Parameter ``src``:
            Source texture.

        Parameter ``filter``:
            Filtering mode to use.
        """

    def encode_compute_commands(self) -> ComputeCommandEncoder:
        """
        Start encoding compute commands.

        The returned ``ComputeCommandEncoder`` is used to bind compute
        pipelines and issue dispatches. The encoding is ended when the
        ``ComputeCommandEncoder`` is destroyed.
        """

    def encode_render_commands(self, arg: Framebuffer, /) -> RenderCommandEncoder:
        """
        Start encoding render commands.

        The returned ``RenderCommandEncoder`` is used to bind graphics
        pipelines and issue dispatches. The encoding is ended when the
        ``RenderCommandEncoder`` is destroyed.
        """

    def encode_ray_tracing_commands(self) -> RayTracingCommandEncoder:
        """
        Start encoding ray tracing commands.

        The returned ``RayTracingCommandEncoder`` is used to bind ray tracing
        pipelines and issue dispatches. It also serves for building and
        managing acceleration structures. The encoding is ended when the
        ``RayTracingCommandEncoder`` is destroyed.
        """

class CommandQueueType(enum.Enum):
    graphics = 0

class ComparisonFunc(enum.Enum):
    never = 0

    less = 1

    equal = 2

    less_equal = 3

    greater = 4

    not_equal = 5

    greater_equal = 6

    always = 7

class ComputeCommandEncoder:
    def __enter__(self) -> ComputeCommandEncoder: ...

    def __exit__(self, exc_type: object | None = None, exc_value: object | None = None, traceback: object | None = None) -> None: ...

    @overload
    def bind_pipeline(self, pipeline: ComputePipeline) -> TransientShaderObject: ...

    @overload
    def bind_pipeline(self, pipeline: ComputePipeline, shader_object: ShaderObject) -> None: ...

    def dispatch(self, thread_count: uint3param) -> None: ...

    def dispatch_thread_groups(self, thread_group_count: uint3param) -> None: ...

class ComputeKernel(Kernel):
    @property
    def pipeline(self) -> ComputePipeline: ...

    def dispatch(self, thread_count: uint3param, vars: dict = {}, command_buffer: CommandBuffer | None = None, **kwargs) -> None: ...

class ComputeKernelDesc:
    def __init__(self) -> None: ...

    @property
    def program(self) -> ShaderProgram: ...

    @program.setter
    def program(self, arg: ShaderProgram, /) -> None: ...

class ComputePipeline(Pipeline):
    """Compute pipeline."""

    @property
    def thread_group_size(self) -> math.uint3:
        """
        Thread group size. Used to determine the number of thread groups to
        dispatch.
        """

class ComputePipelineDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def program(self) -> ShaderProgram: ...

    @program.setter
    def program(self, arg: ShaderProgram, /) -> None: ...

ComputePipelineDescDict = TypedDict("ComputePipelineDescDict", {
    "program": ShaderProgram
}, total = False)

ComputePipelineDescParam = Union[ComputePipelineDesc, ComputePipelineDescDict]

class ConsoleLoggerOutput(LoggerOutput):
    """
    Logger output that writes to the console. Error messages are printed
    to stderr, all other messages to stdout. Messages are optionally
    colored.
    """

    def __init__(self, colored: bool = True) -> None: ...

class CullMode(enum.Enum):
    none = 0

    front = 1

    back = 2

class DataType(enum.Enum):
    """N/A"""

    void = 0

    bool = 1

    int8 = 2

    int16 = 3

    int32 = 4

    int64 = 5

    uint8 = 6

    uint16 = 7

    uint32 = 8

    uint64 = 9

    float16 = 10

    float32 = 11

    float64 = 12

class DebugConsoleLoggerOutput(LoggerOutput):
    """Logger output that writes to the debug console (Windows only)."""

    def __init__(self) -> None: ...

class DeclReflection(BaseReflectionObject):
    class Kind(enum.Enum):
        """Different kinds of decl slang can return."""

        unsupported = 0

        struct = 1

        func = 2

        module = 3

        generic = 4

        variable = 5

    @property
    def kind(self) -> DeclReflection.Kind:
        """Decl kind (struct/function/module/generic/variable)."""

    @property
    def children(self) -> DeclReflectionChildList:
        """List of children of this cursor."""

    @property
    def child_count(self) -> int:
        """Get number of children."""

    @property
    def name(self) -> str: ...

    def children_of_kind(self, kind: DeclReflection.Kind) -> DeclReflectionIndexedChildList:
        """List of children of this cursor of a specific kind."""

    def as_type(self) -> TypeReflection:
        """Get type corresponding to this decl ref."""

    def as_variable(self) -> VariableReflection:
        """Get variable corresponding to this decl ref."""

    def as_function(self) -> FunctionReflection:
        """Get function corresponding to this decl ref."""

    def find_children_of_kind(self, kind: DeclReflection.Kind, child_name: str) -> DeclReflectionIndexedChildList:
        """
        Finds all children of a specific kind with a given name. Note: Only
        supported for types, functions and variables.
        """

    def find_first_child_of_kind(self, kind: DeclReflection.Kind, child_name: str) -> DeclReflection:
        """
        Finds the first child of a specific kind with a given name. Note: Only
        supported for types, functions and variables.
        """

    def __len__(self) -> int: ...

    def __getitem__(self, arg: int, /) -> DeclReflection: ...

    def __repr__(self) -> str: ...

class DeclReflectionChildList:
    """DeclReflection lazy child list evaluation."""

    def __len__(self) -> int: ...

    def __getitem__(self, arg: int, /) -> DeclReflection: ...

class DeclReflectionIndexedChildList:
    """DeclReflection lazy search result evaluation."""

    def __len__(self) -> int: ...

    def __getitem__(self, arg: int, /) -> DeclReflection: ...

class DepthStencilDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def depth_test_enable(self) -> bool: ...

    @depth_test_enable.setter
    def depth_test_enable(self, arg: bool, /) -> None: ...

    @property
    def depth_write_enable(self) -> bool: ...

    @depth_write_enable.setter
    def depth_write_enable(self, arg: bool, /) -> None: ...

    @property
    def depth_func(self) -> ComparisonFunc: ...

    @depth_func.setter
    def depth_func(self, arg: ComparisonFunc, /) -> None: ...

    @property
    def stencil_enable(self) -> bool: ...

    @stencil_enable.setter
    def stencil_enable(self, arg: bool, /) -> None: ...

    @property
    def stencil_read_mask(self) -> int: ...

    @stencil_read_mask.setter
    def stencil_read_mask(self, arg: int, /) -> None: ...

    @property
    def stencil_write_mask(self) -> int: ...

    @stencil_write_mask.setter
    def stencil_write_mask(self, arg: int, /) -> None: ...

    @property
    def front_face(self) -> DepthStencilOpDesc: ...

    @front_face.setter
    def front_face(self, arg: DepthStencilOpDesc, /) -> None: ...

    @property
    def back_face(self) -> DepthStencilOpDesc: ...

    @back_face.setter
    def back_face(self, arg: DepthStencilOpDesc, /) -> None: ...

    @property
    def stencil_ref(self) -> int: ...

    @stencil_ref.setter
    def stencil_ref(self, arg: int, /) -> None: ...

DepthStencilDescDict = TypedDict("DepthStencilDescDict", {
    "depth_test_enable": bool,
    "depth_write_enable": bool,
    "depth_func": ComparisonFunc,
    "stencil_enable": bool,
    "stencil_read_mask": int,
    "stencil_write_mask": int,
    "front_face": DepthStencilOpDesc,
    "back_face": DepthStencilOpDesc,
    "stencil_ref": int
}, total = False)

DepthStencilDescParam = Union[DepthStencilDesc, DepthStencilDescDict]

class DepthStencilOpDesc:
    def __init__(self) -> None: ...

    @property
    def stencil_fail_op(self) -> StencilOp: ...

    @stencil_fail_op.setter
    def stencil_fail_op(self, arg: StencilOp, /) -> None: ...

    @property
    def stencil_depth_fail_op(self) -> StencilOp: ...

    @stencil_depth_fail_op.setter
    def stencil_depth_fail_op(self, arg: StencilOp, /) -> None: ...

    @property
    def stencil_pass_op(self) -> StencilOp: ...

    @stencil_pass_op.setter
    def stencil_pass_op(self, arg: StencilOp, /) -> None: ...

    @property
    def stencil_func(self) -> ComparisonFunc: ...

    @stencil_func.setter
    def stencil_func(self, arg: ComparisonFunc, /) -> None: ...

class Device(Object):
    @overload
    def __init__(self, type: DeviceType = DeviceType.automatic, enable_debug_layers: bool = False, enable_cuda_interop: bool = False, enable_print: bool = False, enable_hot_reload: bool = True, adapter_luid: Sequence[int] | None = None, compiler_options: SlangCompilerOptionsParam | None = None, shader_cache_path: str | os.PathLike | None = None) -> None: ...

    @overload
    def __init__(self, desc: DeviceDescParam) -> None: ...

    @property
    def desc(self) -> DeviceDesc: ...

    @property
    def info(self) -> DeviceInfo:
        """Device information."""

    @property
    def shader_cache_stats(self) -> ShaderCacheStats:
        """Shader cache statistics."""

    @property
    def supported_shader_model(self) -> ShaderModel:
        """The highest shader model supported by the device."""

    @property
    def features(self) -> list[str]:
        """List of features supported by the device."""

    @property
    def supports_cuda_interop(self) -> bool:
        """True if the device supports CUDA interoperability."""

    def get_format_supported_resource_states(self, format: Format) -> set[ResourceState]:
        """Returns the supported resource states for a given format."""

    @property
    def slang_session(self) -> SlangSession:
        """Default slang session."""

    def close(self) -> None:
        r"""
        Close the device.

        This function should be called before the device is released. It waits
        for all pending work to be completed and releases internal resources,
        removing all cyclic references that might prevent the device from
        being destroyed. After closing the device, no new resources must be
        created and no new work must be submitted.

        \note The Python extension will automatically close all open devices
        when the interpreter is terminated through an `atexit` handler. If a
        device is to be destroyed at runtime, it must be closed explicitly.
        """

    @overload
    def create_swapchain(self, window: Window, format: Format = Format.bgra8_unorm_srgb, width: int = 0, height: int = 0, image_count: int = 3, enable_vsync: bool = False) -> Swapchain:
        """
        Create a new swapchain.

        Parameter ``format``:
            Format of the swapchain images.

        Parameter ``width``:
            Width of the swapchain images in pixels.

        Parameter ``height``:
            Height of the swapchain images in pixels.

        Parameter ``image_count``:
            Number of swapchain images.

        Parameter ``enable_vsync``:
            Enable/disable vertical synchronization.

        Parameter ``window``:
            Window to create the swapchain for.

        Returns:
            New swapchain object.
        """

    @overload
    def create_swapchain(self, window_handle: WindowHandle, format: Format = Format.bgra8_unorm_srgb, width: int = 0, height: int = 0, image_count: int = 3, enable_vsync: bool = False) -> Swapchain:
        """
        Create a new swapchain.

        Parameter ``format``:
            Format of the swapchain images.

        Parameter ``width``:
            Width of the swapchain images in pixels.

        Parameter ``height``:
            Height of the swapchain images in pixels.

        Parameter ``image_count``:
            Number of swapchain images.

        Parameter ``enable_vsync``:
            Enable/disable vertical synchronization.

        Parameter ``window_handle``:
            Native window handle to create the swapchain for.

        Returns:
            New swapchain object.
        """

    @overload
    def create_swapchain(self, desc: SwapchainDescParam, window: Window) -> Swapchain:
        """
        Create a new swapchain.

        Parameter ``format``:
            Format of the swapchain images.

        Parameter ``width``:
            Width of the swapchain images in pixels.

        Parameter ``height``:
            Height of the swapchain images in pixels.

        Parameter ``image_count``:
            Number of swapchain images.

        Parameter ``enable_vsync``:
            Enable/disable vertical synchronization.

        Parameter ``window``:
            Window to create the swapchain for.

        Returns:
            New swapchain object.
        """

    @overload
    def create_buffer(self, size: int = 0, element_count: int = 0, struct_size: int = 0, struct_type: object | None = None, format: Format = Format.unknown, usage: ResourceUsage = ResourceUsage.none, memory_type: MemoryType = MemoryType.device_local, debug_name: str = '', data: ArrayLike | None = None) -> Buffer:
        """
        Create a new buffer.

        Parameter ``size``:
            Buffer size in bytes.

        Parameter ``element_count``:
            Buffer size in number of struct elements. Can be used instead of
            ``size``.

        Parameter ``struct_size``:
            Struct size in bytes.

        Parameter ``struct_type``:
            Struct type. Can be used instead of ``struct_size`` to specify the
            size of the struct.

        Parameter ``format``:
            Buffer format. Used when creating typed buffer views.

        Parameter ``initial_state``:
            Initial resource state.

        Parameter ``usage``:
            Resource usage flags.

        Parameter ``memory_type``:
            Memory type.

        Parameter ``debug_name``:
            Resource debug name.

        Parameter ``data``:
            Initial data to upload to the buffer.

        Parameter ``data_size``:
            Size of the initial data in bytes.

        Returns:
            New buffer object.
        """

    @overload
    def create_buffer(self, desc: BufferDescParam) -> Buffer:
        """
        Create a new buffer.

        Parameter ``size``:
            Buffer size in bytes.

        Parameter ``element_count``:
            Buffer size in number of struct elements. Can be used instead of
            ``size``.

        Parameter ``struct_size``:
            Struct size in bytes.

        Parameter ``struct_type``:
            Struct type. Can be used instead of ``struct_size`` to specify the
            size of the struct.

        Parameter ``format``:
            Buffer format. Used when creating typed buffer views.

        Parameter ``initial_state``:
            Initial resource state.

        Parameter ``usage``:
            Resource usage flags.

        Parameter ``memory_type``:
            Memory type.

        Parameter ``debug_name``:
            Resource debug name.

        Parameter ``data``:
            Initial data to upload to the buffer.

        Parameter ``data_size``:
            Size of the initial data in bytes.

        Returns:
            New buffer object.
        """

    @overload
    def create_texture(self, type: ResourceType = ResourceType.unknown, format: Format = Format.unknown, width: int = 0, height: int = 0, depth: int = 0, array_size: int = 1, mip_count: int = 0, sample_count: int = 1, quality: int = 0, usage: ResourceUsage = ResourceUsage.none, memory_type: MemoryType = MemoryType.device_local, debug_name: str = '', data: ArrayLike | None = None) -> Texture:
        """
        Create a new texture.

        Parameter ``type``:
            Resource type (optional). Type is inferred from width, height,
            depth if not specified.

        Parameter ``format``:
            Texture format.

        Parameter ``width``:
            Width in pixels.

        Parameter ``height``:
            Height in pixels.

        Parameter ``depth``:
            Depth in pixels.

        Parameter ``array_size``:
            Number of array slices (1 for non-array textures).

        Parameter ``mip_count``:
            Number of mip levels (0 for auto-generated mips).

        Parameter ``sample_count``:
            Number of samples per pixel (1 for non-multisampled textures).

        Parameter ``quality``:
            Quality level for multisampled textures.

        Parameter ``usage``:
            Resource usage.

        Parameter ``memory_type``:
            Memory type.

        Parameter ``debug_name``:
            Debug name.

        Parameter ``data``:
            Initial data.

        Returns:
            New texture object.
        """

    @overload
    def create_texture(self, desc: TextureDescParam) -> Texture:
        """
        Create a new texture.

        Parameter ``type``:
            Resource type (optional). Type is inferred from width, height,
            depth if not specified.

        Parameter ``format``:
            Texture format.

        Parameter ``width``:
            Width in pixels.

        Parameter ``height``:
            Height in pixels.

        Parameter ``depth``:
            Depth in pixels.

        Parameter ``array_size``:
            Number of array slices (1 for non-array textures).

        Parameter ``mip_count``:
            Number of mip levels (0 for auto-generated mips).

        Parameter ``sample_count``:
            Number of samples per pixel (1 for non-multisampled textures).

        Parameter ``quality``:
            Quality level for multisampled textures.

        Parameter ``usage``:
            Resource usage.

        Parameter ``memory_type``:
            Memory type.

        Parameter ``debug_name``:
            Debug name.

        Parameter ``data``:
            Initial data.

        Returns:
            New texture object.
        """

    @overload
    def create_sampler(self, min_filter: TextureFilteringMode = TextureFilteringMode.linear, mag_filter: TextureFilteringMode = TextureFilteringMode.linear, mip_filter: TextureFilteringMode = TextureFilteringMode.linear, reduction_op: TextureReductionOp = TextureReductionOp.average, address_u: TextureAddressingMode = TextureAddressingMode.wrap, address_v: TextureAddressingMode = TextureAddressingMode.wrap, address_w: TextureAddressingMode = TextureAddressingMode.wrap, mip_lod_bias: float = 0.0, max_anisotropy: int = 1, comparison_func: ComparisonFunc = ComparisonFunc.never, border_color: float4param = ..., min_lod: float = -1000.0, max_lod: float = 1000.0) -> Sampler:
        """
        Create a new sampler.

        Parameter ``min_filter``:
            Minification filter.

        Parameter ``mag_filter``:
            Magnification filter.

        Parameter ``mip_filter``:
            Mip-map filter.

        Parameter ``reduction_op``:
            Reduction operation.

        Parameter ``address_u``:
            Texture addressing mode for the U coordinate.

        Parameter ``address_v``:
            Texture addressing mode for the V coordinate.

        Parameter ``address_w``:
            Texture addressing mode for the W coordinate.

        Parameter ``mip_lod_bias``:
            Mip-map LOD bias.

        Parameter ``max_anisotropy``:
            Maximum anisotropy.

        Parameter ``comparison_func``:
            Comparison function.

        Parameter ``border_color``:
            Border color.

        Parameter ``min_lod``:
            Minimum LOD level.

        Parameter ``max_lod``:
            Maximum LOD level.

        Returns:
            New sampler object.
        """

    @overload
    def create_sampler(self, desc: SamplerDescParam) -> Sampler:
        """
        Create a new sampler.

        Parameter ``min_filter``:
            Minification filter.

        Parameter ``mag_filter``:
            Magnification filter.

        Parameter ``mip_filter``:
            Mip-map filter.

        Parameter ``reduction_op``:
            Reduction operation.

        Parameter ``address_u``:
            Texture addressing mode for the U coordinate.

        Parameter ``address_v``:
            Texture addressing mode for the V coordinate.

        Parameter ``address_w``:
            Texture addressing mode for the W coordinate.

        Parameter ``mip_lod_bias``:
            Mip-map LOD bias.

        Parameter ``max_anisotropy``:
            Maximum anisotropy.

        Parameter ``comparison_func``:
            Comparison function.

        Parameter ``border_color``:
            Border color.

        Parameter ``min_lod``:
            Minimum LOD level.

        Parameter ``max_lod``:
            Maximum LOD level.

        Returns:
            New sampler object.
        """

    @overload
    def create_fence(self, initial_value: int = 0, shared: bool = False) -> Fence:
        """
        Create a new fence.

        Parameter ``initial_value``:
            Initial fence value.

        Parameter ``shared``:
            Create a shared fence.

        Returns:
            New fence object.
        """

    @overload
    def create_fence(self, desc: FenceDescParam) -> Fence:
        """
        Create a new fence.

        Parameter ``initial_value``:
            Initial fence value.

        Parameter ``shared``:
            Create a shared fence.

        Returns:
            New fence object.
        """

    def create_query_pool(self, type: QueryType, count: int) -> QueryPool:
        """
        Create a new query pool.

        Parameter ``type``:
            Query type.

        Parameter ``count``:
            Number of queries in the pool.

        Returns:
            New query pool object.
        """

    @overload
    def create_input_layout(self, input_elements: Sequence[InputElementDescParam], vertex_streams: Sequence[VertexStreamDescParam]) -> InputLayout:
        """
        Create a new input layout.

        Parameter ``input_elements``:
            List of input elements (see InputElementDesc for details).

        Parameter ``vertex_streams``:
            List of vertex streams (see VertexStreamDesc for details).

        Returns:
            New input layout object.
        """

    @overload
    def create_input_layout(self, desc: InputLayoutDescParam) -> InputLayout:
        """
        Create a new input layout.

        Parameter ``input_elements``:
            List of input elements (see InputElementDesc for details).

        Parameter ``vertex_streams``:
            List of vertex streams (see VertexStreamDesc for details).

        Returns:
            New input layout object.
        """

    @overload
    def create_framebuffer(self, render_targets: Sequence[ResourceView], depth_stencil: ResourceView | None = None, layout: FramebufferLayout | None = None) -> Framebuffer:
        """
        Create a new framebuffer.

        Parameter ``render_target``:
            List of render targets (see FramebufferAttachmentDesc for
            details).

        Parameter ``depth_stencil``:
            Optional depth-stencil attachment (see FramebufferAttachmentDesc
            for details).

        Returns:
            New framebuffer object.
        """

    @overload
    def create_framebuffer(self, desc: FramebufferDescParam) -> Framebuffer:
        """
        Create a new framebuffer.

        Parameter ``render_target``:
            List of render targets (see FramebufferAttachmentDesc for
            details).

        Parameter ``depth_stencil``:
            Optional depth-stencil attachment (see FramebufferAttachmentDesc
            for details).

        Returns:
            New framebuffer object.
        """

    def create_command_buffer(self) -> CommandBuffer: ...

    def submit_command_buffer(self, command_buffer: CommandBuffer, queue: CommandQueueType = CommandQueueType.graphics) -> int:
        """
        Submit a command buffer to the device.

        The returned submission ID can be used to wait for the command buffer
        to complete.

        Parameter ``command_buffer``:
            Command buffer to submit.

        Parameter ``queue``:
            Command queue to submit to.

        Returns:
            Submission ID.
        """

    def is_command_buffer_complete(self, id: int) -> bool:
        """
        Check if a command buffer is complete.

        Parameter ``id``:
            Submission ID.

        Returns:
            True if the command buffer is complete.
        """

    def wait_command_buffer(self, id: int) -> None:
        """
        Wait for a command buffer to complete.

        Parameter ``id``:
            Submission ID.
        """

    def wait_for_idle(self, queue: CommandQueueType = CommandQueueType.graphics) -> None:
        """
        Wait for the command queue to be idle.

        Parameter ``queue``:
            Command queue to wait for.
        """

    def sync_to_cuda(self, cuda_stream: int = 0) -> None:
        """
        Synchronize CUDA -> device.

        This signals a shared CUDA semaphore from the CUDA stream and then
        waits for the signal on the command queue.

        Parameter ``cuda_stream``:
            CUDA stream
        """

    def sync_to_device(self, cuda_stream: int = 0) -> None:
        """
        Synchronize device -> CUDA.

        This waits for a shared CUDA semaphore on the CUDA stream, making sure
        all commands on the device have completed.

        Parameter ``cuda_stream``:
            CUDA stream
        """

    def get_acceleration_structure_prebuild_info(self, build_inputs: AccelerationStructureBuildInputsBase) -> AccelerationStructurePrebuildInfo: ...

    def create_acceleration_structure(self, kind: AccelerationStructureKind, buffer: Buffer, offset: int = 0, size: int = 0) -> AccelerationStructure: ...

    @overload
    def create_shader_table(self, program: ShaderProgram, ray_gen_entry_points: Sequence[str] = [], miss_entry_points: Sequence[str] = [], hit_group_names: Sequence[str] = [], callable_entry_points: Sequence[str] = []) -> ShaderTable: ...

    @overload
    def create_shader_table(self, desc: ShaderTableDescParam) -> ShaderTable: ...

    def create_slang_session(self, compiler_options: SlangCompilerOptionsParam | None = None, add_default_include_paths: bool = True, cache_path: str | os.PathLike | None = None) -> SlangSession:
        """
        Create a new slang session.

        Parameter ``compiler_options``:
            Compiler options (see SlangCompilerOptions for details).

        Returns:
            New slang session object.
        """

    def reload_all_programs(self) -> None: ...

    def load_module(self, module_name: str) -> SlangModule: ...

    def load_module_from_source(self, module_name: str, source: str, path: str | os.PathLike | None = None) -> SlangModule: ...

    def link_program(self, modules: Sequence[SlangModule], entry_points: Sequence[SlangEntryPoint], link_options: SlangLinkOptionsParam | None = None) -> ShaderProgram: ...

    def load_program(self, module_name: str, entry_point_names: Sequence[str], additional_source: str | None = None, link_options: SlangLinkOptionsParam | None = None) -> ShaderProgram: ...

    @overload
    def create_mutable_shader_object(self, shader_program: ShaderProgram) -> MutableShaderObject: ...

    @overload
    def create_mutable_shader_object(self, type_layout: TypeLayoutReflection) -> MutableShaderObject: ...

    @overload
    def create_mutable_shader_object(self, cursor: ReflectionCursor) -> MutableShaderObject: ...

    @overload
    def create_compute_pipeline(self, program: ShaderProgram) -> ComputePipeline: ...

    @overload
    def create_compute_pipeline(self, desc: ComputePipelineDescParam) -> ComputePipeline: ...

    @overload
    def create_graphics_pipeline(self, program: ShaderProgram, input_layout: InputLayout | None, framebuffer_layout: FramebufferLayout, primitive_type: PrimitiveType = PrimitiveType.triangle, depth_stencil: DepthStencilDescParam | None = None, rasterizer: RasterizerDescParam | None = None, blend: BlendDescParam | None = None) -> GraphicsPipeline: ...

    @overload
    def create_graphics_pipeline(self, desc: GraphicsPipelineDescParam) -> GraphicsPipeline: ...

    @overload
    def create_ray_tracing_pipeline(self, program: ShaderProgram, hit_groups: Sequence[HitGroupDescParam], max_recursion: int = 0, max_ray_payload_size: int = 0, max_attribute_size: int = 8, flags: RayTracingPipelineFlags = RayTracingPipelineFlags.none) -> RayTracingPipeline: ...

    @overload
    def create_ray_tracing_pipeline(self, desc: RayTracingPipelineDescParam) -> RayTracingPipeline: ...

    @overload
    def create_compute_kernel(self, program: ShaderProgram) -> ComputeKernel: ...

    @overload
    def create_compute_kernel(self, desc: ComputeKernelDesc) -> ComputeKernel: ...

    @overload
    def create_memory_heap(self, memory_type: MemoryType, usage: ResourceUsage, page_size: int = 4194304, retain_large_pages: bool = False, debug_name: str = '') -> MemoryHeap: ...

    @overload
    def create_memory_heap(self, desc: MemoryHeapDesc) -> MemoryHeap: ...

    @property
    def upload_heap(self) -> MemoryHeap: ...

    @property
    def read_back_heap(self) -> MemoryHeap: ...

    def flush_print(self) -> None:
        """Block and flush all shader side debug print output."""

    def flush_print_to_string(self) -> str:
        """Block and flush all shader side debug print output to a string."""

    def run_garbage_collection(self) -> None:
        """
        Execute garbage collection.

        This function should be called regularly to execute deferred releases
        (at least once a frame).
        """

    def wait(self) -> None:
        """Wait for all device work to complete."""

    @staticmethod
    def enumerate_adapters(type: DeviceType = DeviceType.automatic) -> list[AdapterInfo]:
        """Enumerates all available adapters of a given device type."""

    @staticmethod
    def report_live_objects() -> None:
        """
        Report live objects in the slang/gfx layer. This is useful for
        checking clean shutdown with all resources released properly.
        """

class DeviceDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def type(self) -> DeviceType:
        """The type of the device."""

    @type.setter
    def type(self, arg: DeviceType, /) -> None: ...

    @property
    def enable_debug_layers(self) -> bool:
        """Enable debug layers."""

    @enable_debug_layers.setter
    def enable_debug_layers(self, arg: bool, /) -> None: ...

    @property
    def enable_cuda_interop(self) -> bool:
        """Enable CUDA interoperability."""

    @enable_cuda_interop.setter
    def enable_cuda_interop(self, arg: bool, /) -> None: ...

    @property
    def enable_print(self) -> bool:
        """Enable device side printing (adds performance overhead)."""

    @enable_print.setter
    def enable_print(self, arg: bool, /) -> None: ...

    @property
    def enable_hot_reload(self) -> bool:
        """Adapter LUID to select adapter on which the device will be created."""

    @enable_hot_reload.setter
    def enable_hot_reload(self, arg: bool, /) -> None: ...

    @property
    def adapter_luid(self) -> list[int] | None:
        """Adapter LUID to select adapter on which the device will be created."""

    @adapter_luid.setter
    def adapter_luid(self, arg: Sequence[int], /) -> None: ...

    @property
    def compiler_options(self) -> SlangCompilerOptions:
        """Compiler options (used for default slang session)."""

    @compiler_options.setter
    def compiler_options(self, arg: SlangCompilerOptionsParam, /) -> None: ...

    @property
    def shader_cache_path(self) -> pathlib.Path | None:
        """
        Path to the shader cache directory (optional). If a relative path is
        used, the cache is stored in the application data directory.
        """

    @shader_cache_path.setter
    def shader_cache_path(self, arg: str | os.PathLike, /) -> None: ...

DeviceDescDict = TypedDict("DeviceDescDict", {
    "type": DeviceType,
    "enable_debug_layers": bool,
    "enable_cuda_interop": bool,
    "enable_print": bool,
    "enable_hot_reload": bool,
    "adapter_luid": Sequence[int],
    "compiler_options": SlangCompilerOptionsParam,
    "shader_cache_path": str | os.PathLike
}, total = False)

DeviceDescParam = Union[DeviceDesc, DeviceDescDict]

class DeviceInfo:
    @property
    def type(self) -> DeviceType:
        """The type of the device."""

    @property
    def api_name(self) -> str:
        """The name of the graphics API being used by this device."""

    @property
    def adapter_name(self) -> str:
        """The name of the graphics adapter."""

    @property
    def timestamp_frequency(self) -> int:
        """
        The frequency of the timestamp counter. To resolve a timestamp to
        seconds, divide by this value.
        """

    @property
    def limits(self) -> DeviceLimits:
        """Limits of the device."""

class DeviceLimits:
    @property
    def max_texture_dimension_1d(self) -> int:
        """Maximum dimension for 1D textures."""

    @property
    def max_texture_dimension_2d(self) -> int:
        """Maximum dimensions for 2D textures."""

    @property
    def max_texture_dimension_3d(self) -> int:
        """Maximum dimensions for 3D textures."""

    @property
    def max_texture_dimension_cube(self) -> int:
        """Maximum dimensions for cube textures."""

    @property
    def max_texture_array_layers(self) -> int:
        """Maximum number of texture layers."""

    @property
    def max_vertex_input_elements(self) -> int:
        """Maximum number of vertex input elements in a graphics pipeline."""

    @property
    def max_vertex_input_element_offset(self) -> int:
        """Maximum offset of a vertex input element in the vertex stream."""

    @property
    def max_vertex_streams(self) -> int:
        """Maximum number of vertex streams in a graphics pipeline."""

    @property
    def max_vertex_stream_stride(self) -> int:
        """Maximum stride of a vertex stream."""

    @property
    def max_compute_threads_per_group(self) -> int:
        """Maximum number of threads per thread group."""

    @property
    def max_compute_thread_group_size(self) -> math.uint3:
        """Maximum dimensions of a thread group."""

    @property
    def max_compute_dispatch_thread_groups(self) -> math.uint3:
        """Maximum number of thread groups per dimension in a single dispatch."""

    @property
    def max_viewports(self) -> int:
        """Maximum number of viewports per pipeline."""

    @property
    def max_viewport_dimensions(self) -> math.uint2:
        """Maximum viewport dimensions."""

    @property
    def max_framebuffer_dimensions(self) -> math.uint3:
        """Maximum framebuffer dimensions."""

    @property
    def max_shader_visible_samplers(self) -> int:
        """Maximum samplers visible in a shader stage."""

class DeviceResource(Object):
    class MemoryUsage:
        @property
        def device(self) -> int:
            """The amount of memory in bytes used on the device."""

        @property
        def host(self) -> int:
            """The amount of memory in bytes used on the host."""

    @property
    def device(self) -> Device: ...

    @property
    def memory_usage(self) -> DeviceResource.MemoryUsage:
        """The memory usage by this resource."""

class DeviceType(enum.Enum):
    automatic = 0

    d3d12 = 1

    vulkan = 2

    cpu = 3

    cuda = 4

class EntryPointLayout(BaseReflectionObject):
    @property
    def name(self) -> str: ...

    @property
    def name_override(self) -> str: ...

    @property
    def stage(self) -> ShaderStage: ...

    @property
    def compute_thread_group_size(self) -> math.uint3: ...

    @property
    def parameters(self) -> EntryPointLayoutParameterList: ...

    def __repr__(self) -> str: ...

class EntryPointLayoutParameterList:
    """EntryPointLayout lazy parameter list evaluation."""

    def __len__(self) -> int: ...

    def __getitem__(self, arg: int, /) -> VariableLayoutReflection: ...

class Fence(DeviceResource):
    """Fence."""

    @property
    def desc(self) -> FenceDesc: ...

    def signal(self, value: int = 18446744073709551615) -> int:
        """
        Signal the fence. This signals the fence from the host.

        Parameter ``value``:
            The value to signal. If ``AUTO``, the signaled value will be auto-
            incremented.

        Returns:
            The signaled value.
        """

    def wait(self, value: int = 18446744073709551615, timeout_ns: int = 18446744073709551615) -> None:
        """
        Wait for the fence to be signaled on the host. Blocks the host until
        the fence reaches or exceeds the specified value.

        Parameter ``value``:
            The value to wait for. If ``AUTO``, wait for the last signaled
            value.

        Parameter ``timeout_ns``:
            The timeout in nanoseconds. If ``TIMEOUT_INFINITE``, the function
            will block indefinitely.
        """

    @property
    def current_value(self) -> int:
        """Returns the currently signaled value on the device."""

    @property
    def signaled_value(self) -> int:
        """Returns the last signaled value on the device."""

    AUTO: int = 18446744073709551615

    TIMEOUT_INFINITE: int = 18446744073709551615

class FenceDesc:
    """Fence descriptor."""

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def initial_value(self) -> int:
        """Initial fence value."""

    @initial_value.setter
    def initial_value(self, arg: int, /) -> None: ...

    @property
    def shared(self) -> bool:
        """Create a shared fence."""

    @shared.setter
    def shared(self, arg: bool, /) -> None: ...

FenceDescDict = TypedDict("FenceDescDict", {
    "initial_value": int,
    "shared": bool
}, total = False)

FenceDescParam = Union[FenceDesc, FenceDescDict]

class FileLoggerOutput(LoggerOutput):
    """Logger output that writes to a file."""

    def __init__(self, path: str | os.PathLike) -> None: ...

class FillMode(enum.Enum):
    solid = 0

    wireframe = 1

class Format(enum.Enum):
    unknown = 0

    rgba32_typeless = 1

    rgb32_typeless = 2

    rg32_typeless = 3

    r32_typeless = 4

    rgba16_typeless = 5

    rg16_typeless = 6

    r16_typeless = 7

    rgba8_typeless = 8

    rg8_typeless = 9

    r8_typeless = 10

    bgra8_typeless = 11

    rgba32_float = 12

    rgb32_float = 13

    rg32_float = 14

    r32_float = 15

    rgba16_float = 16

    rg16_float = 17

    r16_float = 18

    rgba32_uint = 19

    rgb32_uint = 20

    rg32_uint = 21

    r32_uint = 22

    rgba16_uint = 23

    rg16_uint = 24

    r16_uint = 25

    rgba8_uint = 26

    rg8_uint = 27

    r8_uint = 28

    rgba32_sint = 29

    rgb32_sint = 30

    rg32_sint = 31

    r32_sint = 32

    rgba16_sint = 33

    rg16_sint = 34

    r16_sint = 35

    rgba8_sint = 36

    rg8_sint = 37

    r8_sint = 38

    rgba16_unorm = 39

    rg16_unorm = 40

    r16_unorm = 41

    rgba8_unorm = 42

    rgba8_unorm_srgb = 43

    rg8_unorm = 44

    r8_unorm = 45

    bgra8_unorm = 46

    bgra8_unorm_srgb = 47

    bgrx8_unorm = 48

    bgrx8_unorm_srgb = 49

    rgba16_snorm = 50

    rg16_snorm = 51

    r16_snorm = 52

    rgba8_snorm = 53

    rg8_snorm = 54

    r8_snorm = 55

    d32_float = 56

    d16_unorm = 57

    d32_float_s8_uint = 58

    r32_float_x32_typeless = 59

    bgra4_unorm = 60

    b5g6r5_unorm = 61

    b5g5r5a1_unorm = 62

    r9g9b9e5_sharedexp = 63

    r10g10b10a2_typeless = 64

    r10g10b10a2_unorm = 65

    r10g10b10a2_uint = 66

    r11g11b10_float = 67

    bc1_unorm = 68

    bc1_unorm_srgb = 69

    bc2_unorm = 70

    bc2_unorm_srgb = 71

    bc3_unorm = 72

    bc3_unorm_srgb = 73

    bc4_unorm = 74

    bc4_snorm = 75

    bc5_unorm = 76

    bc5_snorm = 77

    bc6h_uf16 = 78

    bc6h_sf16 = 79

    bc7_unorm = 80

    bc7_unorm_srgb = 81

class FormatChannels(enum.IntFlag):
    none = 0

    r = 1

    g = 2

    b = 4

    a = 8

    rg = 3

    rgb = 7

    rgba = 15

class FormatInfo:
    """Resource format information."""

    @property
    def format(self) -> Format:
        """Resource format."""

    @property
    def name(self) -> str:
        """Format name."""

    @property
    def bytes_per_block(self) -> int:
        """Number of bytes per block (compressed) or pixel (uncompressed)."""

    @property
    def channel_count(self) -> int:
        """Number of channels."""

    @property
    def type(self) -> FormatType:
        """Format type (typeless, float, unorm, unorm_srgb, snorm, uint, sint)."""

    @property
    def is_depth(self) -> bool:
        """True if format has a depth component."""

    @property
    def is_stencil(self) -> bool:
        """True if format has a stencil component."""

    @property
    def is_compressed(self) -> bool:
        """True if format is compressed."""

    @property
    def block_width(self) -> int:
        """Block width for compressed formats (1 for uncompressed formats)."""

    @property
    def block_height(self) -> int:
        """Block height for compressed formats (1 for uncompressed formats)."""

    @property
    def channel_bit_count(self) -> list[int]:
        """Number of bits per channel."""

    @property
    def dxgi_format(self) -> int:
        """DXGI format."""

    @property
    def vk_format(self) -> int:
        """Vulkan format."""

    def is_depth_stencil(self) -> bool:
        """True if format has a depth or stencil component."""

    def is_typeless_format(self) -> bool:
        """True if format is typeless."""

    def is_float_format(self) -> bool:
        """True if format is floating point."""

    def is_integer_format(self) -> bool:
        """True if format is integer."""

    def is_normalized_format(self) -> bool:
        """True if format is normalized."""

    def is_srgb_format(self) -> bool:
        """True if format is sRGB."""

    def get_channels(self) -> FormatChannels:
        """Get the channels for the format (only for color formats)."""

    def get_channel_bits(self, arg: FormatChannels, /) -> int:
        """Get the number of bits for the specified channels."""

    def has_equal_channel_bits(self) -> bool:
        """Check if all channels have the same number of bits."""

    def __repr__(self) -> str: ...

class FormatType(enum.Enum):
    unknown = 0

    typeless = 1

    float = 2

    unorm = 3

    unorm_srgb = 4

    snorm = 5

    uint = 6

    sint = 7

class Framebuffer(DeviceResource):
    @property
    def desc(self) -> FramebufferDesc: ...

    @property
    def layout(self) -> FramebufferLayout: ...

class FramebufferDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def render_targets(self) -> list[ResourceView]:
        """List of render targets."""

    @render_targets.setter
    def render_targets(self, arg: Sequence[ResourceView], /) -> None: ...

    @property
    def depth_stencil(self) -> ResourceView:
        """Depth-stencil target (optional)."""

    @depth_stencil.setter
    def depth_stencil(self, arg: ResourceView, /) -> None: ...

    @property
    def layout(self) -> FramebufferLayout:
        """
        Framebuffer layout (optional). If not provided, framebuffer layout is
        determined from the render targets.
        """

    @layout.setter
    def layout(self, arg: FramebufferLayout, /) -> None: ...

FramebufferDescDict = TypedDict("FramebufferDescDict", {
    "render_targets": Sequence[ResourceView],
    "depth_stencil": ResourceView,
    "layout": FramebufferLayout
}, total = False)

FramebufferDescParam = Union[FramebufferDesc, FramebufferDescDict]

class FramebufferLayout(DeviceResource):
    @property
    def desc(self) -> FramebufferLayoutDesc: ...

class FramebufferLayoutDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def render_targets(self) -> list[FramebufferLayoutTargetDesc]: ...

    @render_targets.setter
    def render_targets(self, arg: Sequence[FramebufferLayoutTargetDescParam], /) -> None: ...

    @property
    def depth_stencil(self) -> FramebufferLayoutTargetDesc | None: ...

    @depth_stencil.setter
    def depth_stencil(self, arg: FramebufferLayoutTargetDescParam, /) -> None: ...

FramebufferLayoutDescDict = TypedDict("FramebufferLayoutDescDict", {
    "render_targets": Sequence[FramebufferLayoutTargetDescParam],
    "depth_stencil": FramebufferLayoutTargetDescParam
}, total = False)

FramebufferLayoutDescParam = Union[FramebufferLayoutDesc, FramebufferLayoutDescDict]

class FramebufferLayoutTargetDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def format(self) -> Format: ...

    @format.setter
    def format(self, arg: Format, /) -> None: ...

    @property
    def sample_count(self) -> int: ...

    @sample_count.setter
    def sample_count(self, arg: int, /) -> None: ...

FramebufferLayoutTargetDescDict = TypedDict("FramebufferLayoutTargetDescDict", {
    "format": Format,
    "sample_count": int
}, total = False)

FramebufferLayoutTargetDescParam = Union[FramebufferLayoutTargetDesc, FramebufferLayoutTargetDescDict]

class FrontFaceMode(enum.Enum):
    counter_clockwise = 0

    clockwise = 1

class FunctionReflection(BaseReflectionObject):
    @property
    def name(self) -> str: ...

    @property
    def return_type(self) -> TypeReflection: ...

    @property
    def parameters(self) -> FunctionReflectionParameterList: ...

    def has_modifier(self, modifier: ModifierID) -> bool:
        """Check if variable has a given modifier (e.g. 'inout')."""

    def specialize_with_arg_types(self, types: Sequence[TypeReflection]) -> FunctionReflection:
        """N/A"""

    @property
    def is_overloaded(self) -> bool:
        """N/A"""

    @property
    def overloads(self) -> FunctionReflectionOverloadList:
        """N/A"""

class FunctionReflectionOverloadList:
    """N/A"""

    def __len__(self) -> int: ...

    def __getitem__(self, arg: int, /) -> FunctionReflection: ...

class FunctionReflectionParameterList:
    """FunctionReflection lazy parameter list evaluation."""

    def __len__(self) -> int: ...

    def __getitem__(self, arg: int, /) -> VariableReflection: ...

class GamepadButton(enum.Enum):
    """Gamepad buttons."""

    a = 0

    b = 1

    x = 2

    y = 3

    left_bumper = 4

    right_bumper = 5

    back = 6

    start = 7

    guide = 8

    left_thumb = 9

    right_thumb = 10

    up = 11

    right = 12

    down = 13

    left = 14

class GamepadEvent:
    """Gamepad event."""

    @property
    def type(self) -> GamepadEventType:
        """The event type."""

    @property
    def button(self) -> GamepadButton:
        """The gamepad button that was pressed/released."""

    def is_button_down(self) -> bool:
        """Returns true if this event is a gamepad button down event."""

    def is_button_up(self) -> bool:
        """Returns true if this event is a gamepad button up event."""

    def is_connect(self) -> bool:
        """Returns true if this event is a gamepad connect event."""

    def is_disconnect(self) -> bool:
        """Returns true if this event is a gamepad disconnect event."""

    def __repr__(self) -> str: ...

class GamepadEventType(enum.Enum):
    """Gamepad event types."""

    button_down = 0

    button_up = 1

    connect = 2

    disconnect = 3

class GamepadState:
    """Gamepad state."""

    @property
    def left_x(self) -> float:
        """X-axis of the left analog stick."""

    @property
    def left_y(self) -> float:
        """Y-axis of the left analog stick."""

    @property
    def right_x(self) -> float:
        """X-axis of the right analog stick."""

    @property
    def right_y(self) -> float:
        """Y-axis of the right analog stick."""

    @property
    def left_trigger(self) -> float:
        """Value of the left analog trigger."""

    @property
    def right_trigger(self) -> float:
        """Value of the right analog trigger."""

    @property
    def buttons(self) -> int:
        """Bitfield of gamepad buttons (see GamepadButton)."""

    def is_button_down(self, arg: GamepadButton, /) -> bool:
        """Returns true if the specified button is down."""

    def __repr__(self) -> str: ...

class GraphicsPipeline(Pipeline):
    """Graphics pipeline."""

class GraphicsPipelineDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def program(self) -> ShaderProgram: ...

    @program.setter
    def program(self, arg: ShaderProgram, /) -> None: ...

    @property
    def input_layout(self) -> InputLayout: ...

    @input_layout.setter
    def input_layout(self, arg: InputLayout, /) -> None: ...

    @property
    def framebuffer_layout(self) -> FramebufferLayout: ...

    @framebuffer_layout.setter
    def framebuffer_layout(self, arg: FramebufferLayout, /) -> None: ...

    @property
    def primitive_type(self) -> PrimitiveType: ...

    @primitive_type.setter
    def primitive_type(self, arg: PrimitiveType, /) -> None: ...

    @property
    def depth_stencil(self) -> DepthStencilDesc: ...

    @depth_stencil.setter
    def depth_stencil(self, arg: DepthStencilDescParam, /) -> None: ...

    @property
    def rasterizer(self) -> RasterizerDesc: ...

    @rasterizer.setter
    def rasterizer(self, arg: RasterizerDescParam, /) -> None: ...

    @property
    def blend(self) -> BlendDesc: ...

    @blend.setter
    def blend(self, arg: BlendDescParam, /) -> None: ...

GraphicsPipelineDescDict = TypedDict("GraphicsPipelineDescDict", {
    "program": ShaderProgram,
    "input_layout": InputLayout,
    "framebuffer_layout": FramebufferLayout,
    "primitive_type": PrimitiveType,
    "depth_stencil": DepthStencilDescParam,
    "rasterizer": RasterizerDescParam,
    "blend": BlendDescParam
}, total = False)

GraphicsPipelineDescParam = Union[GraphicsPipelineDesc, GraphicsPipelineDescDict]

class HitGroupDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @overload
    def __init__(self, hit_group_name: str, closest_hit_entry_point: str = '', any_hit_entry_point: str = '', intersection_entry_point: str = '') -> None: ...

    @property
    def hit_group_name(self) -> str: ...

    @hit_group_name.setter
    def hit_group_name(self, arg: str, /) -> None: ...

    @property
    def closest_hit_entry_point(self) -> str: ...

    @closest_hit_entry_point.setter
    def closest_hit_entry_point(self, arg: str, /) -> None: ...

    @property
    def any_hit_entry_point(self) -> str: ...

    @any_hit_entry_point.setter
    def any_hit_entry_point(self, arg: str, /) -> None: ...

    @property
    def intersection_entry_point(self) -> str: ...

    @intersection_entry_point.setter
    def intersection_entry_point(self, arg: str, /) -> None: ...

HitGroupDescDict = TypedDict("HitGroupDescDict", {
    "hit_group_name": str,
    "closest_hit_entry_point": str,
    "any_hit_entry_point": str,
    "intersection_entry_point": str
}, total = False)

HitGroupDescParam = Union[HitGroupDesc, HitGroupDescDict]

class InputElementDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def semantic_name(self) -> str:
        """The name of the corresponding parameter in shader code."""

    @semantic_name.setter
    def semantic_name(self, arg: str, /) -> None: ...

    @property
    def semantic_index(self) -> int:
        """
        The index of the corresponding parameter in shader code. Only needed
        if multiple parameters share a semantic name.
        """

    @semantic_index.setter
    def semantic_index(self, arg: int, /) -> None: ...

    @property
    def format(self) -> Format:
        """The format of the data being fetched for this element."""

    @format.setter
    def format(self, arg: Format, /) -> None: ...

    @property
    def offset(self) -> int:
        """
        The offset in bytes of this element from the start of the
        corresponding chunk of vertex stream data.
        """

    @offset.setter
    def offset(self, arg: int, /) -> None: ...

    @property
    def buffer_slot_index(self) -> int:
        """The index of the vertex stream to fetch this element's data from."""

    @buffer_slot_index.setter
    def buffer_slot_index(self, arg: int, /) -> None: ...

InputElementDescDict = TypedDict("InputElementDescDict", {
    "semantic_name": str,
    "semantic_index": int,
    "format": Format,
    "offset": int,
    "buffer_slot_index": int
}, total = False)

InputElementDescParam = Union[InputElementDesc, InputElementDescDict]

class InputLayout(DeviceResource):
    @property
    def desc(self) -> InputLayoutDesc: ...

class InputLayoutDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def input_elements(self) -> list[InputElementDesc]: ...

    @input_elements.setter
    def input_elements(self, arg: Sequence[InputElementDescParam], /) -> None: ...

    @property
    def vertex_streams(self) -> list[VertexStreamDesc]: ...

    @vertex_streams.setter
    def vertex_streams(self, arg: Sequence[VertexStreamDescParam], /) -> None: ...

InputLayoutDescDict = TypedDict("InputLayoutDescDict", {
    "input_elements": Sequence[InputElementDescParam],
    "vertex_streams": Sequence[VertexStreamDescParam]
}, total = False)

InputLayoutDescParam = Union[InputLayoutDesc, InputLayoutDescDict]

class InputSlotClass(enum.Enum):
    per_vertex = 0

    per_instance = 1

class Kernel(DeviceResource):
    @property
    def program(self) -> ShaderProgram: ...

    @property
    def reflection(self) -> ReflectionCursor: ...

class KeyCode(enum.Enum):
    """Keyboard key codes."""

    space = 32

    apostrophe = 39

    comma = 44

    minus = 45

    period = 46

    slash = 47

    key0 = 48

    key1 = 49

    key2 = 50

    key3 = 51

    key4 = 52

    key5 = 53

    key6 = 54

    key7 = 55

    key8 = 56

    key9 = 57

    semicolon = 59

    equal = 61

    a = 65

    b = 66

    c = 67

    d = 68

    e = 69

    f = 70

    g = 71

    h = 72

    i = 73

    j = 74

    k = 75

    l = 76

    m = 77

    n = 78

    o = 79

    p = 80

    q = 81

    r = 82

    s = 83

    t = 84

    u = 85

    v = 86

    w = 87

    x = 88

    y = 89

    z = 90

    left_bracket = 91

    backslash = 92

    right_bracket = 93

    grave_accent = 96

    escape = 256

    tab = 257

    enter = 258

    backspace = 259

    insert = 260

    delete = 261

    right = 262

    left = 263

    down = 264

    up = 265

    page_up = 266

    page_down = 267

    home = 268

    end = 269

    caps_lock = 270

    scroll_lock = 271

    num_lock = 272

    print_screen = 273

    pause = 274

    f1 = 275

    f2 = 276

    f3 = 277

    f4 = 278

    f5 = 279

    f6 = 280

    f7 = 281

    f8 = 282

    f9 = 283

    f10 = 284

    f11 = 285

    f12 = 286

    keypad0 = 287

    keypad1 = 288

    keypad2 = 289

    keypad3 = 290

    keypad4 = 291

    keypad5 = 292

    keypad6 = 293

    keypad7 = 294

    keypad8 = 295

    keypad9 = 296

    keypad_del = 297

    keypad_divide = 298

    keypad_multiply = 299

    keypad_subtract = 300

    keypad_add = 301

    keypad_enter = 302

    keypad_equal = 303

    left_shift = 304

    left_control = 305

    left_alt = 306

    left_super = 307

    right_shift = 308

    right_control = 309

    right_alt = 310

    right_super = 311

    menu = 312

    unknown = 313

class KeyModifier(enum.Enum):
    """Keyboard modifiers."""

    shift = 1

    ctrl = 2

    alt = 4

class KeyModifierFlags(enum.Enum):
    """Keyboard modifier flags."""

    none = 0

    shift = 1

    ctrl = 2

    alt = 4

class KeyboardEvent:
    """Keyboard event."""

    @property
    def type(self) -> KeyboardEventType:
        """The event type."""

    @property
    def key(self) -> KeyCode:
        """The key that was pressed/released/repeated."""

    @property
    def mods(self) -> KeyModifierFlags:
        """Keyboard modifier flags."""

    @property
    def codepoint(self) -> int:
        """UTF-32 codepoint for input events."""

    def is_key_press(self) -> bool:
        """Returns true if this event is a key press event."""

    def is_key_release(self) -> bool:
        """Returns true if this event is a key release event."""

    def is_key_repeat(self) -> bool:
        """Returns true if this event is a key repeat event."""

    def is_input(self) -> bool:
        """Returns true if this event is an input event."""

    def has_modifier(self, arg: KeyModifier, /) -> bool:
        """Returns true if the specified modifier is set."""

    def __repr__(self) -> str: ...

class KeyboardEventType(enum.Enum):
    """Keyboard event types."""

    key_press = 0

    key_release = 1

    key_repeat = 2

    input = 3

class LogFrequency(enum.Enum):
    """Log frequency."""

    always = 0
    """Log the message every time."""

    once = 1
    """Log the message only once."""

class LogLevel(enum.IntEnum):
    """Log level."""

    none = 0

    debug = 1

    info = 2

    warn = 3

    error = 4

    fatal = 5

class Logger:
    def __init__(self, level: LogLevel = LogLevel.info, name: str = '', use_default_outputs: bool = True) -> None:
        """
        Constructor.

        Parameter ``level``:
            The log level to use (messages with level >= this will be logged).

        Parameter ``name``:
            The name of the logger.

        Parameter ``use_default_outputs``:
            Whether to use the default outputs (console + debug console on
            windows).
        """

    @property
    def level(self) -> LogLevel:
        """The log level."""

    @level.setter
    def level(self, arg: LogLevel, /) -> None: ...

    @property
    def name(self) -> str:
        """The name of the logger."""

    @name.setter
    def name(self, arg: str, /) -> None: ...

    def add_console_output(self, colored: bool = True) -> LoggerOutput:
        """
        Add a console logger output.

        Parameter ``colored``:
            Whether to use colored output.

        Returns:
            The created logger output.
        """

    def add_file_output(self, path: str | os.PathLike) -> LoggerOutput:
        """
        Add a file logger output.

        Parameter ``path``:
            The path to the log file.

        Returns:
            The created logger output.
        """

    def add_debug_console_output(self) -> LoggerOutput:
        """
        Add a debug console logger output (Windows only).

        Returns:
            The created logger output.
        """

    def add_output(self, output: LoggerOutput) -> None:
        """
        Add a logger output.

        Parameter ``output``:
            The logger output to add.
        """

    def use_same_outputs(self, other: Logger) -> None:
        """
        Use the same outputs as the given logger.

        Parameter ``other``:
            Logger to copy outputs from.
        """

    def remove_output(self, output: LoggerOutput) -> None:
        """
        Remove a logger output.

        Parameter ``output``:
            The logger output to remove.
        """

    def remove_all_outputs(self) -> None:
        """Remove all logger outputs."""

    def log(self, level: LogLevel, msg: str, frequency: LogFrequency = LogFrequency.always) -> None:
        """
        Log a message.

        Parameter ``level``:
            The log level.

        Parameter ``msg``:
            The message.

        Parameter ``frequency``:
            The log frequency.
        """

    def debug(self, msg: str) -> None: ...

    def info(self, msg: str) -> None: ...

    def warn(self, msg: str) -> None: ...

    def error(self, msg: str) -> None: ...

    def fatal(self, msg: str) -> None: ...

    def debug_once(self, msg: str) -> None: ...

    def info_once(self, msg: str) -> None: ...

    def warn_once(self, msg: str) -> None: ...

    def error_once(self, msg: str) -> None: ...

    def fatal_once(self, msg: str) -> None: ...

    @staticmethod
    def get() -> Logger:
        """Returns the global logger instance."""

class LoggerOutput(Object):
    """Abstract base class for logger outputs."""

    def __init__(self) -> None: ...

    def write(self, level: LogLevel, name: str, msg: str) -> None:
        """
        Write a log message.

        Parameter ``level``:
            The log level.

        Parameter ``module``:
            The module name.

        Parameter ``msg``:
            The message.
        """

class LogicOp(enum.Enum):
    no_op = 0

class MemoryHeap(DeviceResource):
    """
    A memory heap is used to allocate temporary host-visible memory.

    A memory heap is a collection of memory pages. Each page has a buffer
    of size ``page_size``. When allocating memory, the heap tries to add
    the allocation to the current page. If the allocation does not fit, a
    new page is allocated. For allocations larger than the configured page
    size, a new large page is allocated.

    The memory heap is tied to a fence. Each allocation records the
    currently signaled fence value when it is created. On release, the
    allocation is put on a deferred release queue. Only if the fence value
    of the memory heap is greater than the fence value of the allocation,
    the allocation is actually freed. This ensures that memory is not
    freed while still in use by the device.

    Allocations are returned as unique pointers. When the pointer is
    destroyed, the allocation is released. This ensures that the memory is
    freed when it is no longer used.
    """

    class Allocation:
        @property
        def buffer(self) -> Buffer:
            """The buffer this allocation belongs to."""

        @property
        def size(self) -> int:
            """The size of the allocation."""

        @property
        def offset(self) -> int:
            """The offset of the allocation within the buffer."""

        @property
        def device_address(self) -> int:
            """The device address of the allocation."""

    class Stats:
        @property
        def total_size(self) -> int:
            """The total size of the heap."""

        @property
        def used_size(self) -> int:
            """The used size of the heap."""

        @property
        def page_count(self) -> int:
            """The number of pages in the heap."""

        @property
        def large_page_count(self) -> int:
            """The number of large pages in the heap."""

    def allocate(self, size: int, alignment: int = 1) -> MemoryHeap.Allocation:
        """
        Allocate memory from this heap.

        Parameter ``size``:
            The number of bytes to allocate.

        Parameter ``alignment``:
            The alignment of the allocation.

        Returns:
            Returns a unique pointer to the allocation.
        """

    @property
    def stats(self) -> MemoryHeap.Stats:
        """Statistics of the heap."""

class MemoryHeapDesc:
    def __init__(self) -> None: ...

    @property
    def memory_type(self) -> MemoryType:
        """The memory type of the heap."""

    @memory_type.setter
    def memory_type(self, arg: MemoryType, /) -> None: ...

    @property
    def usage(self) -> ResourceUsage:
        """The resource usage of the heap."""

    @usage.setter
    def usage(self, arg: ResourceUsage, /) -> None: ...

    @property
    def page_size(self) -> int:
        """The size of a page in bytes."""

    @page_size.setter
    def page_size(self, arg: int, /) -> None: ...

    @property
    def retain_large_pages(self) -> bool:
        """True to retain large pages, false to release them after use."""

    @retain_large_pages.setter
    def retain_large_pages(self, arg: bool, /) -> None: ...

    @property
    def debug_name(self) -> str:
        """The debug name of the heap."""

    @debug_name.setter
    def debug_name(self, arg: str, /) -> None: ...

class MemoryType(enum.Enum):
    device_local = 0

    upload = 1

    read_back = 2

class ModifierID(enum.Enum):
    shared = 0

    nodiff = 1

    static = 2

    const = 3

    export = 4

    extern = 5

    differentiable = 6

    mutating = 7

    inn = 8

    out = 9

    inout = 10

class MouseButton(enum.Enum):
    """Mouse buttons."""

    left = 0

    middle = 1

    right = 2

    unknown = 3

class MouseEvent:
    """Mouse event."""

    @property
    def type(self) -> MouseEventType:
        """The event type."""

    @property
    def pos(self) -> math.float2:
        """The mouse position."""

    @property
    def scroll(self) -> math.float2:
        """The scroll offset."""

    @property
    def button(self) -> MouseButton:
        """The mouse button that was pressed/released."""

    @property
    def mods(self) -> KeyModifierFlags:
        """Keyboard modifier flags."""

    def is_button_down(self) -> bool:
        """Returns true if this event is a mouse button down event."""

    def is_button_up(self) -> bool:
        """Returns true if this event is a mouse button up event."""

    def is_move(self) -> bool:
        """Returns true if this event is a mouse move event."""

    def is_scroll(self) -> bool:
        """Returns true if this event is a mouse scroll event."""

    def has_modifier(self, arg: KeyModifier, /) -> bool:
        """Returns true if the specified modifier is set."""

    def __repr__(self) -> str: ...

class MouseEventType(enum.Enum):
    """Mouse event types."""

    button_down = 0

    button_up = 1

    move = 2

    scroll = 3

class MutableShaderObject(ShaderObject):
    pass

class Object:
    """Base class for all reference counted objects."""

    def __repr__(self) -> str: ...

class Pipeline(DeviceResource):
    """Pipeline base class."""

class PrimitiveTopology(enum.Enum):
    triangle_list = 0

    triangle_strip = 1

    point_list = 2

    line_list = 3

    line_strip = 4

class PrimitiveType(enum.Enum):
    point = 0

    line = 1

    triangle = 2

    patch = 3

class ProgramLayout(BaseReflectionObject):
    class HashedString:
        @property
        def string(self) -> str: ...

        @property
        def hash(self) -> int: ...

    @property
    def globals_type_layout(self) -> TypeLayoutReflection: ...

    @property
    def globals_variable_layout(self) -> VariableLayoutReflection: ...

    @property
    def parameters(self) -> ProgramLayoutParameterList: ...

    @property
    def entry_points(self) -> ProgramLayoutEntryPointList: ...

    def find_type_by_name(self, name: str) -> TypeReflection:
        """N/A"""

    def find_function_by_name(self, name: str) -> FunctionReflection:
        """N/A"""

    def find_function_by_name_in_type(self, type: TypeReflection, name: str) -> FunctionReflection:
        """N/A"""

    def get_type_layout(self, type: TypeReflection) -> TypeLayoutReflection:
        """N/A"""

    def is_sub_type(self, sub_type: TypeReflection, super_type: TypeReflection) -> bool:
        """N/A"""

    @property
    def hashed_strings(self) -> list[ProgramLayout.HashedString]: ...

    def __repr__(self) -> str: ...

class ProgramLayoutEntryPointList:
    """ProgramLayout lazy entry point list evaluation."""

    def __len__(self) -> int: ...

    def __getitem__(self, arg: int, /) -> EntryPointLayout: ...

class ProgramLayoutParameterList:
    """ProgramLayout lazy parameter list evaluation."""

    def __len__(self) -> int: ...

    def __getitem__(self, arg: int, /) -> VariableLayoutReflection: ...

class QueryPool(DeviceResource):
    @property
    def desc(self) -> QueryPoolDesc: ...

    def reset(self) -> None: ...

    def get_result(self, index: int) -> int: ...

    def get_results(self, index: int, count: int) -> list[int]: ...

    def get_timestamp_result(self, index: int) -> float: ...

    def get_timestamp_results(self, index: int, count: int) -> list[float]: ...

class QueryPoolDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def type(self) -> QueryType:
        """Query type."""

    @type.setter
    def type(self, arg: QueryType, /) -> None: ...

    @property
    def count(self) -> int:
        """Number of queries in the pool."""

    @count.setter
    def count(self, arg: int, /) -> None: ...

QueryPoolDescDict = TypedDict("QueryPoolDescDict", {
    "type": QueryType,
    "count": int
}, total = False)

QueryPoolDescParam = Union[QueryPoolDesc, QueryPoolDescDict]

class QueryType(enum.Enum):
    timestamp = 0

    acceleration_structure_compacted_size = 1

    acceleration_structure_serialized_size = 2

    acceleration_structure_current_size = 3

class RasterizerDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def fill_mode(self) -> FillMode: ...

    @fill_mode.setter
    def fill_mode(self, arg: FillMode, /) -> None: ...

    @property
    def cull_mode(self) -> CullMode: ...

    @cull_mode.setter
    def cull_mode(self, arg: CullMode, /) -> None: ...

    @property
    def front_face(self) -> FrontFaceMode: ...

    @front_face.setter
    def front_face(self, arg: FrontFaceMode, /) -> None: ...

    @property
    def depth_bias(self) -> int: ...

    @depth_bias.setter
    def depth_bias(self, arg: int, /) -> None: ...

    @property
    def depth_bias_clamp(self) -> float: ...

    @depth_bias_clamp.setter
    def depth_bias_clamp(self, arg: float, /) -> None: ...

    @property
    def slope_scaled_depth_bias(self) -> float: ...

    @slope_scaled_depth_bias.setter
    def slope_scaled_depth_bias(self, arg: float, /) -> None: ...

    @property
    def depth_clip_enable(self) -> bool: ...

    @depth_clip_enable.setter
    def depth_clip_enable(self, arg: bool, /) -> None: ...

    @property
    def scissor_enable(self) -> bool: ...

    @scissor_enable.setter
    def scissor_enable(self, arg: bool, /) -> None: ...

    @property
    def multisample_enable(self) -> bool: ...

    @multisample_enable.setter
    def multisample_enable(self, arg: bool, /) -> None: ...

    @property
    def antialiased_line_enable(self) -> bool: ...

    @antialiased_line_enable.setter
    def antialiased_line_enable(self, arg: bool, /) -> None: ...

    @property
    def enable_conservative_rasterization(self) -> bool: ...

    @enable_conservative_rasterization.setter
    def enable_conservative_rasterization(self, arg: bool, /) -> None: ...

    @property
    def forced_sample_count(self) -> int: ...

    @forced_sample_count.setter
    def forced_sample_count(self, arg: int, /) -> None: ...

RasterizerDescDict = TypedDict("RasterizerDescDict", {
    "fill_mode": FillMode,
    "cull_mode": CullMode,
    "front_face": FrontFaceMode,
    "depth_bias": int,
    "depth_bias_clamp": float,
    "slope_scaled_depth_bias": float,
    "depth_clip_enable": bool,
    "scissor_enable": bool,
    "multisample_enable": bool,
    "antialiased_line_enable": bool,
    "enable_conservative_rasterization": bool,
    "forced_sample_count": int
}, total = False)

RasterizerDescParam = Union[RasterizerDesc, RasterizerDescDict]

class RayTracingAABB:
    def __init__(self) -> None: ...

    @property
    def min(self) -> math.float3: ...

    @min.setter
    def min(self, arg: float3param, /) -> None: ...

    @property
    def max(self) -> math.float3: ...

    @max.setter
    def max(self, arg: float3param, /) -> None: ...

class RayTracingAABBsDesc:
    def __init__(self) -> None: ...

    @property
    def count(self) -> int:
        """Number of AABBs."""

    @count.setter
    def count(self, arg: int, /) -> None: ...

    @property
    def data(self) -> int:
        """Pointer to an array of `RayTracingAABB` values in device memory."""

    @data.setter
    def data(self, arg: int, /) -> None: ...

    @property
    def stride(self) -> int:
        """Stride in bytes of the AABB values array."""

    @stride.setter
    def stride(self, arg: int, /) -> None: ...

class RayTracingCommandEncoder:
    def __enter__(self) -> RayTracingCommandEncoder: ...

    def __exit__(self, exc_type: object | None = None, exc_value: object | None = None, traceback: object | None = None) -> None: ...

    @overload
    def bind_pipeline(self, pipeline: RayTracingPipeline) -> TransientShaderObject: ...

    @overload
    def bind_pipeline(self, pipeline: RayTracingPipeline, shader_object: ShaderObject) -> None: ...

    def dispatch_rays(self, ray_gen_shader_index: int, shader_table: ShaderTable, dimensions: uint3param) -> None: ...

    def build_acceleration_structure(self, inputs: AccelerationStructureBuildInputsBase, dst: AccelerationStructure, scratch_data: int, src: AccelerationStructure | None = None) -> None: ...

    def copy_acceleration_structure(self, src: AccelerationStructure, dst: AccelerationStructure, mode: AccelerationStructureCopyMode) -> None: ...

class RayTracingGeometryDesc:
    def __init__(self) -> None: ...

    @property
    def type(self) -> RayTracingGeometryType: ...

    @type.setter
    def type(self, arg: RayTracingGeometryType, /) -> None: ...

    @property
    def flags(self) -> RayTracingGeometryFlags: ...

    @flags.setter
    def flags(self, arg: RayTracingGeometryFlags, /) -> None: ...

    @property
    def triangles(self) -> RayTracingTrianglesDesc: ...

    @triangles.setter
    def triangles(self, arg: RayTracingTrianglesDesc, /) -> None: ...

    @property
    def aabbs(self) -> RayTracingAABBsDesc: ...

    @aabbs.setter
    def aabbs(self, arg: RayTracingAABBsDesc, /) -> None: ...

class RayTracingGeometryFlags(enum.IntFlag):
    none = 0

    opaque = 1

    no_duplicate_any_hit_invocation = 2

class RayTracingGeometryType(enum.Enum):
    triangles = 0

    procedural_primitives = 1

class RayTracingInstanceDesc:
    def __init__(self) -> None: ...

    @property
    def transform(self) -> math.float3x4: ...

    @transform.setter
    def transform(self, arg: float3x4param, /) -> None: ...

    @property
    def instance_id(self) -> int: ...

    @instance_id.setter
    def instance_id(self, arg: int, /) -> None: ...

    @property
    def instance_mask(self) -> int: ...

    @instance_mask.setter
    def instance_mask(self, arg: int, /) -> None: ...

    @property
    def instance_contribution_to_hit_group_index(self) -> int: ...

    @instance_contribution_to_hit_group_index.setter
    def instance_contribution_to_hit_group_index(self, arg: int, /) -> None: ...

    @property
    def flags(self) -> RayTracingInstanceFlags: ...

    @flags.setter
    def flags(self, arg: RayTracingInstanceFlags, /) -> None: ...

    @property
    def acceleration_structure(self) -> int: ...

    @acceleration_structure.setter
    def acceleration_structure(self, arg: int, /) -> None: ...

    def to_numpy(self) -> Annotated[NDArray, dict(dtype='uint8', shape=(64), writable=False)]: ...

class RayTracingInstanceFlags(enum.IntFlag):
    none = 0

    triangle_facing_cull_disable = 1

    triangle_front_counter_clockwise = 2

    force_opaque = 4

    no_opaque = 8

class RayTracingPipeline(Pipeline):
    """Ray tracing pipeline."""

class RayTracingPipelineDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def program(self) -> ShaderProgram: ...

    @program.setter
    def program(self, arg: ShaderProgram, /) -> None: ...

    @property
    def hit_groups(self) -> list[HitGroupDesc]: ...

    @property
    def max_recursion(self) -> int: ...

    @max_recursion.setter
    def max_recursion(self, arg: int, /) -> None: ...

    @property
    def max_ray_payload_size(self) -> int: ...

    @max_ray_payload_size.setter
    def max_ray_payload_size(self, arg: int, /) -> None: ...

    @property
    def max_attribute_size(self) -> int: ...

    @max_attribute_size.setter
    def max_attribute_size(self, arg: int, /) -> None: ...

    @property
    def flags(self) -> RayTracingPipelineFlags: ...

    @flags.setter
    def flags(self, arg: RayTracingPipelineFlags, /) -> None: ...

RayTracingPipelineDescDict = TypedDict("RayTracingPipelineDescDict", {
    "program": ShaderProgram,
    "max_recursion": int,
    "max_ray_payload_size": int,
    "max_attribute_size": int,
    "flags": RayTracingPipelineFlags
}, total = False)

RayTracingPipelineDescParam = Union[RayTracingPipelineDesc, RayTracingPipelineDescDict]

class RayTracingPipelineFlags(enum.IntFlag):
    none = 0

    skip_triangles = 1

    skip_procedurals = 2

class RayTracingTrianglesDesc:
    def __init__(self) -> None: ...

    @property
    def transform3x4(self) -> int: ...

    @transform3x4.setter
    def transform3x4(self, arg: int, /) -> None: ...

    @property
    def index_format(self) -> Format: ...

    @index_format.setter
    def index_format(self, arg: Format, /) -> None: ...

    @property
    def vertex_format(self) -> Format: ...

    @vertex_format.setter
    def vertex_format(self, arg: Format, /) -> None: ...

    @property
    def index_count(self) -> int: ...

    @index_count.setter
    def index_count(self, arg: int, /) -> None: ...

    @property
    def vertex_count(self) -> int: ...

    @vertex_count.setter
    def vertex_count(self, arg: int, /) -> None: ...

    @property
    def index_data(self) -> int: ...

    @index_data.setter
    def index_data(self, arg: int, /) -> None: ...

    @property
    def vertex_data(self) -> int: ...

    @vertex_data.setter
    def vertex_data(self, arg: int, /) -> None: ...

    @property
    def vertex_stride(self) -> int: ...

    @vertex_stride.setter
    def vertex_stride(self, arg: int, /) -> None: ...

class ReflectionCursor:
    def __init__(self, shader_program: ShaderProgram) -> None: ...

    def is_valid(self) -> bool: ...

    def find_field(self, name: str) -> ReflectionCursor: ...

    def find_element(self, index: int) -> ReflectionCursor: ...

    def has_field(self, name: str) -> bool: ...

    def has_element(self, index: int) -> bool: ...

    @property
    def type_layout(self) -> TypeLayoutReflection: ...

    @property
    def type(self) -> TypeReflection: ...

    @overload
    def __getitem__(self, arg: str, /) -> ReflectionCursor: ...

    @overload
    def __getitem__(self, arg: int, /) -> ReflectionCursor: ...

    def __getattr__(self, arg: str, /) -> ReflectionCursor: ...

    def __repr__(self) -> str: ...

class RenderCommandEncoder:
    def __enter__(self) -> RenderCommandEncoder: ...

    def __exit__(self, exc_type: object | None = None, exc_value: object | None = None, traceback: object | None = None) -> None: ...

    @overload
    def bind_pipeline(self, pipeline: GraphicsPipeline) -> TransientShaderObject: ...

    @overload
    def bind_pipeline(self, pipeline: GraphicsPipeline, shader_object: ShaderObject) -> None: ...

    def set_viewports(self, viewports: Sequence[ViewportParam]) -> None: ...

    def set_scissor_rects(self, scissor_rects: Sequence[ScissorRectParam]) -> None: ...

    def set_viewport_and_scissor_rect(self, viewport: ViewportParam) -> None: ...

    def set_primitive_topology(self, topology: PrimitiveTopology) -> None: ...

    def set_stencil_reference(self, reference_value: int) -> None: ...

    def set_vertex_buffer(self, slot: int, buffer: Buffer, offset: int = 0) -> None: ...

    def set_index_buffer(self, buffer: Buffer, index_format: Format, offset: int = 0) -> None: ...

    def draw(self, vertex_count: int, start_vertex: int = 0) -> None: ...

    def draw_indexed(self, index_count: int, start_index: int = 0, base_vertex: int = 0) -> None: ...

    def draw_instanced(self, vertex_count: int, instance_count: int, start_vertex: int = 0, start_instance: int = 0) -> None: ...

    def draw_indexed_instanced(self, index_count: int, instance_count: int, start_index: int = 0, base_vertex: int = 0, start_instance: int = 0) -> None: ...

    def draw_indirect(self, max_draw_count: int, arg_buffer: Buffer, arg_offset: int, count_buffer: Buffer | None = None, count_offset: int = 0) -> None: ...

    def draw_indexed_indirect(self, max_draw_count: int, arg_buffer: Buffer, arg_offset: int, count_buffer: Buffer | None = None, count_offset: int = 0) -> None: ...

class RenderTargetWriteMask(enum.IntFlag):
    enable_none = 0

    enable_red = 1

    enable_green = 2

    enable_blue = 4

    enable_alpha = 8

    enable_all = 15

class Resource(DeviceResource):
    @property
    def type(self) -> ResourceType: ...

    @property
    def format(self) -> Format: ...

class ResourceState(enum.Enum):
    undefined = 0

    general = 1

    pre_initialized = 2

    vertex_buffer = 3

    index_buffer = 4

    constant_buffer = 5

    stream_output = 6

    shader_resource = 7

    unordered_access = 8

    render_target = 9

    depth_read = 10

    depth_write = 11

    present = 12

    indirect_argument = 13

    copy_source = 14

    copy_destination = 15

    resolve_source = 16

    resolve_destination = 17

    acceleration_structure = 18

    acceleration_structure_build_output = 19

    pixel_shader_resource = 20

    non_pixel_shader_resource = 21

class ResourceType(enum.Enum):
    unknown = 0

    buffer = 1

    texture_1d = 2

    texture_2d = 3

    texture_3d = 4

    texture_cube = 5

class ResourceUsage(enum.IntFlag):
    none = 0

    vertex = 1

    index = 2

    constant = 4

    stream_output = 8

    shader_resource = 16

    unordered_access = 32

    render_target = 64

    depth_stencil = 128

    indirect_arg = 256

    shared = 512

    acceleration_structure = 2147483648

class ResourceView(Object):
    @property
    def type(self) -> ResourceViewType: ...

    @property
    def resource(self) -> Resource: ...

    @property
    def buffer_range(self) -> BufferRange:
        """N/A"""

    @property
    def subresource_range(self) -> SubresourceRange:
        """N/A"""

class ResourceViewType(enum.Enum):
    unknown = 0

    render_target = 1

    depth_stencil = 2

    shader_resource = 3

    unordered_access = 4

SGL_GIT_VERSION: str = 'commit: a7bde72 / branch: main (local changes)'

SGL_VERSION: str = '0.3.0'

SGL_VERSION_MAJOR: int = 0

SGL_VERSION_MINOR: int = 3

SGL_VERSION_PATCH: int = 0

class SHA1:
    """Helper to compute SHA-1 hash."""

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, data: bytes) -> None: ...

    @overload
    def __init__(self, str: str) -> None: ...

    @overload
    def update(self, data: bytes) -> SHA1:
        """
        Update hash by adding the given data.

        Parameter ``data``:
            Data to hash.

        Parameter ``len``:
            Length of data in bytes.
        """

    @overload
    def update(self, str: str) -> SHA1:
        """
        Update hash by adding the given string.

        Parameter ``str``:
            String to hash.
        """

    def digest(self) -> bytes:
        """Return the message digest."""

    def hex_digest(self) -> str:
        """Return the message digest as a hex string."""

class Sampler(DeviceResource):
    @property
    def desc(self) -> SamplerDesc: ...

class SamplerDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def min_filter(self) -> TextureFilteringMode: ...

    @min_filter.setter
    def min_filter(self, arg: TextureFilteringMode, /) -> None: ...

    @property
    def mag_filter(self) -> TextureFilteringMode: ...

    @mag_filter.setter
    def mag_filter(self, arg: TextureFilteringMode, /) -> None: ...

    @property
    def mip_filter(self) -> TextureFilteringMode: ...

    @mip_filter.setter
    def mip_filter(self, arg: TextureFilteringMode, /) -> None: ...

    @property
    def reduction_op(self) -> TextureReductionOp: ...

    @reduction_op.setter
    def reduction_op(self, arg: TextureReductionOp, /) -> None: ...

    @property
    def address_u(self) -> TextureAddressingMode: ...

    @address_u.setter
    def address_u(self, arg: TextureAddressingMode, /) -> None: ...

    @property
    def address_v(self) -> TextureAddressingMode: ...

    @address_v.setter
    def address_v(self, arg: TextureAddressingMode, /) -> None: ...

    @property
    def address_w(self) -> TextureAddressingMode: ...

    @address_w.setter
    def address_w(self, arg: TextureAddressingMode, /) -> None: ...

    @property
    def mip_lod_bias(self) -> float: ...

    @mip_lod_bias.setter
    def mip_lod_bias(self, arg: float, /) -> None: ...

    @property
    def max_anisotropy(self) -> int: ...

    @max_anisotropy.setter
    def max_anisotropy(self, arg: int, /) -> None: ...

    @property
    def comparison_func(self) -> ComparisonFunc: ...

    @comparison_func.setter
    def comparison_func(self, arg: ComparisonFunc, /) -> None: ...

    @property
    def border_color(self) -> math.float4: ...

    @border_color.setter
    def border_color(self, arg: float4param, /) -> None: ...

    @property
    def min_lod(self) -> float: ...

    @min_lod.setter
    def min_lod(self, arg: float, /) -> None: ...

    @property
    def max_lod(self) -> float: ...

    @max_lod.setter
    def max_lod(self, arg: float, /) -> None: ...

SamplerDescDict = TypedDict("SamplerDescDict", {
    "min_filter": TextureFilteringMode,
    "mag_filter": TextureFilteringMode,
    "mip_filter": TextureFilteringMode,
    "reduction_op": TextureReductionOp,
    "address_u": TextureAddressingMode,
    "address_v": TextureAddressingMode,
    "address_w": TextureAddressingMode,
    "mip_lod_bias": float,
    "max_anisotropy": int,
    "comparison_func": ComparisonFunc,
    "border_color": float4param,
    "min_lod": float,
    "max_lod": float
}, total = False)

SamplerDescParam = Union[SamplerDesc, SamplerDescDict]

class ScissorRect:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def min_x(self) -> int: ...

    @min_x.setter
    def min_x(self, arg: int, /) -> None: ...

    @property
    def min_y(self) -> int: ...

    @min_y.setter
    def min_y(self, arg: int, /) -> None: ...

    @property
    def max_x(self) -> int: ...

    @max_x.setter
    def max_x(self, arg: int, /) -> None: ...

    @property
    def max_y(self) -> int: ...

    @max_y.setter
    def max_y(self, arg: int, /) -> None: ...

ScissorRectDict = TypedDict("ScissorRectDict", {
    "min_x": int,
    "min_y": int,
    "max_x": int,
    "max_y": int
}, total = False)

ScissorRectParam = Union[ScissorRect, ScissorRectDict]

class ShaderCacheStats:
    @property
    def entry_count(self) -> int:
        """Number of entries in the cache."""

    @property
    def hit_count(self) -> int:
        """Number of hits in the cache."""

    @property
    def miss_count(self) -> int:
        """Number of misses in the cache."""

class ShaderCursor:
    def __init__(self, shader_object: ShaderObject) -> None: ...

    def dereference(self) -> ShaderCursor: ...

    def find_entry_point(self, index: int) -> ShaderCursor: ...

    def is_valid(self) -> bool:
        """N/A"""

    def find_field(self, name: str) -> ShaderCursor:
        """N/A"""

    def find_element(self, index: int) -> ShaderCursor:
        """N/A"""

    def has_field(self, name: str) -> bool:
        """N/A"""

    def has_element(self, index: int) -> bool:
        """N/A"""

    @overload
    def __getitem__(self, arg: str, /) -> ShaderCursor: ...

    @overload
    def __getitem__(self, arg: int, /) -> ShaderCursor: ...

    def __getattr__(self, arg: str, /) -> ShaderCursor: ...

    def __setattr__(self, name: str, val: object) -> None:
        """N/A"""

    @overload
    def __setitem__(self, index: str, val: object) -> None:
        """N/A"""

    @overload
    def __setitem__(self, index: int, val: object) -> None:
        """N/A"""

    def set_data(self, data: Annotated[ArrayLike, dict(device='cpu')]) -> None: ...

    def write(self, val: object) -> None:
        """N/A"""

class ShaderModel(enum.IntEnum):
    unknown = 0

    sm_6_0 = 60

    sm_6_1 = 61

    sm_6_2 = 62

    sm_6_3 = 63

    sm_6_4 = 64

    sm_6_5 = 65

    sm_6_6 = 66

    sm_6_7 = 67

class ShaderObject(Object):
    pass

class ShaderOffset:
    """
    Represents the offset of a shader variable relative to its enclosing
    type/buffer/block.

    A `ShaderOffset` can be used to store the offset of a shader variable
    that might use ordinary/uniform data, resources like
    textures/buffers/samplers, or some combination.

    A `ShaderOffset` can also encode an invalid offset, to indicate that a
    particular shader variable is not present.
    """

    @property
    def uniform_offset(self) -> int: ...

    @property
    def binding_range_index(self) -> int: ...

    @property
    def binding_array_index(self) -> int: ...

    def is_valid(self) -> bool:
        """Check whether this offset is valid."""

class ShaderProgram(DeviceResource):
    @property
    def layout(self) -> ProgramLayout: ...

    @property
    def reflection(self) -> ReflectionCursor: ...

class ShaderStage(enum.Enum):
    none = 0

    vertex = 1

    hull = 2

    domain = 3

    geometry = 4

    fragment = 5

    compute = 6

    ray_generation = 7

    intersection = 8

    any_hit = 9

    closest_hit = 10

    miss = 11

    callable = 12

    mesh = 13

    amplification = 14

class ShaderTable(DeviceResource):
    pass

class ShaderTableDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def program(self) -> ShaderProgram: ...

    @program.setter
    def program(self, arg: ShaderProgram, /) -> None: ...

    @property
    def ray_gen_entry_points(self) -> list[str]: ...

    @ray_gen_entry_points.setter
    def ray_gen_entry_points(self, arg: Sequence[str], /) -> None: ...

    @property
    def miss_entry_points(self) -> list[str]: ...

    @miss_entry_points.setter
    def miss_entry_points(self, arg: Sequence[str], /) -> None: ...

    @property
    def hit_group_names(self) -> list[str]: ...

    @hit_group_names.setter
    def hit_group_names(self, arg: Sequence[str], /) -> None: ...

    @property
    def callable_entry_points(self) -> list[str]: ...

    @callable_entry_points.setter
    def callable_entry_points(self, arg: Sequence[str], /) -> None: ...

ShaderTableDescDict = TypedDict("ShaderTableDescDict", {
    "program": ShaderProgram,
    "ray_gen_entry_points": Sequence[str],
    "miss_entry_points": Sequence[str],
    "hit_group_names": Sequence[str],
    "callable_entry_points": Sequence[str]
}, total = False)

ShaderTableDescParam = Union[ShaderTableDesc, ShaderTableDescDict]

class SlangCompileError(Exception):
    pass

class SlangCompilerOptions:
    """Slang compiler options. Can be set when creating a Slang session."""

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def include_paths(self) -> list[pathlib.Path]:
        """
        Specifies a list of include paths to be used when resolving
        module/include paths.
        """

    @include_paths.setter
    def include_paths(self, arg: Sequence[str | os.PathLike], /) -> None: ...

    @property
    def defines(self) -> dict[str, str]:
        """Specifies a list of preprocessor defines."""

    @defines.setter
    def defines(self, arg: Mapping[str, str], /) -> None: ...

    @property
    def shader_model(self) -> ShaderModel:
        """
        Specifies the shader model to use. Defaults to latest available on the
        device.
        """

    @shader_model.setter
    def shader_model(self, arg: ShaderModel, /) -> None: ...

    @property
    def matrix_layout(self) -> SlangMatrixLayout:
        """Specifies the matrix layout. Defaults to row-major."""

    @matrix_layout.setter
    def matrix_layout(self, arg: SlangMatrixLayout, /) -> None: ...

    @property
    def enable_warnings(self) -> list[str]:
        """Specifies a list of warnings to enable (warning codes or names)."""

    @enable_warnings.setter
    def enable_warnings(self, arg: Sequence[str], /) -> None: ...

    @property
    def disable_warnings(self) -> list[str]:
        """Specifies a list of warnings to disable (warning codes or names)."""

    @disable_warnings.setter
    def disable_warnings(self, arg: Sequence[str], /) -> None: ...

    @property
    def warnings_as_errors(self) -> list[str]:
        """
        Specifies a list of warnings to be treated as errors (warning codes or
        names, or "all" to indicate all warnings).
        """

    @warnings_as_errors.setter
    def warnings_as_errors(self, arg: Sequence[str], /) -> None: ...

    @property
    def report_downstream_time(self) -> bool:
        """Turn on/off downstream compilation time report."""

    @report_downstream_time.setter
    def report_downstream_time(self, arg: bool, /) -> None: ...

    @property
    def report_perf_benchmark(self) -> bool:
        """
        Turn on/off reporting of time spend in different parts of the
        compiler.
        """

    @report_perf_benchmark.setter
    def report_perf_benchmark(self, arg: bool, /) -> None: ...

    @property
    def skip_spirv_validation(self) -> bool:
        """
        Specifies whether or not to skip the validation step after emitting
        SPIRV.
        """

    @skip_spirv_validation.setter
    def skip_spirv_validation(self, arg: bool, /) -> None: ...

    @property
    def floating_point_mode(self) -> SlangFloatingPointMode:
        """Specifies the floating point mode."""

    @floating_point_mode.setter
    def floating_point_mode(self, arg: SlangFloatingPointMode, /) -> None: ...

    @property
    def debug_info(self) -> SlangDebugInfoLevel:
        """
        Specifies the level of debug information to include in the generated
        code.
        """

    @debug_info.setter
    def debug_info(self, arg: SlangDebugInfoLevel, /) -> None: ...

    @property
    def optimization(self) -> SlangOptimizationLevel:
        """Specifies the optimization level."""

    @optimization.setter
    def optimization(self, arg: SlangOptimizationLevel, /) -> None: ...

    @property
    def downstream_args(self) -> list[str]:
        """
        Specifies a list of additional arguments to be passed to the
        downstream compiler.
        """

    @downstream_args.setter
    def downstream_args(self, arg: Sequence[str], /) -> None: ...

    @property
    def dump_intermediates(self) -> bool:
        """When set will dump the intermediate source output."""

    @dump_intermediates.setter
    def dump_intermediates(self, arg: bool, /) -> None: ...

    @property
    def dump_intermediates_prefix(self) -> str:
        """The file name prefix for the intermediate source output."""

    @dump_intermediates_prefix.setter
    def dump_intermediates_prefix(self, arg: str, /) -> None: ...

SlangCompilerOptionsDict = TypedDict("SlangCompilerOptionsDict", {
    "include_paths": Sequence[str | os.PathLike],
    "defines": Mapping[str, str],
    "shader_model": ShaderModel,
    "matrix_layout": SlangMatrixLayout,
    "enable_warnings": Sequence[str],
    "disable_warnings": Sequence[str],
    "warnings_as_errors": Sequence[str],
    "report_downstream_time": bool,
    "report_perf_benchmark": bool,
    "skip_spirv_validation": bool,
    "floating_point_mode": SlangFloatingPointMode,
    "debug_info": SlangDebugInfoLevel,
    "optimization": SlangOptimizationLevel,
    "downstream_args": Sequence[str],
    "dump_intermediates": bool,
    "dump_intermediates_prefix": str
}, total = False)

SlangCompilerOptionsParam = Union[SlangCompilerOptions, SlangCompilerOptionsDict]

class SlangDebugInfoLevel(enum.Enum):
    none = 0

    minimal = 1

    standard = 2

    maximal = 3

class SlangEntryPoint(Object):
    @property
    def name(self) -> str: ...

    @property
    def stage(self) -> ShaderStage: ...

    @property
    def layout(self) -> EntryPointLayout: ...

    def rename(self, new_name: str) -> SlangEntryPoint: ...

    def with_name(self, new_name: str) -> SlangEntryPoint:
        """Returns a copy of the entry point with a new name."""

class SlangFloatingPointMode(enum.Enum):
    default = 0

    fast = 1

    precise = 2

class SlangLinkOptions:
    """
    Slang link options. These can optionally be set when linking a shader
    program.
    """

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def floating_point_mode(self) -> SlangFloatingPointMode | None:
        """Specifies the floating point mode."""

    @floating_point_mode.setter
    def floating_point_mode(self, arg: SlangFloatingPointMode, /) -> None: ...

    @property
    def debug_info(self) -> SlangDebugInfoLevel | None:
        """
        Specifies the level of debug information to include in the generated
        code.
        """

    @debug_info.setter
    def debug_info(self, arg: SlangDebugInfoLevel, /) -> None: ...

    @property
    def optimization(self) -> SlangOptimizationLevel | None:
        """Specifies the optimization level."""

    @optimization.setter
    def optimization(self, arg: SlangOptimizationLevel, /) -> None: ...

    @property
    def downstream_args(self) -> list[str] | None:
        """
        Specifies a list of additional arguments to be passed to the
        downstream compiler.
        """

    @downstream_args.setter
    def downstream_args(self, arg: Sequence[str], /) -> None: ...

    @property
    def dump_intermediates(self) -> bool | None:
        """When set will dump the intermediate source output."""

    @dump_intermediates.setter
    def dump_intermediates(self, arg: bool, /) -> None: ...

    @property
    def dump_intermediates_prefix(self) -> str | None:
        """The file name prefix for the intermediate source output."""

    @dump_intermediates_prefix.setter
    def dump_intermediates_prefix(self, arg: str, /) -> None: ...

SlangLinkOptionsDict = TypedDict("SlangLinkOptionsDict", {
    "floating_point_mode": SlangFloatingPointMode,
    "debug_info": SlangDebugInfoLevel,
    "optimization": SlangOptimizationLevel,
    "downstream_args": Sequence[str],
    "dump_intermediates": bool,
    "dump_intermediates_prefix": str
}, total = False)

SlangLinkOptionsParam = Union[SlangLinkOptions, SlangLinkOptionsDict]

class SlangMatrixLayout(enum.Enum):
    row_major = 1

    column_major = 2

class SlangModule(Object):
    @property
    def session(self) -> SlangSession:
        """The session from which this module was built."""

    @property
    def name(self) -> str:
        """Module name."""

    @property
    def path(self) -> pathlib.Path:
        """
        Module source path. This can be empty if the module was generated from
        a string.
        """

    @property
    def layout(self) -> ProgramLayout: ...

    @property
    def entry_points(self) -> list[SlangEntryPoint]:
        """Build and return vector of all current entry points in the module."""

    @property
    def module_decl(self) -> DeclReflection:
        """Get root decl ref for this module"""

    def entry_point(self, name: str, type_conformances: Sequence[TypeConformance] = []) -> SlangEntryPoint:
        """Get an entry point, optionally applying type conformances to it."""

class SlangOptimizationLevel(enum.Enum):
    none = 0

    default = 1

    high = 2

    maximal = 3

class SlangSession(Object):
    """A slang session, used to load modules and link programs."""

    @property
    def device(self) -> Device: ...

    @property
    def desc(self) -> SlangSessionDesc: ...

    def load_module(self, module_name: str) -> SlangModule:
        """Load a module by name."""

    def load_module_from_source(self, module_name: str, source: str, path: str | os.PathLike | None = None) -> SlangModule:
        """Load a module from string source code."""

    def link_program(self, modules: Sequence[SlangModule], entry_points: Sequence[SlangEntryPoint], link_options: SlangLinkOptionsParam | None = None) -> ShaderProgram:
        """Link a program with a set of modules and entry points."""

    def load_program(self, module_name: str, entry_point_names: Sequence[str], additional_source: str | None = None, link_options: SlangLinkOptionsParam | None = None) -> ShaderProgram:
        """
        Load a program from a given module with a set of entry points.
        Internally this simply wraps link_program without requiring the user
        to explicitly load modules.
        """

    def load_source(self, module_name: str) -> str:
        """Load the source code for a given module."""

class SlangSessionDesc:
    """Descriptor for slang session initialization."""

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def compiler_options(self) -> SlangCompilerOptions: ...

    @compiler_options.setter
    def compiler_options(self, arg: SlangCompilerOptionsParam, /) -> None: ...

    @property
    def add_default_include_paths(self) -> bool: ...

    @add_default_include_paths.setter
    def add_default_include_paths(self, arg: bool, /) -> None: ...

    @property
    def cache_path(self) -> pathlib.Path | None: ...

    @cache_path.setter
    def cache_path(self, arg: str | os.PathLike, /) -> None: ...

SlangSessionDescDict = TypedDict("SlangSessionDescDict", {
    "compiler_options": SlangCompilerOptionsParam,
    "add_default_include_paths": bool,
    "cache_path": str | os.PathLike
}, total = False)

SlangSessionDescParam = Union[SlangSessionDesc, SlangSessionDescDict]

class StencilOp(enum.Enum):
    keep = 0

    zero = 0

    replace = 0

    increment_saturate = 0

    decrement_saturate = 0

    invert = 0

    increment_wrap = 0

    decrement_wrap = 0

class Struct(Object):
    """
    Structured data definition.

    This class is used to describe a structured data type layout. It is
    used by the StructConverter class to convert between different
    layouts.
    """

    def __init__(self, pack: bool = False, byte_order: Struct.ByteOrder = Struct.ByteOrder.host) -> None:
        """
        Constructor.

        Parameter ``pack``:
            If true, the struct will be packed.

        Parameter ``byte_order``:
            Byte order of the struct.
        """

    class Type(enum.Enum):
        """Struct field type."""

        int8 = 0

        int16 = 1

        int32 = 2

        int64 = 3

        uint8 = 4

        uint16 = 5

        uint32 = 6

        uint64 = 7

        float16 = 8

        float32 = 9

        float64 = 10

    class Flags(enum.IntFlag):
        """Struct field flags."""

        none = 0

        normalized = 1

        srgb_gamma = 2

        default = 4

    class ByteOrder(enum.Enum):
        """Byte order."""

        little_endian = 0

        big_endian = 1

        host = 2

    class Field:
        """Struct field."""

        @property
        def name(self) -> str:
            """Name of the field."""

        @name.setter
        def name(self, arg: str, /) -> None: ...

        @property
        def type(self) -> Struct.Type:
            """Type of the field."""

        @type.setter
        def type(self, arg: Struct.Type, /) -> None: ...

        @property
        def flags(self) -> Struct.Flags:
            """Field flags."""

        @flags.setter
        def flags(self, arg: Struct.Flags, /) -> None: ...

        @property
        def size(self) -> int:
            """Size of the field in bytes."""

        @size.setter
        def size(self, arg: int, /) -> None: ...

        @property
        def offset(self) -> int:
            """Offset of the field in bytes."""

        @offset.setter
        def offset(self, arg: int, /) -> None: ...

        @property
        def default_value(self) -> float:
            """Default value."""

        @default_value.setter
        def default_value(self, arg: float, /) -> None: ...

        def is_integer(self) -> bool:
            """Check if the field is an integer type."""

        def is_unsigned(self) -> bool:
            """Check if the field is an unsigned type."""

        def is_signed(self) -> bool:
            """Check if the field is a signed type."""

        def is_float(self) -> bool:
            """Check if the field is a floating point type."""

        def __eq__(self, arg: Struct.Field, /) -> bool: ...

        def __ne__(self, arg: Struct.Field, /) -> bool: ...

        def __repr__(self) -> str: ...

    @overload
    def append(self, field: Struct.Field) -> Struct:
        """Append a field to the struct."""

    @overload
    def append(self, name: str, type: Struct.Type, flags: Struct.Flags = Flags.none, default_value: float = 0.0, blend: Sequence[tuple[float, str]] = []) -> Struct:
        """
        Append a field to the struct.

        Parameter ``name``:
            Name of the field.

        Parameter ``type``:
            Type of the field.

        Parameter ``flags``:
            Field flags.

        Parameter ``default_value``:
            Default value.

        Parameter ``blend``:
            List of blend weights/names.

        Returns:
            Reference to the struct.
        """

    def has_field(self, name: str) -> bool:
        """Check if a field with the specified name exists."""

    def field(self, name: str) -> Struct.Field:
        """Access field by name. Throws if field is not found."""

    def __getitem__(self, arg: int, /) -> Struct.Field: ...

    def __len__(self) -> int: ...

    def __eq__(self, arg: Struct, /) -> bool: ...

    def __ne__(self, arg: Struct, /) -> bool: ...

    @property
    def size(self) -> int:
        """The size of the struct in bytes (with padding)."""

    @property
    def alignment(self) -> int:
        """The alignment of the struct in bytes."""

    @property
    def byte_order(self) -> Struct.ByteOrder:
        """The byte order of the struct."""

    @staticmethod
    def type_size(arg: Struct.Type, /) -> int:
        """Get the size of a type in bytes."""

    @staticmethod
    def type_range(arg: Struct.Type, /) -> tuple[float, float]:
        """Get the numeric range of a type."""

    @staticmethod
    def is_integer(arg: Struct.Type, /) -> bool:
        """Check if ``type`` is an integer type."""

    @staticmethod
    def is_unsigned(arg: Struct.Type, /) -> bool:
        """Check if ``type`` is an unsigned type."""

    @staticmethod
    def is_signed(arg: Struct.Type, /) -> bool:
        """Check if ``type`` is a signed type."""

    @staticmethod
    def is_float(arg: Struct.Type, /) -> bool:
        """Check if ``type`` is a floating point type."""

class StructConverter(Object):
    """
    Struct converter.

    This helper class can be used to convert between structs with
    different layouts.
    """

    def __init__(self, src: Struct, dst: Struct) -> None:
        """
        Constructor.

        Parameter ``src``:
            Source struct definition.

        Parameter ``dst``:
            Destination struct definition.
        """

    @property
    def src(self) -> Struct:
        """The source struct definition."""

    @property
    def dst(self) -> Struct:
        """The destination struct definition."""

    def convert(self, input: bytes) -> bytes: ...

class SubresourceLayout:
    @property
    def row_pitch(self) -> int:
        """Size of a single row in bytes (unaligned)."""

    @property
    def row_pitch_aligned(self) -> int:
        """Size of a single row in bytes (aligned to device texture alignment)."""

    @property
    def row_count(self) -> int:
        """Number of rows."""

    @property
    def depth(self) -> int:
        """Number of depth slices."""

    @property
    def total_size(self) -> int:
        """Get the total size of the subresource in bytes (unaligned)."""

    @property
    def total_size_aligned(self) -> int:
        """
        Get the total size of the subresource in bytes (aligned to device
        texture alignment).
        """

class SubresourceRange:
    def __init__(self) -> None: ...

    @property
    def texture_aspect(self) -> TextureAspect:
        """N/A"""

    @property
    def mip_level(self) -> int:
        """N/A"""

    @property
    def mip_count(self) -> int:
        """N/A"""

    @property
    def base_array_layer(self) -> int:
        """N/A"""

    @property
    def layer_count(self) -> int:
        """N/A"""

    def __repr__(self) -> str:
        """N/A"""

class Swapchain(Object):
    @property
    def desc(self) -> SwapchainDesc:
        """Returns the swapchain description."""

    @property
    def images(self) -> list[Texture]:
        """Returns the back buffer images."""

    def get_image(self, index: int) -> Texture:
        """Returns the back buffer image at position `index`."""

    def present(self) -> None:
        """Present the next image in the swapchain."""

    def acquire_next_image(self) -> int:
        """
        Returns the index of next back buffer image that will be presented in
        the next `present` call. Returns -1 if no image is available and the
        caller should skip the frame.
        """

    def resize(self, width: int, height: int) -> None:
        """
        Resizes the back buffers of this swapchain. All render target views
        and framebuffers referencing the back buffer images must be freed
        before calling this method.
        """

    def is_occluded(self) -> bool:
        """Returns true if the window is occluded."""

    @property
    def fullscreen_mode(self) -> bool: ...

    @fullscreen_mode.setter
    def fullscreen_mode(self, arg: bool, /) -> None: ...

class SwapchainDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def format(self) -> Format:
        """Format of the swapchain images."""

    @format.setter
    def format(self, arg: Format, /) -> None: ...

    @property
    def width(self) -> int:
        """Width of the swapchain images in pixels."""

    @width.setter
    def width(self, arg: int, /) -> None: ...

    @property
    def height(self) -> int:
        """Height of the swapchain images in pixels."""

    @height.setter
    def height(self, arg: int, /) -> None: ...

    @property
    def image_count(self) -> int:
        """Number of swapchain images."""

    @image_count.setter
    def image_count(self, arg: int, /) -> None: ...

    @property
    def enable_vsync(self) -> bool:
        """Enable/disable vertical synchronization."""

    @enable_vsync.setter
    def enable_vsync(self, arg: bool, /) -> None: ...

SwapchainDescDict = TypedDict("SwapchainDescDict", {
    "format": Format,
    "width": int,
    "height": int,
    "image_count": int,
    "enable_vsync": bool
}, total = False)

SwapchainDescParam = Union[SwapchainDesc, SwapchainDescDict]

class TargetBlendDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def color(self) -> AspectBlendDesc: ...

    @color.setter
    def color(self, arg: AspectBlendDescParam, /) -> None: ...

    @property
    def alpha(self) -> AspectBlendDesc: ...

    @alpha.setter
    def alpha(self, arg: AspectBlendDescParam, /) -> None: ...

    @property
    def enable_blend(self) -> bool: ...

    @enable_blend.setter
    def enable_blend(self, arg: bool, /) -> None: ...

    @property
    def logic_op(self) -> LogicOp: ...

    @logic_op.setter
    def logic_op(self, arg: LogicOp, /) -> None: ...

    @property
    def write_mask(self) -> RenderTargetWriteMask: ...

    @write_mask.setter
    def write_mask(self, arg: RenderTargetWriteMask, /) -> None: ...

TargetBlendDescDict = TypedDict("TargetBlendDescDict", {
    "color": AspectBlendDescParam,
    "alpha": AspectBlendDescParam,
    "enable_blend": bool,
    "logic_op": LogicOp,
    "write_mask": RenderTargetWriteMask
}, total = False)

TargetBlendDescParam = Union[TargetBlendDesc, TargetBlendDescDict]

class Texture(Resource):
    @property
    def desc(self) -> TextureDesc: ...

    @property
    def width(self) -> int: ...

    @property
    def height(self) -> int: ...

    @property
    def depth(self) -> int: ...

    @property
    def array_size(self) -> int: ...

    @property
    def mip_count(self) -> int: ...

    @property
    def subresource_count(self) -> int: ...

    def get_subresource_index(self, mip_level: int, array_slice: int = 0) -> int: ...

    def get_subresource_array_slice(self, subresource: int) -> int: ...

    def get_subresource_mip_level(self, subresource: int) -> int: ...

    def get_mip_width(self, mip_level: int = 0) -> int: ...

    def get_mip_height(self, mip_level: int = 0) -> int: ...

    def get_mip_depth(self, mip_level: int = 0) -> int: ...

    def get_mip_dimensions(self, mip_level: int = 0) -> math.uint3: ...

    def get_subresource_layout(self, subresource: int) -> SubresourceLayout: ...

    def get_srv(self, mip_level: int = 0, mip_count: int = 4294967295, base_array_layer: int = 0, layer_count: int = 4294967295) -> ResourceView:
        """Get a shader resource view for a subresource range of the texture."""

    def get_uav(self, mip_level: int = 0, base_array_layer: int = 0, layer_count: int = 4294967295) -> ResourceView:
        r"""
        Get a unordered access view for a subresource range of the texture.
        \note Only a single mip level can be bound.
        """

    def get_dsv(self, mip_level: int = 0, base_array_layer: int = 0, layer_count: int = 4294967295) -> ResourceView:
        r"""
        Get a depth stencil view for a subresource range of the texture. \note
        Only a single mip level can be bound.
        """

    def get_rtv(self, mip_level: int = 0, base_array_layer: int = 0, layer_count: int = 4294967295) -> ResourceView:
        r"""
        Get a render target view for a subresource range of the texture. \note
        Only a single mip level can be bound.
        """

    def to_bitmap(self, mip_level: int = 0, array_slice: int = 0) -> Bitmap: ...

    def to_numpy(self, mip_level: int = 0, array_slice: int = 0) -> NDArray: ...

    def from_numpy(self, data: ArrayLike, mip_level: int = 0, array_slice: int = 0) -> None: ...

class TextureAddressingMode(enum.Enum):
    wrap = 0

    clamp_to_edge = 1

    clamp_to_border = 2

    mirror_repeat = 3

    mirror_once = 4

class TextureAspect(enum.Enum):
    color = 1

    depth = 2

    stencil = 4

    meta_data = 8

    plane0 = 16

    plane1 = 32

    plane2 = 64

    depth_stencil = 6

class TextureDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def type(self) -> ResourceType:
        """
        Resource type (optional). Type is inferred from width, height, depth
        if not specified.
        """

    @type.setter
    def type(self, arg: ResourceType, /) -> None: ...

    @property
    def format(self) -> Format:
        """Texture format."""

    @format.setter
    def format(self, arg: Format, /) -> None: ...

    @property
    def width(self) -> int:
        """Width in pixels."""

    @width.setter
    def width(self, arg: int, /) -> None: ...

    @property
    def height(self) -> int:
        """Height in pixels."""

    @height.setter
    def height(self, arg: int, /) -> None: ...

    @property
    def depth(self) -> int:
        """Depth in pixels."""

    @depth.setter
    def depth(self, arg: int, /) -> None: ...

    @property
    def array_size(self) -> int:
        """Number of array slices (1 for non-array textures)."""

    @array_size.setter
    def array_size(self, arg: int, /) -> None: ...

    @property
    def mip_count(self) -> int:
        """Number of mip levels (0 for auto-generated mips)."""

    @mip_count.setter
    def mip_count(self, arg: int, /) -> None: ...

    @property
    def sample_count(self) -> int:
        """Number of samples per pixel (1 for non-multisampled textures)."""

    @sample_count.setter
    def sample_count(self, arg: int, /) -> None: ...

    @property
    def quality(self) -> int:
        """Quality level for multisampled textures."""

    @quality.setter
    def quality(self, arg: int, /) -> None: ...

    @property
    def initial_state(self) -> ResourceState: ...

    @initial_state.setter
    def initial_state(self, arg: ResourceState, /) -> None: ...

    @property
    def usage(self) -> ResourceUsage: ...

    @usage.setter
    def usage(self, arg: ResourceUsage, /) -> None: ...

    @property
    def memory_type(self) -> MemoryType: ...

    @memory_type.setter
    def memory_type(self, arg: MemoryType, /) -> None: ...

    @property
    def debug_name(self) -> str: ...

    @debug_name.setter
    def debug_name(self, arg: str, /) -> None: ...

TextureDescDict = TypedDict("TextureDescDict", {
    "type": ResourceType,
    "format": Format,
    "width": int,
    "height": int,
    "depth": int,
    "array_size": int,
    "mip_count": int,
    "sample_count": int,
    "quality": int,
    "initial_state": ResourceState,
    "usage": ResourceUsage,
    "memory_type": MemoryType,
    "debug_name": str
}, total = False)

TextureDescParam = Union[TextureDesc, TextureDescDict]

class TextureFilteringMode(enum.Enum):
    point = 0

    linear = 1

class TextureLoader(Object):
    """Utility class for loading textures from bitmaps and image files."""

    def __init__(self, device: Device) -> None: ...

    class Options:
        @overload
        def __init__(self) -> None: ...

        @overload
        def __init__(self, arg: dict, /) -> None: ...

        @property
        def load_as_normalized(self) -> bool:
            """Load 8/16-bit integer data as normalized resource format."""

        @load_as_normalized.setter
        def load_as_normalized(self, arg: bool, /) -> None: ...

        @property
        def load_as_srgb(self) -> bool:
            """
            Use ``Format::rgba8_unorm_srgb`` format if bitmap is 8-bit RGBA with
            sRGB gamma.
            """

        @load_as_srgb.setter
        def load_as_srgb(self, arg: bool, /) -> None: ...

        @property
        def extend_alpha(self) -> bool:
            """Extend RGB to RGBA if RGB texture format is not available."""

        @extend_alpha.setter
        def extend_alpha(self, arg: bool, /) -> None: ...

        @property
        def allocate_mips(self) -> bool:
            """Allocate mip levels for the texture."""

        @allocate_mips.setter
        def allocate_mips(self, arg: bool, /) -> None: ...

        @property
        def generate_mips(self) -> bool:
            """Generate mip levels for the texture."""

        @generate_mips.setter
        def generate_mips(self, arg: bool, /) -> None: ...

        @property
        def usage(self) -> ResourceUsage: ...

        @usage.setter
        def usage(self, arg: ResourceUsage, /) -> None: ...

    OptionsDict = TypedDict("OptionsDict", {
        "load_as_normalized": bool,
        "load_as_srgb": bool,
        "extend_alpha": bool,
        "allocate_mips": bool,
        "generate_mips": bool,
        "usage": ResourceUsage
    }, total = False)

    OptionsParam = Union[Options, OptionsDict]

    @overload
    def load_texture(self, bitmap: Bitmap, options: TextureLoader.OptionsParam | None = None) -> Texture:
        """
        Load a texture from a bitmap.

        Parameter ``bitmap``:
            Bitmap to load.

        Parameter ``options``:
            Texture loading options.

        Returns:
            New texture object.
        """

    @overload
    def load_texture(self, path: str | os.PathLike, options: TextureLoader.OptionsParam | None = None) -> Texture:
        """
        Load a texture from an image file.

        Parameter ``path``:
            Image file path.

        Parameter ``options``:
            Texture loading options.

        Returns:
            New texture object.
        """

    @overload
    def load_textures(self, bitmaps: Sequence[Bitmap], options: TextureLoader.OptionsParam | None = None) -> list[Texture]:
        """
        Load textures from a list of bitmaps.

        Parameter ``bitmaps``:
            Bitmaps to load.

        Parameter ``options``:
            Texture loading options.

        Returns:
            List of new of texture objects.
        """

    @overload
    def load_textures(self, paths: Sequence[str | os.PathLike], options: TextureLoader.OptionsParam | None = None) -> list[Texture]:
        """
        Load textures from a list of image files.

        Parameter ``paths``:
            Image file paths.

        Parameter ``options``:
            Texture loading options.

        Returns:
            List of new texture objects.
        """

    @overload
    def load_texture_array(self, bitmaps: Sequence[Bitmap], options: TextureLoader.OptionsParam | None = None) -> Texture:
        """
        Load a texture array from a list of bitmaps.

        All bitmaps need to have the same format and dimensions.

        Parameter ``bitmaps``:
            Bitmaps to load.

        Parameter ``options``:
            Texture loading options.

        Returns:
            New texture array object.
        """

    @overload
    def load_texture_array(self, paths: Sequence[str | os.PathLike], options: TextureLoader.OptionsParam | None = None) -> Texture:
        """
        Load a texture array from a list of image files.

        All images need to have the same format and dimensions.

        Parameter ``paths``:
            Image file paths.

        Parameter ``options``:
            Texture loading options.

        Returns:
            New texture array object.
        """

class TextureReductionOp(enum.Enum):
    average = 0

    comparison = 1

    minimum = 2

    maximum = 3

class Timer:
    """High resolution CPU timer."""

    def __init__(self) -> None: ...

    def reset(self) -> None:
        """Reset the timer."""

    def elapsed_s(self) -> float:
        """Elapsed seconds since last reset."""

    def elapsed_ms(self) -> float:
        """Elapsed milliseconds since last reset."""

    def elapsed_us(self) -> float:
        """Elapsed microseconds since last reset."""

    def elapsed_ns(self) -> float:
        """Elapsed nanoseconds since last reset."""

    @staticmethod
    def delta_s(start: int, end: int) -> float:
        """Compute elapsed seconds between two time points."""

    @staticmethod
    def delta_ms(start: int, end: int) -> float:
        """Compute elapsed milliseconds between two time points."""

    @staticmethod
    def delta_us(start: int, end: int) -> float:
        """Compute elapsed microseconds between two time points."""

    @staticmethod
    def delta_ns(start: int, end: int) -> float:
        """Compute elapsed nanoseconds between two time points."""

    @staticmethod
    def now() -> int:
        """Current time point in nanoseconds since epoch."""

class TransientShaderObject(ShaderObject):
    pass

class TypeConformance:
    """
    Type conformance entry. Type conformances are used to narrow the set
    of types supported by a slang interface. They can be specified on an
    entry point to omit generating code for types that do not conform.
    """

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, type_name: str, interface_name: str, id: int = -1) -> None: ...

    @overload
    def __init__(self, arg: tuple, /) -> None: ...

    @property
    def interface_name(self) -> str:
        """Name of the interface."""

    @interface_name.setter
    def interface_name(self, arg: str, /) -> None: ...

    @property
    def type_name(self) -> str:
        """Name of the concrete type."""

    @type_name.setter
    def type_name(self, arg: str, /) -> None: ...

    @property
    def id(self) -> int:
        """Unique id per type for an interface (optional)."""

    @id.setter
    def id(self, arg: int, /) -> None: ...

    def __repr__(self) -> str: ...

class TypeLayoutReflection(BaseReflectionObject):
    @property
    def kind(self) -> TypeReflection.Kind: ...

    @property
    def name(self) -> str: ...

    @property
    def size(self) -> int: ...

    @property
    def stride(self) -> int: ...

    @property
    def alignment(self) -> int: ...

    @property
    def type(self) -> TypeReflection: ...

    @property
    def fields(self) -> TypeLayoutReflectionFieldList: ...

    @property
    def element_type_layout(self) -> TypeLayoutReflection: ...

    def unwrap_array(self) -> TypeLayoutReflection: ...

    def __repr__(self) -> str: ...

class TypeLayoutReflectionFieldList:
    """TypeLayoutReflection lazy field list evaluation."""

    def __len__(self) -> int: ...

    def __getitem__(self, arg: int, /) -> VariableLayoutReflection: ...

class TypeReflection(BaseReflectionObject):
    class Kind(enum.Enum):
        none = 0

        struct = 1

        array = 2

        matrix = 3

        vector = 4

        scalar = 5

        constant_buffer = 6

        resource = 7

        sampler_state = 8

        texture_buffer = 9

        shader_storage_buffer = 10

        parameter_block = 11

        generic_type_parameter = 12

        interface = 13

        output_stream = 14

        specialized = 16

        feedback = 17

        pointer = 18

    class ScalarType(enum.Enum):
        none = 0

        void = 1

        bool = 2

        int32 = 3

        uint32 = 4

        int64 = 5

        uint64 = 6

        float16 = 7

        float32 = 8

        float64 = 9

        int8 = 10

        uint8 = 11

        int16 = 12

        uint16 = 13

    class ResourceShape(enum.Enum):
        none = 0

        texture_1d = 1

        texture_2d = 2

        texture_3d = 3

        texture_cube = 4

        texture_buffer = 5

        structured_buffer = 6

        byte_address_buffer = 7

        unknown = 8

        acceleration_structure = 9

        texture_feedback_flag = 16

        texture_array_flag = 64

        texture_multisample_flag = 128

        texture_1d_array = 65

        texture_2d_array = 66

        texture_cube_array = 68

        texture_2d_multisample = 130

        texture_2d_multisample_array = 194

    class ResourceAccess(enum.Enum):
        none = 0

        read = 1

        read_write = 2

        raster_ordered = 3

        access_append = 4

        access_consume = 5

        access_write = 6

    class ParameterCategory(enum.Enum):
        none = 0

        mixed = 1

        constant_buffer = 2

        shader_resource = 3

        unordered_access = 4

        varying_input = 5

        varying_output = 6

        sampler_state = 7

        uniform = 8

        descriptor_table_slot = 9

        specialization_constant = 10

        push_constant_buffer = 11

        register_space = 12

        generic = 13

        ray_payload = 14

        hit_attributes = 15

        callable_payload = 16

        shader_record = 17

        existential_type_param = 18

        existential_object_param = 19

    @property
    def kind(self) -> TypeReflection.Kind: ...

    @property
    def name(self) -> str: ...

    @property
    def full_name(self) -> str:
        """N/A"""

    @property
    def fields(self) -> TypeReflectionFieldList: ...

    @property
    def element_count(self) -> int: ...

    @property
    def element_type(self) -> TypeReflection: ...

    @property
    def row_count(self) -> int: ...

    @property
    def col_count(self) -> int: ...

    @property
    def scalar_type(self) -> TypeReflection.ScalarType: ...

    @property
    def resource_result_type(self) -> TypeReflection: ...

    @property
    def resource_shape(self) -> TypeReflection.ResourceShape: ...

    @property
    def resource_access(self) -> TypeReflection.ResourceAccess: ...

    def unwrap_array(self) -> TypeReflection: ...

    def __repr__(self) -> str: ...

class TypeReflectionFieldList:
    """TypeReflection lazy field list evaluation."""

    def __len__(self) -> int: ...

    def __getitem__(self, arg: int, /) -> VariableReflection: ...

class VariableLayoutReflection(BaseReflectionObject):
    @property
    def name(self) -> str: ...

    @property
    def variable(self) -> VariableReflection: ...

    @property
    def type_layout(self) -> TypeLayoutReflection: ...

    @property
    def offset(self) -> int: ...

    def __repr__(self) -> str: ...

class VariableReflection(BaseReflectionObject):
    @property
    def name(self) -> str:
        """Variable name."""

    @property
    def type(self) -> TypeReflection:
        """Variable type reflection."""

    def has_modifier(self, modifier: ModifierID) -> bool:
        """Check if variable has a given modifier (e.g. 'inout')."""

class VertexStreamDesc:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def stride(self) -> int:
        """The stride in bytes for this vertex stream."""

    @stride.setter
    def stride(self, arg: int, /) -> None: ...

    @property
    def slot_class(self) -> InputSlotClass:
        """Whether the stream contains per-vertex or per-instance data."""

    @slot_class.setter
    def slot_class(self, arg: InputSlotClass, /) -> None: ...

    @property
    def instance_data_step_rate(self) -> int:
        """How many instances to draw per chunk of data."""

    @instance_data_step_rate.setter
    def instance_data_step_rate(self, arg: int, /) -> None: ...

VertexStreamDescDict = TypedDict("VertexStreamDescDict", {
    "stride": int,
    "slot_class": InputSlotClass,
    "instance_data_step_rate": int
}, total = False)

VertexStreamDescParam = Union[VertexStreamDesc, VertexStreamDescDict]

class Viewport:
    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, arg: dict, /) -> None: ...

    @property
    def x(self) -> float: ...

    @x.setter
    def x(self, arg: float, /) -> None: ...

    @property
    def y(self) -> float: ...

    @y.setter
    def y(self, arg: float, /) -> None: ...

    @property
    def width(self) -> float: ...

    @width.setter
    def width(self, arg: float, /) -> None: ...

    @property
    def height(self) -> float: ...

    @height.setter
    def height(self, arg: float, /) -> None: ...

    @property
    def min_depth(self) -> float: ...

    @min_depth.setter
    def min_depth(self, arg: float, /) -> None: ...

    @property
    def max_depth(self) -> float: ...

    @max_depth.setter
    def max_depth(self, arg: float, /) -> None: ...

ViewportDict = TypedDict("ViewportDict", {
    "x": float,
    "y": float,
    "width": float,
    "height": float,
    "min_depth": float,
    "max_depth": float
}, total = False)

ViewportParam = Union[Viewport, ViewportDict]

class Window(Object):
    """
    Window class.

    Platform independent class for managing a window and handle input
    events.
    """

    def __init__(self, width: int = 1024, height: int = 1024, title: str = 'sgl', mode: WindowMode = WindowMode.normal, resizable: bool = True) -> None:
        """
        Constructor.

        Parameter ``width``:
            Width of the window in pixels.

        Parameter ``height``:
            Height of the window in pixels.

        Parameter ``title``:
            Title of the window.

        Parameter ``mode``:
            Window mode.

        Parameter ``resizable``:
            Whether the window is resizable.
        """

    @property
    def width(self) -> int:
        """The width of the window in pixels."""

    @property
    def height(self) -> int:
        """The height of the window in pixels."""

    def resize(self, width: int, height: int) -> None:
        """
        Resize the window.

        Parameter ``width``:
            The new width of the window in pixels.

        Parameter ``height``:
            The new height of the window in pixels.
        """

    @property
    def title(self) -> str:
        """The title of the window."""

    @title.setter
    def title(self, arg: str, /) -> None: ...

    def close(self) -> None:
        """Close the window."""

    def should_close(self) -> bool:
        """True if the window should be closed."""

    def process_events(self) -> None:
        """Process any pending events."""

    def set_clipboard(self, text: str) -> None:
        """Set the clipboard content."""

    def get_clipboard(self) -> str | None:
        """Get the clipboard content."""

    @property
    def on_resize(self) -> Callable[[int, int], None]:
        """Event handler to be called when the window is resized."""

    @on_resize.setter
    def on_resize(self, arg: Callable[[int, int], None] | None) -> None: ...

    @property
    def on_keyboard_event(self) -> Callable[[KeyboardEvent], None]:
        """Event handler to be called when a keyboard event occurs."""

    @on_keyboard_event.setter
    def on_keyboard_event(self, arg: Callable[[KeyboardEvent], None] | None) -> None: ...

    @property
    def on_mouse_event(self) -> Callable[[MouseEvent], None]:
        """Event handler to be called when a mouse event occurs."""

    @on_mouse_event.setter
    def on_mouse_event(self, arg: Callable[[MouseEvent], None] | None) -> None: ...

    @property
    def on_gamepad_event(self) -> Callable[[GamepadEvent], None]:
        """Event handler to be called when a gamepad event occurs."""

    @on_gamepad_event.setter
    def on_gamepad_event(self, arg: Callable[[GamepadEvent], None] | None) -> None: ...

    @property
    def on_gamepad_state(self) -> Callable[[GamepadState], None]:
        """Event handler to be called when the gamepad state changes."""

    @on_gamepad_state.setter
    def on_gamepad_state(self, arg: Callable[[GamepadState], None] | None) -> None: ...

    @property
    def on_drop_files(self) -> Callable[[list[str]], None]:
        """Event handler to be called when files are dropped onto the window."""

    @on_drop_files.setter
    def on_drop_files(self, arg: Callable[[Sequence[str]], None] | None) -> None: ...

class WindowHandle:
    """Native window handle."""

    def __init__(self, xdisplay: int, xwindow: int) -> None: ...

class WindowMode(enum.Enum):
    """Window modes."""

    normal = 0

    minimized = 1

    fullscreen = 2

def get_format_info(arg: Format, /) -> FormatInfo: ...

def log(level: LogLevel, msg: str, frequency: LogFrequency = LogFrequency.always) -> None:
    """
    Log a message.

    Parameter ``level``:
        The log level.

    Parameter ``msg``:
        The message.

    Parameter ``frequency``:
        The log frequency.
    """

def log_debug(msg: str) -> None: ...

def log_debug_once(msg: str) -> None: ...

def log_error(msg: str) -> None: ...

def log_error_once(msg: str) -> None: ...

def log_fatal(msg: str) -> None: ...

def log_fatal_once(msg: str) -> None: ...

def log_info(msg: str) -> None: ...

def log_info_once(msg: str) -> None: ...

def log_warn(msg: str) -> None: ...

def log_warn_once(msg: str) -> None: ...
