from typing import List, Dict

from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.mesh_modules.utils import \
    recover_full_mesh_path_bufs_from_relative_mesh_paths_lists
from apollo_toolbox_py.apollo_py.path_buf import PathBuf


class ApolloConvexDecompositionMeshesModule:
    def __init__(self, stl_link_mesh_relative_paths: List[List[str]], obj_link_mesh_relative_paths: List[List[str]],
                 glb_link_mesh_relative_paths: List[List[str]]):
        self.stl_link_mesh_relative_paths: List[List[PathBuf]] = list(
            map(lambda x: list(map(lambda y: PathBuf().append(y), x)), stl_link_mesh_relative_paths))
        self.obj_link_mesh_relative_paths: List[List[PathBuf]] = list(
            map(lambda x: list(map(lambda y: PathBuf().append(y), x)), obj_link_mesh_relative_paths))
        self.glb_link_mesh_relative_paths: List[List[PathBuf]] = list(
            map(lambda x: list(map(lambda y: PathBuf().append(y), x)), glb_link_mesh_relative_paths))

        self._stl_link_mesh_relative_paths = stl_link_mesh_relative_paths
        self._obj_link_mesh_relative_paths = obj_link_mesh_relative_paths
        self._glb_link_mesh_relative_paths = glb_link_mesh_relative_paths

    def __repr__(self):
        return (f"ApolloConvexDecompositionMeshesModule("
                f"stl_link_mesh_relative_paths={self._stl_link_mesh_relative_paths}, "
                f"obj_link_mesh_relative_paths={self._obj_link_mesh_relative_paths},"
                f"glb_link_mesh_relative_paths={self._glb_link_mesh_relative_paths} "
                f")")

    def recover_full_stl_path_bufs(self, resources_root_directory) -> List[
        List[PathBuf]]:
        return recover_full_mesh_path_bufs_from_relative_mesh_paths_lists(resources_root_directory,
                                                                          self.stl_link_mesh_relative_paths)

    def recover_full_obj_path_bufs(self, resources_root_directory) -> List[
        List[PathBuf]]:
        return recover_full_mesh_path_bufs_from_relative_mesh_paths_lists(resources_root_directory,
                                                                          self.obj_link_mesh_relative_paths)

    def recover_full_glb_path_bufs(self, resources_root_directory) -> List[
        List[PathBuf]]:
        return recover_full_mesh_path_bufs_from_relative_mesh_paths_lists(resources_root_directory,
                                                                          self.glb_link_mesh_relative_paths)

    @classmethod
    def from_dict(cls, data: Dict) -> 'ApolloConvexDecompositionMeshesModule':
        return cls(data['stl_link_mesh_relative_paths'], data['obj_link_mesh_relative_paths'],
                   data['glb_link_mesh_relative_paths'])
