import hub.exports.building_energy.idf_helper as idf_cte
import hub.helpers.constants as cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfSurfaces(IdfBase):
  @staticmethod
  def add(self, building, zone_name):
    zone_name = f'{zone_name}'
    file = self._files['surfaces']
    for thermal_zone in building.thermal_zones_from_internal_zones:
      for index, boundary in enumerate(thermal_zone.thermal_boundaries):
        surface_type = idf_cte.idf_surfaces_dictionary[boundary.parent_surface.type]
        outside_boundary_condition = idf_cte.OUTDOORS
        sun_exposure = idf_cte.SUN_EXPOSED
        wind_exposure = idf_cte.WIND_EXPOSED
        outside_boundary_condition_object = idf_cte.EMPTY
        name = f'Building_{building.name}_surface_{index}'
        construction_name = f'{boundary.construction_name} {boundary.parent_surface.type}'
        space_name = idf_cte.EMPTY
        if boundary.parent_surface.type == cte.GROUND:
          outside_boundary_condition = idf_cte.GROUND
          sun_exposure = idf_cte.NON_SUN_EXPOSED
          wind_exposure = idf_cte.NON_WIND_EXPOSED
        if boundary.parent_surface.percentage_shared is not None and boundary.parent_surface.percentage_shared > 0.5:
          outside_boundary_condition_object = f'Building_{building.name}_surface_{index}'
          outside_boundary_condition = idf_cte.SURFACE
          sun_exposure = idf_cte.NON_SUN_EXPOSED
          wind_exposure = idf_cte.NON_WIND_EXPOSED
        self._write_to_idf_format(file, idf_cte.BUILDING_SURFACE)
        self._write_to_idf_format(file, name, 'Name')
        self._write_to_idf_format(file, surface_type, 'Surface Type')
        self._write_to_idf_format(file, construction_name, 'Construction Name')
        self._write_to_idf_format(file, zone_name, 'Zone Name')
        self._write_to_idf_format(file, space_name, 'Space Name')
        self._write_to_idf_format(file, outside_boundary_condition, 'Outside Boundary Condition')
        self._write_to_idf_format(file, outside_boundary_condition_object, 'Outside Boundary Condition Object')
        self._write_to_idf_format(file, sun_exposure, 'Sun Exposure')
        self._write_to_idf_format(file, wind_exposure, 'Wind Exposure')
        self._write_to_idf_format(file, idf_cte.AUTOCALCULATE, 'View Factor to Ground')
        self._write_to_idf_format(file, idf_cte.AUTOCALCULATE, 'Number of Vertices')
        coordinates = self._matrix_to_list(boundary.parent_surface.solid_polygon.coordinates,
                                           self._city.lower_corner)
        eol = ','
        coordinates_length = len(coordinates)
        for i, coordinate in enumerate(coordinates):
          vertex = i + 1
          if vertex == coordinates_length:
            eol = ';'
          self._write_to_idf_format(file, coordinate[0], f'Vertex {vertex} Xcoordinate')
          self._write_to_idf_format(file, coordinate[1], f'Vertex {vertex} Ycoordinate')
          self._write_to_idf_format(file, coordinate[2], f'Vertex {vertex} Zcoordinate', eol)
