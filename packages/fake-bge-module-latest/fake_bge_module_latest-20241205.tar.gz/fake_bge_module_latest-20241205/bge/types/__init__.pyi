"""

--------------------

This module contains the classes that appear as instances in the Game Engine. A
script must interact with these classes if it is to affect the behaviour of
objects in a game.

The following example would move an object (i.e. an instance of
~bge.types.KX_GameObject) one unit up.

```
# bge.types.SCA_PythonController
cont = bge.logic.getCurrentController()

# bge.types.KX_GameObject
obj = cont.owner
obj.worldPosition.z += 1
```

To run the code, it could be placed in a Blender text block and executed with
a ~bge.types.SCA_PythonController logic brick.


--------------------

bge.types.*

:glob:

"""

import typing
import collections.abc
import typing_extensions
import aud
import bpy.types
import mathutils

class BL_ArmatureBone:
    """Proxy to Blender bone structure. All fields are read-only and comply to RNA names.
    All space attribute correspond to the rest pose.
    """

    name: str
    """ bone name.

    :type: str
    """

    connected: bool
    """ true when the bone head is struck to the parent's tail.

    :type: bool
    """

    hinge: bool
    """ true when bone doesn't inherit rotation or scale from parent bone.

    :type: bool
    """

    inherit_scale: bool
    """ true when bone inherits scaling from parent bone.

    :type: bool
    """

    bbone_segments: int
    """ number of B-bone segments.

    :type: int
    """

    roll: float
    """ bone rotation around head-tail axis.

    :type: float
    """

    head: typing.Any
    """ location of head end of the bone in parent bone space."""

    tail: typing.Any
    """ location of head end of the bone in parent bone space."""

    length: float
    """ bone length.

    :type: float
    """

    arm_head: typing.Any
    """ location of head end of the bone in armature space."""

    arm_tail: typing.Any
    """ location of tail end of the bone in armature space."""

    arm_mat: typing.Any
    """ matrix of the bone head in armature space."""

    bone_mat: typing.Any
    """ rotation matrix of the bone in parent bone space."""

    parent: typing.Any
    """ parent bone, or None for root bone."""

    children: typing.Any
    """ list of bone's children."""

class BL_ArmatureChannel:
    """Proxy to armature pose channel. Allows to read and set armature pose.
    The attributes are identical to RNA attributes, but mostly in read-only mode.
    """

    name: str
    """ channel name (=bone name), read-only.

    :type: str
    """

    bone: typing.Any
    """ return the bone object corresponding to this pose channel, read-only."""

    parent: typing.Any
    """ return the parent channel object, None if root channel, read-only."""

    has_ik: bool
    """ true if the bone is part of an active IK chain, read-only.
This flag is not set when an IK constraint is defined but not enabled (miss target information for example).

    :type: bool
    """

    ik_dof_x: bool
    """ true if the bone is free to rotation in the X axis, read-only.

    :type: bool
    """

    ik_dof_y: bool
    """ true if the bone is free to rotation in the Y axis, read-only.

    :type: bool
    """

    ik_dof_z: bool
    """ true if the bone is free to rotation in the Z axis, read-only.

    :type: bool
    """

    ik_limit_x: bool
    """ true if a limit is imposed on X rotation, read-only.

    :type: bool
    """

    ik_limit_y: bool
    """ true if a limit is imposed on Y rotation, read-only.

    :type: bool
    """

    ik_limit_z: bool
    """ true if a limit is imposed on Z rotation, read-only.

    :type: bool
    """

    ik_rot_control: bool
    """ true if channel rotation should applied as IK constraint, read-only.

    :type: bool
    """

    ik_lin_control: bool
    """ true if channel size should applied as IK constraint, read-only.

    :type: bool
    """

    location: typing.Any
    """ displacement of the bone head in armature local space, read-write."""

    scale: typing.Any
    """ scale of the bone relative to its parent, read-write."""

    rotation_quaternion: typing.Any
    """ rotation of the bone relative to its parent expressed as a quaternion, read-write."""

    rotation_euler: typing.Any
    """ rotation of the bone relative to its parent expressed as a set of euler angles, read-write."""

    rotation_mode: typing.Any
    """ Method of updating the bone rotation, read-write."""

    channel_matrix: typing.Any
    """ pose matrix in bone space (deformation of the bone due to action, constraint, etc), Read-only.
This field is updated after the graphic render, it represents the current pose."""

    pose_matrix: typing.Any
    """ pose matrix in armature space, read-only,
This field is updated after the graphic render, it represents the current pose."""

    pose_head: typing.Any
    """ position of bone head in armature space, read-only."""

    pose_tail: typing.Any
    """ position of bone tail in armature space, read-only."""

    ik_min_x: float
    """ minimum value of X rotation in degree (<= 0) when X rotation is limited (see ik_limit_x), read-only.

    :type: float
    """

    ik_max_x: float
    """ maximum value of X rotation in degree (>= 0) when X rotation is limited (see ik_limit_x), read-only.

    :type: float
    """

    ik_min_y: float
    """ minimum value of Y rotation in degree (<= 0) when Y rotation is limited (see ik_limit_y), read-only.

    :type: float
    """

    ik_max_y: float
    """ maximum value of Y rotation in degree (>= 0) when Y rotation is limited (see ik_limit_y), read-only.

    :type: float
    """

    ik_min_z: float
    """ minimum value of Z rotation in degree (<= 0) when Z rotation is limited (see ik_limit_z), read-only.

    :type: float
    """

    ik_max_z: float
    """ maximum value of Z rotation in degree (>= 0) when Z rotation is limited (see ik_limit_z), read-only.

    :type: float
    """

    ik_stiffness_x: typing.Any
    """ bone rotation stiffness in X axis, read-only."""

    ik_stiffness_y: typing.Any
    """ bone rotation stiffness in Y axis, read-only."""

    ik_stiffness_z: typing.Any
    """ bone rotation stiffness in Z axis, read-only."""

    ik_stretch: float
    """ ratio of scale change that is allowed, 0=bone can't change size, read-only.

    :type: float
    """

    ik_rot_weight: typing.Any
    """ weight of rotation constraint when ik_rot_control is set, read-write."""

    ik_lin_weight: typing.Any
    """ weight of size constraint when ik_lin_control is set, read-write."""

    joint_rotation: typing.Any
    """ Control bone rotation in term of joint angle (for robotic applications), read-write.When writing to this attribute, you pass a [x, y, z] vector and an appropriate set of euler angles or quaternion is calculated according to the rotation_mode.When you read this attribute, the current pose matrix is converted into a [x, y, z] vector representing the joint angles.The value and the meaning of the x, y, z depends on the ik_dof_x/ik_dof_y/ik_dof_z attributes:"""

class BL_ArmatureConstraint:
    """Proxy to Armature Constraint. Allows to change constraint on the fly.
    Obtained through `~bge.types.BL_ArmatureObject`.constraints.
    """

    type: int
    """ Type of constraint, (read-only).Use one of `these constants<armatureconstraint-constants-type>`.

    :type: int
    """

    name: str
    """ Name of constraint constructed as <bone_name>:<constraint_name>. constraints list.This name is also the key subscript on `~bge.types.BL_ArmatureObject`.

    :type: str
    """

    enforce: float
    """ fraction of constraint effect that is enforced. Between 0 and 1.

    :type: float
    """

    headtail: typing.Any
    """ Position of target between head and tail of the target bone: 0=head, 1=tail."""

    lin_error: float
    """ runtime linear error (in Blender units) on constraint at the current frame.This is a runtime value updated on each frame by the IK solver. Only available on IK constraint and iTaSC solver.

    :type: float
    """

    rot_error: typing.Any
    """ Runtime rotation error (in radiant) on constraint at the current frame.This is a runtime value updated on each frame by the IK solver. Only available on IK constraint and iTaSC solver.It is only set if the constraint has a rotation part, for example, a CopyPose+Rotation IK constraint."""

    target: typing.Any
    """ Primary target object for the constraint. The position of this object in the GE will be used as target for the constraint."""

    subtarget: typing.Any
    """ Secondary target object for the constraint. The position of this object in the GE will be used as secondary target for the constraint.Currently this is only used for pole target on IK constraint."""

    active: bool
    """ True if the constraint is active.

    :type: bool
    """

    ik_weight: float
    """ Weight of the IK constraint between 0 and 1.Only defined for IK constraint.

    :type: float
    """

    ik_type: int
    """ Type of IK constraint, (read-only).Use one of `these constants<armatureconstraint-constants-ik-type>`.

    :type: int
    """

    ik_flag: int
    """ Combination of IK constraint option flags, read-only.Use one of `these constants<armatureconstraint-constants-ik-flag>`.

    :type: int
    """

    ik_dist: float
    """ Distance the constraint is trying to maintain with target, only used when ik_type=CONSTRAINT_IK_DISTANCE.

    :type: float
    """

    ik_mode: int
    """ Use one of `these constants<armatureconstraint-constants-ik-mode>`.Additional mode for IK constraint. Currently only used for Distance constraint:

    :type: int
    """

class BL_ArmatureObject:
    """An armature object."""

    constraints: typing.Any
    """ The list of armature constraint defined on this armature.
Elements of the list can be accessed by index or string.
The key format for string access is '<bone_name>:<constraint_name>'."""

    channels: typing.Any
    """ The list of armature channels.
Elements of the list can be accessed by index or name the bone."""

    def update(self):
        """Ensures that the armature will be updated on next graphic frame.This action is unnecessary if a KX_ArmatureActuator with mode run is active
        or if an action is playing. Use this function in other cases. It must be called
        on each frame to ensure that the armature is updated continuously.

        """

    def draw(self):
        """Draw lines that represent armature to view it in real time."""

class BL_Shader:
    """BL_Shader is a class used to compile and use custom shaders scripts.
    This header set the #version directive, so the user must not define his own #version.
    Since 0.3.0, this class is only used with custom 2D filters.The list of python callbacks executed when the shader is used to render an object.
    All the functions can expect as argument the object currently rendered.def callback(object):
        print("render object %r" % object.name)type

    list of functions and/or methods0.3.0The list of python callbacks executed when the shader is begin used to render.type

    list of functions and/or methods0.3.0Clear the shader. Use this method before the source is changed with `setSource`.0.3.0Set attribute location. (The parameter is ignored a.t.m. and the value of "tangent" is always used.)arg enum

    attribute location value

    type enum

    integer0.3.0Set the vertex and fragment programsarg vertexProgram

    Vertex program

    type vertexProgram

    string

    arg fragmentProgram

    Fragment program

    type fragmentProgram

    string

    arg apply

    Enable the shader.

    type apply

    boolean0.3.0Set the vertex, fragment and geometry shader programs.arg sources

    Dictionary of all programs. The keys `vertex`, `fragment` and `geometry` represent shader programs of the same name.
    `geometry` is an optional program.
    This dictionary can be similar to:

    sources = {
        "vertex" : vertexProgram,
        "fragment" : fragmentProgram,
        "geometry" : geometryProgram
    }

    type sources

    dict

    arg apply

    Enable the shader.

    type apply

    boolean0.3.0Set a uniform with a float value that reflects the eye being render in stereo mode:
    0.0 for the left eye, 0.5 for the right eye. In non stereo mode, the value of the uniform
    is fixed to 0.0. The typical use of this uniform is in stereo mode to sample stereo textures
    containing the left and right eye images in a top-bottom order.arg name

    the uniform name

    type name

    string0.3.0
    """

    enabled: bool
    """ Set shader enabled to use.

    :type: bool
    """

    objectCallbacks: typing.Any
    bindCallbacks: typing.Any

    def setUniformfv(self, name: str, fList):
        """Set a uniform with a list of float values

        :param name: the uniform name
        :type name: str
        :param fList: a list (2, 3 or 4 elements) of float values
        """

    def delSource(self): ...
    def getFragmentProg(self) -> str:
        """Returns the fragment program.

        :return: The fragment program.
        :rtype: str
        """

    def getVertexProg(self) -> str:
        """Get the vertex program.

        :return: The vertex program.
        :rtype: str
        """

    def isValid(self) -> bool:
        """Check if the shader is valid.

        :return: True if the shader is valid
        :rtype: bool
        """

    def setAttrib(self, enum):
        """

        :param enum:
        """

    def setSampler(self, name: str, index: int):
        """Set uniform texture sample index.

        :param name: Uniform name
        :type name: str
        :param index: Texture sample index.
        :type index: int
        """

    def setSource(self, vertexProgram, fragmentProgram, apply):
        """

        :param vertexProgram:
        :param fragmentProgram:
        :param apply:
        """

    def setSourceList(self, sources, apply):
        """

        :param sources:
        :param apply:
        """

    def setUniform1f(self, name: str, fx: float):
        """Set a uniform with 1 float value.

        :param name: the uniform name
        :type name: str
        :param fx: Uniform value
        :type fx: float
        """

    def setUniform1i(self, name: str, ix: int):
        """Set a uniform with an integer value.

        :param name: the uniform name
        :type name: str
        :param ix: the uniform value
        :type ix: int
        """

    def setUniform2f(self, name: str, fx: float, fy: float):
        """Set a uniform with 2 float values

        :param name: the uniform name
        :type name: str
        :param fx: first float value
        :type fx: float
        :param fy: second float value
        :type fy: float
        """

    def setUniform2i(self, name: str, ix: int, iy: int):
        """Set a uniform with 2 integer values

        :param name: the uniform name
        :type name: str
        :param ix: first integer value
        :type ix: int
        :param iy: second integer value
        :type iy: int
        """

    def setUniform3f(self, name: str, fx: float, fy: float, fz: float):
        """Set a uniform with 3 float values.

        :param name: the uniform name
        :type name: str
        :param fx: first float value
        :type fx: float
        :param fy: second float value
        :type fy: float
        :param fz: third float value
        :type fz: float
        """

    def setUniform3i(self, name: str, ix: int, iy: int, iz: int):
        """Set a uniform with 3 integer values

        :param name: the uniform name
        :type name: str
        :param ix: first integer value
        :type ix: int
        :param iy: second integer value
        :type iy: int
        :param iz: third integer value
        :type iz: int
        """

    def setUniform4f(self, name: str, fx: float, fy: float, fz: float, fw: float):
        """Set a uniform with 4 float values.

        :param name: the uniform name
        :type name: str
        :param fx: first float value
        :type fx: float
        :param fy: second float value
        :type fy: float
        :param fz: third float value
        :type fz: float
        :param fw: fourth float value
        :type fw: float
        """

    def setUniform4i(self, name: str, ix: int, iy: int, iz: int, iw: int):
        """Set a uniform with 4 integer values

        :param name: the uniform name
        :type name: str
        :param ix: first integer value
        :type ix: int
        :param iy: second integer value
        :type iy: int
        :param iz: third integer value
        :type iz: int
        :param iw: fourth integer value
        :type iw: int
        """

    def setUniformDef(self, name: str, type: int):
        """Define a new uniform

        :param name: the uniform name
        :type name: str
        :param type: uniform type, one of `these constants <shader-defined-uniform>`
        :type type: int
        """

    def setUniformMatrix3(self, name: str, mat, transpose: bool):
        """Set a uniform with a 3x3 matrix value

        :param name: the uniform name
        :type name: str
        :param mat: A 3x3 matrix [[f, f, f], [f, f, f], [f, f, f]]
        :param transpose: set to True to transpose the matrix
        :type transpose: bool
        """

    def setUniformMatrix4(self, name: str, mat, transpose: bool):
        """Set a uniform with a 4x4 matrix value

        :param name: the uniform name
        :type name: str
        :param mat: A 4x4 matrix [[f, f, f, f], [f, f, f, f], [f, f, f, f], [f, f, f, f]]
        :param transpose: set to True to transpose the matrix
        :type transpose: bool
        """

    def setUniformiv(self, name: str, iList):
        """Set a uniform with a list of integer values

        :param name: the uniform name
        :type name: str
        :param iList: a list (2, 3 or 4 elements) of integer values
        """

    def setUniformEyef(self, name):
        """

        :param name:
        """

    def validate(self):
        """Validate the shader object."""

