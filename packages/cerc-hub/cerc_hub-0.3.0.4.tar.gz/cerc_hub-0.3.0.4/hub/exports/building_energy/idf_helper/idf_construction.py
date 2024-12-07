import hub.exports.building_energy.idf_helper as idf_cte
from hub.city_model_structure.building_demand.layer import Layer
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfConstruction(IdfBase):

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
  def _add_default_material(self):
    layer = Layer()
    layer.material_name = 'DefaultMaterial'
    layer.thickness = 0.1
    layer.conductivity = 0.1
    layer.density = 1000
    layer.specific_heat = 1000
    layer.thermal_absorptance = 0.9
    layer.solar_absorptance = 0.9
    layer.visible_absorptance = 0.7
    IdfConstruction._add_solid_material(self, layer)
    return layer

  @staticmethod
  def add(self, thermal_boundary):
    if thermal_boundary.layers is None:
      thermal_boundary.layers = [IdfConstruction._add_default_material(self)]
    name = f'{thermal_boundary.construction_name} {thermal_boundary.parent_surface.type}'

    if name not in self._constructions_added_to_idf:
      self._constructions_added_to_idf[name] = True
      file = self._files['constructions']
      self._write_to_idf_format(file, idf_cte.CONSTRUCTION)
      self._write_to_idf_format(file, name, 'Name')
      eol = ','
      if len(thermal_boundary.layers) == 1:
        eol = ';'
      self._write_to_idf_format(file, thermal_boundary.layers[0].material_name, 'Outside Layer', eol)
      for i in range(1, len(thermal_boundary.layers) - 1):
        comment = f'Layer {i + 1}'
        material_name = thermal_boundary.layers[i].material_name
        if i == len(thermal_boundary.layers) - 2:
          eol = ';'
        self._write_to_idf_format(file, material_name, comment, eol)
