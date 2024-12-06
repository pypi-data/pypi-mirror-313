"""
InternalZone module. It saves the original geometrical information from interiors together with some attributes of those
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
"""

import uuid
from typing import Union, List
from hub.city_model_structure.building_demand.usage import Usage
from hub.city_model_structure.building_demand.thermal_archetype import ThermalArchetype
from hub.city_model_structure.building_demand.thermal_zone import ThermalZone
from hub.city_model_structure.building_demand.thermal_boundary import ThermalBoundary
from hub.city_model_structure.attributes.polyhedron import Polyhedron


class InternalZone:
  """
  InternalZone class
  """
  def __init__(self, surfaces, area, volume):
    self._surfaces = surfaces
    self._id = None
    self._geometry = None
    self._volume = volume
    self._area = area
    self._thermal_zones_from_internal_zones = None
    self._usages = None
    self._thermal_archetype = None

  @property
  def id(self):
    """
    Get internal zone id, a universally unique identifier randomly generated
    :return: str
    """
    if self._id is None:
      self._id = uuid.uuid4()
    return self._id

  @property
  def geometry(self) -> Polyhedron:
    """
    Get internal zone geometry
    :return: Polyhedron
    """
    if self._geometry is None:
      polygons = []
      for surface in self.surfaces:
        polygons.append(surface.perimeter_polygon)
      self._geometry = Polyhedron(polygons)
    return self._geometry

  @property
  def surfaces(self):
    """
    Get internal zone surfaces
    :return: [Surface]
    """
    return self._surfaces

  @property
  def volume(self):
    """
    Get internal zone volume in cubic meters
    :return: float
    """
    return self._volume

  @property
  def area(self):
    """
    Get internal zone area in square meters
    :return: float
    """
    return self._area

  @property
  def mean_height(self):
    """
    Get internal zone mean height in meters
    :return: float
    """
    return self.volume / self.area

  @property
  def usages(self) -> [Usage]:
    """
    Get usage archetypes
    :return: [Usage]
    """
    return self._usages

  @usages.setter
  def usages(self, value):
    """
    Set usage archetypes
    :param value: [Usage]
    """
    self._usages = value

  @property
  def thermal_archetype(self) -> ThermalArchetype:
    """
    Get thermal archetype parameters
    :return: ThermalArchetype
    """
    return self._thermal_archetype

  @thermal_archetype.setter
  def thermal_archetype(self, value):
    """
    Set thermal archetype parameters
    :param value: ThermalArchetype
    """
    self._thermal_archetype = value

  @property
  def thermal_zones_from_internal_zones(self) -> Union[None, List[ThermalZone]]:
    """
    Get building thermal zones as one per internal zone
    :return: [ThermalZone]
    """
    _thermal_boundaries = []
    for surface in self.surfaces:
      if surface.holes_polygons is None:
        windows_areas = None
      else:
        windows_areas = []
        for hole in surface.holes_polygons:
          windows_areas.append(hole.area)
      _thermal_boundary = ThermalBoundary(surface, surface.solid_polygon.area, windows_areas)
      surface.associated_thermal_boundaries = [_thermal_boundary]
      _thermal_boundaries.append(_thermal_boundary)
    if self.thermal_archetype is None:
      return None  # there are no archetype
    _number_of_storeys = int(self.volume / self.area / self.thermal_archetype.average_storey_height)
    if _number_of_storeys == 0:
      _number_of_storeys = 1
    _thermal_zone = ThermalZone(_thermal_boundaries, self, self.volume, self.area, _number_of_storeys)
    for thermal_boundary in _thermal_zone.thermal_boundaries:
      thermal_boundary.thermal_zones = [_thermal_zone]
    self._thermal_zones_from_internal_zones = [_thermal_zone]
    return self._thermal_zones_from_internal_zones

  @thermal_zones_from_internal_zones.setter
  def thermal_zones_from_internal_zones(self, value):
    """
    Set city object thermal zones as one per internal zone
    :param value: [ThermalZone]
    """
    self._thermal_zones_from_internal_zones = value
