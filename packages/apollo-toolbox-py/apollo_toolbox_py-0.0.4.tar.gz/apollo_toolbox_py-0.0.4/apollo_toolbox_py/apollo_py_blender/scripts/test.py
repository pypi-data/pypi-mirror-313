from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.vectors import V
from apollo_toolbox_py.prelude import *

__all__ = ['tester']


def tester():
    motion = [[1., 0., 0., 0., 0., 0.], [1., 2., 3., 0., 0., 0.], [-1., -2., 3., 0., 0., 0.], [1., -2., 3., 4., 5., 0.]]

    r = ResourcesRootDirectory.new_from_default_apollo_robots_dir()
    s = r.get_subdirectory('ur5')
    c = s.to_chain_numpy()
    ch = ChainBlender.spawn(c, r)
    ch.keyframe_discrete_trajectory(motion, frame_stride=50)
    print(ch)
    return ch


if __name__ == '__main__':
    tester()
