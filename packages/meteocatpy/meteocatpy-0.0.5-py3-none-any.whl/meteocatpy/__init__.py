"""METEOCAT API.

Python Package to collect data from Meteocat API and interact with Meteocat Home Assistant Integration
SPDX-License-Identifier: Apache-2.0

For more details about this API, please refer to the documentation at
https://gitlab.com/figorr/meteocatpy
"""

# meteocatpy/__init__.py
from .town import MeteocatTown
from .forecast import MeteocatForecast
from .symbols import MeteocatSymbols
from .stations import MeteocatStations
from .townstations import MeteocatTownStations
from .data import MeteocatStationData
from .variables import MeteocatVariables

__all__ = [
    "MeteocatTown", 
    "MeteocatForecast", 
    "MeteocatSymbols", 
    "MeteocatStations", 
    "MeteocatTownStations", 
    "MeteocatStationData", 
    "MeteocatVariables"
]
