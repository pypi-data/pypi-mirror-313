import typing
import collections.abc
import typing_extensions
import bpy.ops.transform
import bpy.types
import bpy.typing

def active_frame_delete(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    all: bool | None = False,
):
    """Delete the active Grease Pencil frame(s)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param all: Delete all, Delete active keyframes of all layers
    :type all: bool | None
    """

def bake_grease_pencil_animation(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    frame_start: int | None = 1,
    frame_end: int | None = 250,
    step: int | None = 1,
    only_selected: bool | None = False,
    frame_target: int | None = 1,
    project_type: typing.Literal["KEEP", "FRONT", "SIDE", "TOP", "VIEW", "CURSOR"]
    | None = "KEEP",
):
    """Bake Grease Pencil object transform to Grease Pencil keyframes

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param frame_start: Start Frame, The start frame
        :type frame_start: int | None
        :param frame_end: End Frame, The end frame of animation
        :type frame_end: int | None
        :param step: Step, Step between generated frames
        :type step: int | None
        :param only_selected: Only Selected Keyframes, Convert only selected keyframes
        :type only_selected: bool | None
        :param frame_target: Target Frame, Destination frame
        :type frame_target: int | None
        :param project_type: Projection Type

    KEEP
    No Reproject.

    FRONT
    Front -- Reproject the strokes using the X-Z plane.

    SIDE
    Side -- Reproject the strokes using the Y-Z plane.

    TOP
    Top -- Reproject the strokes using the X-Y plane.

    VIEW
    View -- Reproject the strokes to end up on the same plane, as if drawn from the current viewpoint using 'Cursor' Stroke Placement.

    CURSOR
    Cursor -- Reproject the strokes using the orientation of 3D cursor.
        :type project_type: typing.Literal['KEEP','FRONT','SIDE','TOP','VIEW','CURSOR'] | None
    """

def brush_stroke(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    | None = None,
    mode: typing.Literal["NORMAL", "INVERT", "SMOOTH", "ERASE"] | None = "NORMAL",
    pen_flip: bool | None = False,
):
    """Draw a new stroke in the active Grease Pencil object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param stroke: Stroke
        :type stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement] | None
        :param mode: Stroke Mode, Action taken when a paint stroke is made

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.

    SMOOTH
    Smooth -- Switch brush to smooth mode for duration of stroke.

    ERASE
    Erase -- Switch brush to erase mode for duration of stroke.
        :type mode: typing.Literal['NORMAL','INVERT','SMOOTH','ERASE'] | None
        :param pen_flip: Pen Flip, Whether a tablet's eraser mode is being used
        :type pen_flip: bool | None
    """

def caps_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["ROUND", "FLAT", "START", "END"] | None = "ROUND",
):
    """Change curve caps mode (rounded or flat)

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type

    ROUND
    Rounded -- Set as default rounded.

    FLAT
    Flat.

    START
    Toggle Start.

    END
    Toggle End.
        :type type: typing.Literal['ROUND','FLAT','START','END'] | None
    """

def clean_loose(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    limit: int | None = 1,
):
    """Remove loose points

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param limit: Limit, Number of points to consider stroke as loose
    :type limit: int | None
    """

def copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy the selected Grease Pencil points or strokes to the internal clipboard

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def cyclical_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["CLOSE", "OPEN", "TOGGLE"] | None = "TOGGLE",
):
    """Close or open the selected stroke adding a segment from last to first point

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: typing.Literal['CLOSE','OPEN','TOGGLE'] | None
    """

def delete(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Delete selected strokes or points

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def delete_frame(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["ACTIVE_FRAME", "ALL_FRAMES"] | None = "ACTIVE_FRAME",
):
    """Delete Grease Pencil Frame(s)

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type, Method used for deleting Grease Pencil frames

    ACTIVE_FRAME
    Active Frame -- Deletes current frame in the active layer.

    ALL_FRAMES
    All Active Frames -- Delete active frames for all layers.
        :type type: typing.Literal['ACTIVE_FRAME','ALL_FRAMES'] | None
    """

def dissolve(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["POINTS", "BETWEEN", "UNSELECT"] | None = "POINTS",
):
    """Delete selected points without splitting strokes

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type, Method used for dissolving stroke points

    POINTS
    Dissolve -- Dissolve selected points.

    BETWEEN
    Dissolve Between -- Dissolve points between selected points.

    UNSELECT
    Dissolve Unselect -- Dissolve all unselected points.
        :type type: typing.Literal['POINTS','BETWEEN','UNSELECT'] | None
    """

def duplicate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Duplicate the selected points

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def duplicate_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    GREASE_PENCIL_OT_duplicate: typing.Any | None = None,
    TRANSFORM_OT_translate: bpy.ops.transform.translate | None = None,
):
    """Make copies of the selected Grease Pencil strokes and move them

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param GREASE_PENCIL_OT_duplicate: Duplicate, Duplicate the selected points
    :type GREASE_PENCIL_OT_duplicate: typing.Any | None
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: bpy.ops.transform.translate | None
    """

