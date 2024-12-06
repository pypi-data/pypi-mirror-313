"""
Model representation of a city object
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""

import datetime
import logging

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Float
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import DateTime

from hub.city_model_structure.building import Building
from hub.persistence.configuration import Models


class CityObject(Models):
  """
  A model representation of an application
  """
  __tablename__ = 'city_object'
  id = Column(Integer, Sequence('city_object_id_seq'), primary_key=True)
  city_id = Column(Integer, ForeignKey('city.id', ondelete='CASCADE'), nullable=False)
  name = Column(String, nullable=False)
  aliases = Column(String, nullable=True)
  type = Column(String, nullable=False)
  year_of_construction = Column(Integer, nullable=True)
  function = Column(String, nullable=True)
  usage = Column(JSON, nullable=True)
  volume = Column(Float, nullable=False)
  area = Column(Float, nullable=False)
  total_heating_area = Column(Float, nullable=False)
  wall_area = Column(Float, nullable=False)
  windows_area = Column(Float, nullable=False)
  roof_area = Column(Float, nullable=False)
  total_pv_area = Column(Float, nullable=False)
  system_name = Column(String, nullable=False)
  created = Column(DateTime, default=datetime.datetime.utcnow)
  updated = Column(DateTime, default=datetime.datetime.utcnow)

  def __init__(self, city_id, building: Building):
    self.city_id = city_id
    self.name = building.name
    self.aliases = building.aliases
    self.type = building.type
    self.year_of_construction = building.year_of_construction
    self.function = building.function
    self.usage = building.usages
    self.volume = building.volume
    self.area = building.floor_area
    self.roof_area = sum(roof.solid_polygon.area for roof in building.roofs)
    self.total_pv_area = sum(roof.solid_polygon.area * roof.solar_collectors_area_reduction_factor for roof in building.roofs)
    storeys = building.storeys_above_ground
    wall_area = 0
    window_ratio = 0
    try:
      if storeys is None:
        storeys = building.max_height / building.average_storey_height
      for internal_zone in building.internal_zones:
        for thermal_zone in internal_zone.thermal_zones_from_internal_zones:
          for thermal_boundary in thermal_zone.thermal_boundaries:
            window_ratio = thermal_boundary.window_ratio
            break
    except TypeError:
      storeys = 0
      logging.warning(
        'building %s has no storey height so heating area, storeys and window ratio cannot be calculated',
        self.name
      )
    self.total_heating_area = building.floor_area * storeys

    for wall in building.walls:
      wall_area += wall.solid_polygon.area
    self.wall_area = wall_area
    self.windows_area = wall_area * window_ratio
    system_name = building.energy_systems_archetype_name
    if system_name is None:
      system_name = ''
    self.system_name = system_name
