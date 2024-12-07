from typing import List, Optional, Dict

from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.mesh_modules.utils import \
    recover_full_mesh_path_bufs_from_relative_mesh_paths_options
from apollo_toolbox_py.apollo_py.path_buf import PathBuf


# from apollo_toolbox_py.apollo_py.path_buf import PathBufPyWrapper


class ApolloOriginalMeshesModule:
    def __init__(self, link_mesh_relative_paths: List[Optional[str]]):
        self.link_mesh_relative_paths: List[Optional[PathBuf]] = list(
            map(lambda x: None if x is None else PathBuf().append(x), link_mesh_relative_paths))

    def __repr__(self):
        return f"ApolloOriginalMeshesModule(link_mesh_relative_paths={list(map(lambda x: None if x is None else x.to_string(), self.link_mesh_relative_paths))})"

    def recover_full_path_bufs(self, resources_root_directory) -> List[Optional[PathBuf]]:
        return recover_full_mesh_path_bufs_from_relative_mesh_paths_options(resources_root_directory, self.link_mesh_relative_paths)

    @classmethod
    def from_dict(cls, data: Dict) -> 'ApolloOriginalMeshesModule':
        return cls(data['link_mesh_relative_paths'])