def extrude(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Extrude the selected points

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def extrude_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    GREASE_PENCIL_OT_extrude: typing.Any | None = None,
    TRANSFORM_OT_translate: bpy.ops.transform.translate | None = None,
):
    """Extrude selected points and move them

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param GREASE_PENCIL_OT_extrude: Extrude Stroke Points, Extrude the selected points
    :type GREASE_PENCIL_OT_extrude: typing.Any | None
    :param TRANSFORM_OT_translate: Move, Move selected items
    :type TRANSFORM_OT_translate: bpy.ops.transform.translate | None
    """

def fill(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    invert: bool | None = False,
    precision: bool | None = False,
):
    """Fill with color the shape formed by strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param invert: Invert, Find boundary of unfilled instead of filled regions
    :type invert: bool | None
    :param precision: Precision, Use precision movement for extension lines
    :type precision: bool | None
    """

def frame_clean_duplicate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    selected: bool | None = False,
):
    """Remove any keyframe that is a duplicate of the previous one

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param selected: Selected, Only delete selected keyframes
    :type selected: bool | None
    """

def frame_duplicate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    all: bool | None = False,
):
    """Make a copy of the active Grease Pencil frame(s)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param all: Duplicate all, Duplicate active keyframes of all layer
    :type all: bool | None
    """

def insert_blank_frame(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    all_layers: bool | None = False,
    duration: int | None = 0,
):
    """Insert a blank frame on the current scene frame

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param all_layers: All Layers, Insert a blank frame in all editable layers
    :type all_layers: bool | None
    :param duration: Duration
    :type duration: int | None
    """

def interpolate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    shift: float | None = 0.0,
    layers: typing.Literal["ACTIVE", "ALL"] | None = "ACTIVE",
    exclude_breakdowns: bool | None = False,
    use_selection: bool | None = False,
    flip: typing.Literal["NONE", "FLIP", "AUTO"] | None = "AUTO",
    smooth_steps: int | None = 1,
    smooth_factor: float | None = 0.0,
):
    """Interpolate Grease Pencil strokes between frames

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param shift: Shift, Bias factor for which frame has more influence on the interpolated strokes
    :type shift: float | None
    :param layers: Layer, Layers included in the interpolation
    :type layers: typing.Literal['ACTIVE','ALL'] | None
    :param exclude_breakdowns: Exclude Breakdowns, Exclude existing Breakdowns keyframes as interpolation extremes
    :type exclude_breakdowns: bool | None
    :param use_selection: Use Selection, Use only selected strokes for interpolating
    :type use_selection: bool | None
    :param flip: Flip Mode, Invert destination stroke to match start and end with source stroke
    :type flip: typing.Literal['NONE','FLIP','AUTO'] | None
    :param smooth_steps: Iterations, Number of times to smooth newly created strokes
    :type smooth_steps: int | None
    :param smooth_factor: Smooth, Amount of smoothing to apply to interpolated strokes, to reduce jitter/noise
    :type smooth_factor: float | None
    """

def interpolate_sequence(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    step: int | None = 1,
    layers: typing.Literal["ACTIVE", "ALL"] | None = "ACTIVE",
    exclude_breakdowns: bool | None = False,
    flip: typing.Literal["NONE", "FLIP", "AUTO"] | None = "AUTO",
    smooth_steps: int | None = 1,
    smooth_factor: float | None = 0.0,
    type: typing.Literal[
        "LINEAR",
        "CUSTOM",
        "SINE",
        "QUAD",
        "CUBIC",
        "QUART",
        "QUINT",
        "EXPO",
        "CIRC",
        "BACK",
        "BOUNCE",
        "ELASTIC",
    ]
    | None = "LINEAR",
    easing: bpy.typing.BeztripleInterpolationEasingItems | None = "EASE_IN",
    back: float | None = 1.702,
    amplitude: float | None = 0.15,
    period: float | None = 0.15,
):
    """Generate 'in-betweens' to smoothly interpolate between Grease Pencil frames

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param step: Step, Number of frames between generated interpolated frames
        :type step: int | None
        :param layers: Layer, Layers included in the interpolation
        :type layers: typing.Literal['ACTIVE','ALL'] | None
        :param exclude_breakdowns: Exclude Breakdowns, Exclude existing Breakdowns keyframes as interpolation extremes
        :type exclude_breakdowns: bool | None
        :param flip: Flip Mode, Invert destination stroke to match start and end with source stroke
        :type flip: typing.Literal['NONE','FLIP','AUTO'] | None
        :param smooth_steps: Iterations, Number of times to smooth newly created strokes
        :type smooth_steps: int | None
        :param smooth_factor: Smooth, Amount of smoothing to apply to interpolated strokes, to reduce jitter/noise
        :type smooth_factor: float | None
        :param type: Type, Interpolation method to use the next time 'Interpolate Sequence' is run

    LINEAR
    Linear -- Straight-line interpolation between A and B (i.e. no ease in/out).

    CUSTOM
    Custom -- Custom interpolation defined using a curve map.

    SINE
    Sinusoidal -- Sinusoidal easing (weakest, almost linear but with a slight curvature).

    QUAD
    Quadratic -- Quadratic easing.

    CUBIC
    Cubic -- Cubic easing.

    QUART
    Quartic -- Quartic easing.

    QUINT
    Quintic -- Quintic easing.

    EXPO
    Exponential -- Exponential easing (dramatic).

    CIRC
    Circular -- Circular easing (strongest and most dynamic).

    BACK
    Back -- Cubic easing with overshoot and settle.

    BOUNCE
    Bounce -- Exponentially decaying parabolic bounce, like when objects collide.

    ELASTIC
    Elastic -- Exponentially decaying sine wave, like an elastic band.
        :type type: typing.Literal['LINEAR','CUSTOM','SINE','QUAD','CUBIC','QUART','QUINT','EXPO','CIRC','BACK','BOUNCE','ELASTIC'] | None
        :param easing: Easing, Which ends of the segment between the preceding and following Grease Pencil frames easing interpolation is applied to
        :type easing: bpy.typing.BeztripleInterpolationEasingItems | None
        :param back: Back, Amount of overshoot for 'back' easing
        :type back: float | None
        :param amplitude: Amplitude, Amount to boost elastic bounces for 'elastic' easing
        :type amplitude: float | None
        :param period: Period, Time between bounces for elastic easing
        :type period: float | None
    """

