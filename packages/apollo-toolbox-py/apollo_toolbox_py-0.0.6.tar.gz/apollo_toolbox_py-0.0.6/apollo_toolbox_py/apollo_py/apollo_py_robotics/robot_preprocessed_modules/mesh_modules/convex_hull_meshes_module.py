from typing import List, Optional, Dict

from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.mesh_modules.utils import \
    recover_full_mesh_path_bufs_from_relative_mesh_paths_options
from apollo_toolbox_py.apollo_py.path_buf import PathBuf


# from apollo_toolbox_py.apollo_py.path_buf import PathBufPyWrapper


class ApolloConvexHullMeshesModule:
    def __init__(self, stl_link_mesh_relative_paths: List[Optional[str]],
                 obj_link_mesh_relative_paths: List[Optional[str]], glb_link_mesh_relative_paths: List[Optional[str]]):
        self.stl_link_mesh_relative_paths: List[Optional[PathBuf]] = list(
            map(lambda x: None if x is None else PathBuf().append(x), stl_link_mesh_relative_paths))

        self.obj_link_mesh_relative_paths: List[Optional[PathBuf]] = list(
            map(lambda x: None if x is None else PathBuf().append(x), obj_link_mesh_relative_paths))

        self.glb_link_mesh_relative_paths: List[Optional[PathBuf]] = list(
            map(lambda x: None if x is None else PathBuf().append(x), glb_link_mesh_relative_paths))

    def __repr__(self):
        return (f"ApolloConvexHullMeshesModule("
                f"stl_link_mesh_relative_paths={list(map(lambda x: None if x is None else x.to_string(), self.stl_link_mesh_relative_paths))}, "
                f"obj_link_mesh_relative_paths={list(map(lambda x: None if x is None else x.to_string(), self.obj_link_mesh_relative_paths))},"
                f"glb_link_mesh_relative_paths={list(map(lambda x: None if x is None else x.to_string(), self.glb_link_mesh_relative_paths))} "
                f")")

    def recover_full_stl_path_bufs(self, resources_root_directory) -> List[
        Optional[PathBuf]]:
        return recover_full_mesh_path_bufs_from_relative_mesh_paths_options(resources_root_directory,
                                                                            self.stl_link_mesh_relative_paths)

    def recover_full_obj_path_bufs(self, resources_root_directory) -> List[
        Optional[PathBuf]]:
        return recover_full_mesh_path_bufs_from_relative_mesh_paths_options(resources_root_directory,
                                                                            self.obj_link_mesh_relative_paths)

    def recover_full_glb_path_bufs(self, resources_root_directory) -> List[
        Optional[PathBuf]]:
        return recover_full_mesh_path_bufs_from_relative_mesh_paths_options(resources_root_directory,
                                                                            self.glb_link_mesh_relative_paths)

    @classmethod
    def from_dict(cls, data: Dict) -> 'ApolloConvexHullMeshesModule':
        return cls(data['stl_link_mesh_relative_paths'], data['obj_link_mesh_relative_paths'],
                   data['glb_link_mesh_relative_paths'])
