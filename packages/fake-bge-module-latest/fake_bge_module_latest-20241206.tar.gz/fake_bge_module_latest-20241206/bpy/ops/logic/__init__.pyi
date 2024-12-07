import typing
import collections.abc
import typing_extensions
import bpy.types
import bpy.typing

def actuator_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "",
    name: str = "",
    object: str = "",
):
    """Add an actuator to the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Type of actuator to add
    :type type: str | None
    :param name: Name, Name of the Actuator to add
    :type name: str
    :param object: Object, Name of the Object to add the Actuator to
    :type object: str
    """

def actuator_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    actuator: str = "",
    object: str = "",
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
):
    """Move Actuator

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param actuator: Actuator, Name of the actuator to edit
    :type actuator: str
    :param object: Object, Name of the object the actuator belongs to
    :type object: str
    :param direction: Direction, Move Up or Down
    :type direction: typing.Literal['UP','DOWN'] | None
    """

def actuator_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    actuator: str = "",
    object: str = "",
):
    """Remove an actuator from the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param actuator: Actuator, Name of the actuator to edit
    :type actuator: str
    :param object: Object, Name of the object the actuator belongs to
    :type object: str
    """

def controller_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: bpy.typing.ControllerTypeItems | None = "LOGIC_AND",
    name: str = "",
    object: str = "",
):
    """Add a controller to the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Type of controller to add
    :type type: bpy.typing.ControllerTypeItems | None
    :param name: Name, Name of the Controller to add
    :type name: str
    :param object: Object, Name of the Object to add the Controller to
    :type object: str
    """

def controller_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    controller: str = "",
    object: str = "",
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
):
    """Move Controller

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param controller: Controller, Name of the controller to edit
    :type controller: str
    :param object: Object, Name of the object the controller belongs to
    :type object: str
    :param direction: Direction, Move Up or Down
    :type direction: typing.Literal['UP','DOWN'] | None
    """

def controller_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    controller: str = "",
    object: str = "",
):
    """Remove a controller from the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param controller: Controller, Name of the controller to edit
    :type controller: str
    :param object: Object, Name of the object the controller belongs to
    :type object: str
    """

def custom_object_create(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    class_name: str = "module.MyObject",
):
    """Create a KX_GameObject subclass and attach it to the selected object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param class_name: MyObject, The class name with module (module.ClassName)
    :type class_name: str
    """

def custom_object_register(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    class_name: str = "module.MyObject",
):
    """Use a custom KX_GameObject subclass for the selected object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param class_name: MyObject, The class name with module (module.ClassName)
    :type class_name: str
    """

def custom_object_reload(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Reload custom object from the source script

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def custom_object_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove this custom class from the object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def links_cut(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None = None,
    cursor: int | None = 15,
):
    """Remove logic brick connections

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param path: Path
    :type path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None
    :param cursor: Cursor
    :type cursor: int | None
    """

def properties(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Toggle the properties region visibility

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def python_component_create(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    component_name: str = "module.Component",
):
    """Create a Python component to the selected object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param component_name: Component, The component class name with module (module.ComponentName)
    :type component_name: str
    """

def python_component_move_down(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    index: int | None = 0,
):
    """Move this component down in the list

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param index: Index, Component index to move
    :type index: int | None
    """

def python_component_move_up(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    index: int | None = 0,
):
    """Move this component up in the list

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param index: Index, Component index to move
    :type index: int | None
    """

def python_component_register(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    component_name: str = "module.Component",
):
    """Add a Python component to the selected object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param component_name: Component, The component class name with module (module.ComponentName)
    :type component_name: str
    """

def python_component_reload(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    index: int | None = 0,
):
    """Reload component from the source script

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param index: Index, Component index to reload
    :type index: int | None
    """

def python_component_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    index: int | None = 0,
):
    """Remove this component from the object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param index: Index, Component index to remove
    :type index: int | None
    """

def region_flip(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Toggle the properties region's alignment (left/right)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

def sensor_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    type: str | None = "",
    name: str = "",
    object: str = "",
):
    """Add a sensor to the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param type: Type, Type of sensor to add
    :type type: str | None
    :param name: Name, Name of the Sensor to add
    :type name: str
    :param object: Object, Name of the Object to add the Sensor to
    :type object: str
    """

def sensor_move(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    sensor: str = "",
    object: str = "",
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
):
    """Move Sensor

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param sensor: Sensor, Name of the sensor to edit
    :type sensor: str
    :param object: Object, Name of the object the sensor belongs to
    :type object: str
    :param direction: Direction, Move Up or Down
    :type direction: typing.Literal['UP','DOWN'] | None
    """

def sensor_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    sensor: str = "",
    object: str = "",
):
    """Remove a sensor from the active object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param sensor: Sensor, Name of the sensor to edit
    :type sensor: str
    :param object: Object, Name of the object the sensor belongs to
    :type object: str
    """

def view_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Resize view so you can see all logic bricks

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """
