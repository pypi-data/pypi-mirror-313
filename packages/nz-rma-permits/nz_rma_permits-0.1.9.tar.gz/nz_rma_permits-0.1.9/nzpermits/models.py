#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 14:10:31 2021

@author: mike
"""
from datetime import datetime, date
from typing import List, Optional, Union, Dict, Literal
from enum import Enum
import msgspec

# from .utils import orjson_dumps
# from utils import orjson_dumps

from .gjson import Geometry
# from gjson import Geometry

#########################################
### Models

## Station
class StationBase(msgspec.Struct, omit_defaults=True):
    """
    Contains the base station data.
    """
    station_id: str
    geometry: Geometry
    ref: Optional[str] = None
    name: Optional[str] = None
    altitude: Optional[float] = None
    properties: Optional[dict] = None


class Period(str, Enum):
    seconds = 'S'
    hours = 'H'
    days = 'D'
    weeks = 'W'
    months = 'M'
    years = 'Y'
    multi_years = 'multiple years'


class Units(str, Enum):
    liters = 'l'
    cubic_meters = 'm3'
    mg_l = 'mg/l'


class LimitBoundary(str, Enum):
    min = 'min'
    max = 'max'


class AggregationStat(str, Enum):
    min = 'min'
    max = 'max'
    median = 'median'
    mean = 'mean'
    sum = 'sum'
    perc_95 = '95th percentile'
    exceeded_8_perc = 'Exceeded no more than 8% of samples'
    exceeded_17_perc = 'Exceeded no more than 17% of samples'


class Limit(msgspec.Struct, omit_defaults=True):
    """
    The aggregation statistic describes what statistic should be applied on the source data to be assessed against the limit.
    """
    value: Union[int, float]
    period: Period
    units: Units
    limit_boundary: LimitBoundary
    aggregation_stat: AggregationStat
    name: Optional[str] = None
    notes: Optional[str] = None


class ConditionType(str, Enum):
    abstraction_limit = 'abstraction limit'
    streamflow_limit = 'streamflow limit'


class Condition(msgspec.Struct, omit_defaults=True):
    """

    """
    condition_type: ConditionType
    limits: List[Limit]
    text: Optional[str] = None


class ActivityType(str, Enum):
    consumptive_take_water = 'consumptive take water'
    non_consumptive_take_water = 'non-consumptive take water'
    divert_water = 'divert water'
    dam_water = 'dam water'
    use_water = 'use water'
    discharge_water = 'discharge water'


class SdMethod(str, Enum):
    """
    The stream depletion method assigned for the permit.
    """
    theis_1941 = 'theis_1941'
    hunt_1999 = 'hunt_1999'
    hunt_2003 = 'hunt_2003'
    hunt_2009 = 'hunt_2009'
    ward_lough_2011 = 'ward_lough_2011'


class AquiferProp(msgspec.Struct, omit_defaults=True):
    """
    stream_depletion_ratio: The stream depletion ratio calculated from the n_days and the method.
    n_days: The number of pumping days assigned to the permit associated with the stream depletion calculation requirements.
    sep_distance: The separation distance from the pumped well to the stream.
    pump_aq_trans: The pumped (confined) aquifer transmissivity (m2/day).
    pump_aq_s: The storage coefficient of the pumped aquifer.
    upper_aq_trans: The surficial aquifer transmissivity (m2/day).
    upper_aq_s: The storage coefficient of the surficial aquifer.
    lower_aq_trans: The confined aquifer transmissivity (m2/day).
    lower_aq_s: The storage coefficient (specific storage) of the confined aquifer.
    aqt_k: The aquitard hydraulic conductivity (m/day).
    aqt_s: The aquitard storage coefficient.
    aqt_thick: The aquitard vertical thickness (m).
    stream_k: Streambed hydraulic conductivity (m/day).
    stream_thick: The streambed vertical thickness (m).
    stream_width: The streambed width (m).
    """
    method: SdMethod
    stream_depletion_ratio: Optional[float] = None
    n_days: Optional[int] = None
    sep_distance : Optional[int] = None
    pump_aq_trans : Optional[int] = None
    pump_aq_s : Optional[float] = None
    upper_aq_trans: Optional[int] = None
    upper_aq_s : Optional[float] = None
    lower_aq_trans: Optional[int] = None
    lower_aq_s : Optional[float] = None
    aqt_k : Optional[float] = None
    aqt_s : Optional[float] = None
    aqt_thick : Optional[int] = None
    stream_k : Optional[float] = None
    stream_thick : Optional[int] = None
    stream_width : Optional[int] = None


class Station(StationBase, omit_defaults=True):
    """
    Contains the station data.
    """
    properties: Optional[AquiferProp] = None


class Feature(str, Enum):
    waterways = 'surface water'
    groundwater = 'groundwater'
    still_waters = 'still waters'


class Activity(msgspec.Struct, omit_defaults=True):
    """

    """
    activity_type: ActivityType
    feature: Feature
    stations: List[Station]
    conditions: Optional[List[Condition]] = None
    primary_purpose: Optional[str] = None
    notes: Optional[str] = None


class Status(str, Enum):
    expired = 'Expired'
    surrendered = 'Surrendered'
    active = 'Active'
    archived = 'Archived'
    lapsed = 'Lapsed'
    superseded = 'Superseded'
    cancelled = 'Cancelled'
    expired_124 = 'Expired - S.124 Protection'


class PermitType(str, Enum):
    water_permit = 'water permit'


class Permit(msgspec.Struct, kw_only=True, omit_defaults=True):
    """

    """
    permit_id: str
    parent_permit_id: Optional[str] = None
    status: Status
    status_changed_date: Optional[date] = None
    commencement_date: date
    expiry_date: date
    effective_end_date: Optional[date] = None
    exercised: bool
    permitting_authority: str
    permit_type: PermitType
    activity: Activity
    modified_date: datetime


##########################################
### Export json schema

