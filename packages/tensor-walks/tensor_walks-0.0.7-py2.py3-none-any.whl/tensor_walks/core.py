"""Core of the TensorTree library
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt


class General_Impl:
    """General Implementation that is tensor library independent and provides the main functionalities"""

    def __init__(self, backend, axis):
        self.backend = backend
        self.axis = axis

    @staticmethod
    def zeros(*args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def ones(*args, **kwargs):
        raise NotImplementedError()

    def zeros_like(self, *args, **kwargs):
        return self.backend.zeros_like(*args, **kwargs)

    def to_numpy(self, data) -> np.array:
        raise NotImplementedError()

    def unique(self, *args, **kwargs):
        return self.backend.unique(*args, **kwargs)

    @staticmethod
    def array(*args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def masked_array(data, mask, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def repeat(data, *args):
        raise NotImplementedError()

    @staticmethod
    def shape(data):
        # pylint: disable=W0613
        return NotImplementedError()

    @staticmethod
    def copy(data):
        # pylint: disable=W0613
        return NotImplementedError()

    def compute_num_children(self, tracking: npt.ArrayLike[int]) -> np.array:
        """Compute the number of children for every node in the tracking

        Args:
            tracking (np.array): (N,) for every node

        Returns:
            np.array: _description_
        """
        # compute number of children for every node
        numChildren = self.zeros((len(tracking),), dtype=self.backend.int64)
        unique, count = self.unique(tracking, return_counts=True)
        # mask is needed because node id can be -1
        mask = unique >= 0
        numChildren[unique[mask]] = count[mask]

        return numChildren

    def compute_walks_upward(self, tracking, sources, num_steps, stop_at_split=False):
        """
        Compute walks on a direted graph where every node has at most one parent

        Returns walks starting with the source node and ending with the last possible parent or after num_steps (or at a parent that divides)

        tracking: parent index associating graph definition
        sources: index array of walk starting nodes
        num_steps: max length of the walk

        returns an index matrix len(sources) x (num_steps+1) containing node indices. An index of -1 denotes that the walk ended (due to no more parents)
        """
        num_sources = len(sources)

        # initialize the walk matrix
        parents = self.zeros((num_sources, num_steps + 1), dtype=self.backend.int64) - 1
        # fill first column with sources
        parents[:, 0] = sources

        active_mask = self.ones((num_sources,), dtype=bool)

        if stop_at_split:
            num_children = self.compute_num_children(tracking)

        for i in range(num_steps):
            matrix_col = i + 1

            # move one step backwards
            new_parents = tracking[parents[:, i][active_mask]]

            if stop_at_split:
                active_mask[self.copy(active_mask)] &= num_children[new_parents] <= 1

            parents[:, matrix_col][active_mask] = tracking[parents[:, i][active_mask]]

            active_mask &= parents[:, matrix_col] >= 0

            if not self.backend.any(active_mask):
                # if no more walks are active we can end
                break

        return parents

    def compute_centroids(self, walk_matrix, centroids):
        """
        Compute centroids for every element in the walk matrix

        walk_matrix: NxM matrix of detection indices
        centroids: detection centroid list

        returns NxMx2 matrix of all centroids for elements in walk matrix
        """
        num_parents = self.shape(walk_matrix)[1] - 1

        # now construct the centroids
        all_centroids = self.zeros(
            (walk_matrix.shape[0], walk_matrix.shape[1], 2), dtype=self.backend.float32
        )

        for i in range(num_parents + 1):
            # get mask of active walks
            active_mask = walk_matrix[:, i] >= 0

            # insert centroids for active walk positions
            all_centroids[:, i][active_mask] = centroids[walk_matrix[:, i][active_mask]]

        # return the collected
        return all_centroids

    def compute_moving_distances(self, walk_matrix, all_centroids):
        """
        Computes the moving distances along a walk matrix

        walk_matrix: NxM walks from sources N for at max M steps
        all_centroids: Kx2 centroid matrix

        returns N x (M-1) masked array of moving distances
        """

        # compute movement vectors
        all_movements, all_mask = self.compute_differences_along_walk(
            walk_matrix, all_centroids
        )
        # compute movement distances
        all_distances = self.backend.linalg.norm(all_movements, **{self.axis: -1})
        # reduce the mask
        all_mask = self.backend.all(all_mask, **{self.axis: -1})
        # create masked array
        masked_distances = self.masked_array(all_distances, ~all_mask)

        return masked_distances

    def compute_differences_along_walk(
        self, walk_matrix, all_properties, distance_metric=None, distance_dims=2
    ):
        """
        Computes the distance vectors along paths

        walk_matrix: NxM matrix containing upward walks
        all_properties: NxMxD contains all node properties (e.g centroid positions) of dimensionality D (usually D=2)

        returns: Nx(M-1)xD matrix of the difference vectors
        """

        # TODO: add stop at split

        if distance_metric is None:
            distance_metric = self.backend.subtract

        num_sources, num_steps = self.shape(walk_matrix)

        # prepare data arrays
        all_movements = self.zeros(
            (num_sources, num_steps - 1, distance_dims), dtype=self.backend.float32
        )
        all_mask = self.zeros((num_sources, num_steps - 1, distance_dims), dtype=bool)

        if distance_dims == 1:
            # collapse distance dimension if it is a single dimension
            all_movements = np.squeeze(all_movements, axis=-1)
            all_mask = np.squeeze(all_mask, axis=-1)

        # compute step distance
        for i in range(num_steps - 1):
            # compute the distance on active walks (Note: i:i+2 returns elements i and i+1)
            local_walk_matrix = walk_matrix[:, i : i + 2]
            mask = local_walk_matrix >= 0
            active_mask = self.backend.all(mask, **{self.axis: 1})

            active_walk_matrix = local_walk_matrix[active_mask]
            # compute the distances
            all_movements[active_mask, i] = distance_metric(
                all_properties[active_walk_matrix[:, 0]],
                all_properties[active_walk_matrix[:, 1]],
            )
            # reshape mask to full movement array
            if distance_dims > 1:
                tiled = self.repeat(active_mask, 2).reshape((-1, 2))
            else:
                tiled = active_mask
            all_mask[:, i] = tiled

        return all_movements, all_mask

    def compute_avg_property_along_walk(
        self,
        walk_matrix,
        all_properties,
        exp_moving_average=None,
        distance_metric=np.subtract,
        distance_dims=2,
    ):
        """
        Computes average movement vectors

        walk_matrix NxM, N sources and M steps

        all_properties Nx2, all possible centroids

        returns Nx2 average movement vectors
        """
        # create the distances between consecutive moves
        all_distances, all_mask = self.compute_differences_along_walk(
            walk_matrix, all_properties, distance_metric, distance_dims
        )

        # create a masked array
        masked_distances = self.masked_array(all_distances, ~all_mask)

        if exp_moving_average is not None:
            masked_distances *= exp_moving_average
            for j in range(masked_distances.shape[1]):
                masked_distances[:, j] *= np.power((1 - exp_moving_average), j)

            average_movement = masked_distances.sum(axis=1)
        else:
            # compute the average movement
            average_movement = masked_distances.mean(axis=1)

        return average_movement
