from math import cos, pi
from typing import Tuple

import haversine


def get_direction(from_geo_point: Tuple[float, float], to_geo_point :Tuple[float,float] ):
    degrees = haversine.haversine(from_geo_point,to_geo_point, unit=haversine.Unit.DEGREES)

    return (degrees)

def get_surrounding_location_matrix(latitude:float, longitude: float, direction_in_degrees: float):
    r_earth = 6378000 # meters
    radius_of_search = 25 # meters
    latitude_offset = (radius_of_search/ r_earth) * (180 / pi)
    longitude_offset = (radius_of_search / r_earth) * (180 / pi) / cos(latitude * pi/180)

    offsets = []
    if(direction_in_degrees > 290 or direction_in_degrees <= 35):
        offsets.append([latitude, longitude + longitude_offset])
    if(direction_in_degrees >35 and direction_in_degrees <=80):
        offsets.append([latitude+latitude_offset, longitude+longitude_offset])
    if(direction_in_degrees >80 and direction_in_degrees <=100):
        offsets.append([latitude+latitude_offset, longitude])
    if(direction_in_degrees>100 and direction_in_degrees <=130):
        offsets.append([latitude-latitude_offset, longitude-longitude_offset])
    if(direction_in_degrees >130 and direction_in_degrees <=200):
        offsets.append([latitude, longitude-longitude_offset])
    if(direction_in_degrees >200 and direction_in_degrees <=250):
        offsets.append([latitude+latitude, longitude-longitude_offset])
    if(direction_in_degrees >250 and direction_in_degrees <=300):
        offsets.append([latitude-latitude_offset, longitude])
    if(direction_in_degrees >300 and direction_in_degrees <=290):
        offsets.append([latitude-latitude_offset, longitude+longitude_offset])
    
    return offsets