def join_selection(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["JOINCOPY", "JOIN"] | None = "JOIN",
):
    """New stroke from selected points/strokes

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Type, Defines how the operator will behave on the selection in the active layer

    JOINCOPY
    Join and Copy -- Copy the selection in the new stroke.

    JOIN
    Join -- Move the selection to the new stroke.
        :type type: typing.Literal['JOINCOPY','JOIN'] | None
    """

def layer_active(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    layer: int | None = 0,
):
    """Set the active Grease Pencil layer

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param layer: Grease Pencil Layer
    :type layer: int | None
    """

def layer_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    new_layer_name: str = "Layer",
):
    """Add a new Grease Pencil layer in the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param new_layer_name: Name, Name of the new layer
    :type new_layer_name: str
    """

def layer_duplicate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    empty_keyframes: bool | None = False,
):
    """Make a copy of the active Grease Pencil layer

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param empty_keyframes: Empty Keyframes, Add Empty Keyframes
    :type empty_keyframes: bool | None
    """

def layer_duplicate_object(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    only_active: bool | None = True,
    mode: typing.Literal["ALL", "ACTIVE"] | None = "ALL",
):
    """Make a copy of the active Grease Pencil layer to selected object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param only_active: Only Active, Copy only active Layer, uncheck to append all layers
    :type only_active: bool | None
    :param mode: Mode
    :type mode: typing.Literal['ALL','ACTIVE'] | None
    """

def layer_group_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    new_layer_group_name: str = "",
):
    """Add a new Grease Pencil layer group in the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param new_layer_group_name: Name, Name of the new layer group
    :type new_layer_group_name: str
    """

def layer_group_color_tag(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    color_tag: typing.Literal[
        "NONE",
        "COLOR1",
        "COLOR2",
        "COLOR3",
        "COLOR4",
        "COLOR5",
        "COLOR6",
        "COLOR7",
        "COLOR8",
    ]
    | None = "COLOR1",
):
    """Change layer group icon

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param color_tag: Color Tag
    :type color_tag: typing.Literal['NONE','COLOR1','COLOR2','COLOR3','COLOR4','COLOR5','COLOR6','COLOR7','COLOR8'] | None
    """

def layer_group_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    keep_children: bool | None = False,
):
    """Remove Grease Pencil layer group in the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param keep_children: Keep children nodes, Keep the children nodes of the group and only delete the group itself
    :type keep_children: bool | None
    """

def layer_hide(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    unselected: bool | None = False,
):
    """Hide selected/unselected Grease Pencil layers

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param unselected: Unselected, Hide unselected rather than selected layers
    :type unselected: bool | None
    """

def layer_isolate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    affect_visibility: bool | None = False,
):
    """Make only active layer visible/editable

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param affect_visibility: Affect Visibility, Also affect the visibility
    :type affect_visibility: bool | None
    """

def layer_lock_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    lock: bool | None = True,
):
    """Lock all Grease Pencil layers to prevent them from being accidentally modified

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param lock: Lock Value, Lock/Unlock all layers
    :type lock: bool | None
    """

def layer_mask_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str = "",
):
    """Add new layer as masking

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Layer, Name of the layer
    :type name: str
    """

def layer_mask_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove Layer Mask

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def layer_mask_reorder(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
):
    """Reorder the active Grease Pencil mask layer up/down in the list

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction
    :type direction: typing.Literal['UP','DOWN'] | None
    """

