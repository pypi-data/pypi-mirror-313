# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 15:28:28 2018

@author: MichaelEK
"""
import numpy as np
import pandas as pd
import geopandas as gpd
from gistools import vector, util
from gistools import data_io

pd.options.display.max_columns = 10

####################################
### Parameters

stream_depletion_csv = '/media/sdb1/Projects/git/tethys/tethys-extraction-es-hilltop/permits/es_stream_depletion_ratios.csv'

#######################################
### Tests




def test_sel_sites_poly():
    pts1 = vector.sel_sites_poly(sites_shp_path, rec_catch_shp_path, buffer_dis=10)

    assert (len(pts1) == 2) & isinstance(pts1, gpd.GeoDataFrame)












