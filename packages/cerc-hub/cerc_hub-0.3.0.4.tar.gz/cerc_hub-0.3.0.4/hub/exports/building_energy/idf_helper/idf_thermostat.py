import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfThermostat(IdfBase):
  @staticmethod
  def add(self, thermal_zone):
    thermostat_name = f'Thermostat {thermal_zone.usage_name}'
    heating_schedule = f'Heating thermostat schedules {thermal_zone.usage_name}'
    cooling_schedule = f'Cooling thermostat schedules {thermal_zone.usage_name}'
    if thermostat_name not in self._thermostat_added_to_idf:
      self._thermostat_added_to_idf[thermostat_name] = True
      file = self._files['thermostat']
      self._write_to_idf_format(file, idf_cte.THERMOSTAT)
      self._write_to_idf_format(file, thermostat_name, 'Name')
      self._write_to_idf_format(file, heating_schedule, 'Heating Setpoint Schedule Name')
      self._write_to_idf_format(file, idf_cte.EMPTY, 'Constant Heating Setpoint')
      self._write_to_idf_format(file, cooling_schedule, 'Cooling Setpoint Schedule Name', ';')
