from apollo_toolbox_py.apollo_py_numpy.apollo_py_numpy_linalg.vectors import V
from apollo_toolbox_py.prelude import *

__all__ = ['tester']


def interpolate_color(color1, color2, t):
    t = max(0, min(1, t))

    r = color1[0] * (1 - t) + color2[0] * t
    g = color1[1] * (1 - t) + color2[1] * t
    b = color1[2] * (1 - t) + color2[2] * t

    return r, g, b, 1.0


def tester(n: int):
    start = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    end = [0.0, 0.0, 0.0, 1.4, 0.5, 0.0, 0.0, -1.4, 1.3, 0.0, 0.3, 0.3, 1.3, 1.6, 0.2, -0.8, -1.3, -0.9, 0.5]

    start = V(start)
    end = V(end)

    start_color = [0.6, 0.8, 1.0]
    end_color = [0.4, 0.0, 0.6]

    r = ResourcesRootDirectory.new_from_default_apollo_robots_dir()
    c = r.get_subdirectory('h1').to_chain_numpy()
    for i in range(n):
        t = float(i) / (float(n) - 1)
        color = interpolate_color(start_color, end_color, t)
        state = (1.0 - t) * start + t * end

        cb = ChainBlender.spawn(c, r)
        cb.set_state_v(state)
        cb.set_all_links_plain_mesh_color(color)
        cb.set_all_links_plain_mesh_alpha(0.3)


if __name__ == '__main__':
    tester(2)