def layer_merge(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["ACTIVE", "GROUP", "ALL"] | None = "ACTIVE",
):
    """Combine layers based on the mode into one layer

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Mode

    ACTIVE
    Active -- Combine the active layer with the layer just below (if it exists).

    GROUP
    Group -- Combine layers in the active group into a single layer.

    ALL
    All -- Combine all layers into a single layer.
        :type mode: typing.Literal['ACTIVE','GROUP','ALL'] | None
    """

def layer_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
):
    """Move the active Grease Pencil layer or Group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction
    :type direction: typing.Literal['UP','DOWN'] | None
    """

def layer_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove the active Grease Pencil layer

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def layer_reorder(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    target_layer_name: str = "Layer",
    location: typing.Literal["ABOVE", "BELOW"] | None = "ABOVE",
):
    """Reorder the active Grease Pencil layer

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param target_layer_name: Target Name, Name of the target layer
    :type target_layer_name: str
    :param location: Location
    :type location: typing.Literal['ABOVE','BELOW'] | None
    """

def layer_reveal(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Show all Grease Pencil layers

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_copy_to_object(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    only_active: bool | None = True,
):
    """Append Materials of the active Grease Pencil to other object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param only_active: Only Active, Append only active material, uncheck to append all materials
    :type only_active: bool | None
    """

def material_hide(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    invert: bool | None = False,
):
    """Hide active/inactive Grease Pencil material(s)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param invert: Invert, Hide inactive materials instead of the active one
    :type invert: bool | None
    """

def material_isolate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    affect_visibility: bool | None = False,
):
    """Toggle whether the active material is the only one that is editable and/or visible

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param affect_visibility: Affect Visibility, In addition to toggling the editability, also affect the visibility
    :type affect_visibility: bool | None
    """

