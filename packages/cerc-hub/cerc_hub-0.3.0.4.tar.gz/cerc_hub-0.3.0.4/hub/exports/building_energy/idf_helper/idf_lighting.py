import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfLighting(IdfBase):
  @staticmethod
  def add(self, thermal_zone, zone_name):
    storeys_number = int(thermal_zone.total_floor_area / thermal_zone.footprint_area)
    watts_per_zone_floor_area = thermal_zone.lighting.density * storeys_number
    subcategory = f'ELECTRIC EQUIPMENT#{zone_name}#GeneralLights'
    schedule_name = f'Lighting schedules {thermal_zone.usage_name}'
    file = self._files['lighting']
    self._write_to_idf_format(file, idf_cte.LIGHTS)
    self._write_to_idf_format(file, f'{zone_name}_lights', 'Name')
    self._write_to_idf_format(file, zone_name, 'Zone or ZoneList or Space or SpaceList Name')
    self._write_to_idf_format(file, schedule_name, 'Schedule Name')
    self._write_to_idf_format(file, 'Watts/Area', 'Design Level Calculation Method')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Lighting Level')
    self._write_to_idf_format(file, watts_per_zone_floor_area, 'Watts per Zone Floor Area')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Watts per Person')
    self._write_to_idf_format(file, 0, 'Return Air Fraction')
    self._write_to_idf_format(file, thermal_zone.lighting.radiative_fraction, 'Fraction Radiant')
    self._write_to_idf_format(file, 0, 'Fraction Visible')
    self._write_to_idf_format(file, 1, 'Fraction Replaceable')
    self._write_to_idf_format(file, subcategory, 'EndUse Subcategory')
    self._write_to_idf_format(file, 'No', 'Return Air Fraction Calculated from Plenum Temperature')
    self._write_to_idf_format(file, 0, 'Return Air Fraction Function of Plenum Temperature Coefficient 1')
    self._write_to_idf_format(file, 0, 'Return Air Fraction Function of Plenum Temperature Coefficient 2', ';')