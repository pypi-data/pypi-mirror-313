import numpy as np


def get_combined_mask(dimensions: tuple[str], masks: dict[str, any]):
    """Combines the masks for the given dimensions.

    Combines the masks for the given dimensions into a single mask.
    The masks are combined in the order of the dimensions.

    Parameters:
    - dimensions (tuple[str]): The dimensions to combine the masks for.
    - masks (dict[str, any]): The masks to combine.

    Returns:
    - list: The combined mask.
    """

    combined_mask = []

    for dimension in dimensions:
        combined_mask.append(masks[dimension])

    return combined_mask


def fit_mask_to_shape(mask: any, shape: tuple[int]):
    """Fits the mask to the given shape.

    Fits the mask to the given shape by adding trailing slices.

    Parameters:
    - mask (any): The mask to fit.
    - shape (tuple[int]): The shape to fit the mask to.

    Returns:
    - any: The mask fitted to the shape.
    """

    if mask.shape != shape and type(mask) == np.bool_:
        return np.full(shape, mask)

    if mask.shape != shape and type(mask) != np.bool_:
        raise ValueError("Unable to fit mask to shape. Mask is not a boolean array.")

    return mask
