from typing import List, Dict

__all__ = ['ApolloDOFModule']


class ApolloDOFModule:
    def __init__(self, num_dofs: int, dof_idx_to_joint_idx_mapping: List[int],
                 joint_idx_to_dof_idxs_mapping: List[List[int]]):
        self.num_dofs = num_dofs
        self.dof_idx_to_joint_idx_mapping = dof_idx_to_joint_idx_mapping
        self.joint_idx_to_dof_idxs_mapping = joint_idx_to_dof_idxs_mapping

    def __repr__(self):
        return (f"ApolloDOFModule(num_dofs={self.num_dofs}, "
                f"dof_idx_to_joint_idx_mapping={self.dof_idx_to_joint_idx_mapping}, "
                f"joint_idx_to_dof_idxs_mapping={self.joint_idx_to_dof_idxs_mapping})")

    @classmethod
    def from_dict(cls, data: Dict) -> 'ApolloDOFModule':
        return cls(
            num_dofs=data['num_dofs'],
            dof_idx_to_joint_idx_mapping=data['dof_idx_to_joint_idx_mapping'],
            joint_idx_to_dof_idxs_mapping=data['joint_idx_to_dof_idxs_mapping']
        )
