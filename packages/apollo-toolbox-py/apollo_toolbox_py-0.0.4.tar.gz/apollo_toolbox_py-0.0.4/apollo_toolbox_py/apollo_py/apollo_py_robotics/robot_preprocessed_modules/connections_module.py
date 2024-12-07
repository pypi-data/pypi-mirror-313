from typing import List, Optional, Dict

__all__ = ['ApolloConnectionsModule']


class ApolloConnectionsModule:
    def __init__(self, link_connection_paths: List[List[Optional[List[int]]]]):
        self.link_connection_paths = link_connection_paths

    def link_connection_paths(self) -> List[List[Optional[List[int]]]]:
        return self.link_connection_paths

    def get_link_connection_path(self, link_idx_i: int, link_idx_j: int) -> Optional[List[int]]:
        return self.link_connection_paths[link_idx_i][link_idx_j]

    def link_connection_exists(self, link_idx_i: int, link_idx_j: int) -> bool:
        return self.link_connection_paths[link_idx_i][link_idx_j] is not None

    @classmethod
    def from_dict(cls, data: Dict) -> 'ApolloConnectionsModule':
        link_connection_paths = data['link_connection_paths']
        return cls(link_connection_paths=link_connection_paths)

    def __repr__(self):
        return f"ApolloConnectionsModule(link_connection_paths={self.link_connection_paths})"
