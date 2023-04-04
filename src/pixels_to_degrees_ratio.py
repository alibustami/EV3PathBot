"""This module contains the pixel to degrees ratio calculator."""

def convert_pixels_to_degrees( img, distance_list, wheel_diameter):
    img_scale = img.shape[1] / 236.2
    wheel_scale = (wheel_diameter * 3.14) / 360
    degrees_list = []
    for distance in distance_list:
        degrees_list.append(round((distance / img_scale) / wheel_scale))
    return degrees_list