class EXP_Value:
    """This class is a basis for other classes."""

    name: str
    """ The name of this EXP_Value derived object (read-only).

    :type: str
    """

class EXP_ListValue:
    """This is a list like object used in the game engine internally that behaves similar to a python list in most ways.As well as the normal index lookup (val= clist[i]), EXP_ListValue supports string lookups (val= scene.objects["Cube"])Other operations such as len(clist), list(clist), clist[0:10] are also supported."""

    def append(self, val):
        """Add an item to the list (like pythons append)

        :param val:
        """

    def count(self, val) -> int:
        """Count the number of instances of a value in the list.

        :param val:
        :return: number of instances
        :rtype: int
        """

    def index(self, val) -> int:
        """Return the index of a value in the list.

        :param val:
        :return: The index of the value in the list.
        :rtype: int
        """

    def reverse(self):
        """Reverse the order of the list."""

    def get(self, key, default=None):
        """Return the value matching key, or the default value if its not found.

        :param key:
        :param default:
        :return: The key value or a default.
        """

    def filter(self, name, prop):
        """Return a list of items with name matching name regex and with a property matching prop regex.
        If name is empty every items are checked, if prop is empty no property check is proceeded.

                :param name:
                :param prop:
                :return: The list of matching items.
        """

    def from_id(self, id):
        """This is a function especially for the game engine to return a value with a specific id.Since object names are not always unique, the id of an object can be used to get an object from the CValueList.Example:Where myObID is an int or long from the id function.This has the advantage that you can store the id in places you could not store a gameObject.

        :param id:
        """

class EXP_PropValue:
    """This class has no python functions"""

class EXP_PyObjectPlus:
    """EXP_PyObjectPlus base class of most other types in the Game Engine."""

    invalid: bool
    """ Test if the object has been freed by the game engine and is no longer valid.Normally this is not a problem but when storing game engine data in the GameLogic module,
KX_Scenes or other KX_GameObjects its possible to hold a reference to invalid data.
Calling an attribute or method on an invalid object will raise a SystemError.The invalid attribute allows testing for this case without exception handling.

    :type: bool
    """

class KX_2DFilter:
    """2D filter shader object. Can be alternated with `~bge.types.BL_Shader`'s functions."""

    mipmap: bool
    """ Request mipmap generation of the render bgl_RenderedTexture texture. Accessing mipmapping level is similar to:

    :type: bool
    """

    offScreen: typing.Any
    """ The custom off screen (framebuffer in 0.3.0) the filter render to (read-only)."""

    def setTexture(self, index: int, bindCode: int, samplerName: str = ""):
        """Set specified texture bind code `bindCode` in specified slot `index`. Any call to `setTexture`
        should be followed by a call to `BL_Shader.setSampler <bge.types.BL_Shader.setSampler>` with the same `index` if `sampleName` is not specified.

                :param index: The texture slot.
                :type index: int
                :param bindCode: The texture bind code/Id.
                :type bindCode: int
                :param samplerName: The shader sampler name set to `index` if `samplerName` is passed in the function. (optional)
                :type samplerName: str
        """

    def setCubeMap(self, index: int, bindCode: int, samplerName: str = ""):
        """Set specified cube map texture bind code `bindCode` in specified slot `index`. Any call to `setCubeMap`
        should be followed by a call to `BL_Shader.setSampler <bge.types.BL_Shader.setSampler>` with the same `index` if `sampleName` is not specified.

                :param index: The texture slot.
                :type index: int
                :param bindCode: The cube map texture bind code/Id.
                :type bindCode: int
                :param samplerName: The shader sampler name set to `index` if `samplerName` is passed in the function. (optional)
                :type samplerName: str
        """

    def addOffScreen(
        self,
        slots: int,
        width: int | None = None,
        height: int | None = None,
        mipmap: bool = False,
    ):
        """Register a custom off screen (framebuffer in 0.3.0) to render the filter to.

        :param slots: The number of color texture attached to the off screen, between 0 and 8 excluded.
        :type slots: int
        :param width: In 0.3.0, always canvas width (optional).
        :type width: int | None
        :param height: In 0.3.0, always canvas height (optional).
        :type height: int | None
        :param mipmap: True if the color texture generate mipmap at the end of the filter rendering (optional).
        :type mipmap: bool
        """

    def removeOffScreen(self):
        """Unregister the custom off screen (framebuffer in 0.3.0) the filter render to."""

class KX_2DFilterFrameBuffer:
    """2D filter custom off screen (framebuffer in 0.3.0)."""

    width: int
    """ The off screen width, always canvas width in 0.3.0 (read-only).

    :type: int
    """

    height: int
    """ The off screen height, always canvas height in 0.3.0 (read-only).

    :type: int
    """

    colorBindCodes: typing.Any
    """ The bind code of the color textures attached to the off screen (read-only)."""

    depthBindCode: int
    """ The bind code of the depth texture attached to the off screen (read-only).

    :type: int
    """

    def getColorTexture(self, slot: int = 0):
        """Returns the color buffer as texture.

        :param slot: index of the slot (0-7).
        :type slot: int
        :return: Texture object.
        """

    def getDepthTexture(self):
        """Returns the depth buffer as texture.

        :return: Texture object.
        """

class KX_2DFilterManager:
    """2D filter manager used to add, remove and find filters in a scene."""

    def addFilter(self, index: int, type: int, fragmentProgram: str | None = ""):
        """Add a filter to the pass index `index`, type `type` and fragment program if custom filter.

                :param index: The filter pass index.
                :type index: int
                :param type: The filter type, one of:

        `bge.logic.RAS_2DFILTER_BLUR`

        `bge.logic.RAS_2DFILTER_DILATION`

        `bge.logic.RAS_2DFILTER_EROSION`

        `bge.logic.RAS_2DFILTER_SHARPEN`

        `bge.logic.RAS_2DFILTER_LAPLACIAN`

        `bge.logic.RAS_2DFILTER_PREWITT`

        `bge.logic.RAS_2DFILTER_SOBEL`

        `bge.logic.RAS_2DFILTER_GRAYSCALE`

        `bge.logic.RAS_2DFILTER_SEPIA`

        `bge.logic.RAS_2DFILTER_CUSTOMFILTER`
                :type type: int
                :param fragmentProgram: The filter shader fragment program.
        Specified only if `type` is `bge.logic.RAS_2DFILTER_CUSTOMFILTER`. (optional)
                :type fragmentProgram: str | None
                :return: The 2D Filter.
        """

    def removeFilter(self, index: int):
        """Remove filter to the pass index `index`.

        :param index: The filter pass index.
        :type index: int
        """

    def getFilter(self, index: int):
        """Return filter to the pass index `index`.

        :param index: The filter pass index.
        :type index: int
        :return: The filter in the specified pass index or None.
        """

class KX_BlenderMaterial:
    """This is kept for backward compatibility with some scripts."""

    textures: typing.Any
    """ List of all material's textures (read only)."""

class KX_Camera:
    """A Camera object."""

    INSIDE: typing.Any
    """ See `sphereInsideFrustum` and `boxInsideFrustum`"""

    INTERSECT: typing.Any
    """ See `sphereInsideFrustum` and `boxInsideFrustum`"""

    OUTSIDE: typing.Any
    """ See `sphereInsideFrustum` and `boxInsideFrustum`"""

    lens: float
    """ The camera's lens value.

    :type: float
    """

    lodDistanceFactor: float
    """ The factor to multiply distance to camera to adjust levels of detail.
A float < 1.0f will make the distance to camera used to compute
levels of detail decrease.

    :type: float
    """

    fov: float
    """ The camera's field of view value.

    :type: float
    """

    ortho_scale: float
    """ The camera's view scale when in orthographic mode.

    :type: float
    """

    near: float
    """ The camera's near clip distance.

    :type: float
    """

    far: float
    """ The camera's far clip distance.

    :type: float
    """

    shift_x: float
    """ The camera's horizontal shift.

    :type: float
    """

    shift_y: float
    """ The camera's vertical shift.

    :type: float
    """

    perspective: bool
    """ True if this camera has a perspective transform, False for an orthographic projection.

    :type: bool
    """

    projection_matrix: typing.Any
    """ This camera's 4x4 projection matrix."""

    modelview_matrix: typing.Any
    """ This camera's 4x4 model view matrix. (read-only)."""

    camera_to_world: typing.Any
    """ This camera's camera to world transform. (read-only)."""

    world_to_camera: typing.Any
    """ This camera's world to camera transform. (read-only)."""

    useViewport: bool
    """ True when the camera is used as a viewport, set True to enable a viewport for this camera.

    :type: bool
    """

    activityCulling: bool
    """ True if this camera is used to compute object distance for object activity culling.

    :type: bool
    """

    def sphereInsideFrustum(self, centre, radius: float) -> int:
        """Tests the given sphere against the view frustum.

        :param centre: The centre of the sphere (in world coordinates.)
        :param radius: the radius of the sphere
        :type radius: float
        :return: `~bge.types.KX_Camera.INSIDE`, `~bge.types.KX_Camera.OUTSIDE` or `~bge.types.KX_Camera.INTERSECT`
        :rtype: int
        """

    def boxInsideFrustum(self, box):
        """Tests the given box against the view frustum.

        :param box: Eight (8) corner points of the box (in world coordinates.)
        :return: `~bge.types.KX_Camera.INSIDE`, `~bge.types.KX_Camera.OUTSIDE` or `~bge.types.KX_Camera.INTERSECT`
        """

    def pointInsideFrustum(
        self, point: collections.abc.Sequence[float] | mathutils.Vector
    ) -> bool:
        """Tests the given point against the view frustum.

        :param point: The point to test (in world coordinates.)
        :type point: collections.abc.Sequence[float] | mathutils.Vector
        :return: True if the given point is inside this camera's viewing frustum.
        :rtype: bool
        """

    def getCameraToWorld(self):
        """Returns the camera-to-world transform.

        :return: the camera-to-world transform matrix.
        """

    def getWorldToCamera(self):
        """Returns the world-to-camera transform.This returns the inverse matrix of getCameraToWorld().

        :return: the world-to-camera transform matrix.
        """

    def setOnTop(self):
        """Set this cameras viewport ontop of all other viewport."""

    def setViewport(self, left: int, bottom: int, right: int, top: int):
        """Sets the region of this viewport on the screen in pixels.Use `bge.render.getWindowHeight` and `bge.render.getWindowWidth` to calculate values relative to the entire display.

        :param left: left pixel coordinate of this viewport
        :type left: int
        :param bottom: bottom pixel coordinate of this viewport
        :type bottom: int
        :param right: right pixel coordinate of this viewport
        :type right: int
        :param top: top pixel coordinate of this viewport
        :type top: int
        """

    def getScreenPosition(
        self, object: collections.abc.Sequence[float] | mathutils.Vector
    ):
        """Gets the position of an object projected on screen space.

        :param object: object name or list [x, y, z]
        :type object: collections.abc.Sequence[float] | mathutils.Vector
        :return: the object's position in screen coordinates.
        """

    def getScreenVect(
        self, x: float, y: float
    ) -> collections.abc.Sequence[float] | mathutils.Vector:
        """Gets the vector from the camera position in the screen coordinate direction.

        :param x: X Axis
        :type x: float
        :param y: Y Axis
        :type y: float
        :return: The vector from screen coordinate.
        :rtype: collections.abc.Sequence[float] | mathutils.Vector
        """

    def getScreenRay(
        self, x: float, y: float, dist: float = inf, property: str | None = None
    ):
        """Look towards a screen coordinate (x, y) and find first object hit within dist that matches prop.
        The ray is similar to KX_GameObject->rayCastTo.

                :param x: X Axis
                :type x: float
                :param y: Y Axis
                :type y: float
                :param dist: max distance to look (can be negative => look behind); 0 or omitted => detect up to other
                :type dist: float
                :param property: property name that object must have; can be omitted => detect any object
                :type property: str | None
                :return: the first object hit or None if no object or object does not match prop
        """

class KX_CharacterWrapper:
    """A wrapper to expose character physics options."""

    onGround: bool
    """ Whether or not the character is on the ground. (read-only)

    :type: bool
    """

    gravity: typing.Any
    """ The gravity vector used for the character."""

    fallSpeed: float
    """ The character falling speed.

    :type: float
    """

    maxJumps: int
    """ The maximum number of jumps a character can perform before having to touch the ground. By default this is set to 1. 2 allows for a double jump, etc.

    :type: int
    """

    jumpCount: int
    """ The current jump count. This can be used to have different logic for a single jump versus a double jump. For example, a different animation for the second jump.

    :type: int
    """

    jumpSpeed: float
    """ The character jumping speed.

    :type: float
    """

    maxSlope: float
    """ The maximum slope which the character can climb.

    :type: float
    """

    walkDirection: typing.Any
    """ The speed and direction the character is traveling in using world coordinates. This should be used instead of applyMovement() to properly move the character."""

    def jump(self):
        """The character jumps based on it's jump speed."""

    def setVelocity(
        self,
        velocity: collections.abc.Sequence[float] | mathutils.Vector,
        time: float,
        local: bool = False,
    ):
        """Sets the character's linear velocity for a given period.This method sets character's velocity through it's center of mass during a period.

                :param velocity: Linear velocity vector.
                :type velocity: collections.abc.Sequence[float] | mathutils.Vector
                :param time: Period while applying linear velocity.
                :type time: float
                :param local: False: you get the "global" velocity ie: relative to world orientation.

        True: you get the "local" velocity ie: relative to object orientation.
                :type local: bool
        """

    def reset(self):
        """Resets the character velocity and walk direction."""

class KX_CollisionContactPoint:
    """A collision contact point passed to the collision callbacks."""

    localPointA: mathutils.Vector
    """ The contact point in the owner object space.

    :type: mathutils.Vector
    """

    localPointB: mathutils.Vector
    """ The contact point in the collider object space.

    :type: mathutils.Vector
    """

    worldPoint: mathutils.Vector
    """ The contact point in world space.

    :type: mathutils.Vector
    """

    normal: mathutils.Vector
    """ The contact normal in owner object space.

    :type: mathutils.Vector
    """

    combinedFriction: float
    """ The combined friction of the owner and collider object.

    :type: float
    """

    combinedRollingFriction: float
    """ The combined rolling friction of the owner and collider object.

    :type: float
    """

    combinedRestitution: float
    """ The combined restitution of the owner and collider object.

    :type: float
    """

    appliedImpulse: float
    """ The applied impulse to the owner object.

    :type: float
    """

