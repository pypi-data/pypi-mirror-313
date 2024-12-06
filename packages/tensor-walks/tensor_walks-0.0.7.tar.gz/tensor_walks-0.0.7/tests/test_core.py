"""Basic tests for tensor_walks core
"""

import unittest

import numpy as np

from tensor_walks.core import General_Impl
from tensor_walks.impl_np import NP_Impl
from tensor_walks.impl_torch import Torch_Impl

BACKENDS: list[General_Impl] = [NP_Impl(), Torch_Impl("cpu")]


class TestIndexing(unittest.TestCase):
    """Test the linearization of z and t stacks"""

    def setUp(self):
        #                  0   1  2  3  4  5  6  7
        self.tracking_1 = [-1, 0, 1, 2, 3, 4, 5, 5]
        self.num_children_gt = [1, 1, 1, 1, 1, 2, 0, 0]

        self.walk_tests = [
            {
                "tracking": self.tracking_1,
                "sources": [7],
                "num_steps": 6,
                "walk_gt": [[7, 5, 4, 3, 2, 1, 0]],
            },
            {
                "tracking": self.tracking_1,
                "sources": [7],
                "num_steps": 7,
                "walk_gt": [[7, 5, 4, 3, 2, 1, 0, -1]],
            },
            {
                "tracking": self.tracking_1,
                "sources": [7, 6],
                "num_steps": 6,
                "walk_gt": [
                    [
                        7,
                        5,
                        4,
                        3,
                        2,
                        1,
                        0,
                    ],
                    [6, 5, 4, 3, 2, 1, 0],
                ],
            },
            {
                "tracking": self.tracking_1,
                "sources": [7, 6],
                "num_steps": 3,
                "walk_gt": [[7, 5, 4, 3], [6, 5, 4, 3]],
            },
            {
                "tracking": self.tracking_1,
                "sources": [7, 6],
                "num_steps": 3,
                "walk_gt": [[7, -1, -1, -1], [6, -1, -1, -1]],
                "stop_at_split": True,
            },
        ]

        #               0  1  2  3  4  5  6  7
        ct_tracking = [-1, 0, 1, 2, 3, 3, 4, 5]
        #               0       1       2       3       4         5        6         7
        ct_centroids = [
            [0, 0],
            [3, 0],
            [6, 0],
            [9, 0],
            [12, -5],
            [12, 5],
            [15, -5],
            [15, 5],
        ]

        self.centroid_tests = [
            {
                "tracking": ct_tracking,
                "centroids": ct_centroids,
                "sources": [7],
                "num_steps": 2,
                "centroids_gt": [[[15, 5], [12, 5], [9, 0]]],
            }
        ]

        self.distance_tests = [
            {
                "tracking": ct_tracking,
                "centroids": ct_centroids,
                "sources": [7],
                "num_steps": 2,
                "centroids_gt": [[[15, 5], [12, 5], [9, 0]]],
                "avg_movement_gt": [
                    np.mean(list(map(np.linalg.norm, [[3, 0], [3, 5]])))
                ],
                "movement_gt": [[[3, 0], [3, 5]]],
                "movement_gt_mask": [[[True, True], [True, True]]],
            }
        ]

    def test_num_children(self):

        for backend in BACKENDS:
            tracking = backend.array(self.tracking_1, dtype=backend.backend.int64)
            gt_num_children = backend.array(
                self.num_children_gt, dtype=backend.backend.int64
            )

            num_children = backend.compute_num_children(tracking)

            num_children = backend.to_numpy(num_children)
            gt_num_children = backend.to_numpy(gt_num_children)

            np.testing.assert_array_equal(num_children, gt_num_children)

    def test_walk_upward(self):

        for backend in BACKENDS:
            for walk_test in self.walk_tests:
                tracking = backend.array(
                    walk_test["tracking"], dtype=backend.backend.int64
                )
                sources = backend.array(
                    walk_test["sources"], dtype=backend.backend.int64
                )
                walk_gt = backend.array(
                    walk_test["walk_gt"], dtype=backend.backend.int64
                )
                num_steps = walk_test["num_steps"]
                stop_at_split = walk_test.get("stop_at_split", None) or False

                walk_comp = backend.compute_walks_upward(
                    tracking, sources, num_steps, stop_at_split=stop_at_split
                )

                walk_gt = backend.to_numpy(walk_gt)
                walk_comp = backend.to_numpy(walk_comp)

                np.testing.assert_array_equal(walk_gt, walk_comp)

    def test_compute_centroids(self):
        for backend in BACKENDS:
            for centroid_test in self.distance_tests:
                tracking = backend.array(
                    centroid_test["tracking"], dtype=backend.backend.int64
                )
                sources = backend.array(
                    centroid_test["sources"], dtype=backend.backend.int64
                )
                centroids = backend.array(
                    centroid_test["centroids"], dtype=backend.backend.float32
                )
                num_steps = centroid_test["num_steps"]
                stop_at_split = centroid_test.get("stop_at_split", None) or False

                # compute the walks
                walk_comp = backend.compute_walks_upward(
                    tracking, sources, num_steps, stop_at_split=stop_at_split
                )

                # test the centroids
                centroids_comp = backend.compute_centroids(walk_comp, centroids)
                centroids_gt = backend.to_numpy(
                    backend.array(centroid_test["centroids_gt"])
                )

                np.testing.assert_equal(backend.to_numpy(centroids_comp), centroids_gt)

                # test the movement
                movement_comp = backend.compute_moving_distances(
                    walk_comp, centroids
                ).mean(**{backend.axis: -1})
                movement_gt = backend.to_numpy(
                    backend.array(centroid_test["avg_movement_gt"])
                )

                np.testing.assert_almost_equal(
                    backend.to_numpy(movement_comp), movement_gt
                )

                (
                    movement_dist_comp,
                    movement_dist_mask_comp,
                ) = backend.compute_differences_along_walk(walk_comp, centroids)
                movement_dist_gt = backend.to_numpy(
                    backend.array(centroid_test["movement_gt"])
                )
                movement_dist_mask_gt = backend.to_numpy(
                    backend.array(centroid_test["movement_gt_mask"])
                )

                np.testing.assert_almost_equal(
                    backend.to_numpy(movement_dist_comp), movement_dist_gt
                )
                np.testing.assert_almost_equal(
                    backend.to_numpy(movement_dist_mask_comp), movement_dist_mask_gt
                )


if __name__ == "__main__":
    unittest.main()
