from apollo_toolbox_py.apollo_py.apollo_py_robotics.resources_directories import ResourcesSubDirectory

__all__ = ['Chain']


class Chain:
    def __init__(self, s: ResourcesSubDirectory):
        self.sub_directory = s
        self.base_urdf_module = s.to_urdf_module()
        self.dof_module = s.to_dof_module()
        self.chain_module = s.to_chain_module()
        self.connections_module = s.to_connections_module()
        self.original_meshes_module = s.to_original_meshes_module()
        self.plain_meshes_module = s.to_plain_meshes_module()
        self.convex_hull_meshes_module = s.to_convex_hull_meshes_module()
        self.convex_decomposition_meshes_module = s.to_convex_decomposition_meshes_module()