class KX_ConstraintWrapper:
    """KX_ConstraintWrapper"""

    constraint_id: int
    """ Returns the constraint ID  (read only)

    :type: int
    """

    constraint_type: int
    """ Returns the constraint type (read only)

    :type: int
    """

    breakingThreshold: typing.Any
    """ The impulse threshold breaking the constraint, if the constraint is broken `enabled` is set to False."""

    enabled: bool
    """ The status of the constraint. Set to True to restore a constraint after breaking.

    :type: bool
    """

    def getConstraintId(self, val) -> int:
        """Returns the constraint ID

        :param val:
        :return: the constraint ID
        :rtype: int
        """

    def setParam(self, axis: int, value0: float, value1: float):
        """Set the constraint limitsFor PHY_LINEHINGE_CONSTRAINT = 2 or PHY_ANGULAR_CONSTRAINT = 3:For PHY_CONE_TWIST_CONSTRAINT = 4:For PHY_GENERIC_6DOF_CONSTRAINT = 12:

        :param axis:
        :type axis: int
        :param value0: Set the minimum limit of the axisSet the minimum limit of the axisSet the minimum limit of the axisSet the linear velocity of the axisSet the stiffness of the spring
        :type value0: float
        :param value1: Set the maximum limit of the axisSet the maximum limit of the axisSet the maximum limit of the axisSet the maximum force limit of the axisTendency of the spring to return to it's original position
        :type value1: float
        """

    def getParam(self, axis: int) -> float:
        """Get the constraint position or euler angle of a generic 6DOF constraint

        :param axis:
        :type axis: int
        :return: positionangle
        :rtype: float
        """

class KX_FontObject:
    """A Font game object.It is possible to use attributes from :type: `~bpy.types.TextCurve`"""

class KX_GameObject:
    """All game objects are derived from this class.Properties assigned to game objects are accessible as attributes of this class.KX_GameObject can be subclassed to extend functionality. For example:When subclassing objects other than empties and meshes, the specific type
    should be used - e.g. inherit from `~bge.types.BL_ArmatureObject` when the object
    to mutate is an armature.The layer mask used for shadow and real-time cube map render.type

    integer (bit mask)0.3.0(You can use bpy.types.Object.bound_box instead) The object's bounding volume box used for culling.type

    `~bge.types.KX_BoundingBox`0.3.0Returns True if the object is culled, else False.This variable returns an invalid value if it is called outside the scene's callbacks `KX_Scene.pre_draw <~bge.types.KX_Scene.pre_draw>` and `KX_Scene.post_draw <~bge.types.KX_Scene.post_draw>`.type

    boolean (read only)0.3.0occlusion capability flag.type

    boolean0.3.0The object batch group containing the batched mesh.type

    `~bge.types.KX_BatchGroup`0.3.0Sets the game object's occlusion capability.arg occlusion

    the state to set the occlusion to.

    type occlusion

    boolean

    arg recursive

    optional argument to set all childrens visibility flag too, defaults to False if no value passed.

    type recursive

    boolean0.3.0Gets the game object's reaction force.The reaction force is the force applied to this object over the last simulation timestep.
    This also includes impulses, eg from collisions.return

    the reaction force of this object.

    rtype

    Vector((fx, fy, fz))This is not implemented at the moment. (Removed when switching from Sumo to Bullet)0.0.0
    """

    name: str
    """ The object's name.

    :type: str
    """

    mass: float
    """ The object's mass

    :type: float
    """

    friction: float
    """ The object's friction

    :type: float
    """

    isSuspendDynamics: bool
    """ The object's dynamic state (read-only).:py:meth:`suspendDynamics` and :py:meth:`restoreDynamics` allow you to change the state.

    :type: bool
    """

    linearDamping: typing.Any
    """ The object's linear damping, also known as translational damping. Can be set simultaneously with angular damping using the `setDamping` method."""

    angularDamping: typing.Any
    """ The object's angular damping, also known as rotationation damping. Can be set simultaneously with linear damping using the `setDamping` method."""

    linVelocityMin: float
    """ Enforces the object keeps moving at a minimum velocity.

    :type: float
    """

    linVelocityMax: float
    """ Clamp the maximum linear velocity to prevent objects moving beyond a set speed.

    :type: float
    """

    angularVelocityMin: typing.Any
    """ Enforces the object keeps rotating at a minimum velocity. A value of 0.0 disables this."""

    angularVelocityMax: typing.Any
    """ Clamp the maximum angular velocity to prevent objects rotating beyond a set speed.
A value of 0.0 disables clamping; it does not stop rotation."""

    localInertia: typing.Any
    """ the object's inertia vector in local coordinates. Read only."""

    parent: typing.Any
    """ The object's parent object. (read-only)."""

    groupMembers: typing.Any
    """ Returns the list of group members if the object is a group object (dupli group instance), otherwise None is returned."""

    groupObject: typing.Any
    """ Returns the group object (dupli group instance) that the object belongs to or None if the object is not part of a group."""

    collisionGroup: typing.Any
    """ The object's collision group."""

    collisionMask: typing.Any
    """ The object's collision mask."""

    collisionCallbacks: typing.Any
    """ A list of functions to be called when a collision occurs.Callbacks should either accept one argument (object), or four
arguments (object, point, normal, points). For simplicity, per
colliding object the first collision point is reported in second
and third argument."""

    scene: typing.Any
    """ The object's scene. (read-only)."""

    visible: bool
    """ visibility flag.

    :type: bool
    """

    layer: typing.Any
    cullingBox: typing.Any
    culled: typing.Any
    color: mathutils.Vector
    """ The object color of the object. [r, g, b, a]

    :type: mathutils.Vector
    """

    physicsCulling: bool
    """ True if the object suspends its physics depending on its nearest distance to any camera.

    :type: bool
    """

    logicCulling: bool
    """ True if the object suspends its logic and animation depending on its nearest distance to any camera.

    :type: bool
    """

    physicsCullingRadius: float
    """ Suspend object's physics if this radius is smaller than its nearest distance to any camera
and `physicsCulling` set to True.

    :type: float
    """

    logicCullingRadius: float
    """ Suspend object's logic and animation if this radius is smaller than its nearest distance to any camera
and `logicCulling` set to True.

    :type: float
    """

    occlusion: typing.Any
    position: mathutils.Vector
    """ The object's position. [x, y, z] On write: local position, on read: world positionUse `localPosition` and `worldPosition`.0.0.1

    :type: mathutils.Vector
    """

    orientation: mathutils.Matrix
    """ The object's orientation. 3x3 Matrix. You can also write a Quaternion or Euler vector. On write: local orientation, on read: world orientationUse `localOrientation` and `worldOrientation`.0.0.1

    :type: mathutils.Matrix
    """

    scaling: mathutils.Vector
    """ The object's scaling factor. [sx, sy, sz] On write: local scaling, on read: world scalingUse `localScale` and `worldScale`.0.0.1

    :type: mathutils.Vector
    """

    localOrientation: mathutils.Matrix
    """ The object's local orientation. 3x3 Matrix. You can also write a Quaternion or Euler vector.

    :type: mathutils.Matrix
    """

    worldOrientation: mathutils.Matrix
    """ The object's world orientation. 3x3 Matrix.

    :type: mathutils.Matrix
    """

    localScale: mathutils.Vector
    """ The object's local scaling factor. [sx, sy, sz]

    :type: mathutils.Vector
    """

    worldScale: mathutils.Vector
    """ The object's world scaling factor. [sx, sy, sz]

    :type: mathutils.Vector
    """

    localPosition: mathutils.Vector
    """ The object's local position. [x, y, z]

    :type: mathutils.Vector
    """

    worldPosition: mathutils.Vector
    """ The object's world position. [x, y, z]

    :type: mathutils.Vector
    """

    localTransform: mathutils.Matrix
    """ The object's local space transform matrix. 4x4 Matrix.

    :type: mathutils.Matrix
    """

    worldTransform: mathutils.Matrix
    """ The object's world space transform matrix. 4x4 Matrix.

    :type: mathutils.Matrix
    """

    localLinearVelocity: mathutils.Vector
    """ The object's local linear velocity. [x, y, z]

    :type: mathutils.Vector
    """

    worldLinearVelocity: mathutils.Vector
    """ The object's world linear velocity. [x, y, z]

    :type: mathutils.Vector
    """

    localAngularVelocity: mathutils.Vector
    """ The object's local angular velocity. [x, y, z]

    :type: mathutils.Vector
    """

    worldAngularVelocity: mathutils.Vector
    """ The object's world angular velocity. [x, y, z]

    :type: mathutils.Vector
    """

    gravity: mathutils.Vector
    """ The object's gravity. [x, y, z]

    :type: mathutils.Vector
    """

    timeOffset: float
    """ adjust the slowparent delay at runtime.

    :type: float
    """

    blenderObject: typing.Any
    """ This KX_GameObject's Object."""

    state: int
    """ the game object's state bitmask, using the first 30 bits, one bit must always be set.

    :type: int
    """

    meshes: typing.Any
    """ a list meshes for this object."""

    batchGroup: typing.Any
    sensors: list
    """ a sequence of `~bge.types.SCA_ISensor` objects with string/index lookups and iterator support.

    :type: list
    """

    controllers: typing.Any
    """ a sequence of `~bge.types.SCA_IController` objects with string/index lookups and iterator support."""

    actuators: list
    """ a list of `~bge.types.SCA_IActuator` with string/index lookups and iterator support.

    :type: list
    """

    attrDict: dict
    """ get the objects internal python attribute dictionary for direct (faster) access.

    :type: dict
    """

    components: typing.Any
    """ All python components."""

    children: typing.Any
    """ direct children of this object, (read-only)."""

    childrenRecursive: typing.Any
    """ all children of this object including children's children, (read-only)."""

    life: float
    """ The number of frames until the object ends, assumes one frame is 1/60 second (read-only).

    :type: float
    """

    debug: bool
    """ If true, the object's debug properties will be displayed on screen.

    :type: bool
    """

    debugRecursive: bool
    """ If true, the object's and children's debug properties will be displayed on screen.

    :type: bool
    """

    currentLodLevel: int
    """ The index of the level of detail (LOD) currently used by this object (read-only).

    :type: int
    """

    lodManager: typing.Any
    """ Return the lod manager of this object.
Needed to access to lod manager to set attributes of levels of detail of this object.
The lod manager is shared between instance objects and can be changed to use the lod levels of an other object.
If the lod manager is set to None the object's mesh backs to the mesh of the previous first lod level."""

    onRemove: list
    """ A list of callables to run when the KX_GameObject is destroyed.or

    :type: list
    """

    logger: typing.Any
    """ A logger instance that can be used to log messages related to this object (read-only)."""

    loggerName: str
    """ A name used to create the logger instance. By default, it takes the form Type[Name]
and can be optionally overridden as below:

    :type: str
    """

    def endObject(self):
        """Delete this object, can be used in place of the EndObject Actuator.The actual removal of the object from the scene is delayed."""

    def replaceMesh(
        self, mesh: str, useDisplayMesh: bool = True, usePhysicsMesh: bool = False
    ):
        """Replace the mesh of this object with a new mesh. This works the same was as the actuator.

        :param mesh: mesh to replace or the meshes name.
        :type mesh: str
        :param useDisplayMesh: when enabled the display mesh will be replaced (optional argument).
        :type useDisplayMesh: bool
        :param usePhysicsMesh: when enabled the physics mesh will be replaced (optional argument).
        :type usePhysicsMesh: bool
        """

    def setVisible(self, visible: bool, recursive: bool | None = False):
        """Sets the game object's visible flag.

        :param visible: the visible state to set.
        :type visible: bool
        :param recursive: optional argument to set all childrens visibility flag too, defaults to False if no value passed.
        :type recursive: bool | None
        """

    def setOcclusion(self, occlusion, recursive):
        """

        :param occlusion:
        :param recursive:
        """

    def alignAxisToVect(
        self,
        vect: collections.abc.Sequence[float] | mathutils.Vector,
        axis: int = 2,
        factor: float = 1.0,
    ):
        """Aligns any of the game object's axis along the given vector.

                :param vect: a vector to align the axis.
                :type vect: collections.abc.Sequence[float] | mathutils.Vector
                :param axis: The axis you want to align

        0: X axis

        1: Y axis

        2: Z axis
                :type axis: int
                :param factor: Only rotate a fraction of the distance to the target vector (0.0 - 1.0)
                :type factor: float
        """

    def getAxisVect(self, vect: collections.abc.Sequence[float] | mathutils.Vector):
        """Returns the axis vector rotates by the object's worldspace orientation.
        This is the equivalent of multiplying the vector by the orientation matrix.

                :param vect: a vector to align the axis.
                :type vect: collections.abc.Sequence[float] | mathutils.Vector
                :return: The vector in relation to the objects rotation.
        """

    def applyMovement(
        self, movement: collections.abc.Sequence[float] | mathutils.Vector, local
    ):
        """Sets the game object's movement.

                :param movement: movement vector.
                :type movement: collections.abc.Sequence[float] | mathutils.Vector
                :param local: False: you get the "global" movement ie: relative to world orientation.

        True: you get the "local" movement ie: relative to object orientation.

        Default to False if not passed.boolean
        """

    def applyRotation(
        self, rotation: collections.abc.Sequence[float] | mathutils.Vector, local
    ):
        """Sets the game object's rotation.

                :param rotation: rotation vector.
                :type rotation: collections.abc.Sequence[float] | mathutils.Vector
                :param local: False: you get the "global" rotation ie: relative to world orientation.

        True: you get the "local" rotation ie: relative to object orientation.

        Default to False if not passed.boolean
        """

    def applyForce(
        self, force: collections.abc.Sequence[float] | mathutils.Vector, local: bool
    ):
        """Sets the game object's force.This requires a dynamic object.

                :param force: force vector.
                :type force: collections.abc.Sequence[float] | mathutils.Vector
                :param local: False: you get the "global" force ie: relative to world orientation.

        True: you get the "local" force ie: relative to object orientation.

        Default to False if not passed.
                :type local: bool
        """

    def applyTorque(
        self, torque: collections.abc.Sequence[float] | mathutils.Vector, local: bool
    ):
        """Sets the game object's torque.This requires a dynamic object.

                :param torque: torque vector.
                :type torque: collections.abc.Sequence[float] | mathutils.Vector
                :param local: False: you get the "global" torque ie: relative to world orientation.

        True: you get the "local" torque ie: relative to object orientation.

        Default to False if not passed.
                :type local: bool
        """

    def getLinearVelocity(self, local: bool):
        """Gets the game object's linear velocity.This method returns the game object's velocity through it's center of mass, ie no angular velocity component.

                :param local: False: you get the "global" velocity ie: relative to world orientation.

        True: you get the "local" velocity ie: relative to object orientation.

        Default to False if not passed.
                :type local: bool
                :return: the object's linear velocity.
        """

    def setLinearVelocity(
        self, velocity: collections.abc.Sequence[float] | mathutils.Vector, local: bool
    ):
        """Sets the game object's linear velocity.This method sets game object's velocity through it's center of mass,
        ie no angular velocity component.This requires a dynamic object.

                :param velocity: linear velocity vector.
                :type velocity: collections.abc.Sequence[float] | mathutils.Vector
                :param local: False: you get the "global" velocity ie: relative to world orientation.

        True: you get the "local" velocity ie: relative to object orientation.

        Default to False if not passed.
                :type local: bool
        """

    def getAngularVelocity(self, local: bool):
        """Gets the game object's angular velocity.

                :param local: False: you get the "global" velocity ie: relative to world orientation.

        True: you get the "local" velocity ie: relative to object orientation.

        Default to False if not passed.
                :type local: bool
                :return: the object's angular velocity.
        """

    def setAngularVelocity(self, velocity: bool, local):
        """Sets the game object's angular velocity.This requires a dynamic object.

                :param velocity: angular velocity vector.
                :type velocity: bool
                :param local: False: you get the "global" velocity ie: relative to world orientation.

        True: you get the "local" velocity ie: relative to object orientation.

        Default to False if not passed.
        """

    def getVelocity(
        self, point: collections.abc.Sequence[float] | mathutils.Vector | None = []
    ):
        """Gets the game object's velocity at the specified point.Gets the game object's velocity at the specified point, including angular
        components.

                :param point: optional point to return the velocity for, in local coordinates, defaults to (0, 0, 0) if no value passed.
                :type point: collections.abc.Sequence[float] | mathutils.Vector | None
                :return: the velocity at the specified point.
        """

    def getReactionForce(self): ...
    def applyImpulse(
        self,
        point,
        impulse: collections.abc.Sequence[float] | mathutils.Vector,
        local: bool,
    ):
        """Applies an impulse to the game object.This will apply the specified impulse to the game object at the specified point.
        If point != position, applyImpulse will also change the object's angular momentum.
        Otherwise, only linear momentum will change.

                :param point: the point to apply the impulse to (in world or local coordinates)
                :param impulse: impulse vector.
                :type impulse: collections.abc.Sequence[float] | mathutils.Vector
                :param local: False: you get the "global" impulse ie: relative to world coordinates with world orientation.

        True: you get the "local" impulse ie: relative to local coordinates with object orientation.

        Default to False if not passed.
                :type local: bool
        """

    def setDamping(self, linear_damping, angular_damping):
        """Sets both the `linearDamping` and `angularDamping` simultaneously. This is more efficient than setting both properties individually.

        :param linear_damping: Linear ("translational") damping factor.
        :param angular_damping: Angular ("rotational") damping factor.
        """

    def suspendPhysics(self, freeConstraints: bool):
        """Suspends physics for this object.

                :param freeConstraints: When set to True physics constraints used by the object are deleted.
        Else when False (the default) constraints are restored when restoring physics.
                :type freeConstraints: bool
        """

    def restorePhysics(self):
        """Resumes physics for this object. Also reinstates collisions."""

    def suspendDynamics(self, ghost: bool):
        """Suspends dynamics physics for this object.:py:attr:`isSuspendDynamics` allows you to inspect whether the object is in a suspended state.

                :param ghost: When set to True, collisions with the object will be ignored, similar to the "ghost" checkbox in
        Blender. When False (the default), the object becomes static but still collide with other objects.
                :type ghost: bool
        """

    def restoreDynamics(self):
        """Resumes dynamics physics for this object. Also reinstates collisions; the object will no longer be a ghost."""

    def enableRigidBody(self):
        """Enables rigid body physics for this object.Rigid body physics allows the object to roll on collisions."""

    def disableRigidBody(self):
        """Disables rigid body physics for this object."""

    def setCcdMotionThreshold(self, ccd_motion_threshold):
        """Sets `ccdMotionThreshold` that is the delta of movement that has to happen in one physics tick to trigger the continuous motion detection.

        :param ccd_motion_threshold: delta of movement.
        """

    def setCcdSweptSphereRadius(self, ccd_swept_sphere_radius):
        """Sets `ccdSweptSphereRadius` that is the radius of the sphere that is used to check for possible collisions when ccd is activated.

        :param ccd_swept_sphere_radius: sphere radius.
        """

    def setParent(self, parent, compound: bool = True, ghost: bool = True):
        """Sets this object's parent.
        Control the shape status with the optional compound and ghost parameters:In that case you can control if it should be ghost or not:

                :param parent: new parent object.
                :param compound: whether the shape should be added to the parent compound shape.

        True: the object shape should be added to the parent compound shape.

        False: the object should keep its individual shape.
                :type compound: bool
                :param ghost: whether the object should be ghost while parented.

        True: if the object should be made ghost while parented.

        False: if the object should be solid while parented.
                :type ghost: bool
        """

    def removeParent(self):
        """Removes this objects parent."""

    def getPhysicsId(self):
        """Returns the user data object associated with this game object's physics controller."""

    def getPropertyNames(self) -> list:
        """Gets a list of all property names.

        :return: All property names for this object.
        :rtype: list
        """

    def getDistanceTo(self, other) -> float:
        """

        :param other: a point or another `~bge.types.KX_GameObject` to measure the distance to.
        :return: distance to another object or point.
        :rtype: float
        """

    def getVectTo(self, other):
        """Returns the vector and the distance to another object or point.
        The vector is normalized unless the distance is 0, in which a zero length vector is returned.

                :param other: a point or another `~bge.types.KX_GameObject` to get the vector and distance to.
                :return: (distance, globalVector(3), localVector(3))
        """

    def rayCastTo(self, other, dist: float = 0, prop: str = ""):
        """Look towards another point/object and find first object hit within dist that matches prop.The ray is always casted from the center of the object, ignoring the object itself.
        The ray is casted towards the center of another object or an explicit [x, y, z] point.
        Use rayCast() if you need to retrieve the hit point

                :param other: [x, y, z] or object towards which the ray is casted
                :param dist: max distance to look (can be negative => look behind); 0 or omitted => detect up to other
                :type dist: float
                :param prop: property name that object must have; can be omitted => detect any object
                :type prop: str
                :return: the first object hit or None if no object or object does not match prop
        """

    def rayCast(
        self,
        objto,
        objfrom=None,
        dist: float = 0,
        prop: str = "",
        face: int = False,
        xray: int = False,
        poly: int = 0,
        mask=65535,
    ):
        """Look from a point/object to another point/object and find first object hit within dist that matches prop.
        if poly is 0, returns a 3-tuple with object reference, hit point and hit normal or (None, None, None) if no hit.
        if poly is 1, returns a 4-tuple with in addition a `~bge.types.KX_PolyProxy` as 4th element.
        if poly is 2, returns a 5-tuple with in addition a 2D vector with the UV mapping of the hit point as 5th element.The face parameter determines the orientation of the normal.The ray has X-Ray capability if xray parameter is 1, otherwise the first object hit (other than self object) stops the ray.
        The prop and xray parameters interact as follow.The `~bge.types.KX_PolyProxy` 4th element of the return tuple when poly=1 allows to retrieve information on the polygon hit by the ray.
        If there is no hit or the hit object is not a static mesh, None is returned as 4th element.The ray ignores collision-free objects and faces that dont have the collision flag enabled, you can however use ghost objects.

                :param objto: [x, y, z] or object to which the ray is casted
                :param objfrom: [x, y, z] or object from which the ray is casted; None or omitted => use self object center
                :param dist: max distance to look (can be negative => look behind); 0 or omitted => detect up to to
                :type dist: float
                :param prop: property name that object must have; can be omitted or "" => detect any object
                :type prop: str
                :param face: normal option: 1=>return face normal; 0 or omitted => normal is oriented towards origin
                :type face: int
                :param xray: X-ray option: 1=>skip objects that don't match prop; 0 or omitted => stop on first object
                :type xray: int
                :param poly: polygon option: 0, 1 or 2 to return a 3-, 4- or 5-tuple with information on the face hit.

        0 or omitted: return value is a 3-tuple (object, hitpoint, hitnormal) or (None, None, None) if no hit

        1: return value is a 4-tuple and the 4th element is a `~bge.types.KX_PolyProxy` or None if no hit or the object doesn't use a mesh collision shape.

        2: return value is a 5-tuple and the 5th element is a 2-tuple (u, v) with the UV mapping of the hit point or None if no hit, or the object doesn't use a mesh collision shape, or doesn't have a UV mapping.
                :type poly: int
                :param mask: collision mask: The collision mask (16 layers mapped to a 16-bit integer) is combined with each object's collision group, to hit only a subset of the objects in the scene. Only those objects for which collisionGroup & mask is true can be hit.
                :return: (object, hitpoint, hitnormal) or (object, hitpoint, hitnormal, polygon) or (object, hitpoint, hitnormal, polygon, hituv).

        object, hitpoint and hitnormal are None if no hit.

        polygon is valid only if the object is valid and is a static object, a dynamic object using mesh collision shape or a soft body object, otherwise it is None

        hituv is valid only if polygon is valid and the object has a UV mapping, otherwise it is None
        """

    def collide(
        self, obj: str | typing_extensions.Self
    ) -> list[KX_CollisionContactPoint]:
        """Test if this object collides object `obj`.

                :param obj: the object to test collision with
                :type obj: str | typing_extensions.Self
                :return: (collide, points)

        collide, True if this object collides object `obj`

        points, contact point data of the collision or None
                :rtype: list[KX_CollisionContactPoint]
        """

    def setCollisionMargin(self, margin: float):
        """Set the objects collision margin.

        :param margin: the collision margin distance in blender units.
        :type margin: float
        """

    def sendMessage(self, subject: str, body: str = "", to: str = ""):
        """Sends a message.

        :param subject: The subject of the message
        :type subject: str
        :param body: The body of the message (optional)
        :type body: str
        :param to: The name of the object to send the message to (optional)
        :type to: str
        """

    def reinstancePhysicsMesh(
        self,
        gameObject: str | None = "",
        meshObject: str | None = "",
        dupli: bool | None = False,
        evaluated: bool | None = False,
    ) -> bool:
        """Updates the physics system with the changed mesh.If no arguments are given the physics mesh will be re-created from the first mesh assigned to the game object.

        :param gameObject: optional argument, set the physics shape from this gameObjets mesh.
        :type gameObject: str | None
        :param meshObject: optional argument, set the physics shape from this mesh.
        :type meshObject: str | None
        :param dupli: optional argument, duplicate the physics shape.
        :type dupli: bool | None
        :param evaluated: optional argument, use evaluated object physics shape (Object with modifiers applied).
        :type evaluated: bool | None
        :return: True if reinstance succeeded, False if it failed.
        :rtype: bool
        """

    def replacePhysicsShape(self, gameObject: str) -> bool:
        """Replace the current physics shape.

        :param gameObject: set the physics shape from this gameObjets.
        :type gameObject: str
        :return: True if replace succeeded, False if it failed.
        :rtype: bool
        """

    def get(self, key, default):
        """Return the value matching key, or the default value if its not found.
        :arg key: the matching key
        :type key: string
        :arg default: optional default value is the key isn't matching, defaults to None if no value passed.
        :return: The key value or a default.

                :param key:
                :param default:
        """

    def playAction(
        self,
        name: str,
        start_frame,
        end_frame,
        layer: int = 0,
        priority: int = 0,
        blendin: float = 0,
        play_mode: int = KX_ACTION_MODE_PLAY,
        layer_weight: float = 0.0,
        ipo_flags=0,
        speed: float = 1.0,
        blend_mode: int = KX_ACTION_BLEND_BLEND,
    ):
        """Plays an action.

        :param name: the name of the action.
        :type name: str
        :param start_frame:
        :param end_frame:
        :param layer: the layer the action will play in (actions in different layers are added/blended together).
        :type layer: int
        :param priority: only play this action if there isn't an action currently playing in this layer with a higher (lower number) priority.
        :type priority: int
        :param blendin: the amount of blending between this animation and the previous one on this layer.
        :type blendin: float
        :param play_mode: the play mode. one of `these constants <gameobject-playaction-mode>`.
        :type play_mode: int
        :param layer_weight: how much of the previous layer to use for blending.
        :type layer_weight: float
        :param ipo_flags: flags for the old IPO behaviors (force, etc).
        :param speed: the playback speed of the action as a factor (1.0 = normal speed, 2.0 = 2x speed, etc).
        :type speed: float
        :param blend_mode: how to blend this layer with previous layers. one of `these constants <gameobject-playaction-blend>`.
        :type blend_mode: int
        """

    def stopAction(self, layer: int):
        """Stop playing the action on the given layer.

        :param layer: The layer to stop playing, defaults to 0 if no value passed.
        :type layer: int
        """

    def getActionFrame(self, layer: int) -> float:
        """Gets the current frame of the action playing in the supplied layer.

        :param layer: The layer that you want to get the frame from, defaults to 0 if no value passed.
        :type layer: int
        :return: The current frame of the action
        :rtype: float
        """

    def getActionName(self, layer: int) -> str:
        """Gets the name of the current action playing in the supplied layer.

        :param layer: The layer that you want to get the action name from, defaults to 0 if no value passed.
        :type layer: int
        :return: The name of the current action
        :rtype: str
        """

    def setActionFrame(self, frame: float, layer: int):
        """Set the current frame of the action playing in the supplied layer.

        :param frame: The frame to set the action to
        :type frame: float
        :param layer: The layer where you want to set the frame, defaults to 0 if no value passed.
        :type layer: int
        """

    def isPlayingAction(self, layer: int) -> bool:
        """Checks to see if there is an action playing in the given layer.

        :param layer: The layer to check for a playing action, defaults to 0 if no value passed.
        :type layer: int
        :return: Whether or not the action is playing
        :rtype: bool
        """

    def addDebugProperty(self, name: str, debug: bool):
        """Adds a single debug property to the debug list.

        :param name: name of the property that added to the debug list.
        :type name: str
        :param debug: the debug state, defaults to True if no value passed.
        :type debug: bool
        """

