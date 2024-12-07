import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfWindowsMaterial(IdfBase):
  @staticmethod
  def add(self, thermal_boundary, thermal_opening):
    name = f'{thermal_boundary.construction_name}_window'
    if name not in self._windows_added_to_idf:
      self._windows_added_to_idf[name] = True
      file = self._files['window_materials']
      self._write_to_idf_format(file, idf_cte.WINDOW_MATERIAL)
      self._write_to_idf_format(file, name, 'Name')
      self._write_to_idf_format(file, thermal_opening.overall_u_value, 'UFactor')
      self._write_to_idf_format(file, thermal_opening.g_value, 'Solar Heat Gain Coefficient', ';')