def material_lock_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Lock all Grease Pencil materials to prevent them from being accidentally modified

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_lock_unselected(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Lock any material not used in any selected stroke

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_lock_unused(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Lock and hide any material not used

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_reveal(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Unhide all hidden Grease Pencil materials

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def material_select(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    deselect: bool | None = False,
):
    """Select/Deselect all Grease Pencil strokes using current material

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param deselect: Deselect, Unselect strokes
    :type deselect: bool | None
    """

def material_unlock_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Unlock all Grease Pencil materials so that they can be edited

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def move_to_layer(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    target_layer_name: str = "",
    add_new_layer: bool | None = False,
):
    """Move selected strokes to another layer

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param target_layer_name: Name, Target Grease Pencil Layer
    :type target_layer_name: str
    :param add_new_layer: New Layer, Move selection to a new layer
    :type add_new_layer: bool | None
    """

def paintmode_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    back: bool | None = False,
):
    """Enter/Exit paint mode for Grease Pencil strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param back: Return to Previous Mode, Return to previous mode
    :type back: bool | None
    """

def paste(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    paste_back: bool | None = False,
    keep_world_transform: bool | None = False,
):
    """Paste Grease Pencil points or strokes from the internal clipboard to the active layer

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param paste_back: Paste on Back, Add pasted strokes behind all strokes
    :type paste_back: bool | None
    :param keep_world_transform: Keep World Transform, Keep the world transform of strokes from the clipboard unchanged
    :type keep_world_transform: bool | None
    """

def primitive_arc(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    subdivision: int | None = 62,
    type: typing.Literal["BOX", "LINE", "POLYLINE", "CIRCLE", "ARC", "CURVE"]
    | None = "ARC",
):
    """Create predefined Grease Pencil stroke arcs

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param subdivision: Subdivisions, Number of subdivisions per segment
    :type subdivision: int | None
    :param type: Type, Type of shape
    :type type: typing.Literal['BOX','LINE','POLYLINE','CIRCLE','ARC','CURVE'] | None
    """

def primitive_box(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    subdivision: int | None = 3,
    type: typing.Literal["BOX", "LINE", "POLYLINE", "CIRCLE", "ARC", "CURVE"]
    | None = "BOX",
):
    """Create predefined Grease Pencil stroke boxes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param subdivision: Subdivisions, Number of subdivisions per segment
    :type subdivision: int | None
    :param type: Type, Type of shape
    :type type: typing.Literal['BOX','LINE','POLYLINE','CIRCLE','ARC','CURVE'] | None
    """

def primitive_circle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    subdivision: int | None = 94,
    type: typing.Literal["BOX", "LINE", "POLYLINE", "CIRCLE", "ARC", "CURVE"]
    | None = "CIRCLE",
):
    """Create predefined Grease Pencil stroke circles

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param subdivision: Subdivisions, Number of subdivisions per segment
    :type subdivision: int | None
    :param type: Type, Type of shape
    :type type: typing.Literal['BOX','LINE','POLYLINE','CIRCLE','ARC','CURVE'] | None
    """

def primitive_curve(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    subdivision: int | None = 62,
    type: typing.Literal["BOX", "LINE", "POLYLINE", "CIRCLE", "ARC", "CURVE"]
    | None = "CURVE",
):
    """Create predefined Grease Pencil stroke curve shapes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param subdivision: Subdivisions, Number of subdivisions per segment
    :type subdivision: int | None
    :param type: Type, Type of shape
    :type type: typing.Literal['BOX','LINE','POLYLINE','CIRCLE','ARC','CURVE'] | None
    """

def primitive_line(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    subdivision: int | None = 6,
    type: typing.Literal["BOX", "LINE", "POLYLINE", "CIRCLE", "ARC", "CURVE"]
    | None = "LINE",
):
    """Create predefined Grease Pencil stroke lines

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param subdivision: Subdivisions, Number of subdivisions per segment
    :type subdivision: int | None
    :param type: Type, Type of shape
    :type type: typing.Literal['BOX','LINE','POLYLINE','CIRCLE','ARC','CURVE'] | None
    """

def primitive_polyline(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    subdivision: int | None = 6,
    type: typing.Literal["BOX", "LINE", "POLYLINE", "CIRCLE", "ARC", "CURVE"]
    | None = "POLYLINE",
):
    """Create predefined Grease Pencil stroke polylines

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param subdivision: Subdivisions, Number of subdivisions per segment
    :type subdivision: int | None
    :param type: Type, Type of shape
    :type type: typing.Literal['BOX','LINE','POLYLINE','CIRCLE','ARC','CURVE'] | None
    """

def reorder(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    direction: typing.Literal["TOP", "UP", "DOWN", "BOTTOM"] | None = "TOP",
):
    """Change the display order of the selected strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param direction: Direction
    :type direction: typing.Literal['TOP','UP','DOWN','BOTTOM'] | None
    """

def reproject(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: typing.Literal["FRONT", "SIDE", "TOP", "VIEW", "SURFACE", "CURSOR"]
    | None = "VIEW",
    keep_original: bool | None = False,
    offset: float | None = 0.0,
):
    """Reproject the selected strokes from the current viewpoint as if they had been newly drawn (e.g. to fix problems from accidental 3D cursor movement or accidental viewport changes, or for matching deforming geometry)

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param type: Projection Type

    FRONT
    Front -- Reproject the strokes using the X-Z plane.

    SIDE
    Side -- Reproject the strokes using the Y-Z plane.

    TOP
    Top -- Reproject the strokes using the X-Y plane.

    VIEW
    View -- Reproject the strokes to end up on the same plane, as if drawn from the current viewpoint using 'Cursor' Stroke Placement.

    SURFACE
    Surface -- Reproject the strokes on to the scene geometry, as if drawn using 'Surface' placement.

    CURSOR
    Cursor -- Reproject the strokes using the orientation of 3D cursor.
        :type type: typing.Literal['FRONT','SIDE','TOP','VIEW','SURFACE','CURSOR'] | None
        :param keep_original: Keep Original, Keep original strokes and create a copy before reprojecting
        :type keep_original: bool | None
        :param offset: Surface Offset
        :type offset: float | None
    """

def reset_uvs(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Reset UV transformation to default values

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def sculpt_paint(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    | None = None,
    mode: typing.Literal["NORMAL", "INVERT", "SMOOTH", "ERASE"] | None = "NORMAL",
    pen_flip: bool | None = False,
):
    """Sculpt strokes in the active Grease Pencil object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param stroke: Stroke
        :type stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement] | None
        :param mode: Stroke Mode, Action taken when a paint stroke is made

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.

    SMOOTH
    Smooth -- Switch brush to smooth mode for duration of stroke.

    ERASE
    Erase -- Switch brush to erase mode for duration of stroke.
        :type mode: typing.Literal['NORMAL','INVERT','SMOOTH','ERASE'] | None
        :param pen_flip: Pen Flip, Whether a tablet's eraser mode is being used
        :type pen_flip: bool | None
    """

def sculptmode_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    back: bool | None = False,
):
    """Enter/Exit sculpt mode for Grease Pencil strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param back: Return to Previous Mode, Return to previous mode
    :type back: bool | None
    """

def select_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
):
    """(De)select all visible strokes

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param action: Action, Selection action to execute

    TOGGLE
    Toggle -- Toggle selection for all elements.

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.

    INVERT
    Invert -- Invert selection of all elements.
        :type action: typing.Literal['TOGGLE','SELECT','DESELECT','INVERT'] | None
    """

def select_alternate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    deselect_ends: bool | None = False,
):
    """Select alternated points in strokes with already selected points

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param deselect_ends: Deselect Ends, (De)select the first and last point of each stroke
    :type deselect_ends: bool | None
    """

def select_ends(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    amount_start: int | None = 0,
    amount_end: int | None = 1,
):
    """Select end points of strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param amount_start: Amount Start, Number of points to select from the start
    :type amount_start: int | None
    :param amount_end: Amount End, Number of points to select from the end
    :type amount_end: int | None
    """