class KX_LibLoadStatus:
    """Libload is deprecated since 0.3.0. An object providing information about a LibLoad() operation."""

    onFinish: collections.abc.Callable
    """ A callback that gets called when the lib load is done.

    :type: collections.abc.Callable
    """

    finished: bool
    """ The current status of the lib load.

    :type: bool
    """

    progress: float
    """ The current progress of the lib load as a normalized value from 0.0 to 1.0.

    :type: float
    """

    libraryName: str
    """ The name of the library being loaded (the first argument to LibLoad).

    :type: str
    """

    timeTaken: float
    """ The amount of time, in seconds, the lib load took (0 until the operation is complete).

    :type: float
    """

class KX_LightObject:
    """A Light game object.It is possible to use attributes from :type: `~bpy.types.Light`"""

class KX_LodLevel:
    """A single lod level for a game object lod manager.Return True if the lod level uses a different mesh than the original object mesh. (read only)type

    boolean0.3.0Return True if the lod level uses a different material than the original object mesh material. (read only)type

    boolean0.3.0
    """

    mesh: typing.Any
    """ The mesh used for this lod level. (read only)"""

    level: int
    """ The number of the lod level. (read only)

    :type: int
    """

    distance: typing.Any
    """ Distance to begin using this level of detail. (read only)"""

    hysteresis: typing.Any
    """ Minimum distance factor change required to transition to the previous level of detail in percent. (read only)"""

    useMesh: typing.Any
    useMaterial: typing.Any
    useHysteresis: bool
    """ Return true if the lod level uses hysteresis override. (read only)

    :type: bool
    """

class KX_LodManager:
    """This class contains a list of all levels of detail used by a game object."""

    levels: typing.Any
    """ Return the list of all levels of detail of the lod manager."""

    distanceFactor: float
    """ Method to multiply the distance to the camera.

    :type: float
    """

