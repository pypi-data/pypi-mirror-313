""" Tests for :code:`circle_detection.operations.non_maximum_suppression`. """

import numpy as np

from circle_detection.operations import non_maximum_suppression


class TestNonMaximumSuppression:
    """Tests for :code:`circle_detection.operations.non_maximum_suppression`."""

    def test_non_overlapping_circles(self):
        circles = np.array([[0, 0, 1], [3, 0, 0.5], [0, 2, 0.1]], dtype=np.float64)
        fitting_losses = np.zeros(3, dtype=np.float64)

        filtered_circles, filtered_fitting_losses = non_maximum_suppression(circles, fitting_losses)

        np.testing.assert_array_equal(circles, filtered_circles)
        np.testing.assert_array_equal(fitting_losses, filtered_fitting_losses)

    def test_overlapping_circles(self):
        circles = np.array([[0, 0, 1], [0.9, 0.1, 1], [0, 2, 0.1]], dtype=np.float64)
        fitting_losses = np.array([-1, -2, -3], dtype=np.float64)

        expected_filtered_circles = np.array([[0, 2, 0.1], [0.9, 0.1, 1]], dtype=np.float64)
        expected_filtered_fitting_losses = np.array([-3, -2], dtype=np.float64)

        filtered_circles, filtered_fitting_losses = non_maximum_suppression(circles, fitting_losses)

        np.testing.assert_array_equal(expected_filtered_circles, filtered_circles)
        np.testing.assert_array_equal(expected_filtered_fitting_losses, filtered_fitting_losses)
