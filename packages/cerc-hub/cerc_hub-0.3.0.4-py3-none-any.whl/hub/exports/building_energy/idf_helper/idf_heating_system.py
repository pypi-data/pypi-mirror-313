import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfHeatingSystem(IdfBase):
  @staticmethod
  def add(self, thermal_zone, zone_name):
    availability_schedule = f'HVAC AVAIL SCHEDULES {thermal_zone.usage_name}'
    thermostat_name = f'Thermostat {thermal_zone.usage_name}'
    file = self._files['ideal_load_system']
    self._write_to_idf_format(file, idf_cte.IDEAL_LOAD_SYSTEM)
    self._write_to_idf_format(file, zone_name, 'Zone Name')
    self._write_to_idf_format(file, thermostat_name, 'Template Thermostat Name')
    self._write_to_idf_format(file, availability_schedule, 'System Availability Schedule Name')
    self._write_to_idf_format(file, 50, 'Maximum Heating Supply Air Temperature')
    self._write_to_idf_format(file, 13, 'Minimum Cooling Supply Air Temperature')
    self._write_to_idf_format(file, 0.0156, 'Maximum Heating Supply Air Humidity Ratio')
    self._write_to_idf_format(file, 0.0077, 'Minimum Cooling Supply Air Humidity Ratio')
    self._write_to_idf_format(file, 'NoLimit', 'Heating Limit')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Maximum Heating Air Flow Rate')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Maximum Sensible Heating Capacity')
    self._write_to_idf_format(file, 'NoLimit', 'Cooling Limit')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Maximum Cooling Air Flow Rate')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Maximum Total Cooling Capacity')
    self._write_to_idf_format(file, availability_schedule, 'Heating Availability Schedule Name')
    self._write_to_idf_format(file, availability_schedule, 'Cooling Availability Schedule Name')
    self._write_to_idf_format(file, 'ConstantSensibleHeatRatio', 'Dehumidification Control Type')
    self._write_to_idf_format(file, 0.7, 'Cooling Sensible Heat Ratio')
    self._write_to_idf_format(file, 60, 'Dehumidification Setpoint')
    self._write_to_idf_format(file, 'None', 'Humidification Control Type')
    self._write_to_idf_format(file, 30, 'Humidification Setpoint')
    self._write_to_idf_format(file, 'None', 'Outdoor Air Method')
    self._write_to_idf_format(file, 0.00944, 'Outdoor Air Flow Rate per Person')
    self._write_to_idf_format(file, 0.0, 'Outdoor Air Flow Rate per Zone Floor Area')
    self._write_to_idf_format(file, 0, 'Outdoor Air Flow Rate per Zone')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Design Specification Outdoor Air Object Name')
    self._write_to_idf_format(file, 'None', 'Demand Controlled Ventilation Type')
    self._write_to_idf_format(file, 'NoEconomizer', 'Outdoor Air Economizer Type')
    self._write_to_idf_format(file, 'None', 'Heat Recovery Type')
    self._write_to_idf_format(file, 0.70, 'Sensible Heat Recovery Effectiveness')
    self._write_to_idf_format(file, 0.65, 'Latent Heat Recovery Effectiveness', ';')