class KX_MeshProxy:
    """A mesh object.You can only change the vertex properties of a mesh object, not the mesh topology.To use mesh objects effectively, you should know a bit about how the game engine handles them.The correct method of iterating over every `~bge.types.KX_VertexProxy` in a game object"""

    materials: typing.Any
    numPolygons: int
    """ 

    :type: int
    """

    numMaterials: int
    """ 

    :type: int
    """

    polygons: typing.Any
    """ Returns the list of polygons of this mesh."""

    def getMaterialName(self, matid: int) -> str:
        """Gets the name of the specified material.

        :param matid: the specified material.
        :type matid: int
        :return: the attached material name.
        :rtype: str
        """

    def getTextureName(self, matid: int) -> str:
        """Gets the name of the specified material's texture.

        :param matid: the specified material
        :type matid: int
        :return: the attached material's texture name.
        :rtype: str
        """

    def getVertexArrayLength(self, matid: int) -> int:
        """Gets the length of the vertex array associated with the specified material.There is one vertex array for each material.

        :param matid: the specified material
        :type matid: int
        :return: the number of vertices in the vertex array.
        :rtype: int
        """

    def getVertex(self, matid: int, index: int):
        """Gets the specified vertex from the mesh object.

        :param matid: the specified material
        :type matid: int
        :param index: the index into the vertex array.
        :type index: int
        :return: a vertex object.
        """

    def getPolygon(self, index: int):
        """Gets the specified polygon from the mesh.

        :param index: polygon number
        :type index: int
        :return: a polygon object.
        """

    def transform(self, matid: int, matrix):
        """Transforms the vertices of a mesh.

        :param matid: material index, -1 transforms all.
        :type matid: int
        :param matrix: transformation matrix.
        """

    def transformUV(
        self, matid: int, matrix, uv_index: int = -1, uv_index_from: int = -1
    ):
        """Transforms the vertices UV's of a mesh.

        :param matid: material index, -1 transforms all.
        :type matid: int
        :param matrix: transformation matrix.
        :param uv_index: optional uv index, -1 for all, otherwise 0 or 1.
        :type uv_index: int
        :param uv_index_from: optional uv index to copy from, -1 to transform the current uv.
        :type uv_index_from: int
        """

    def replaceMaterial(self, matid: int, material):
        """Replace the material in slot `matid` by the material `material`.

        :param matid: The material index.
        :type matid: int
        :param material: The material replacement.
        """

class KX_NavMeshObject:
    """Python interface for using and controlling navigation meshes."""

    def findPath(self, start, goal):
        """Finds the path from start to goal points.

        :param start: the start point3D Vector3D Vector
        :param goal: the goal point
        :return: a path as a list of points
        """

    def raycast(self, start, goal) -> float:
        """Raycast from start to goal points.

        :param start: the start point3D Vector3D Vector
        :param goal: the goal point
        :return: the hit factor
        :rtype: float
        """

    def draw(self, mode):
        """Draws a debug mesh for the navigation mesh.

        :param mode: the drawing mode (one of `these constants <navmesh-draw-mode>`)integer
        :return: None
        """

    def rebuild(self):
        """Rebuild the navigation mesh.

        :return: None
        """

class KX_PolyProxy:
    """A polygon holds the index of the vertex forming the poylgon.Note:
    The polygon attributes are read-only, you need to retrieve the vertex proxy if you want
    to change the vertex settings.
    """

    material_name: str
    """ The name of polygon material, empty if no material.

    :type: str
    """

    material: typing.Any
    """ The material of the polygon."""

    texture_name: str
    """ The texture name of the polygon.

    :type: str
    """

    material_id: int
    """ The material index of the polygon, use this to retrieve vertex proxy from mesh proxy.

    :type: int
    """

    v1: int
    """ vertex index of the first vertex of the polygon, use this to retrieve vertex proxy from mesh proxy.

    :type: int
    """

    v2: int
    """ vertex index of the second vertex of the polygon, use this to retrieve vertex proxy from mesh proxy.

    :type: int
    """

    v3: int
    """ vertex index of the third vertex of the polygon, use this to retrieve vertex proxy from mesh proxy.

    :type: int
    """

    v4: int
    """ Vertex index of the fourth vertex of the polygon, 0 if polygon has only 3 vertex
Use this to retrieve vertex proxy from mesh proxy.

    :type: int
    """

    visible: int
    """ visible state of the polygon: 1=visible, 0=invisible.

    :type: int
    """

    collide: int
    """ collide state of the polygon: 1=receives collision, 0=collision free.

    :type: int
    """

    vertices: typing.Any
    """ Returns the list of vertices of this polygon."""

    def getMaterialName(self) -> str:
        """Returns the polygon material name with MA prefix

        :return: material name
        :rtype: str
        """

    def getMaterial(self):
        """

        :return: The polygon material
        """

    def getTextureName(self) -> str:
        """

        :return: The texture name
        :rtype: str
        """

    def getMaterialIndex(self) -> int:
        """Returns the material bucket index of the polygon.
        This index and the ones returned by getVertexIndex() are needed to retrieve the vertex proxy from `~bge.types.KX_MeshProxy`.

                :return: the material index in the mesh
                :rtype: int
        """

    def getNumVertex(self) -> int:
        """Returns the number of vertex of the polygon.

        :return: number of vertex, 3 or 4.
        :rtype: int
        """

    def isVisible(self) -> bool:
        """Returns whether the polygon is visible or not

        :return: 0=invisible, 1=visible
        :rtype: bool
        """

    def isCollider(self) -> int:
        """Returns whether the polygon is receives collision or not

        :return: 0=collision free, 1=receives collision
        :rtype: int
        """

    def getVertexIndex(self, vertex) -> int:
        """Returns the mesh vertex index of a polygon vertex
        This index and the one returned by getMaterialIndex() are needed to retrieve the vertex proxy from `~bge.types.KX_MeshProxy`.

                :param vertex: index of the vertex in the polygon: 0->3integer
                :return: mesh vertex index
                :rtype: int
        """

    def getMesh(self):
        """Returns a mesh proxy

        :return: mesh proxy
        """

class KX_PythonComponent:
    """Python component can be compared to python logic bricks with parameters.
    The python component is a script loaded in the UI, this script defined a component class by inheriting from `~bge.types.KX_PythonComponent`.
    This class must contain a dictionary of properties: `args` and two default functions: `start` and `update`.The script must have .py extension.The component properties are loaded from the `args` attribute from the UI at loading time.
    When the game start the function `start` is called with as arguments a dictionary of the properties' name and value.
    The `update` function is called every frames during the logic stage before running logics bricks,
    the goal of this function is to handle and process everything.The following component example moves and rotates the object when pressing the keys W, A, S and D.Since the components are loaded for the first time outside the bge, then `bge` is a fake module that contains only the class
    `~bge.types.KX_PythonComponent` to avoid importing all the bge modules.
    This behavior is safer but creates some issues at loading when the user want to use functions or attributes from the bge modules other
    than the `~bge.types.KX_PythonComponent` class. The way is to not call these functions at loading outside the bge. To detect it, the bge
    module contains the attribute `__component__` when it's imported outside the bge.The following component example add a "Cube" object at initialization and move it along x for each update. It shows that the user can
    use functions from scene and load the component outside the bge by setting global attributes in a condition at the beginning of the
    script.The property types supported are float, integer, boolean, string, set (for enumeration) and Vector 2D, 3D and 4D. The following example
    show all of these property types.
    """

    object: typing.Any
    """ The object owner of the component."""

    args: dict
    """ Dictionary of the component properties, the keys are string and the value can be: float, integer, Vector(2D/3D/4D), set, string.

    :type: dict
    """

    logger: typing.Any
    """ A logger instance that can be used to log messages related to this object (read-only)."""

    loggerName: str
    """ A name used to create the logger instance. By default, it takes the form Type[Name]
and can be optionally overridden as below:

    :type: str
    """

    def start(self, args: dict):
        """Initialize the component.

        :param args: The dictionary of the properties' name and value.
        :type args: dict
        """

    def update(self):
        """Process the logic of the component."""

    def dispose(self):
        """Function called when the component is destroyed."""

class KX_Scene:
    """An active scene that gives access to objects, cameras, lights and scene attributes.The activity culling stuff is supposed to disable logic bricks when their owner gets too far
    from the active camera.  It was taken from some code lurking at the back of KX_Scene - who knows
    what it does!@bug: All attributes are read only at the moment.The override camera used for scene culling, if set to None the culling is proceeded with the camera used to render.type

    `~bge.types.KX_Camera` or None0.3.0The current active world, (read-only).type

    `~bge.types.KX_WorldInfo`0.3.0True if the scene is suspended, (read-only).type

    boolean0.3.0True when Dynamic Bounding box Volume Tree is set (read-only).type

    boolean0.3.0Suspends this scene.0.3.0Resume this scene.0.3.0
    """

    name: str
    """ The scene's name, (read-only).

    :type: str
    """

    objects: typing.Any
    """ A list of objects in the scene, (read-only)."""

    objectsInactive: typing.Any
    """ A list of objects on background layers (used for the addObject actuator), (read-only)."""

    lights: typing.Any
    """ A list of lights in the scene, (read-only)."""

    cameras: typing.Any
    """ A list of cameras in the scene, (read-only)."""

    texts: typing.Any
    """ A list of texts in the scene, (read-only)."""

    active_camera: typing.Any
    """ The current active camera."""

    overrideCullingCamera: typing.Any
    world: typing.Any
    filterManager: typing.Any
    """ The scene's 2D filter manager, (read-only)."""

    suspended: typing.Any
    activityCulling: bool
    """ True if the scene allow object activity culling.

    :type: bool
    """

    dbvt_culling: typing.Any
    pre_draw: list
    """ A list of callables to be run before the render step. The callbacks can take as argument the rendered camera.

    :type: list
    """

    post_draw: list
    """ A list of callables to be run after the render step.

    :type: list
    """

    pre_draw_setup: list
    """ A list of callables to be run before the drawing setup (i.e., before the model view and projection matrices are computed).
The callbacks can take as argument the rendered camera, the camera could be temporary in case of stereo rendering.

    :type: list
    """

    onRemove: list
    """ A list of callables to run when the scene is destroyed.

    :type: list
    """

    gravity: typing.Any
    """ The scene gravity using the world x, y and z axis."""

    logger: typing.Any
    """ A logger instance that can be used to log messages related to this object (read-only)."""

    loggerName: str
    """ A name used to create the logger instance. By default, it takes the form KX_Scene[Name].

    :type: str
    """

    def addObject(
        self,
        object: str,
        reference: str | None = "",
        time: float = 0.0,
        dupli: bool = False,
    ):
        """Adds an object to the scene like the Add Object Actuator would.

        :param object: The (name of the) object to add.
        :type object: str
        :param reference: The (name of the) object which position, orientation, and scale to copy (optional), if the object to add is a light and there is not reference the light's layer will be the same that the active layer in the blender scene.
        :type reference: str | None
        :param time: The lifetime of the added object, in frames (assumes one frame is 1/60 second). A time of 0.0 means the object will last forever (optional).
        :type time: float
        :param dupli: Full duplication of object data (mesh, materials...).
        :type dupli: bool
        :return: The newly added object.
        """

    def end(self):
        """Removes the scene from the game."""

    def restart(self):
        """Restarts the scene."""

    def replace(self, scene: str) -> bool:
        """Replaces this scene with another one.

        :param scene: The name of the scene to replace this scene with.
        :type scene: str
        :return: True if the scene exists and was scheduled for addition, False otherwise.
        :rtype: bool
        """

    def suspend(self): ...
    def resume(self): ...
    def get(self, key, default=None):
        """Return the value matching key, or the default value if its not found.
        :return: The key value or a default.

                :param key:
                :param default:
        """

    def drawObstacleSimulation(self):
        """Draw debug visualization of obstacle simulation."""

    def convertBlenderObject(self, blenderObject):
        """Converts a `~bpy.types.Object` into a `~bge.types.KX_GameObject` during runtime.
        For example, you can append an Object from another .blend file during bge runtime
        using: bpy.ops.wm.append(...) then convert this Object into a KX_GameObject to have
        logic bricks, physics... converted. This is meant to replace libload.

                :param blenderObject: The Object to be converted.
                :return: Returns the newly converted gameobject.
        """

    def convertBlenderObjectsList(self, blenderObjectsList, asynchronous: bool):
        """Converts all bpy.types.Object inside a python List into its correspondent `~bge.types.KX_GameObject` during runtime.
        For example, you can append an Object List during bge runtime using: ob = object_data_add(...) and ML.append(ob) then convert the Objects
        inside the List into several KX_GameObject to have logic bricks, physics... converted. This is meant to replace libload.
        The conversion can be asynchronous or synchronous.

                :param blenderObjectsList: The Object list to be converted.
                :param asynchronous: The Object list conversion can be asynchronous or not.
                :type asynchronous: bool
        """

    def convertBlenderCollection(self, blenderCollection, asynchronous: bool):
        """Converts all bpy.types.Object inside a Collection into its correspondent `~bge.types.KX_GameObject` during runtime.
        For example, you can append a Collection from another .blend file during bge runtime
        using: bpy.ops.wm.append(...) then convert the Objects inside the Collection into several KX_GameObject to have
        logic bricks, physics... converted. This is meant to replace libload. The conversion can be asynchronous
        or synchronous.

                :param blenderCollection: The collection to be converted.
                :param asynchronous: The collection conversion can be asynchronous or not.
                :type asynchronous: bool
        """

    def convertBlenderAction(self, Action):
        """Registers a bpy.types.Action into the bge logic manager to be abled to play it during runtime.
        For example, you can append an Action from another .blend file during bge runtime
        using: bpy.ops.wm.append(...) then register this Action to be abled to play it.

                :param Action: The Action to be converted.
        """

    def unregisterBlenderAction(self, Action):
        """Unregisters a bpy.types.Action from the bge logic manager.
        The unregistered action will still be in the .blend file
        but can't be played anymore with bge. If you want to completely
        remove the action you need to call bpy.data.actions.remove(Action, do_unlink=True)
        after you unregistered it from bge logic manager.

                :param Action: The Action to be unregistered.
        """

    def addOverlayCollection(self, kxCamera, blenderCollection):
        """Adds an overlay collection (as with collection actuator) to render this collection objects
        during a second render pass in overlay using the KX_Camera passed as argument.

                :param kxCamera: The camera used to render the overlay collection.
                :param blenderCollection: The overlay collection to add.
        """

    def removeOverlayCollection(self, blenderCollection):
        """Removes an overlay collection (as with collection actuator).

        :param blenderCollection: The overlay collection to remove.
        """

    def getGameObjectFromObject(self, blenderObject: bpy.types.Object):
        """Get the KX_GameObject corresponding to the blenderObject.

        :param blenderObject: the Object from which we want to get the KX_GameObject.
        :type blenderObject: bpy.types.Object
        """

