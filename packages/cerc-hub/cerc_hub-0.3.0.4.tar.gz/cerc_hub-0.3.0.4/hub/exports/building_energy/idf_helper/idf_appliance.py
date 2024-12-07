import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfAppliance(IdfBase):
  @staticmethod
  def add(self, thermal_zone, zone_name):
    schedule_name = f'Appliance schedules {thermal_zone.usage_name}'
    storeys_number = int(thermal_zone.total_floor_area / thermal_zone.footprint_area)
    watts_per_zone_floor_area = thermal_zone.appliances.density * storeys_number
    subcategory = f'ELECTRIC EQUIPMENT#{zone_name}#InteriorEquipment'
    file = self._files['appliances']
    self._write_to_idf_format(file, idf_cte.APPLIANCES)
    self._write_to_idf_format(file, zone_name, 'Name')
    self._write_to_idf_format(file, 'Electricity', 'Fuel Type')
    self._write_to_idf_format(file, zone_name, 'Zone or ZoneList or Space or SpaceList Name')
    self._write_to_idf_format(file, schedule_name, 'Schedule Name')
    self._write_to_idf_format(file, 'Watts/Area', 'Design Level Calculation Method')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Design Level')
    self._write_to_idf_format(file, watts_per_zone_floor_area, 'Power per Zone Floor Area')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Power per Person')
    self._write_to_idf_format(file, thermal_zone.appliances.latent_fraction, 'Fraction Latent')
    self._write_to_idf_format(file, thermal_zone.appliances.radiative_fraction, 'Fraction Radiant')
    self._write_to_idf_format(file, 0, 'Fraction Lost')
    self._write_to_idf_format(file, 0, 'Carbon Dioxide Generation Rate')
    self._write_to_idf_format(file, subcategory, 'EndUse Subcategory', ';')