def select_less(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Shrink the selection by one point

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_linked(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Select all points in curves with any point selection

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_more(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Grow the selection by one point

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def select_random(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    ratio: float | None = 0.5,
    seed: int | None = 0,
    action: typing.Literal["SELECT", "DESELECT"] | None = "SELECT",
):
    """Selects random points from the current strokes selection

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param ratio: Ratio, Portion of items to select randomly
        :type ratio: float | None
        :param seed: Random Seed, Seed for the random number generator
        :type seed: int | None
        :param action: Action, Selection action to execute

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.
        :type action: typing.Literal['SELECT','DESELECT'] | None
    """

def select_similar(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["LAYER", "MATERIAL", "VERTEX_COLOR", "RADIUS", "OPACITY"]
    | None = "LAYER",
    threshold: float | None = 0.1,
):
    """Select all strokes with similar characteristics

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: typing.Literal['LAYER','MATERIAL','VERTEX_COLOR','RADIUS','OPACITY'] | None
    :param threshold: Threshold
    :type threshold: float | None
    """

def separate(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["SELECTED", "MATERIAL", "LAYER"] | None = "SELECTED",
):
    """Separate the selected geometry into a new Grease Pencil object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param mode: Mode

    SELECTED
    Selection -- Separate selected geometry.

    MATERIAL
    By Material -- Separate by material.

    LAYER
    By Layer -- Separate by layer.
        :type mode: typing.Literal['SELECTED','MATERIAL','LAYER'] | None
    """

def set_active_material(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Set the selected stroke material as the active material

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def set_curve_resolution(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    resolution: int | None = 12,
):
    """Set resolution of selected curves

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param resolution: Resolution, The resolution to use for each curve segment
    :type resolution: int | None
    """

def set_curve_type(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: bpy.typing.CurvesTypeItems | None = "POLY",
    use_handles: bool | None = False,
):
    """Set type of selected curves

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Curve type
    :type type: bpy.typing.CurvesTypeItems | None
    :param use_handles: Handles, Take handle information into account in the conversion
    :type use_handles: bool | None
    """

def set_handle_type(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: bpy.typing.CurvesHandleTypeItems | None = "AUTO",
):
    """Set the handle type for bezier curves

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type
    :type type: bpy.typing.CurvesHandleTypeItems | None
    """

def set_material(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    slot: str | None = "DEFAULT",
):
    """Set active material

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param slot: Material Slot
    :type slot: str | None
    """

def set_selection_mode(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: bpy.typing.GreasePencilSelectmodeItems | None = "POINT",
):
    """Change the selection mode for Grease Pencil strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: bpy.typing.GreasePencilSelectmodeItems | None
    """

def set_uniform_opacity(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    opacity: float | None = 1.0,
):
    """Set all stroke points to same opacity

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param opacity: Opacity
    :type opacity: float | None
    """

def set_uniform_thickness(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    thickness: float | None = 0.1,
):
    """Set all stroke points to same thickness

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param thickness: Thickness, Thickness
    :type thickness: float | None
    """

def snap_cursor_to_selected(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Snap cursor to center of selected points

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def snap_to_cursor(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_offset: bool | None = True,
):
    """Snap selected points/strokes to the cursor

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_offset: With Offset, Offset the entire stroke instead of selected points only
    :type use_offset: bool | None
    """

def snap_to_grid(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Snap selected points to the nearest grid points

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def stroke_material_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    material: str = "",
):
    """Assign the active material slot to the selected strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param material: Material, Name of the material
    :type material: str
    """

def stroke_merge_by_distance(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    threshold: float | None = 0.001,
    use_unselected: bool | None = False,
):
    """Merge points by distance

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param threshold: Threshold
    :type threshold: float | None
    :param use_unselected: Unselected, Use whole stroke, not only selected points
    :type use_unselected: bool | None
    """

def stroke_reset_vertex_color(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["STROKE", "FILL", "BOTH"] | None = "BOTH",
):
    """Reset vertex color for all or selected strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: typing.Literal['STROKE','FILL','BOTH'] | None
    """

def stroke_simplify(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    factor: float | None = 0.01,
    length: float | None = 0.05,
    distance: float | None = 0.01,
    steps: int | None = 1,
    mode: typing.Literal["FIXED", "ADAPTIVE", "SAMPLE", "MERGE"] | None = "FIXED",
):
    """Simplify selected strokes

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param factor: Factor
        :type factor: float | None
        :param length: Length
        :type length: float | None
        :param distance: Distance
        :type distance: float | None
        :param steps: Steps
        :type steps: int | None
        :param mode: Mode, Method used for simplifying stroke points

    FIXED
    Fixed -- Delete alternating vertices in the stroke, except extremes.

    ADAPTIVE
    Adaptive -- Use a Ramer-Douglas-Peucker algorithm to simplify the stroke preserving main shape.

    SAMPLE
    Sample -- Re-sample the stroke with segments of the specified length.

    MERGE
    Merge -- Simplify the stroke by merging vertices closer than a given distance.
        :type mode: typing.Literal['FIXED','ADAPTIVE','SAMPLE','MERGE'] | None
    """

def stroke_smooth(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    iterations: int | None = 10,
    factor: float | None = 1.0,
    smooth_ends: bool | None = False,
    keep_shape: bool | None = False,
    smooth_position: bool | None = True,
    smooth_radius: bool | None = True,
    smooth_opacity: bool | None = False,
):
    """Smooth selected strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param iterations: Iterations
    :type iterations: int | None
    :param factor: Factor
    :type factor: float | None
    :param smooth_ends: Smooth Endpoints
    :type smooth_ends: bool | None
    :param keep_shape: Keep Shape
    :type keep_shape: bool | None
    :param smooth_position: Position
    :type smooth_position: bool | None
    :param smooth_radius: Radius
    :type smooth_radius: bool | None
    :param smooth_opacity: Opacity
    :type smooth_opacity: bool | None
    """

def stroke_subdivide(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    number_cuts: int | None = 1,
    only_selected: bool | None = True,
):
    """Subdivide between continuous selected points of the stroke adding a point half way between them

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param number_cuts: Number of Cuts
    :type number_cuts: int | None
    :param only_selected: Selected Points, Smooth only selected points in the stroke
    :type only_selected: bool | None
    """

def stroke_subdivide_smooth(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    GREASE_PENCIL_OT_stroke_subdivide: typing.Any | None = None,
    GREASE_PENCIL_OT_stroke_smooth: typing.Any | None = None,
):
    """Subdivide strokes and smooth them

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param GREASE_PENCIL_OT_stroke_subdivide: Subdivide Stroke, Subdivide between continuous selected points of the stroke adding a point half way between them
    :type GREASE_PENCIL_OT_stroke_subdivide: typing.Any | None
    :param GREASE_PENCIL_OT_stroke_smooth: Smooth Stroke, Smooth selected strokes
    :type GREASE_PENCIL_OT_stroke_smooth: typing.Any | None
    """

def stroke_switch_direction(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Change direction of the points of the selected strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def stroke_trim(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None = None,
    use_smooth_stroke: bool | None = False,
    smooth_stroke_factor: float | None = 0.75,
    smooth_stroke_radius: int | None = 35,
):
    """Delete stroke points in between intersecting strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param path: Path
    :type path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None
    :param use_smooth_stroke: Stabilize Stroke, Selection lags behind mouse and follows a smoother path
    :type use_smooth_stroke: bool | None
    :param smooth_stroke_factor: Smooth Stroke Factor, Higher values gives a smoother stroke
    :type smooth_stroke_factor: float | None
    :param smooth_stroke_radius: Smooth Stroke Radius, Minimum distance from last point before selection continues
    :type smooth_stroke_radius: int | None
    """

def texture_gradient(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    xstart: int | None = 0,
    xend: int | None = 0,
    ystart: int | None = 0,
    yend: int | None = 0,
    flip: bool | None = False,
    cursor: int | None = 5,
):
    """Draw a line to set the fill material gradient for the selected strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param xstart: X Start
    :type xstart: int | None
    :param xend: X End
    :type xend: int | None
    :param ystart: Y Start
    :type ystart: int | None
    :param yend: Y End
    :type yend: int | None
    :param flip: Flip
    :type flip: bool | None
    :param cursor: Cursor, Mouse cursor style to use during the modal operator
    :type cursor: int | None
    """

def trace_image(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    target: typing.Literal["NEW", "SELECTED"] | None = "NEW",
    radius: float | None = 0.01,
    threshold: float | None = 0.5,
    turnpolicy: typing.Literal[
        "FOREGROUND", "BACKGROUND", "LEFT", "RIGHT", "MINORITY", "MAJORITY", "RANDOM"
    ]
    | None = "MINORITY",
    mode: typing.Literal["SINGLE", "SEQUENCE"] | None = "SINGLE",
    use_current_frame: bool | None = True,
    frame_number: int | None = 0,
):
    """Extract Grease Pencil strokes from image

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param target: Target Object, Target Grease Pencil
        :type target: typing.Literal['NEW','SELECTED'] | None
        :param radius: Radius
        :type radius: float | None
        :param threshold: Color Threshold, Determine the lightness threshold above which strokes are generated
        :type threshold: float | None
        :param turnpolicy: Turn Policy, Determines how to resolve ambiguities during decomposition of bitmaps into paths

    FOREGROUND
    Foreground -- Prefers to connect foreground components.

    BACKGROUND
    Background -- Prefers to connect background components.

    LEFT
    Left -- Always take a left turn.

    RIGHT
    Right -- Always take a right turn.

    MINORITY
    Minority -- Prefers to connect the color that occurs least frequently in the local neighborhood of the current position.

    MAJORITY
    Majority -- Prefers to connect the color that occurs most frequently in the local neighborhood of the current position.

    RANDOM
    Random -- Choose pseudo-randomly.
        :type turnpolicy: typing.Literal['FOREGROUND','BACKGROUND','LEFT','RIGHT','MINORITY','MAJORITY','RANDOM'] | None
        :param mode: Mode, Determines if trace simple image or full sequence

    SINGLE
    Single -- Trace the current frame of the image.

    SEQUENCE
    Sequence -- Trace full sequence.
        :type mode: typing.Literal['SINGLE','SEQUENCE'] | None
        :param use_current_frame: Start At Current Frame, Trace Image starting in current image frame
        :type use_current_frame: bool | None
        :param frame_number: Trace Frame, Used to trace only one frame of the image sequence, set to zero to trace all
        :type frame_number: int | None
    """

def vertex_brush_stroke(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    | None = None,
    mode: typing.Literal["NORMAL", "INVERT", "SMOOTH", "ERASE"] | None = "NORMAL",
    pen_flip: bool | None = False,
):
    """Draw on vertex colors in the active Grease Pencil object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param stroke: Stroke
        :type stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement] | None
        :param mode: Stroke Mode, Action taken when a paint stroke is made

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.

    SMOOTH
    Smooth -- Switch brush to smooth mode for duration of stroke.

    ERASE
    Erase -- Switch brush to erase mode for duration of stroke.
        :type mode: typing.Literal['NORMAL','INVERT','SMOOTH','ERASE'] | None
        :param pen_flip: Pen Flip, Whether a tablet's eraser mode is being used
        :type pen_flip: bool | None
    """

def vertex_color_brightness_contrast(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["STROKE", "FILL", "BOTH"] | None = "BOTH",
    brightness: float | None = 0.0,
    contrast: float | None = 0.0,
):
    """Adjust vertex color brightness/contrast

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: typing.Literal['STROKE','FILL','BOTH'] | None
    :param brightness: Brightness
    :type brightness: float | None
    :param contrast: Contrast
    :type contrast: float | None
    """

def vertex_color_hsv(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["STROKE", "FILL", "BOTH"] | None = "BOTH",
    h: float | None = 0.5,
    s: float | None = 1.0,
    v: float | None = 1.0,
):
    """Adjust vertex color HSV values

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: typing.Literal['STROKE','FILL','BOTH'] | None
    :param h: Hue
    :type h: float | None
    :param s: Saturation
    :type s: float | None
    :param v: Value
    :type v: float | None
    """

def vertex_color_invert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["STROKE", "FILL", "BOTH"] | None = "BOTH",
):
    """Invert RGB values

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: typing.Literal['STROKE','FILL','BOTH'] | None
    """

def vertex_color_levels(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["STROKE", "FILL", "BOTH"] | None = "BOTH",
    offset: float | None = 0.0,
    gain: float | None = 1.0,
):
    """Adjust levels of vertex colors

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: typing.Literal['STROKE','FILL','BOTH'] | None
    :param offset: Offset, Value to add to colors
    :type offset: float | None
    :param gain: Gain, Value to multiply colors by
    :type gain: float | None
    """

def vertex_color_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    mode: typing.Literal["STROKE", "FILL", "BOTH"] | None = "BOTH",
    factor: float | None = 1.0,
):
    """Set active color to all selected vertex

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param mode: Mode
    :type mode: typing.Literal['STROKE','FILL','BOTH'] | None
    :param factor: Factor, Mix Factor
    :type factor: float | None
    """

def vertex_group_normalize(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Normalize weights of the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def vertex_group_normalize_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    lock_active: bool | None = True,
):
    """Normalize the weights of all vertex groups, so that for each vertex, the sum of all weights is 1.0

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param lock_active: Lock Active, Keep the values of the active group while normalizing others
    :type lock_active: bool | None
    """

def vertex_group_smooth(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    factor: float | None = 0.5,
    repeat: int | None = 1,
):
    """Smooth the weights of the active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param factor: Factor
    :type factor: float | None
    :param repeat: Iterations
    :type repeat: int | None
    """

def vertexmode_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    back: bool | None = False,
):
    """Enter/Exit vertex paint mode for Grease Pencil strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param back: Return to Previous Mode, Return to previous mode
    :type back: bool | None
    """

def weight_brush_stroke(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    | None = None,
    mode: typing.Literal["NORMAL", "INVERT", "SMOOTH", "ERASE"] | None = "NORMAL",
    pen_flip: bool | None = False,
):
    """Draw weight on stroke points in the active Grease Pencil object

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param stroke: Stroke
        :type stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement] | None
        :param mode: Stroke Mode, Action taken when a paint stroke is made

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.

    SMOOTH
    Smooth -- Switch brush to smooth mode for duration of stroke.

    ERASE
    Erase -- Switch brush to erase mode for duration of stroke.
        :type mode: typing.Literal['NORMAL','INVERT','SMOOTH','ERASE'] | None
        :param pen_flip: Pen Flip, Whether a tablet's eraser mode is being used
        :type pen_flip: bool | None
    """

def weight_invert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Invert the weight of active vertex group

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def weight_sample(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Set the weight of the Draw tool to the weight of the vertex under the mouse cursor

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def weight_toggle_direction(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Toggle Add/Subtract for the weight paint draw tool

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def weightmode_toggle(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    back: bool | None = False,
):
    """Enter/Exit weight paint mode for Grease Pencil strokes

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param back: Return to Previous Mode, Return to previous mode
    :type back: bool | None
    """
