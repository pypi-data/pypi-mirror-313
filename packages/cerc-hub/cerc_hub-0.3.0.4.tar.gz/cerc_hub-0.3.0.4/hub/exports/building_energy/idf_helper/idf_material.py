import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfMaterial(IdfBase):
  @staticmethod
  def _add_solid_material(self, layer):
    file = self._files['solid_materials']
    self._write_to_idf_format(file, idf_cte.SOLID_MATERIAL)
    self._write_to_idf_format(file, layer.material_name, 'Name')
    self._write_to_idf_format(file, idf_cte.ROUGHNESS, 'Roughness')
    self._write_to_idf_format(file, layer.thickness, 'Thickness')
    self._write_to_idf_format(file, layer.conductivity, 'Conductivity')
    self._write_to_idf_format(file, layer.density, 'Density')
    self._write_to_idf_format(file, layer.specific_heat, 'Specific Heat')
    self._write_to_idf_format(file, layer.thermal_absorptance, 'Thermal Absorptance')
    self._write_to_idf_format(file, layer.solar_absorptance, 'Solar Absorptance')
    self._write_to_idf_format(file, layer.visible_absorptance, 'Visible Absorptance', ';')

  @staticmethod
  def _add_nomass_material(self, layer):
    file = self._files['nomass_materials']
    self._write_to_idf_format(file, idf_cte.NOMASS_MATERIAL)
    self._write_to_idf_format(file, layer.material_name, 'Name')
    self._write_to_idf_format(file, idf_cte.ROUGHNESS, 'Roughness')
    self._write_to_idf_format(file, layer.thermal_resistance, 'Thermal Resistance')
    self._write_to_idf_format(file, 0.9, 'Thermal Absorptance')
    self._write_to_idf_format(file, 0.7, 'Solar Absorptance')
    self._write_to_idf_format(file, 0.7, 'Visible Absorptance', ';')

  @staticmethod
  def add(self, thermal_boundary):
    for layer in thermal_boundary.layers:
      if layer.material_name not in self._materials_added_to_idf:
        self._materials_added_to_idf[layer.material_name] = True
        if layer.no_mass:
          IdfMaterial._add_nomass_material(self, layer)
        else:
          IdfMaterial._add_solid_material(self, layer)