class KX_VehicleWrapper:
    """KX_VehicleWrapperTODO - description"""

    rayMask: typing.Any
    """ Set ray cast mask."""

    def addWheel(
        self,
        wheel,
        attachPos,
        downDir,
        axleDir,
        suspensionRestLength: float,
        wheelRadius: float,
        hasSteering: bool,
    ):
        """Add a wheel to the vehicle

        :param wheel: The object to use as a wheel.
        :param attachPos: The position to attach the wheel, relative to the chassis object center.
        :param downDir: The direction vector pointing down to where the vehicle should collide with the floor.
        :param axleDir: The axis the wheel rotates around, relative to the chassis.
        :param suspensionRestLength: The length of the suspension when no forces are being applied.
        :type suspensionRestLength: float
        :param wheelRadius: The radius of the wheel (half the diameter).
        :type wheelRadius: float
        :param hasSteering: True if the wheel should turn with steering, typically used in front wheels.
        :type hasSteering: bool
        """

    def applyBraking(self, force: float, wheelIndex: int):
        """Apply a braking force to the specified wheel

        :param force: the brake force
        :type force: float
        :param wheelIndex: index of the wheel where the force needs to be applied
        :type wheelIndex: int
        """

    def applyEngineForce(self, force: float, wheelIndex: int):
        """Apply an engine force to the specified wheel

        :param force: the engine force
        :type force: float
        :param wheelIndex: index of the wheel where the force needs to be applied
        :type wheelIndex: int
        """

    def getConstraintId(self) -> int:
        """Get the constraint ID

        :return: the constraint id
        :rtype: int
        """

    def getConstraintType(self) -> int:
        """Returns the constraint type.

        :return: constraint type
        :rtype: int
        """

    def getNumWheels(self) -> int:
        """Returns the number of wheels.

        :return: the number of wheels for this vehicle
        :rtype: int
        """

    def getWheelOrientationQuaternion(self, wheelIndex: int):
        """Returns the wheel orientation as a quaternion.

        :param wheelIndex: the wheel index
        :type wheelIndex: int
        :return: TODO Description
        """

    def getWheelPosition(self, wheelIndex: int):
        """Returns the position of the specified wheel

        :param wheelIndex: the wheel index
        :type wheelIndex: int
        :return: position vector
        """

    def getWheelRotation(self, wheelIndex: int) -> float:
        """Returns the rotation of the specified wheel

        :param wheelIndex: the wheel index
        :type wheelIndex: int
        :return: the wheel rotation
        :rtype: float
        """

    def setRollInfluence(self, rollInfluece: float, wheelIndex: int):
        """Set the specified wheel's roll influence.
        The higher the roll influence the more the vehicle will tend to roll over in corners.

                :param rollInfluece: the wheel roll influence
                :type rollInfluece: float
                :param wheelIndex: the wheel index
                :type wheelIndex: int
        """

    def setSteeringValue(self, steering: float, wheelIndex: int):
        """Set the specified wheel's steering

        :param steering: the wheel steering
        :type steering: float
        :param wheelIndex: the wheel index
        :type wheelIndex: int
        """

    def setSuspensionCompression(self, compression: float, wheelIndex: int):
        """Set the specified wheel's compression

        :param compression: the wheel compression
        :type compression: float
        :param wheelIndex: the wheel index
        :type wheelIndex: int
        """

    def setSuspensionDamping(self, damping: float, wheelIndex: int):
        """Set the specified wheel's damping

        :param damping: the wheel damping
        :type damping: float
        :param wheelIndex: the wheel index
        :type wheelIndex: int
        """

    def setSuspensionStiffness(self, stiffness: float, wheelIndex: int):
        """Set the specified wheel's stiffness

        :param stiffness: the wheel stiffness
        :type stiffness: float
        :param wheelIndex: the wheel index
        :type wheelIndex: int
        """

    def setTyreFriction(self, friction: float, wheelIndex: int):
        """Set the specified wheel's tyre friction

        :param friction: the tyre friction
        :type friction: float
        :param wheelIndex: the wheel index
        :type wheelIndex: int
        """

class KX_VertexProxy:
    """A vertex holds position, UV, color and normal information.Note:
    The physics simulation is NOT currently updated - physics will not respond
    to changes in the vertex position.
    """

    XYZ: typing.Any
    """ The position of the vertex."""

    UV: typing.Any
    """ The texture coordinates of the vertex."""

    uvs: typing.Any
    """ The texture coordinates list of the vertex."""

    normal: typing.Any
    """ The normal of the vertex."""

    color: typing.Any
    """ The color of the vertex.Black = [0.0, 0.0, 0.0, 1.0], White = [1.0, 1.0, 1.0, 1.0]"""

    colors: typing.Any
    """ The color list of the vertex."""

    x: float
    """ The x coordinate of the vertex.

    :type: float
    """

    y: float
    """ The y coordinate of the vertex.

    :type: float
    """

    z: float
    """ The z coordinate of the vertex.

    :type: float
    """

    u: float
    """ The u texture coordinate of the vertex.

    :type: float
    """

    v: float
    """ The v texture coordinate of the vertex.

    :type: float
    """

    u2: float
    """ The second u texture coordinate of the vertex.

    :type: float
    """

    v2: float
    """ The second v texture coordinate of the vertex.

    :type: float
    """

    r: float
    """ The red component of the vertex color. 0.0 <= r <= 1.0.

    :type: float
    """

    g: float
    """ The green component of the vertex color. 0.0 <= g <= 1.0.

    :type: float
    """

    b: float
    """ The blue component of the vertex color. 0.0 <= b <= 1.0.

    :type: float
    """

    a: float
    """ The alpha component of the vertex color. 0.0 <= a <= 1.0.

    :type: float
    """

    def getXYZ(self):
        """Gets the position of this vertex.

        :return: this vertexes position in local coordinates.
        """

    def setXYZ(self, pos):
        """Sets the position of this vertex.

        :param pos: the new position for this vertex in local coordinates.
        """

    def getUV(self):
        """Gets the UV (texture) coordinates of this vertex.

        :return: this vertexes UV (texture) coordinates.
        """

    def setUV(self, uv):
        """Sets the UV (texture) coordinates of this vertex.

        :param uv:
        """

    def getUV2(self):
        """Gets the 2nd UV (texture) coordinates of this vertex.

        :return: this vertexes UV (texture) coordinates.
        """

    def setUV2(self, uv, unit):
        """Sets the 2nd UV (texture) coordinates of this vertex.

        :param uv:
        :param unit: optional argument, FLAT==1, SECOND_UV==2, defaults to SECOND_UVinteger
        """

    def getRGBA(self) -> int:
        """Gets the color of this vertex.The color is represented as four bytes packed into an integer value.  The color is
        packed as RGBA.Since Python offers no way to get each byte without shifting, you must use the struct module to
        access color in an machine independent way.Because of this, it is suggested you use the r, g, b and a attributes or the color attribute instead.

                :return: packed color. 4 byte integer with one byte per color channel in RGBA format.
                :rtype: int
        """

    def setRGBA(self, col: int):
        """Sets the color of this vertex.See getRGBA() for the format of col, and its relevant problems.  Use the r, g, b and a attributes
        or the color attribute instead.setRGBA() also accepts a four component list as argument col.  The list represents the color as [r, g, b, a]
        with black = [0.0, 0.0, 0.0, 1.0] and white = [1.0, 1.0, 1.0, 1.0]

                :param col: the new color of this vertex in packed RGBA format.
                :type col: int
        """

    def getNormal(self):
        """Gets the normal vector of this vertex.

        :return: normalized normal vector.
        """

    def setNormal(self, normal):
        """Sets the normal vector of this vertex.

        :param normal: the new normal of this vertex.
        """

class SCA_2DFilterActuator:
    """Create, enable and disable 2D filters.The following properties don't have an immediate effect.
    You must active the actuator to get the result.
    The actuator is not persistent: it automatically stops itself after setting up the filter
    but the filter remains active. To stop a filter you must activate the actuator with 'type'
    set to `~bge.logic.RAS_2DFILTER_DISABLED` or `~bge.logic.RAS_2DFILTER_NOFILTER`.action on motion blur: 0=enable, 1=disable.type

    integer0.3.0argument for motion blur filter.type

    float (0.0-100.0)0.3.0
    """

    shaderText: str
    """ shader source code for custom shader.

    :type: str
    """

    disableMotionBlur: typing.Any
    mode: int
    """ Type of 2D filter, use one of `these constants <Two-D-FilterActuator-mode>`.

    :type: int
    """

    passNumber: typing.Any
    """ order number of filter in the stack of 2D filters. Filters are executed in increasing order of passNb.Only be one filter can be defined per passNb."""

    value: typing.Any

class SCA_ANDController:
    """An AND controller activates only when all linked sensors are activated.There are no special python methods for this controller."""

class SCA_ActionActuator:
    """Action Actuators apply an action to an actor."""

    action: str
    """ The name of the action to set as the current action.

    :type: str
    """

    frameStart: float
    """ Specifies the starting frame of the animation.

    :type: float
    """

    frameEnd: float
    """ Specifies the ending frame of the animation.

    :type: float
    """

    blendIn: float
    """ Specifies the number of frames of animation to generate when making transitions between actions.

    :type: float
    """

    priority: int
    """ Sets the priority of this actuator. Actuators will lower priority numbers will override actuators with higher numbers.

    :type: int
    """

    frame: float
    """ Sets the current frame for the animation.

    :type: float
    """

    propName: str
    """ Sets the property to be used in FromProp playback mode.

    :type: str
    """

    mode: int
    """ The operation mode of the actuator. Can be one of `these constants<action-actuator>`.

    :type: int
    """

    useContinue: bool
    """ The actions continue option, True or False. When True, the action will always play from where last left off,
otherwise negative events to this actuator will reset it to its start frame.

    :type: bool
    """

    framePropName: str
    """ The name of the property that is set to the current frame number.

    :type: str
    """

class SCA_ActuatorSensor:
    """Actuator sensor detect change in actuator state of the parent object.
    It generates a positive pulse if the corresponding actuator is activated
    and a negative pulse if the actuator is deactivated.
    """

    actuator: str
    """ the name of the actuator that the sensor is monitoring.

    :type: str
    """

class SCA_AddObjectActuator:
    """Edit Object Actuator (in Add Object Mode)"""

    object: typing.Any
    """ the object this actuator adds."""

    objectLastCreated: typing.Any
    """ the last added object from this actuator (read-only)."""

    time: float
    """ the lifetime of added objects, in frames. Set to 0 to disable automatic deletion.

    :type: float
    """

    linearVelocity: typing.Any
    """ the initial linear velocity of added objects."""

    angularVelocity: typing.Any
    """ the initial angular velocity of added objects."""

    def instantAddObject(self):
        """adds the object without needing to calling SCA_PythonController.activate()"""

class SCA_AlwaysSensor:
    """This sensor is always activated."""

class SCA_ArmatureActuator:
    """Armature Actuators change constraint condition on armatures."""

    type: int
    """ The type of action that the actuator executes when it is active.Can be one of `these constants <armatureactuator-constants-type>`

    :type: int
    """

    constraint: typing.Any
    """ The constraint object this actuator is controlling."""

    target: typing.Any
    """ The object that this actuator will set as primary target to the constraint it controls."""

    subtarget: typing.Any
    """ The object that this actuator will set as secondary target to the constraint it controls."""

    weight: typing.Any
    """ The weight this actuator will set on the constraint it controls."""

    influence: typing.Any
    """ The influence this actuator will set on the constraint it controls."""

class SCA_ArmatureSensor:
    """Armature sensor detect conditions on armatures."""

    type: int
    """ The type of measurement that the sensor make when it is active.Can be one of `these constants <armaturesensor-type>`

    :type: int
    """

    constraint: typing.Any
    """ The constraint object this sensor is watching."""

    value: float
    """ The threshold used in the comparison with the constraint error
The linear error is only updated on CopyPose/Distance IK constraint with iTaSC solver
The rotation error is only updated on CopyPose+rotation IK constraint with iTaSC solver
The linear error on CopyPose is always >= 0: it is the norm of the distance between the target and the bone
The rotation error on CopyPose is always >= 0: it is the norm of the equivalent rotation vector between the bone and the target orientations
The linear error on Distance can be positive if the distance between the bone and the target is greater than the desired distance, and negative if the distance is smaller.

    :type: float
    """

class SCA_CameraActuator:
    """Applies changes to a camera."""

    damping: float
    """ strength of of the camera following movement.

    :type: float
    """

    axis: int
    """ The camera axis (0, 1, 2) for positive XYZ, (3, 4, 5) for negative XYZ.

    :type: int
    """

    min: float
    """ minimum distance to the target object maintained by the actuator.

    :type: float
    """

    max: float
    """ maximum distance to stay from the target object.

    :type: float
    """

    height: float
    """ height to stay above the target object.

    :type: float
    """

    object: typing.Any
    """ the object this actuator tracks."""

class SCA_CollisionSensor:
    """Collision sensor detects collisions between objects."""

    propName: str
    """ The property or material to collide with.

    :type: str
    """

    useMaterial: bool
    """ Determines if the sensor is looking for a property or material. KX_True = Find material; KX_False = Find property.

    :type: bool
    """

    usePulseCollision: bool
    """ When enabled, changes to the set of colliding objects generate a pulse.

    :type: bool
    """

    hitObject: typing.Any
    """ The last collided object. (read-only)."""

    hitObjectList: typing.Any
    """ A list of colliding objects. (read-only)."""

    hitMaterial: str
    """ The material of the object in the face hit by the ray. (read-only).

    :type: str
    """

class SCA_ConstraintActuator:
    """A constraint actuator limits the position, rotation, distance or orientation of an object."""

    damp: int
    """ Time constant of the constraint expressed in frame (not use by Force field constraint).

    :type: int
    """

    rotDamp: int
    """ Time constant for the rotation expressed in frame (only for the distance constraint), 0 = use damp for rotation as well.

    :type: int
    """

    direction: typing.Any
    """ The reference direction in world coordinate for the orientation constraint."""

    option: int
    """ Binary combination of `these constants <constraint-actuator-option>`

    :type: int
    """

    time: int
    """ activation time of the actuator. The actuator disables itself after this many frame. If set to 0, the actuator is not limited in time.

    :type: int
    """

    propName: str
    """ the name of the property or material for the ray detection of the distance constraint.

    :type: str
    """

    min: float
    """ The lower bound of the constraint. For the rotation and orientation constraint, it represents radiant.

    :type: float
    """

    distance: float
    """ the target distance of the distance constraint.

    :type: float
    """

    max: float
    """ the upper bound of the constraint. For rotation and orientation constraints, it represents radiant.

    :type: float
    """

    rayLength: float
    """ the length of the ray of the distance constraint.

    :type: float
    """

    limit: int
    """ type of constraint. Use one of the `these constants <constraint-actuator-limit>`

    :type: int
    """

class SCA_DelaySensor:
    """The Delay sensor generates positive and negative triggers at precise time,
    expressed in number of frames. The delay parameter defines the length of the initial OFF period. A positive trigger is generated at the end of this period.The duration parameter defines the length of the ON period following the OFF period.
    There is a negative trigger at the end of the ON period. If duration is 0, the sensor stays ON and there is no negative trigger.The sensor runs the OFF-ON cycle once unless the repeat option is set: the OFF-ON cycle repeats indefinitely (or the OFF cycle if duration is 0).Use `SCA_ISensor.reset <bge.types.SCA_ISensor.reset>` at any time to restart sensor.
    """

    delay: int
    """ length of the initial OFF period as number of frame, 0 for immediate trigger.

    :type: int
    """

    duration: int
    """ length of the ON period in number of frame after the initial OFF period.If duration is greater than 0, a negative trigger is sent at the end of the ON pulse.

    :type: int
    """

    repeat: int
    """ 1 if the OFF-ON cycle should be repeated indefinitely, 0 if it should run once.

    :type: int
    """

class SCA_DynamicActuator:
    """Dynamic Actuator."""

    mode: int
    """ the type of operation of the actuator, 0-4

    :type: int
    """

    mass: float
    """ the mass value for the KX_DYN_SET_MASS operation.

    :type: float
    """

class SCA_EndObjectActuator:
    """Edit Object Actuator (in End Object mode)This actuator has no python methods."""

class SCA_GameActuator:
    """The game actuator loads a new .blend file, restarts the current .blend file or quits the game."""

    fileName: str
    """ the new .blend file to load.

    :type: str
    """

    mode: typing.Any
    """ The mode of this actuator. Can be on of `these constants <game-actuator>`"""

class SCA_IActuator:
    """Base class for all actuator logic bricks."""

class SCA_IController:
    """Base class for all controller logic bricks."""

    state: typing.Any
    """ The controllers state bitmask. This can be used with the GameObject's state to test if the controller is active."""

    sensors: typing.Any
    """ A list of sensors linked to this controller."""

    actuators: typing.Any
    """ A list of actuators linked to this controller."""

    useHighPriority: bool
    """ When set the controller executes always before all other controllers that dont have this set.

    :type: bool
    """

