import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfShading(IdfBase):
  @staticmethod
  def add(self, building):
    name = building.name
    file = self._files['shading']
    for s, surface in enumerate(building.surfaces):

      self._write_to_idf_format(file, idf_cte.SHADING)
      self._write_to_idf_format(file, f'{name}_{s}', 'Name')
      self._write_to_idf_format(file, idf_cte.EMPTY, 'Transmittance Schedule Name')
      self._write_to_idf_format(file, idf_cte.AUTOCALCULATE, 'Number of Vertices')
      eol = ','
      coordinates = self._matrix_to_list(surface.solid_polygon.coordinates, self._city.lower_corner)
      coordinates_length = len(coordinates)
      for i, coordinate in enumerate(coordinates):
        vertex = i + 1
        if vertex == coordinates_length:
          eol = ';'
        self._write_to_idf_format(file, coordinate[0], f'Vertex {vertex} Xcoordinate')
        self._write_to_idf_format(file, coordinate[1], f'Vertex {vertex} Ycoordinate')
        self._write_to_idf_format(file, coordinate[2], f'Vertex {vertex} Zcoordinate', eol)
