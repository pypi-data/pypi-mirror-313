import typing
import collections.abc
import typing_extensions
import bpy.types

def edge_face_count(mesh):
    """

    :return: list face users for each item in mesh.edges.
    """

def edge_face_count_dict(mesh):
    """

    :return: Dictionary of edge keys with their value set to the number of faces using each edge.
    """

def edge_loops_from_edges(mesh, edges=None):
    """Edge loops defined by edgesTakes me.edges or a list of edges and returns the edge loopsreturn a list of vertex indices.
    [ [1, 6, 7, 2], ...]closed loops have matching start and end values.

    """

def mesh_linked_triangles(mesh: bpy.types.Mesh):
    """Splits the mesh into connected triangles, use this for separating cubes from
    other mesh elements within 1 mesh data-block.

        :param mesh: the mesh used to group with.
        :type mesh: bpy.types.Mesh
        :return: Lists of lists containing triangles.
    """

def mesh_linked_uv_islands(mesh: bpy.types.Mesh):
    """Returns lists of polygon indices connected by UV islands.

    :param mesh: the mesh used to group with.
    :type mesh: bpy.types.Mesh
    :return: list of lists containing polygon indices
    """

def ngon_tessellate(from_data, indices, fix_loops: bool = True, debug_print=True):
    """Takes a poly-line of indices (ngon) and returns a list of face
    index lists. Designed to be used for importers that need indices for an
    ngon to create from existing verts.

        :param from_data: Either a mesh, or a list/tuple of 3D vectors.
        :param indices: a list of indices to use this list
    is the ordered closed poly-line
    to fill, and can be a subset of the data given.
        :param fix_loops: If this is enabled poly-lines
    that use loops to make multiple
    poly-lines are dealt with correctly.
        :type fix_loops: bool
    """

def triangle_random_points(num_points: int, loop_triangles):
    """Generates a list of random points over mesh loop triangles.

    :param num_points: The number of random points to generate on each triangle.
    :type num_points: int
    :param loop_triangles: Sequence of the triangles to generate points on.
    :return: List of random points over all triangles.
    """