class SCA_ILogicBrick:
    """Base class for all logic bricks."""

    executePriority: int
    """ This determines the order controllers are evaluated, and actuators are activated (lower priority is executed first).

    :type: int
    """

    owner: typing.Any
    """ The game object this logic brick is attached to (read-only)."""

    name: str
    """ The name of this logic brick (read-only).

    :type: str
    """

class SCA_IObject:
    """This class has no python functions"""

class SCA_ISensor:
    """Base class for all sensor logic bricks."""

    usePosPulseMode: bool
    """ Flag to turn positive pulse mode on and off.

    :type: bool
    """

    useNegPulseMode: bool
    """ Flag to turn negative pulse mode on and off.

    :type: bool
    """

    frequency: int
    """ The frequency for pulse mode sensors.Use `skippedTicks`0.0.1

    :type: int
    """

    skippedTicks: int
    """ Number of logic ticks skipped between 2 active pulses

    :type: int
    """

    level: bool
    """ level Option whether to detect level or edge transition when entering a state.
It makes a difference only in case of logic state transition (state actuator).
A level detector will immediately generate a pulse, negative or positive
depending on the sensor condition, as soon as the state is activated.
A edge detector will wait for a state change before generating a pulse.
note: mutually exclusive with `tap`, enabling will disable `tap`.

    :type: bool
    """

    tap: bool
    """ When enabled only sensors that are just activated will send a positive event,
after this they will be detected as negative by the controllers.
This will make a key that's held act as if its only tapped for an instant.
note: mutually exclusive with `level`, enabling will disable `level`.

    :type: bool
    """

    invert: bool
    """ Flag to set if this sensor activates on positive or negative events.

    :type: bool
    """

    triggered: bool
    """ True if this sensor brick is in a positive state. (read-only).

    :type: bool
    """

    positive: bool
    """ True if this sensor brick is in a positive state. (read-only).

    :type: bool
    """

    pos_ticks: int
    """ The number of ticks since the last positive pulse (read-only).

    :type: int
    """

    neg_ticks: int
    """ The number of ticks since the last negative pulse (read-only).

    :type: int
    """

    status: int
    """ The status of the sensor (read-only): can be one of `these constants<sensor-status>`.

    :type: int
    """

    def reset(self):
        """Reset sensor internal state, effect depends on the type of sensor and settings.The sensor is put in its initial state as if it was just activated."""

class SCA_InputEvent:
    """Events for a keyboard or mouse input."""

    status: list[int]
    """ A list of existing status of the input from the last frame.
Can contain `bge.logic.KX_INPUT_NONE` and `bge.logic.KX_INPUT_ACTIVE`.
The list always contains one value.
The first value of the list is the last value of the list in the last frame. (read-only)

    :type: list[int]
    """

    queue: list[int]
    """ A list of existing events of the input from the last frame.
Can contain `bge.logic.KX_INPUT_JUST_ACTIVATED` and `bge.logic.KX_INPUT_JUST_RELEASED`.
The list can be empty. (read-only)

    :type: list[int]
    """

    values: list[int]
    """ A list of existing value of the input from the last frame.
For keyboard it contains 1 or 0 and for mouse the coordinate of the mouse or the movement of the wheel mouse.
The list contains always one value, the size of the list is the same than `queue` + 1 only for keyboard inputs.
The first value of the list is the last value of the list in the last frame. (read-only)Example to get the non-normalized mouse coordinates:

    :type: list[int]
    """

    inactive: bool
    """ True if the input was inactive from the last frame.

    :type: bool
    """

    active: bool
    """ True if the input was active from the last frame.

    :type: bool
    """

    activated: bool
    """ True if the input was activated from the last frame.

    :type: bool
    """

    released: bool
    """ True if the input was released from the last frame.Example to execute some action when I click or release mouse left button:

    :type: bool
    """

    type: int
    """ The type of the input.
One of `these constants<keyboard-keys>`

    :type: int
    """

class SCA_JoystickSensor:
    """This sensor detects player joystick events."""

    axisValues: list[int]
    """ The state of the joysticks axis as a list of values `numAxis` long. (read-only).Each specifying the value of an axis between -32767 and 32767 depending on how far the axis is pushed, 0 for nothing.
The first 2 values are used by most joysticks and gamepads for directional control. 3rd and 4th values are only on some joysticks and can be used for arbitrary controls.

    :type: list[int]
    """

    axisSingle: int
    """ like `axisValues` but returns a single axis value that is set by the sensor. (read-only).

    :type: int
    """

    hatValues: list[int]
    """ The state of the joysticks hats as a list of values `numHats` long. (read-only).Each specifying the direction of the hat from 1 to 12, 0 when inactive.Hat directions are as follows...Use `button` instead.0.2.2

    :type: list[int]
    """

    hatSingle: int
    """ Like `hatValues` but returns a single hat direction value that is set by the sensor. (read-only).Use `button` instead.0.2.2

    :type: int
    """

    numAxis: int
    """ The number of axes for the joystick at this index. (read-only).

    :type: int
    """

    numButtons: int
    """ The number of buttons for the joystick at this index. (read-only).

    :type: int
    """

    numHats: int
    """ The number of hats for the joystick at this index. (read-only).Use `numButtons` instead.0.2.2

    :type: int
    """

    connected: bool
    """ True if a joystick is connected at this joysticks index. (read-only).

    :type: bool
    """

    index: int
    """ The joystick index to use (from 0 to 7). The first joystick is always 0.

    :type: int
    """

    threshold: int
    """ Axis threshold. Joystick axis motion below this threshold wont trigger an event. Use values between (0 and 32767), lower values are more sensitive.

    :type: int
    """

    button: int
    """ The button index the sensor reacts to (first button = 0). When the "All Events" toggle is set, this option has no effect.

    :type: int
    """

    axis: typing.Any
    """ The axis this sensor reacts to, as a list of two values [axisIndex, axisDirection]"""

    hat: typing.Any
    """ The hat the sensor reacts to, as a list of two values: [hatIndex, hatDirection]Use `button` instead.0.2.2"""

    def getButtonActiveList(self) -> list:
        """

        :return: A list containing the indicies of the currently pressed buttons.
        :rtype: list
        """

    def getButtonStatus(self, buttonIndex: int) -> bool:
        """

        :param buttonIndex: the button index, 0=first button
        :type buttonIndex: int
        :return: The current pressed state of the specified button.
        :rtype: bool
        """

class SCA_KeyboardSensor:
    """A keyboard sensor detects player key presses.See module `bge.events` for keycode values."""

    key: int
    """ The key code this sensor is looking for. Expects a keycode from `bge.events` module.

    :type: int
    """

    hold1: int
    """ The key code for the first modifier this sensor is looking for. Expects a keycode from `bge.events` module.

    :type: int
    """

    hold2: int
    """ The key code for the second modifier this sensor is looking for. Expects a keycode from `bge.events` module.

    :type: int
    """

    toggleProperty: str
    """ The name of the property that indicates whether or not to log keystrokes as a string.

    :type: str
    """

    targetProperty: str
    """ The name of the property that receives keystrokes in case in case a string is logged.

    :type: str
    """

    useAllKeys: bool
    """ Flag to determine whether or not to accept all keys.

    :type: bool
    """

    inputs: typing.Any
    """ A list of pressed input keys that have either been pressed, or just released, or are active this frame. (read-only)."""

    events: typing.Any
    """ a list of pressed keys that have either been pressed, or just released, or are active this frame. (read-only).Use `inputs`0.2.2"""

    def getKeyStatus(self, keycode: int) -> int:
        """Get the status of a key.

        :param keycode: The code that represents the key you want to get the state of, use one of `these constants<keyboard-keys>`
        :type keycode: int
        :return: The state of the given key, can be one of `these constants<input-status>`
        :rtype: int
        """

class SCA_MouseActuator:
    """The mouse actuator gives control over the visibility of the mouse cursor and rotates the parent object according to mouse movement."""

    visible: bool
    """ The visibility of the mouse cursor.

    :type: bool
    """

    use_axis_x: bool
    """ Mouse movement along the x axis effects object rotation.

    :type: bool
    """

    use_axis_y: bool
    """ Mouse movement along the y axis effects object rotation.

    :type: bool
    """

    threshold: typing.Any
    """ Amount of movement from the mouse required before rotation is triggered.The values in the list should be between 0.0 and 0.5."""

    reset_x: bool
    """ Mouse is locked to the center of the screen on the x axis.

    :type: bool
    """

    reset_y: bool
    """ Mouse is locked to the center of the screen on the y axis.

    :type: bool
    """

    object_axis: typing.Any
    """ The object's 3D axis to rotate with the mouse movement. ([x, y])"""

    local_x: bool
    """ Rotation caused by mouse movement along the x axis is local.

    :type: bool
    """

    local_y: bool
    """ Rotation caused by mouse movement along the y axis is local.

    :type: bool
    """

    sensitivity: typing.Any
    """ The amount of rotation caused by mouse movement along the x and y axis.Negative values invert the rotation."""

    limit_x: typing.Any
    """ The minimum and maximum angle of rotation caused by mouse movement along the x axis in degrees.
limit_x[0] is minimum, limit_x[1] is maximum."""

    limit_y: typing.Any
    """ The minimum and maximum angle of rotation caused by mouse movement along the y axis in degrees.
limit_y[0] is minimum, limit_y[1] is maximum."""

    angle: typing.Any
    """ The current rotational offset caused by the mouse actuator in degrees."""

    def reset(self):
        """Undoes the rotation caused by the mouse actuator."""

class SCA_MouseFocusSensor:
    """The mouse focus sensor detects when the mouse is over the current game object.The mouse focus sensor works by transforming the mouse coordinates from 2d device
    space to 3d space then raycasting away from the camera.
    """

    raySource: typing.Any
    """ The worldspace source of the ray (the view position)."""

    rayTarget: typing.Any
    """ The worldspace target of the ray."""

    rayDirection: typing.Any
    """ The `rayTarget` - `raySource` normalized."""

    hitObject: typing.Any
    """ the last object the mouse was over."""

    hitPosition: typing.Any
    """ The worldspace position of the ray intersection."""

    hitNormal: typing.Any
    """ the worldspace normal from the face at point of intersection."""

    hitUV: typing.Any
    """ the UV coordinates at the point of intersection.If the object has no UV mapping, it returns [0, 0].The UV coordinates are not normalized, they can be < 0 or > 1 depending on the UV mapping."""

    usePulseFocus: bool
    """ When enabled, moving the mouse over a different object generates a pulse. (only used when the 'Mouse Over Any' sensor option is set).

    :type: bool
    """

    useXRay: bool
    """ 

    :type: bool
    """

    mask: typing.Any
    """ The collision mask (16 layers mapped to a 16-bit integer) combined with each object's collision group, to hit only a subset of the
objects in the scene. Only those objects for which collisionGroup & mask is true can be hit."""

    propName: str
    """ 

    :type: str
    """

    useMaterial: bool
    """ 

    :type: bool
    """

class SCA_MouseSensor:
    """Mouse Sensor logic brick."""

    position: typing.Any
    """ current [x, y] coordinates of the mouse, in frame coordinates (pixels)."""

    mode: int
    """ sensor mode. one of the following constants:

    :type: int
    """

    def getButtonStatus(self, button: int) -> int:
        """Get the mouse button status.

        :param button: The code that represents the key you want to get the state of, use one of `these constants<mouse-keys>`
        :type button: int
        :return: The state of the given key, can be one of `these constants<input-status>`
        :rtype: int
        """

class SCA_NANDController:
    """An NAND controller activates when all linked sensors are not active.There are no special python methods for this controller."""

class SCA_NORController:
    """An NOR controller activates only when all linked sensors are de-activated.There are no special python methods for this controller."""

class SCA_NearSensor:
    """A near sensor is a specialised form of touch sensor."""

    distance: float
    """ The near sensor activates when an object is within this distance.

    :type: float
    """

    resetDistance: float
    """ The near sensor deactivates when the object exceeds this distance.

    :type: float
    """

class SCA_NetworkMessageActuator:
    """Message Actuator"""

    propName: str
    """ Messages will only be sent to objects with the given property name.

    :type: str
    """

    subject: str
    """ The subject field of the message.

    :type: str
    """

    body: str
    """ The body of the message.

    :type: str
    """

    usePropBody: bool
    """ Send a property instead of a regular body message.

    :type: bool
    """

class SCA_NetworkMessageSensor:
    """The Message Sensor logic brick.Currently only loopback (local) networks are supported."""

    subject: str
    """ The subject the sensor is looking for.

    :type: str
    """

    frameMessageCount: int
    """ The number of messages received since the last frame. (read-only).

    :type: int
    """

    subjects: list[str]
    """ The list of message subjects received. (read-only).

    :type: list[str]
    """

    bodies: list[str]
    """ The list of message bodies received. (read-only).

    :type: list[str]
    """

class SCA_ORController:
    """An OR controller activates when any connected sensor activates.There are no special python methods for this controller."""

class SCA_ObjectActuator:
    """The object actuator ("Motion Actuator") applies force, torque, displacement, angular displacement,
    velocity, or angular velocity to an object.
    Servo control allows to regulate force to achieve a certain speed target.
    """

    force: typing.Any
    """ The force applied by the actuator."""

    useLocalForce: bool
    """ A flag specifying if the force is local.

    :type: bool
    """

    torque: typing.Any
    """ The torque applied by the actuator."""

    useLocalTorque: bool
    """ A flag specifying if the torque is local.

    :type: bool
    """

    dLoc: typing.Any
    """ The displacement vector applied by the actuator."""

    useLocalDLoc: bool
    """ A flag specifying if the dLoc is local.

    :type: bool
    """

    dRot: typing.Any
    """ The angular displacement vector applied by the actuator"""

    useLocalDRot: bool
    """ A flag specifying if the dRot is local.

    :type: bool
    """

    linV: typing.Any
    """ The linear velocity applied by the actuator."""

    useLocalLinV: bool
    """ A flag specifying if the linear velocity is local.

    :type: bool
    """

    angV: typing.Any
    """ The angular velocity applied by the actuator."""

    useLocalAngV: bool
    """ A flag specifying if the angular velocity is local.

    :type: bool
    """

    damping: typing.Any
    """ The damping parameter of the servo controller."""

    forceLimitX: typing.Any
    """ The min/max force limit along the X axis and activates or deactivates the limits in the servo controller."""

    forceLimitY: typing.Any
    """ The min/max force limit along the Y axis and activates or deactivates the limits in the servo controller."""

    forceLimitZ: typing.Any
    """ The min/max force limit along the Z axis and activates or deactivates the limits in the servo controller."""

    pid: list[float]
    """ The PID coefficients of the servo controller.

    :type: list[float]
    """

    reference: typing.Any
    """ The object that is used as reference to compute the velocity for the servo controller."""

class SCA_ParentActuator:
    """The parent actuator can set or remove an objects parent object."""

    object: typing.Any
    """ the object this actuator sets the parent too."""

    mode: typing.Any
    """ The mode of this actuator."""

    compound: bool
    """ Whether the object shape should be added to the parent compound shape when parenting.Effective only if the parent is already a compound shape.

    :type: bool
    """

    ghost: bool
    """ Whether the object should be made ghost when parenting
Effective only if the shape is not added to the parent compound shape.

    :type: bool
    """

class SCA_PropertyActuator:
    """Property Actuator"""

    propName: str
    """ the property on which to operate.

    :type: str
    """

    value: str
    """ the value with which the actuator operates.

    :type: str
    """

    mode: int
    """ TODO - add constants to game logic dict!.

    :type: int
    """

