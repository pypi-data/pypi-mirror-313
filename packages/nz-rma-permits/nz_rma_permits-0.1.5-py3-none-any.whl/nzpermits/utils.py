#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 21 14:18:45 2021

@author: mike
"""
from hashlib import blake2b
from shapely import wkt
from shapely.geometry import shape, mapping, box, Point, Polygon, MultiPoint

###################################################
### Functions


def create_geometry(geometry, precision=None, as_dict=False):
    """

    """
    geo = shape(geometry)

    if isinstance(precision, int):
        geo = wkt.loads(wkt.dumps(geo, rounding_precision=precision))

    if as_dict:
        geo = geo.__geo_interface__

    return geo


def assign_station_id(geometry):
    """
    Parameters
    ----------
    geometry : shapely geometry class or geojson geometry
    """
    if isinstance(geometry, dict):
        geo = create_geometry(geometry, precision=5)
    else:
        geo = wkt.loads(wkt.dumps(geometry, rounding_precision=5))

    station_id = blake2b(geo.wkb, digest_size=12).hexdigest()

    return station_id


# def orjson_dumps(v, *, default):
#     # orjson.dumps returns bytes, to match standard json.dumps we need to decode
#     # return orjson.dumps(v, default=default, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_OMIT_MICROSECONDS | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2).decode()
#     return orjson.dumps(v, default=default, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_OMIT_MICROSECONDS | orjson.OPT_SERIALIZE_NUMPY).decode()

