from typing import List, Optional, Dict

__all__ = ['ApolloChainModule', 'ApolloLinkInChain', 'ApolloJointInChain']

class ApolloLinkInChain:
    def __init__(self, name: str, link_idx: int, parent_joint_idx: Optional[int], parent_link_idx: Optional[int],
                 children_joint_idxs: List[int], children_link_idxs: List[int]):
        self.name = name
        self.link_idx = link_idx
        self.parent_joint_idx = parent_joint_idx
        self.parent_link_idx = parent_link_idx
        self.children_joint_idxs = children_joint_idxs
        self.children_link_idxs = children_link_idxs

    def __repr__(self):
        return f"ApolloLinkInChain(name={self.name}, link_idx={self.link_idx}, parent_joint_idx={self.parent_joint_idx}, parent_link_idx={self.parent_link_idx}, children_joint_idxs={self.children_joint_idxs}, children_link_idxs={self.children_link_idxs})"


class ApolloJointInChain:
    def __init__(self, joint_name: str, joint_idx: int, parent_link_name: str, parent_link_idx: int,
                 child_link_name: str, child_link_idx: int):
        self.joint_name = joint_name
        self.joint_idx = joint_idx
        self.parent_link_name = parent_link_name
        self.parent_link_idx = parent_link_idx
        self.child_link_name = child_link_name
        self.child_link_idx = child_link_idx

    def __repr__(self):
        return f"ApolloJointInChain(joint_name={self.joint_name}, joint_idx={self.joint_idx}, parent_link_name={self.parent_link_name}, parent_link_idx={self.parent_link_idx}, child_link_name={self.child_link_name}, child_link_idx={self.child_link_idx})"


class ApolloChainModule:
    def __init__(self, links_in_chain: List[ApolloLinkInChain], joints_in_chain: List[ApolloJointInChain],
                 kinematic_hierarchy: List[List[int]], root_idx: int):
        self.links_in_chain = links_in_chain
        self.joints_in_chain = joints_in_chain
        self.kinematic_hierarchy = kinematic_hierarchy
        self.root_idx = root_idx

    @staticmethod
    def from_dict(data: Dict):
        links_in_chain = [ApolloLinkInChain(**link) for link in data['links_in_chain']]
        joints_in_chain = [ApolloJointInChain(**joint) for joint in data['joints_in_chain']]
        kinematic_hierarchy = data['kinematic_hierarchy']
        root_idx = data['root_idx']
        return ApolloChainModule(links_in_chain, joints_in_chain, kinematic_hierarchy, root_idx)

    def __repr__(self):
        return f"ApolloChainModule(links_in_chain={self.links_in_chain}, joints_in_chain={self.joints_in_chain}, kinematic_hierarchy={self.kinematic_hierarchy}, root_idx={self.root_idx})"