class SCA_PropertySensor:
    """Activates when the game object property matches."""

    mode: int
    """ Type of check on the property. Can be one of `these constants <logic-property-sensor>`

    :type: int
    """

    propName: str
    """ the property the sensor operates.

    :type: str
    """

    value: str
    """ the value with which the sensor compares to the value of the property.

    :type: str
    """

    min: str
    """ the minimum value of the range used to evaluate the property when in interval mode.

    :type: str
    """

    max: str
    """ the maximum value of the range used to evaluate the property when in interval mode.

    :type: str
    """

class SCA_PythonController:
    """A Python controller uses a Python script to activate it's actuators,
    based on it's sensors.
    """

    owner: typing.Any
    """ The object the controller is attached to."""

    script: str
    """ The value of this variable depends on the execution method.

    :type: str
    """

    mode: int
    """ the execution mode for this controller (read-only).

    :type: int
    """

    def activate(self, actuator: str):
        """Activates an actuator attached to this controller.

        :param actuator: The actuator to operate on. Expects either an actuator instance or its name.
        :type actuator: str
        """

    def deactivate(self, actuator: str):
        """Deactivates an actuator attached to this controller.

        :param actuator: The actuator to operate on. Expects either an actuator instance or its name.
        :type actuator: str
        """

class SCA_PythonJoystick:
    """A Python interface to a joystick."""

    name: str
    """ The name assigned to the joystick by the operating system. (read-only)

    :type: str
    """

    activeButtons: list
    """ A list of active button values. (read-only)

    :type: list
    """

    axisValues: list[int]
    """ The state of the joysticks axis as a list of values `numAxis` long. (read-only).Each specifying the value of an axis between -1.0 and 1.0
depending on how far the axis is pushed, 0 for nothing.
The first 2 values are used by most joysticks and gamepads for directional control.
3rd and 4th values are only on some joysticks and can be used for arbitrary controls.

    :type: list[int]
    """

    hatValues: typing.Any
    """ Use `activeButtons` instead.0.2.2"""

    numAxis: int
    """ The number of axes for the joystick at this index. (read-only).

    :type: int
    """

    numButtons: int
    """ The number of buttons for the joystick at this index. (read-only).

    :type: int
    """

    numHats: typing.Any
    """ Use `numButtons` instead.0.2.2"""

    strengthLeft: typing.Any
    """ Strength of the Low frequency joystick's motor (placed at left position usually)."""

    strengthRight: typing.Any
    """ Strength of the High frequency joystick's motor (placed at right position usually)."""

    duration: typing.Any
    """ Duration of the vibration in milliseconds."""

    isVibrating: typing.Any
    """ Check status of joystick vibration"""

    hasVibration: typing.Any
    """ Check if the joystick supports vibration"""

    def startVibration(self):
        """Starts the vibration.

        :return: None
        """

    def stopVibration(self):
        """Stops the vibration.

        :return: None
        """

class SCA_PythonKeyboard:
    """The current keyboard."""

    inputs: typing.Any
    """ A dictionary containing the input of each keyboard key. (read-only)."""

    events: typing.Any
    """ A dictionary containing the status of each keyboard event or key. (read-only).Use `inputs`.0.2.2"""

    activeInputs: typing.Any
    """ A dictionary containing the input of only the active keyboard keys. (read-only)."""

    active_events: typing.Any
    """ A dictionary containing the status of only the active keyboard events or keys. (read-only).Use `activeInputs`.0.2.2"""

    text: str
    """ The typed unicode text from the last frame.

    :type: str
    """

    def getClipboard(self) -> str:
        """Gets the clipboard text.

        :return:
        :rtype: str
        """

    def setClipboard(self, text: str):
        """Sets the clipboard text.

        :param text: New clipboard text
        :type text: str
        """

class SCA_PythonMouse:
    """The current mouse."""

    inputs: typing.Any
    """ A dictionary containing the input of each mouse event. (read-only)."""

    events: typing.Any
    """ a dictionary containing the status of each mouse event. (read-only).Use `inputs`.0.2.2"""

    activeInputs: typing.Any
    """ A dictionary containing the input of only the active mouse events. (read-only)."""

    active_events: typing.Any
    """ a dictionary containing the status of only the active mouse events. (read-only).Use `activeInputs`.0.2.2"""

    position: typing.Any
    """ The normalized x and y position of the mouse cursor."""

    visible: bool
    """ The visibility of the mouse cursor.

    :type: bool
    """

class SCA_RadarSensor:
    """Radar sensor is a near sensor with a conical sensor object."""

    coneOrigin: list[float]
    """ The origin of the cone with which to test. The origin is in the middle of the cone. (read-only).

    :type: list[float]
    """

    coneTarget: list[float]
    """ The center of the bottom face of the cone with which to test. (read-only).

    :type: list[float]
    """

    distance: float
    """ The height of the cone with which to test (read-only).

    :type: float
    """

    angle: float
    """ The angle of the cone (in degrees) with which to test (read-only).

    :type: float
    """

    axis: typing.Any
    """ The axis on which the radar cone is cast.KX_RADAR_AXIS_POS_X, KX_RADAR_AXIS_POS_Y, KX_RADAR_AXIS_POS_Z,
KX_RADAR_AXIS_NEG_X, KX_RADAR_AXIS_NEG_Y, KX_RADAR_AXIS_NEG_Z"""

class SCA_RandomActuator:
    """Random Actuator"""

    seed: int
    """ Seed of the random number generator.Equal seeds produce equal series. If the seed is 0, the generator will produce the same value on every call.

    :type: int
    """

    para1: float
    """ the first parameter of the active distribution.Refer to the documentation of the generator types for the meaning of this value.

    :type: float
    """

    para2: float
    """ the second parameter of the active distribution.Refer to the documentation of the generator types for the meaning of this value.

    :type: float
    """

    distribution: int
    """ Distribution type. (read-only). Can be one of `these constants <logic-random-distributions>`

    :type: int
    """

    propName: str
    """ the name of the property to set with the random value.If the generator and property types do not match, the assignment is ignored.

    :type: str
    """

    def setBoolConst(self, value: bool):
        """Sets this generator to produce a constant boolean value.

        :param value: The value to return.
        :type value: bool
        """

    def setBoolUniform(self):
        """Sets this generator to produce a uniform boolean distribution.The generator will generate True or False with 50% chance."""

    def setBoolBernouilli(self, value: float):
        """Sets this generator to produce a Bernouilli distribution.

                :param value: Specifies the proportion of False values to produce.

        0.0: Always generate True

        1.0: Always generate False
                :type value: float
        """

    def setIntConst(self, value: int):
        """Sets this generator to always produce the given value.

        :param value: the value this generator produces.
        :type value: int
        """

    def setIntUniform(self, lower_bound: int, upper_bound: int):
        """Sets this generator to produce a random value between the given lower and
        upper bounds (inclusive).

                :param lower_bound:
                :type lower_bound: int
                :param upper_bound:
                :type upper_bound: int
        """

    def setIntPoisson(self, value: float):
        """Generate a Poisson-distributed number.This performs a series of Bernouilli tests with parameter value.
        It returns the number of tries needed to achieve success.

                :param value:
                :type value: float
        """

    def setFloatConst(self, value: float):
        """Always generate the given value.

        :param value:
        :type value: float
        """

    def setFloatUniform(self, lower_bound: float, upper_bound: float):
        """Generates a random float between lower_bound and upper_bound with a
        uniform distribution.

                :param lower_bound:
                :type lower_bound: float
                :param upper_bound:
                :type upper_bound: float
        """

    def setFloatNormal(self, mean: float, standard_deviation: float):
        """Generates a random float from the given normal distribution.

        :param mean: The mean (average) value of the generated numbers
        :type mean: float
        :param standard_deviation: The standard deviation of the generated numbers.
        :type standard_deviation: float
        """

    def setFloatNegativeExponential(self, half_life: float):
        """Generate negative-exponentially distributed numbers.The half-life 'time' is characterized by half_life.

        :param half_life:
        :type half_life: float
        """

class SCA_RandomSensor:
    """This sensor activates randomly."""

    lastDraw: int
    """ The seed of the random number generator.

    :type: int
    """

    seed: int
    """ The seed of the random number generator.

    :type: int
    """

class SCA_RaySensor:
    """A ray sensor detects the first object in a given direction."""

    propName: str
    """ The property the ray is looking for.

    :type: str
    """

    range: float
    """ The distance of the ray.

    :type: float
    """

    useMaterial: bool
    """ Whether or not to look for a material (false = property).

    :type: bool
    """

    useXRay: bool
    """ Whether or not to use XRay.

    :type: bool
    """

    mask: typing.Any
    """ The collision mask (16 layers mapped to a 16-bit integer) combined with each object's collision group, to hit only a subset of the
objects in the scene. Only those objects for which collisionGroup & mask is true can be hit."""

    hitObject: typing.Any
    """ The game object that was hit by the ray. (read-only)."""

    hitPosition: typing.Any
    """ The position (in worldcoordinates) where the object was hit by the ray. (read-only)."""

    hitNormal: typing.Any
    """ The normal (in worldcoordinates) of the object at the location where the object was hit by the ray. (read-only)."""

    hitMaterial: str
    """ The material of the object in the face hit by the ray. (read-only).

    :type: str
    """

    rayDirection: typing.Any
    """ The direction from the ray (in worldcoordinates). (read-only)."""

    axis: typing.Any
    """ The axis the ray is pointing on."""

class SCA_ReplaceMeshActuator:
    """Edit Object actuator, in Replace Mesh mode."""

    mesh: typing.Any
    """ `~bge.types.KX_MeshProxy` or the name of the mesh that will replace the current one.Set to None to disable actuator."""

    useDisplayMesh: bool
    """ when true the displayed mesh is replaced.

    :type: bool
    """

    usePhysicsMesh: bool
    """ when true the physics mesh is replaced.

    :type: bool
    """

    def instantReplaceMesh(self):
        """Immediately replace mesh without delay."""

class SCA_SceneActuator:
    """Scene Actuator logic brick."""

    scene: str
    """ the name of the scene to change to/overlay/underlay/remove/suspend/resume.

    :type: str
    """

    camera: str
    """ the camera to change to.

    :type: str
    """

    useRestart: bool
    """ Set flag to True to restart the sene.

    :type: bool
    """

    mode: typing.Any
    """ The mode of the actuator."""

class SCA_SoundActuator:
    """Sound Actuator.The `startSound`, `pauseSound` and `stopSound` do not require the actuator to be activated - they act instantly provided that the actuator has been activated once at least."""

    volume: float
    """ The volume (gain) of the sound.

    :type: float
    """

    time: float
    """ The current position in the audio stream (in seconds).

    :type: float
    """

    pitch: float
    """ The pitch of the sound.

    :type: float
    """

    mode: int
    """ The operation mode of the actuator. Can be one of `these constants<logic-sound-actuator>`

    :type: int
    """

    sound: aud.Sound
    """ The sound the actuator should play.

    :type: aud.Sound
    """

    is3D: bool
    """ Whether or not the actuator should be using 3D sound. (read-only)

    :type: bool
    """

    volume_maximum: float
    """ The maximum gain of the sound, no matter how near it is.

    :type: float
    """

    volume_minimum: float
    """ The minimum gain of the sound, no matter how far it is away.

    :type: float
    """

    distance_reference: float
    """ The distance where the sound has a gain of 1.0.

    :type: float
    """

    distance_maximum: float
    """ The maximum distance at which you can hear the sound.

    :type: float
    """

    attenuation: float
    """ The influence factor on volume depending on distance.

    :type: float
    """

    cone_angle_inner: float
    """ The angle of the inner cone.

    :type: float
    """

    cone_angle_outer: float
    """ The angle of the outer cone.

    :type: float
    """

    cone_volume_outer: float
    """ The gain outside the outer cone (the gain in the outer cone will be interpolated between this value and the normal gain in the inner cone).

    :type: float
    """

    def startSound(self):
        """Starts the sound.

        :return: None
        """

    def pauseSound(self):
        """Pauses the sound.

        :return: None
        """

    def stopSound(self):
        """Stops the sound.

        :return: None
        """

class SCA_StateActuator:
    """State actuator changes the state mask of parent object."""

    operation: int
    """ Type of bit operation to be applied on object state mask.You can use one of `these constants <state-actuator-operation>`

    :type: int
    """

    mask: int
    """ Value that defines the bits that will be modified by the operation.The bits that are 1 in the mask will be updated in the object state.The bits that are 0 are will be left unmodified expect for the Copy operation which copies the mask to the object state.

    :type: int
    """

class SCA_SteeringActuator:
    """Steering Actuator for navigation."""

    behavior: int
    """ The steering behavior to use. One of `these constants <logic-steering-actuator>`.

    :type: int
    """

    velocity: float
    """ Velocity magnitude

    :type: float
    """

    acceleration: float
    """ Max acceleration

    :type: float
    """

    turnspeed: float
    """ Max turn speed

    :type: float
    """

    distance: float
    """ Relax distance

    :type: float
    """

    target: typing.Any
    """ Target object"""

    navmesh: typing.Any
    """ Navigation mesh"""

    selfterminated: bool
    """ Terminate when target is reached

    :type: bool
    """

    enableVisualization: bool
    """ Enable debug visualization

    :type: bool
    """

    pathUpdatePeriod: int
    """ Path update period

    :type: int
    """

    path: list[mathutils.Vector]
    """ Path point list.

    :type: list[mathutils.Vector]
    """

class SCA_TrackToActuator:
    """Edit Object actuator in Track To mode."""

    object: typing.Any
    """ the object this actuator tracks."""

    time: int
    """ the time in frames with which to delay the tracking motion.

    :type: int
    """

    use3D: bool
    """ the tracking motion to use 3D.

    :type: bool
    """

    upAxis: typing.Any
    """ The axis that points upward."""

    trackAxis: typing.Any
    """ The axis that points to the target object."""

class SCA_VibrationActuator:
    """Vibration Actuator."""

    joyindex: typing.Any
    """ Joystick index."""

    strengthLeft: typing.Any
    """ Strength of the Low frequency joystick's motor (placed at left position usually)."""

    strengthRight: typing.Any
    """ Strength of the High frequency joystick's motor (placed at right position usually)."""

    duration: typing.Any
    """ Duration of the vibration in milliseconds."""

    isVibrating: typing.Any
    """ Check status of joystick vibration"""

    hasVibration: typing.Any
    """ Check if the joystick supports vibration"""

    def startVibration(self):
        """Starts the vibration.

        :return: None
        """

    def stopVibration(self):
        """Stops the vibration.

        :return: None
        """

class SCA_VisibilityActuator:
    """Visibility Actuator."""

    visibility: bool
    """ whether the actuator makes its parent object visible or invisible.

    :type: bool
    """

    useOcclusion: bool
    """ whether the actuator makes its parent object an occluder or not.

    :type: bool
    """

    useRecursion: bool
    """ whether the visibility/occlusion should be propagated to all children of the object.

    :type: bool
    """

class SCA_XNORController:
    """An XNOR controller activates when all linked sensors are the same (activated or inative).There are no special python methods for this controller."""

class SCA_XORController:
    """An XOR controller activates when there is the input is mixed, but not when all are on or off.There are no special python methods for this controller."""

class BL_Texture(EXP_Value):
    """This is kept for backward compatibility with some scripts (bindCode mainly)."""

    bindCode: int
    """ Texture bind code/Id/number.

    :type: int
    """
