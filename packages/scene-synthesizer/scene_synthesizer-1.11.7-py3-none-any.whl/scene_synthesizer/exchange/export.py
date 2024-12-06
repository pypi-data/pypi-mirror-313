# Standard Library
import os
import json

# Third Party
import trimesh

# Local Folder
from ..utils import log
from .urdf import export_urdf
from .usd import export_usd


def export_glb(scene, **kwargs):
    """Export a scene as a binary GLTF (GLB 2.0) file.

    This uses trimesh.exchange.gltf.export_glb

    Args:
        scene (scene_synthesizer.Scene): Scene to be exported.
        **extras (JSON serializable): Will be stored in the extras field.
        **include_normals (bool): Whether to include vertex normals in output file. Defaults to None.
        **unitize_normals (bool): Whether to unitize normals. Defaults to False.
        **tree_postprocessor (func): Custom function to (in-place) post-process the tree before exporting.
        **buffer_postprocessor (func): Custom function to (in-place) post-process the buffer before exporting.
    
    Returns:
        bytes: Exported result in GLB 2.0
    """
    # without concatening everything the transformations of the scene graph are lost
    return trimesh.exchange.gltf.export_glb(
        scene.scene,
        **kwargs,
    )


def export_gltf(scene, **kwargs):
    """Export a scene object as a GLTF directory.

    This puts each mesh into a separate file (i.e. a `buffer`)
    as opposed to one larger file.

    This uses trimesh.exchange.gltf.export_gltf

    Args:
        scene (scene_synthesizer.Scene): Scene to be exported.
        **include_normals (bool): Whether to include vertex normals. Defaults to None.
        **merge_buffers (bool): Whether to merge buffers into one blob. Defaults to False.
        **resolver (trimesh.resolvers.Resolver): If passed will use to write each file.
        **tree_postprocesser (None or callable): Run this on the header tree before exiting. Defaults to None.
        **embed_buffers (bool): Embed the buffer into JSON file as a base64 string in the URI. Defaults to False.
    
    Returns:
        dict: Format: {file name : file data}
    """
    return trimesh.exchange.gltf.export_gltf(
        scene.scene,
        **kwargs,
    )


def export_obj(scene, concatenate=True, **kwargs):
    """Export a scene as a Wavefront OBJ file.

    This uses trimesh.exchange.obj.export_obj
    
    Args:
        scene (scene_synthesizer.Scene): Scene to be exported.
        concatenate (bool, optional): Whether to concatenate all meshes into a single one. Note, that currently trimesh can't export textured scenes. Defaults to True.
        **include_normals (bool): Include vertex normals in export. If None will only be included if vertex normals are in cache.
        **include_color (bool): Include vertex color in export
        **include_texture (bool): Include `vt` texture in file text
        **return_texture (bool): If True, return a dict with texture files
        **write_texture (bool): If True and a writable resolver is passed write the referenced texture files with resolver
        **resolver (None or trimesh.resolvers.Resolver): Resolver which can write referenced text objects
        **digits (int): Number of digits to include for floating point
        **mtl_name (None or str): If passed, the file name of the MTL file.
        **header (str or None): Header string for top of file or None for no header.

    Returns:
        str: OBJ format output
        dict: Contains texture files that need to be saved in the same directory as the exported mesh: {file name : bytes}
    """
    
    # for i, g in enumerate(scene.geometry):
    #     if hasattr(scene.geometry[g].visual, "material"):
    #         scene.geometry[g].visual.material.name = f"material_{i}"
    
    if 'header' not in kwargs:
        kwargs['header'] = "scene_synthesizer"
    
    if concatenate:
        s = scene.scene.dump(concatenate=True)
    else:
        s = scene.scene
    
    return trimesh.exchange.obj.export_obj(s, **kwargs)

def export_stl(scene, ascii=False):
    """Export a scene as a binary or ASCII STL file.

    This uses trimesh.exchange.stl.export_stl

    Args:
        scene (scene_synthesizer.Scene): Scene to be exported.
        ascii (bool, optional): Binary or ASCII encoding. Defaults to False.

    Returns:
        str or bytes: Scene mesh represented in binary or ASCII STL form.
    """
    if ascii:
        return trimesh.exchange.stl.export_stl_ascii(
            scene.scene.dump(concatenate=True),
        )
    else:
        return trimesh.exchange.stl.export_stl(
            scene.scene.dump(concatenate=True),
        )

def export_ply(scene, **kwargs):
    """Export a scene in the PLY format.

    This uses trimesh.exchange.ply.export_ply

    Args:
        scene (scene_synthesizer.Scene): Scene to be exported.
        **encoding (str): PLY encoding: 'ascii' or 'binary_little_endian'. Defaults to 'binary'.
        **vertex_normal (bool or None) : None or include vertex normals. Defaults to None.
        **include_attributes (bool) : Defaults to True.

    Returns:
        str or bytes: Scene mesh represented in binary or ASCII PLY form.
    """
    return trimesh.exchange.ply.export_ply(
        scene.scene.dump(concatenate=True),
        **kwargs
    )
    

