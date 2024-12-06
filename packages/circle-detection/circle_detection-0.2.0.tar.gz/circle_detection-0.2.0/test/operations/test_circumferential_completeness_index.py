""" Tests for :code:`circle_detection.operations.circumferential_completeness_index`. """

from typing import Optional

import numpy as np
import pytest

from circle_detection.operations import circumferential_completeness_index, filter_circumferential_completeness_index


class TestCircumferentialCompletenessIndex:  # pylint: disable=too-few-public-methods
    """Tests for :code:`circle_detection.operations.circumferential_completeness_index`."""

    @pytest.mark.parametrize("max_dist", [0.1, None])
    def test_circumferential_completeness_index(self, max_dist: Optional[float]):
        circles = np.array([[0, 0, 1], [5, 0, 1]], dtype=np.float64)

        xy = np.array([[0, 1], [0, -1], [1, 0], [-1, 0], [5, 1], [5, -1]], dtype=np.float64)
        num_regions = 4

        expected_circumferential_completness_indices = np.array([1, 0.5], dtype=np.float64)

        circumferential_completeness_indices = circumferential_completeness_index(
            circles, xy, num_regions=num_regions, max_dist=max_dist
        )

        np.testing.assert_array_equal(
            expected_circumferential_completness_indices, circumferential_completeness_indices
        )

        expected_filtered_circles = circles[:1]
        expected_selected_indices = np.array([0], dtype=np.int64)

        filtered_circles, selected_indices = filter_circumferential_completeness_index(
            circles, xy, min_circumferential_completeness_index=0.6, num_regions=num_regions, max_dist=max_dist
        )

        np.testing.assert_array_equal(expected_filtered_circles, filtered_circles)
        np.testing.assert_array_equal(expected_selected_indices, selected_indices)
