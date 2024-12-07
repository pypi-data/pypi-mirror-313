
import json
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.chain_module import ApolloChainModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.connections_module import \
    ApolloConnectionsModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.dof_module import ApolloDOFModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.mesh_modules.convex_decomposition_meshes_module import \
    ApolloConvexDecompositionMeshesModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.mesh_modules.convex_hull_meshes_module import \
    ApolloConvexHullMeshesModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.mesh_modules.original_meshes_module import \
    ApolloOriginalMeshesModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.mesh_modules.plain_meshes_module import \
    ApolloPlainMeshesModule
from apollo_toolbox_py.apollo_py.apollo_py_robotics.robot_preprocessed_modules.urdf_module import ApolloURDFModule
from apollo_toolbox_py.apollo_py.path_buf import PathBuf
# from apollo_toolbox_py.apollo_py.path_buf import PathBufPyWrapper
from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_robotics.robot_runtime_modules.urdf_numpy_module import \
    ApolloURDFNumpyModule

__all__ = ['ResourcesRootDirectory', 'ResourcesSubDirectory']


class ResourcesRootDirectory:
    def __init__(self, directory: PathBuf):
        self.directory = directory

    @staticmethod
    def new_from_default_apollo_robots_dir() -> 'ResourcesRootDirectory':
        return ResourcesRootDirectory(PathBuf.new_from_default_apollo_robots_dir())

    @staticmethod
    def new_from_default_apollo_environments_dir() -> 'ResourcesRootDirectory':
        return ResourcesRootDirectory(PathBuf.new_from_default_apollo_environments_dir())

    def get_subdirectory(self, name: str) -> 'ResourcesSubDirectory':
        directory = self.directory.append(name)
        return ResourcesSubDirectory(name, self.directory, directory)


class ResourcesSubDirectory:
    def __init__(self, name: str, robots_directory: PathBuf, directory: PathBuf):
        self.name: str = name
        self.root_directory: PathBuf = robots_directory
        self.directory: PathBuf = directory

    def to_urdf_module(self) -> 'ApolloURDFModule':
        dd = self.directory.append('urdf_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloURDFModule.from_dict(d)

    def to_urdf_numpy_module(self) -> 'ApolloURDFNumpyModule':
        urdf_module = self.to_urdf_module()
        return ApolloURDFNumpyModule.from_urdf_module(urdf_module)

    def to_chain_module(self) -> 'ApolloChainModule':
        dd = self.directory.append('chain_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloChainModule.from_dict(d)

    def to_dof_module(self) -> 'ApolloDOFModule':
        dd = self.directory.append('dof_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloDOFModule.from_dict(d)

    def to_connections_module(self) -> 'ApolloConnectionsModule':
        dd = self.directory.append('connections_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloConnectionsModule.from_dict(d)

    def to_original_meshes_module(self) -> 'ApolloOriginalMeshesModule':
        dd = self.directory.append('mesh_modules/original_meshes_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloOriginalMeshesModule.from_dict(d)

    def to_plain_meshes_module(self) -> 'ApolloPlainMeshesModule':
        dd = self.directory.append('mesh_modules/plain_meshes_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloPlainMeshesModule.from_dict(d)

    def to_convex_hull_meshes_module(self) -> 'ApolloConvexHullMeshesModule':
        dd = self.directory.append('mesh_modules/convex_hull_meshes_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloConvexHullMeshesModule.from_dict(d)

    def to_convex_decomposition_meshes_module(self) -> 'ApolloConvexDecompositionMeshesModule':
        dd = self.directory.append('mesh_modules/convex_decomposition_meshes_module/module.json')
        st = dd.read_file_contents_to_string()
        d = json.loads(st)
        return ApolloConvexDecompositionMeshesModule.from_dict(d)

    def to_chain(self):
        from apollo_toolbox_py.apollo_py.apollo_py_robotics.chain import Chain
        return Chain(self)

    def to_chain_numpy(self):
        from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_robotics.chain_numpy import ChainNumpy
        return ChainNumpy(self)