def export_dict(scene, use_base64=False, include_metadata=True):
    """Export a scene to a dictionary.
    
    This uses trimesh.exchange.export.scene_to_dict

    Args:
        scene (scene_synthesizer.Scene): Scene to be exported.
        use_base64 (bool, optional): Encode arrays with base64 or not. Defaults to False.
        include_metadata (bool, optional): Whether to include scene metadata. Defaults to True.

    Returns:
        dict: Scene as dictionary.
    """
    return trimesh.exchange.export.scene_to_dict(
        scene=scene.scene,
        use_base64=use_base64,
        include_metadata=include_metadata,
    )

def export_json(scene, use_base64=False, include_metadata=True):
    """Export a scene to a JSON string.

    Note, the resulting JSON file can be loaded again via scene_synthesizer.Scene.load().

    Args:
        scene (scene_synthesizer.Scene): Scene to be exported.
        use_base64 (bool, optional): Encode arrays with base64 or not. Defaults to False.
        include_metadata (bool, optional): Whether to include scene metadata. Defaults to True.

    Returns:
        str: Scene as JSON string.
    """
    dict_data = trimesh.exchange.export.scene_to_dict(
        scene=scene.scene,
        use_base64=use_base64,
        include_metadata=include_metadata,
    )

    data = json.dumps(dict_data)

    return data

def export_scene(scene, file_obj, file_type=None, resolver=None, **kwargs):
    """Export a scene to the desired file format.

    Args:
        scene (scene_synthesizer.Scene): Scene to export.
        file_obj (str or None): Filename or None. If None will return data.
        file_type (str, optional): If None, file_obj will be used to infer file_type. Defaults to None.
        resolver (trimesh.resolvers.Resolver, optional): If None, a FilePathResolver is used. Defaults to None.

    Raises:
        ValueError: If file format is unknown.
        ValueError: If file_obj is None and file_type is None.

    Returns:
        str or bytes or dict: Only if file_obj is None.
    """
    if len(scene.geometry) == 0:
        raise ValueError("Can't export empty scene!")
    
    # if we weren't passed a file type extract from file_obj
    if file_type is None:
        if isinstance(file_obj, str):
            file_type = str(file_obj).split(".")[-1]
        else:
            raise ValueError("file_type not specified!")

    # remove whitepace and leading characters
    file_type = file_type.strip().lower().lstrip(".")
    
    data = None
    
    # handle different export file types
    if file_type == "glb":
        data = export_glb(scene, **kwargs)
    elif file_type == "gltf":
        data = export_gltf(scene, **kwargs)
    elif file_type == "obj":
        # if we are exporting by name automatically create a
        # resolver which lets the exporter write assets like
        # the materials and textures next to the exported mesh
        if resolver is None and isinstance(file_obj, str):
            resolver = trimesh.resolvers.FilePathResolver(file_obj)
        data = export_obj(scene, resolver=resolver, **kwargs)
    elif file_type == "stl":
        data = export_stl(scene, **kwargs)
    elif file_type == "ply":
        data = export_ply(scene, **kwargs)
    elif file_type == "dict":
        data = export_dict(scene, **kwargs)
    elif file_type == "json":
        data = export_json(scene, **kwargs)
    elif file_type == "urdf":
        data = export_urdf(scene, fname=file_obj, **kwargs)
        return data
    elif file_type == "usd" or file_type == "usda" or file_type == "usdc":
        data = export_usd(scene, fname=file_obj, file_type=file_type, **kwargs)
        return data
    else:
        raise ValueError(f"Unknown file format: {file_type}")
    
    if isinstance(data, dict):
        # GLTF files return a dict-of-bytes as they
        # represent multiple files so create a filepath
        # resolver and write the files if someone passed
        # a path we can write to.
        if resolver is None and isinstance(file_obj, str):
            resolver = trimesh.resolvers.FilePathResolver(file_obj)
            # the requested "gltf"
            bare_path = os.path.split(file_obj)[-1]
            for name, blob in data.items():
                if name == "model.gltf":
                    # write the root data to specified file
                    resolver.write(bare_path, blob)
                else:
                    # write the supporting files
                    resolver.write(name, blob)
        return data

    if isinstance(file_obj, str) and data is not None:
        # write data to file
        file_path = os.path.expanduser(os.path.abspath(file_obj))

        with open(file_path, "wb") as f:
            trimesh.util.write_encoded(f, data)
    else:
        return data
