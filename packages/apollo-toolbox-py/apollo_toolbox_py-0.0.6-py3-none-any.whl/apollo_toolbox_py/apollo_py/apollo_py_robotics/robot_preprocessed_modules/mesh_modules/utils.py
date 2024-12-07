from typing import Optional, List

from apollo_toolbox_py.apollo_py.path_buf import PathBuf


def recover_full_mesh_path_bufs_from_relative_mesh_paths_options(resources_root_directory,
                                                                 relative_paths: List[Optional[str]]) -> List[
    Optional[PathBuf]]:
    return list(map(lambda x: None if x is None else resources_root_directory.directory.append_path(x), relative_paths))


def recover_full_mesh_path_bufs_from_relative_mesh_paths_lists(resources_root_directory,
                                                               relative_paths: List[List[str]]) -> List[
    List[PathBuf]]:
    return list(
        map(lambda x: list(map(lambda y: resources_root_directory.directory.append_path(y), x)), relative_paths))
