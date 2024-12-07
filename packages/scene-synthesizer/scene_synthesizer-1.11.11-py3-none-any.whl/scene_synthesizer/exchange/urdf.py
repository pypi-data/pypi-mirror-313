# Standard Library
import copy
import os

# Third Party
import numpy as np
import trimesh
import trimesh.transformations as tra
import yourdfpy

# Local Folder
from .. import utils
from ..utils import log


def export_urdf(scene,
                fname,
                folder=None,
                mesh_dir=None,
                use_absolute_mesh_paths=False,
                include_camera_node=False,
                include_light_nodes=False,
                separate_assets=False,
                write_mesh_files=False,
                write_mesh_file_type="obj",
                single_geometry_per_link=False,
                mesh_path_prefix=None,
                ignore_layers=None,
                ):
    """Export scene to one/multiple URDF files or return URDF data as string(s).

    Args:
        scene (scene_synthesizer.Scene): Scene description.
        fname (str): URDF filename or None. If None, the URDF data is returned as one or multiple strings.
        folder (str, optional): Only used if fname is None. The folder in which to export the URDF. Affects the location of textures. Defaults to None.
        mesh_dir (str, optional): Mesh directory to write polygon meshes to. Defaults to the directory part of fname or folder if fname is None.
        use_absolute_mesh_paths (bool, optional): If set to True will convert all mesh paths to absolute ones. Defaults to False.
        mesh_path_prefix (str, optional): Can be used to set file name prefix for meshes to "file://" or "package://". Defaults to "".
        write_mesh_files (bool, optional): If False, mesh file names in the URDF will point to the asset source files. If True, the meshes will be written to the URDF mesh directory. Defaults to True.
        write_mesh_file_type (str, optional): File type that will be used if write_mesh_files is True. Defaults to "obj".
        separate_assets (bool, optional): If True, each asset in the scene will be exported to a separate URDF file, named according to its object identifier. Note: The scene itself will not be exported; each asset's transformation will not be preserved. Defaults to False.
        include_camera_node (bool, optional): Whether to include a link for the camera node. Defaults to False.
        include_light_nodes (bool, optional): Whether to include a link for the light nodes. Defaults to False.
        single_geometry_per_link (bool, optional): If True will add only one visual/collision geometry per link. This creates a lot of links and fixed joints. Defaults to False.
        ignore_layers (bool, optional): If True will add all geometries as visual and collision geometries. If None, will it will be (num_layers < 2). Defaults to None.

    Raises:
        ValueError: Raise an exception if mesh_dir is not absolute but use_absolute_mesh_paths=True.

    Returns:
        str (optional): If fname is None, will return the URDF data as a string.
        dict[str, str] (optional): If fname=None and separate_assets=True will return the additional assets as URDF strings in a dictionary.
    """
    if fname is not None and folder is not None:
        log.warn(f"URDF export: folder={folder} will be ignored since file name is already specified.")
    
    if folder is None or len(folder) == 0:
        folder = "."
    if fname is not None:
        folder, fname = os.path.split(fname)
    
    # Remember current scene configuration to re-apply it after export
    current_configuration = scene.get_configuration()
    scene.zero_configurations()

    if mesh_dir is None:
        mesh_dir = folder
    else:
        # attach to URDF file directory (in case it's not an absolute path)
        mesh_dir = os.path.join(folder, mesh_dir)

    # create directory
    if not os.path.exists(mesh_dir):
        os.makedirs(mesh_dir)

    if not os.path.exists(folder):
        os.makedirs(folder)

    if use_absolute_mesh_paths:
        if not os.path.isabs(mesh_dir):
            raise ValueError(
                f"The used mesh path is not absolute ('{mesh_dir}') but"
                " use_absolute_mesh_paths=True."
            )

    def _add_mesh_path_prefix(urdf_model, prefix):
        for l in urdf_model.robot.links:
            for vc in l.visuals + l.collisions:
                if vc.geometry is not None and vc.geometry.mesh is not None:
                    vc.geometry.mesh.filename = prefix + vc.geometry.mesh.filename

    urdf_models = {}

    if ignore_layers is None:
        num_layers = len(
            set(
                [
                    scene._scene.geometry[g].metadata["layer"]
                    for g in scene._scene.geometry
                    if "layer" in scene._scene.geometry[g].metadata
                ]
            )
        )
        ignore_layers = num_layers < 2

    if separate_assets:
        for obj_id in scene.metadata["object_nodes"]:
            urdf_model = scene_as_urdf(
                scene=scene,
                include_camera_node=include_camera_node,
                include_light_nodes=include_light_nodes,
                robot_name=obj_id,
                nodes=scene.metadata["object_nodes"][obj_id],
                ignore_namespace=True,
                write_mesh_files=write_mesh_files,
                write_mesh_file_type=write_mesh_file_type,
                write_mesh_dir=mesh_dir,
                ignore_layers=ignore_layers,
                single_geometry_per_link=single_geometry_per_link,
            )
            urdf_fname = os.path.join(folder, obj_id + ".urdf")
            urdf_models[urdf_fname] = urdf_model
    else:
        main_urdf_model = scene_as_urdf(
            scene=scene,
            include_camera_node=include_camera_node,
            include_light_nodes=include_light_nodes,
            write_mesh_files=write_mesh_files,
            write_mesh_file_type=write_mesh_file_type,
            write_mesh_dir=mesh_dir,
            ignore_layers=ignore_layers,
            single_geometry_per_link=single_geometry_per_link,
        )
        if fname is not None:
            urdf_models[os.path.join(folder, fname)] = main_urdf_model

    extra_return_data = None
    for urdf_fname, urdf_model in urdf_models.items():
        if not use_absolute_mesh_paths:
            for l in urdf_model.robot.links:
                for vc in l.visuals + l.collisions:
                    if vc.geometry is not None and vc.geometry.mesh is not None:
                        # get relative path
                        vc.geometry.mesh.filename = os.path.relpath(
                            vc.geometry.mesh.filename, os.path.dirname(urdf_fname)
                        )

        if mesh_path_prefix is not None:
            _add_mesh_path_prefix(urdf_model=urdf_model, prefix=mesh_path_prefix)

        if fname is None:
            extra_return_data[urdf_fname] = urdf_model.write_xml_string()
        else:
            urdf_model.write_xml_file(urdf_fname)

    # set scene configuration back to original values
    scene.update_configuration(current_configuration)

    if fname is None:
        if extra_return_data is None:
            return main_urdf_model.write_xml_string()
        else:
            return main_urdf_model.write_xml_string(), extra_return_data


