"""
export a city into Geojson format
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez guillermo.gutierrezmorote@concordia.ca
"""
import json
from pathlib import Path

import numpy as np
import pyproj
from pyproj import Transformer

from hub.helpers.geometry_helper import GeometryHelper


class Geojson:
  """
  Export to geojson format
  """
  def __init__(self, city, path, target_buildings):
    self._city = city
    self._file_path = Path(path / f'{self._city.name}.geojson').resolve()
    try:
      srs_name = self._city.srs_name
      if self._city.srs_name in GeometryHelper.srs_transformations:
        srs_name = GeometryHelper.srs_transformations[self._city.srs_name]
      input_reference = pyproj.CRS(srs_name)  # Projected coordinate system from input data
    except pyproj.exceptions.CRSError as err:
      raise pyproj.exceptions.CRSError from err
    self._to_gps = Transformer.from_crs(input_reference, pyproj.CRS('EPSG:4326'))
    if target_buildings is None:
      target_buildings = [b.name for b in self._city.buildings]
    self._geojson_skeleton = {
      'type': 'FeatureCollection',
      'features': []
    }
    self._feature_skeleton = {
      'type': 'Feature',
      'geometry': {
        'type': 'Polygon',
        'coordinates': []
      },
      'properties': {}
    }
    self._export()

  def _export(self):
    for building in self._city.buildings:
      if len(building.grounds) == 1:
        ground = building.grounds[0]
        feature = self._polygon(ground)
      else:
        feature = self._multipolygon(building.grounds)
      feature['id'] = building.name
      feature['properties']['height'] = f'{building.max_height - building.lower_corner[2]}'
      feature['properties']['function'] = f'{building.function}'
      feature['properties']['year_of_construction'] = f'{building.year_of_construction}'
      feature['properties']['aliases'] = building.aliases
      feature['properties']['elevation'] = f'{building.lower_corner[2]}'
      self._geojson_skeleton['features'].append(feature)
    with open(self._file_path, 'w', encoding='utf-8') as f:
      json.dump(self._geojson_skeleton, f, indent=2)

  def _polygon(self, ground):
    feature = {
      'type': 'Feature',
      'geometry': {
        'type': 'Polygon',
        'coordinates': []
      },
      'properties': {}
    }
    ground_coordinates = []
    for coordinate in ground.solid_polygon.coordinates:
      gps_coordinate = self._to_gps.transform(coordinate[0], coordinate[1])
      ground_coordinates.insert(0, [gps_coordinate[1], gps_coordinate[0]])

    first_gps_coordinate = self._to_gps.transform(
      ground.solid_polygon.coordinates[0][0],
      ground.solid_polygon.coordinates[0][1]
    )
    ground_coordinates.insert(0, [first_gps_coordinate[1], first_gps_coordinate[0]])
    feature['geometry']['coordinates'].append(ground_coordinates)
    return feature

  def _multipolygon(self, grounds):
    feature = {
      'type': 'Feature',
      'geometry': {
        'type': 'MultiPolygon',
        'coordinates': []
      },
      'properties': {}
    }
    polygons = []
    for ground in grounds:
      ground_coordinates = []
      for coordinate in ground.solid_polygon.coordinates:
        gps_coordinate = self._to_gps.transform(coordinate[0], coordinate[1])
        ground_coordinates.insert(0, [gps_coordinate[1], gps_coordinate[0]])

      first_gps_coordinate = self._to_gps.transform(
        ground.solid_polygon.coordinates[0][0],
        ground.solid_polygon.coordinates[0][1]
      )
      ground_coordinates.insert(0, [first_gps_coordinate[1], first_gps_coordinate[0]])
      polygons.append(ground_coordinates)
    feature['geometry']['coordinates'].append(polygons)
    return feature


