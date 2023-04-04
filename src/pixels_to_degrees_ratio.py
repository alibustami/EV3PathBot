"""This module contains the pixel to degrees ratio calculator."""


def convert_pixels_to_degrees(img, distance_list, wheel_diameter):
    """Convert pixels to degrees.

    Parameters
    ----------
    img : np.array
        table image
    distance_list : list
        the input distances
    wheel_diameter : float
        wheel diameter

    Returns
    -------
    list
        the degrees the robot should move
    """
    img_scale = img.shape[1] / 236.2
    wheel_scale = (wheel_diameter * 3.14) / 360
    degrees_list = []
    for distance in distance_list:
        degrees_list.append(round((distance / img_scale) / wheel_scale))
    return degrees_list