def scene_as_urdf(
    scene,
    include_camera_node=False,
    include_light_nodes=False,
    robot_name="Scene",
    nodes=None,
    ignore_namespace=False,
    write_mesh_files=False,
    write_mesh_file_type="obj",
    write_mesh_dir=None,
    ignore_layers=False,
    single_geometry_per_link=False,
):
    """Create a URDF data structure based on yourdfpy of a scene.

    Args:
        scene (scene_synthesizer.Scene): A scene.
        include_camera_node (bool, optional): Whether to include a link for the camera node. Defaults to False.
        include_light_nodes (bool, optional): Whether to include a link for the light nodes. Defaults to False.
        robot_name (str, optional): Name of the URDF <robot>. Defaults to "Scene".
        nodes (list[str], optional): The scene graph nodes to consider. None means the all nodes in the scene are used. Defaults to None.
        ignore_namespace (bool, optional): If True will remove namespace when converting node/edge names to link/joint names, if possible. Defaults to False.
        write_mesh_files (bool, optional): If True will write meshes to files on disk. Defaults to True.
        write_mesh_file_type (str, optional): File type that will be used if write_mesh_files is True. Defaults to 'obj'.
        write_mesh_dir (str, optional): Output directory that will be used if write_mesh_files is True. None is current directory. Defaults to None.
        ignore_layers (bool, optional): If True will add all geometries as visual and collision geometries. Defaults to False.
        single_geometry_per_link (bool, optional): If True will add only one visual/collision geometry per link. This creates a lot of links and fixed joints. Defaults to False.
    Returns:
        model (yourdfpy.URDF): URDF model.
    """
    urdf_model = yourdfpy.Robot(name=robot_name)

    def _get_urdf_geometry(
        node, write_mesh_files=False, write_mesh_file_type="obj", write_mesh_dir=None
    ):
        geom_name = scene._scene.graph.transforms.node_data[node]["geometry"]
        trimesh_geometry = scene._scene.geometry[geom_name]
        origin = np.eye(4)

        primitive_possible = hasattr(trimesh_geometry, "primitive")

        if not primitive_possible:
            scale = None
            output_dir = "" if write_mesh_dir is None else write_mesh_dir
            filename = (
                _get_urdf_name(geom_name, ignore_namespace=False) + "." + write_mesh_file_type
            )

            need_to_write_mesh_file = ("file_path" not in trimesh_geometry.metadata) or (
                "file_path" in trimesh_geometry.metadata
                and not trimesh_geometry.metadata["file_path"]
                .upper()
                .endswith(("OBJ", "STL", "DAE", "GLB", "GLTF", "MESH"))
            )
            if write_mesh_files or need_to_write_mesh_file:
                output_fname = os.path.join(output_dir, filename)

                material_name = _get_urdf_name(
                        geom_name, ignore_namespace=False
                    )
                if hasattr(trimesh_geometry.visual, "material"):
                    trimesh_geometry.visual.material.name = material_name
                
                trimesh_geometry.export(output_fname, mtl_name=material_name + ".mtl")

            else:
                if (
                    "file_element" in trimesh_geometry.metadata
                    and trimesh_geometry.metadata["file_element"] > 0
                ):
                    # This means this mesh came from an obj that is already included
                    return None, None

                output_fname = trimesh_geometry.metadata["file_path"]
                if "scale" in trimesh_geometry.metadata:
                    scale = trimesh_geometry.metadata["scale"]
                elif os.path.exists(output_fname):
                    # Alternative load file and check
                    log.debug(f"Will load original mesh {output_fname} to calculate scaling.")

                    if "file_element" in trimesh_geometry.metadata:
                        m = list(
                            trimesh.load(
                                output_fname, force="scene", skip_materials=True
                            ).geometry.values()
                        )[0]
                    else:
                        m = trimesh.load(output_fname, force="mesh", skip_materials=True)

                    # avoid division by zero
                    if len(np.nonzero(m.bounds[0])) < 3:
                        scale = scene.get_bounds(query=[node], frame=node)[1] / m.bounds[1]
                    else:
                        scale = scene.get_bounds(query=[node], frame=node)[0] / m.bounds[0]

                    if np.allclose(scale[0], scale):
                        # use scalar scale
                        scale = scale[0]
                else:
                    scale = 1.0
                    log.warning(
                        f"Can't find original extents of file {output_fname}. Will assume scale"
                        f" = {scale}."
                    )

                if not os.path.exists(output_fname):
                    # This is a generated mesh, e.g. by boolean operations
                    output_fname = os.path.join(output_dir, filename)

                    trimesh_geometry.export(output_fname)

            return origin, yourdfpy.Geometry(
                mesh=yourdfpy.Mesh(
                    filename=output_fname,
                    scale=scale,
                )
            )
        elif hasattr(trimesh_geometry, "primitive"):
            if isinstance(trimesh_geometry, trimesh.primitives.Sphere):
                origin = tra.translation_matrix(trimesh_geometry.primitive.center)
                return origin, yourdfpy.Geometry(
                    sphere=yourdfpy.Sphere(radius=trimesh_geometry.primitive.radius)
                )
            elif isinstance(trimesh_geometry, trimesh.primitives.Box):
                origin = trimesh_geometry.primitive.transform.copy()
                return origin, yourdfpy.Geometry(
                    box=yourdfpy.Box(size=trimesh_geometry.primitive.extents)
                )
            elif isinstance(trimesh_geometry, trimesh.primitives.Cylinder):
                origin = trimesh_geometry.primitive.transform.copy()
                return origin, yourdfpy.Geometry(
                    cylinder=yourdfpy.Cylinder(
                        radius=trimesh_geometry.primitive.radius,
                        length=trimesh_geometry.primitive.height,
                    )
                )
            elif isinstance(trimesh_geometry, trimesh.primitives.Capsule):
                raise ValueError("URDF doesn't have a capsule primitive.")
            else:
                raise ValueError("Unknown primitive. Can't convert.")

    def _get_urdf_name(name, ignore_namespace):
        if name is None:
            return None

        if ignore_namespace and "/" in name:
            node_name = "_".join(name.split("/")[1:])
        else:
            node_name = name
        return node_name.replace("/", "_").replace(":", "_")

    def _get_urdf_joint_name(joint_name, parent_link, child_link):
        if joint_name is None:
            return parent_link + "_to_" + child_link

        return joint_name

    if not single_geometry_per_link:
        link_nodes, link_roots, joints = scene.get_links(nodes=nodes)

        for l_nodes, root_node in zip(link_nodes, link_roots):
            # inertial = yourdfpy.Inertial(mass=mass, inertia=np.eye(3), origin=inertial_origin)

            link = yourdfpy.Link(
                name=_get_urdf_name(root_node, ignore_namespace=ignore_namespace),
                inertial=None,
                visuals=[],
                collisions=[],
            )
            inertial_origins = []
            masses = []
            for node in l_nodes:
                if not include_camera_node and node == scene._scene.camera.name:
                    # Avoid exporting camera node
                    continue

                if not include_light_nodes and node in [x.name for x in scene._scene.lights]:
                    # Avoid exporting light nodes
                    continue

                # node_name = _get_urdf_name(node, ignore_namespace=ignore_namespace)

                if node in scene._scene.graph.nodes_geometry:
                    geom_name_export = _get_urdf_name(
                        scene._scene.graph.transforms.node_data[node]["geometry"],
                        ignore_namespace=False,
                    )
                    geometry_origin, geometry = _get_urdf_geometry(
                        node=node,
                        write_mesh_files=write_mesh_files,
                        write_mesh_file_type=write_mesh_file_type,
                        write_mesh_dir=write_mesh_dir,
                    )

                    visuals = []
                    collisions = []
                    if geometry is not None:
                        geom_name = scene._scene.graph.transforms.node_data[node]["geometry"]
                        trimesh_geometry = scene._scene.geometry[geom_name]

                        geometry_origin = scene.get_transform(node, root_node) @ geometry_origin

                        mass, center_mass, _, _ = utils.get_mass_properties(trimesh_geometry)
                        inertial_origin = np.eye(4)
                        inertial_origin[:3, 3] = center_mass
                        # inertial_origin[:3, :3] = inertia

                        inertial_origins.append(inertial_origin)
                        masses.append(mass)

                        if (
                            (
                                "layer" in trimesh_geometry.metadata
                                and trimesh_geometry.metadata["layer"] == "visual"
                            )
                            or not "layer" in trimesh_geometry.metadata
                            or ignore_layers
                        ):
                            material = None
                            if hasattr(trimesh_geometry.visual, "main_color"):
                                color = yourdfpy.Color(
                                    rgba=trimesh_geometry.visual.main_color / 255.0
                                )
                                material = yourdfpy.Material(
                                    name=f"{geom_name_export}_main_color", color=color
                                )

                            link.visuals.append(
                                yourdfpy.Visual(
                                    name=geom_name_export,
                                    origin=geometry_origin,
                                    geometry=geometry,
                                    material=material,
                                )
                            )

                        if (
                            (
                                "layer" in trimesh_geometry.metadata
                                and trimesh_geometry.metadata["layer"] == "collision"
                            )
                            or not "layer" in trimesh_geometry.metadata
                            or ignore_layers
                        ):
                            link.collisions.append(
                                yourdfpy.Collision(
                                    name=geom_name_export,
                                    origin=geometry_origin.copy(),
                                    geometry=copy.deepcopy(geometry),
                                )
                            )

            if len(masses) > 0:
                inertial_origin = np.eye(4)
                inertial_origin[:3, 3] = np.array(masses).dot(
                    np.array(inertial_origins)[:, :3, 3]
                ) / sum(masses)
                link.inertial = yourdfpy.Inertial(
                    mass=sum(masses), inertia=np.eye(3), origin=inertial_origin
                )
            else:
                # default value
                link.inertial = (
                    None
                )

            urdf_model.links.append(link)

        for parent_node, child_node in joints:
            joint_data = joints[(parent_node, child_node)]
            old_parent, _, properties = joint_data
            joint_properties = properties["extras"]["joint"]

            parent_name = _get_urdf_name(parent_node, ignore_namespace=ignore_namespace)
            child_name = _get_urdf_name(child_node, ignore_namespace=ignore_namespace)

            joint_limit = None
            joint_axis = None
            if joint_properties["type"] not in ["fixed", "floating"]:
                joint_limit = yourdfpy.Limit(
                    effort=joint_properties["limit_effort"],
                    velocity=joint_properties["limit_velocity"],
                    lower=joint_properties["limit_lower"],
                    upper=joint_properties["limit_upper"],
                )
                joint_axis = joint_properties["axis"]

            joint_origin = properties.get("matrix", np.eye(4))
            joint = yourdfpy.Joint(
                name=_get_urdf_joint_name(
                    joint_name=_get_urdf_name(
                        joint_properties["name"], ignore_namespace=ignore_namespace
                    ),
                    parent_link=parent_name,
                    child_link=child_name,
                ),
                type=joint_properties["type"],
                parent=parent_name,
                child=child_name,
                origin=scene.get_transform(old_parent, parent_node) @ joint_origin,
                axis=joint_axis,
                limit=joint_limit,
            )
            urdf_model.joints.append(joint)
    else:
        graph_nodes = scene._scene.graph.nodes if nodes is None else nodes

        for node in graph_nodes:
            if not include_camera_node and node == scene._scene.camera.name:
                # Avoid exporting camera node
                continue

            if not include_light_nodes and node in [x.name for x in scene._scene.lights]:
                # Avoid exporting light nodes
                continue

            node_name = _get_urdf_name(node, ignore_namespace=ignore_namespace)

            if node in scene._scene.graph.nodes_geometry:
                geom_name_export = _get_urdf_name(
                    scene._scene.graph.transforms.node_data[node]["geometry"],
                    ignore_namespace=False,
                )
                geometry_origin, geometry = _get_urdf_geometry(
                    node=node,
                    write_mesh_files=write_mesh_files,
                    write_mesh_file_type=write_mesh_file_type,
                    write_mesh_dir=write_mesh_dir,
                )

                mass = None
                inertial_origin = np.eye(4)
                visuals = []
                collisions = []
                if geometry is not None:
                    geom_name = scene._scene.graph.transforms.node_data[node]["geometry"]
                    trimesh_geometry = scene._scene.geometry[geom_name]

                    mass, center_mass, _, _ = utils.get_mass_properties(trimesh_geometry)
                    inertial_origin[:3, 3] = center_mass
                    # inertial_origin[:3, :3] = inertia

                    if (
                        (
                            "layer" in trimesh_geometry.metadata
                            and trimesh_geometry.metadata["layer"] == "visual"
                        )
                        or not "layer" in trimesh_geometry.metadata
                        or ignore_layers
                    ):
                        material = None
                        if hasattr(trimesh_geometry.visual, "main_color"):
                            color = yourdfpy.Color(rgba=trimesh_geometry.visual.main_color / 255.0)
                            material = yourdfpy.Material(
                                name=f"{geom_name_export}_main_color", color=color
                            )

                        visuals = [
                            yourdfpy.Visual(
                                name=geom_name_export,
                                origin=geometry_origin.copy(),
                                geometry=geometry,
                                material=material,
                            )
                        ]

                    if (
                        (
                            "layer" in trimesh_geometry.metadata
                            and trimesh_geometry.metadata["layer"] == "collision"
                        )
                        or not "layer" in trimesh_geometry.metadata
                        or ignore_layers
                    ):
                        collisions = [
                            yourdfpy.Collision(
                                name=geom_name_export,
                                origin=geometry_origin.copy(),
                                geometry=copy.deepcopy(geometry),
                            )
                        ]
                inertial = yourdfpy.Inertial(mass=mass, inertia=np.eye(3), origin=inertial_origin)

                link = yourdfpy.Link(
                    name=node_name,
                    inertial=inertial,
                    visuals=visuals,
                    collisions=collisions,
                )
            else:
                # inertial = yourdfpy.Inertial(
                #     mass=0.0,
                #     inertia=np.eye(3),  # origin=np.eye(4)
                # )
                link = yourdfpy.Link(name=node_name)

            urdf_model.links.append(link)

        link_names = [l.name for l in urdf_model.links]

        for parent, child, properties in scene._scene.graph.to_edgelist():
            if nodes is not None and ((parent not in nodes) or (child not in nodes)):
                continue

            parent_name = _get_urdf_name(parent, ignore_namespace=ignore_namespace)
            child_name = _get_urdf_name(child, ignore_namespace=ignore_namespace)

            if parent_name not in link_names or child_name not in link_names:
                # parent or child is not part of the urdf
                # this can be e.g. the case for a camera or light node
                continue

            edge_data = scene._scene.graph.transforms.edge_data[(parent, child)]
            if (
                "extras" in edge_data
                and edge_data["extras"] is not None
                and "joint" in edge_data["extras"]
            ):
                joint_properties = edge_data["extras"]["joint"]

                joint_limit = None
                joint_axis = None
                if joint_properties["type"] not in ["fixed", "floating"]:
                    joint_limit = yourdfpy.Limit(
                        effort=joint_properties["limit_effort"],
                        velocity=joint_properties["limit_velocity"],
                        lower=joint_properties["limit_lower"],
                        upper=joint_properties["limit_upper"],
                    )
                    joint_axis = joint_properties["axis"]

                joint = yourdfpy.Joint(
                    name=_get_urdf_joint_name(
                        joint_name=_get_urdf_name(
                            joint_properties["name"], ignore_namespace=ignore_namespace
                        ),
                        parent_link=parent_name,
                        child_link=child_name,
                    ),
                    type=joint_properties["type"],
                    parent=parent_name,
                    child=child_name,
                    origin=properties["matrix"],
                    axis=joint_axis,
                    limit=joint_limit,
                )
            else:
                joint = yourdfpy.Joint(
                    name=_get_urdf_joint_name(
                        joint_name=None,
                        parent_link=parent_name,
                        child_link=child_name,
                    ),
                    type="fixed",
                    parent=parent_name,
                    child=child_name,
                    origin=properties["matrix"] if "matrix" in properties else None,
                )
            urdf_model.joints.append(joint)

    return yourdfpy.URDF(
        urdf_model,
        build_scene_graph=False,
        load_meshes=False,
        build_collision_scene_graph=False,
        load_collision_meshes=False,
        filename_handler=yourdfpy.urdf.filename_handler_null,
    )
