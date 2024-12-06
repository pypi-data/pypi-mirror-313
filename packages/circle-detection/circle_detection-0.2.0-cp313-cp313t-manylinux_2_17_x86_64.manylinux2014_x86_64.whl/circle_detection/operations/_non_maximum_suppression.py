""" Non-maximum suppression operation to remove overlapping circles. """

__all__ = ["non_maximum_suppression"]

from typing import Tuple

import numpy as np
import numpy.typing as npt

from circle_detection.operations._operations_cpp import (  # type: ignore[import-not-found] # pylint: disable=import-error, no-name-in-module
    non_maximum_suppression as non_maximum_suppression_cpp,
)


def non_maximum_suppression(
    circles: npt.NDArray[np.float64], fitting_losses: npt.NDArray[np.float64]
) -> Tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    r"""
    Non-maximum suppression operation to remove overlapping circles. If a circle overlaps with other circles, it is
    only kept if it has the lowest fitting loss among the circles with which it overlaps.

    Args:
        circles: Parameters of the circles to which apply non-maximum suppression (in the following order:
            x-coordinate of the center, y-coordinate of the center, radius).
        fitting_losses: Fitting losses of the circles to which apply non-maximum suppression (lower means better).

    Returns:
        : Tuple of two arrays. The first contains the parameters of the circles remaining after non-maximum suppression
        and the second the corresponding fitting losses.

    Shape:
        - :code:`circles`: :math:`(C, 3)`
        - :code:`fitting_losses`: :math:`(C)`
        - Output: The first array in the output tuple has shape :math:`(C, 3)` and the second shape :math:`(C)`.

        | where
        |
        | :math:`C = \text{ number of circles}`
    """

    return non_maximum_suppression_cpp(circles, fitting_losses)
