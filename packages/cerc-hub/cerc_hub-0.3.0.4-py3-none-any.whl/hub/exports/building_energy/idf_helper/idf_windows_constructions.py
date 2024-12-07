import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfWindowsConstructions(IdfBase):
  @staticmethod
  def add(self, thermal_boundary):
    name = f'{thermal_boundary.construction_name}_window'
    if name not in self._windows_added_to_idf:
      return  # Material not added or already assigned to construction
    construction_name = f'{thermal_boundary.construction_name}_window_construction'
    if construction_name not in self._constructions_added_to_idf:
      self._constructions_added_to_idf[construction_name] = True
      file = self._files['constructions']
      self._write_to_idf_format(file, idf_cte.CONSTRUCTION)
      self._write_to_idf_format(file, construction_name, 'Name')
      self._write_to_idf_format(file, name, 'Outside Layer', ';')
