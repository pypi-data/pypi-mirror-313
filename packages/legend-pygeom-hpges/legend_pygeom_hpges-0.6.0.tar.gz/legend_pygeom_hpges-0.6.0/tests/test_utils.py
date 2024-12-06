from __future__ import annotations

import numpy as np

from legendhpges import utils


def test_distances():
    # test conversion of coordinates

    coords = np.array([[1, 1, 1], [0, 0, 0]])
    coords_rz = utils.convert_coords(coords)

    assert coords_rz.ndim == 2
    assert np.shape(coords_rz) == (2, 2)
    assert np.allclose(coords_rz[1], np.array([0, 0]))

    # test shortest distance
    # in all these
    s1 = np.array([[0, 0]])
    s2 = np.array([[1, 0]])

    # first point on segment (distance is 0)
    # second directly above start (distance is 5)
    # third above the segment (distance is 7)
    # fourth outside the segment by 3 units in x and 4 in y (distance is 5)
    # last the same but for the first point

    points = np.array([[0.5, 0], [0, 5], [0.3, 7], [4, 4], [-3, 4]])
    res = np.array([0.0, 5.0, 7.0, 5.0, 5.0])
    assert np.allclose(utils.shortest_distance(s1, s2, points)[:, 0], res)

    # all distances shouldn't be affected by a global offset and rotation
    offset = np.array([107, -203])
    rot = np.array(
        [
            [np.cos(np.deg2rad(37)), -np.sin(np.deg2rad(37))],
            [np.sin(np.deg2rad(37)), np.cos(np.deg2rad(37))],
        ]
    )

    points_new = np.array([rot @ (p_tmp + offset) for p_tmp in points])
    s1_new = np.array([rot @ (s1_t + offset) for s1_t in s1])
    s2_new = np.array([rot @ (s2_t + offset) for s2_t in s2])
    assert np.allclose(
        utils.shortest_distance(s1_new, s2_new, points_new)[:, 0],
        res,
    )


def test_plane_distance_unconstrained():
    # start with a plane on the x,y plane
    a = np.array([0, 0, 1])
    d = 0
    points = np.array([[0, 0, 1], [1, 1, 7], [-5, 2, 9], [1, 0, 0]])
    assert np.allclose(
        utils.shortest_distance_to_plane(a, d, points), np.array([1, 7, 9, 0])
    )

    # a is the normal vector while d=p*a where p is a point on the plane i.e 0

    offset = np.array([107, -203, 197])
    d_new = np.sum(a * offset)

    assert np.allclose(
        utils.shortest_distance_to_plane(a, d_new, points + offset),
        np.array([1, 7, 9, 0]),
    )

    # now arbitrary rotation

    alpha = 35
    beta = 18
    gamma = 48

    ca = np.cos(np.deg2rad(alpha))
    cb = np.cos(np.deg2rad(beta))
    cg = np.cos(np.deg2rad(gamma))

    sa = np.sin(np.deg2rad(alpha))
    sb = np.sin(np.deg2rad(beta))
    sg = np.sin(np.deg2rad(gamma))

    rot = np.array(
        [
            [cb * cg, sa * sb * cg - ca * sg, ca * sb * cg + sa * sg],
            [cb * sg, sa * sb * sg + ca * cg, ca * sb * sg - sa * cg],
            [-sb, sa * cb, ca * cb],
        ]
    )
    p_new = rot @ offset
    points_new = np.array([rot @ (p_tmp + offset) for p_tmp in points])
    a_new = rot @ a
    d_new = np.sum(p_new * a_new)

    assert np.allclose(
        utils.shortest_distance_to_plane(a_new, d_new, points_new),
        np.array([1, 7, 9, 0]),
    )


def test_plane_distance_constrained():
    # vertical plane at x=3
    a = np.array([1, 0, 0])
    d = 3
    points = np.array([[0, 0, 10], [2, 0, -7], [3, 5, -17], [2.9, 4, -5]])

    assert np.allclose(
        utils.shortest_distance_to_plane(a, d, points, rmax=5),
        np.array([3, 1, np.nan, 0.1]),
        equal_nan=True,
    )
    assert np.allclose(
        utils.shortest_distance_to_plane(a, d, points, rmax=5, zrange=[-100, 1]),
        np.array([np.nan, 1, np.nan, 0.1]),
        equal_nan=True,
    )
