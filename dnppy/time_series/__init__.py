"""
The time_series module is centered around the time_series class. One or more time_series objects
should be central to any data analysis task that examines temporal relationships in data sets of
raster or tabular format. This module also houses the rast_series class, which is an extension of
time_series for handling filepaths to raster data.

Requires ``arcpy``: Requires raster module, which depends upon arcpy.
"""

__author__ = ["Jwely"]


# local imports
from time_series_class import *
from rast_series_class import *

