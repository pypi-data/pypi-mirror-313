import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfDhw(IdfBase):
  @staticmethod
  def add(self, thermal_zone, zone_name):
    peak_flow_rate = thermal_zone.domestic_hot_water.peak_flow * thermal_zone.total_floor_area
    flow_rate_schedule = f'DHW_prof schedules {thermal_zone.usage_name}'
    dhw_schedule = f'DHW_temp schedules {thermal_zone.usage_name}'
    cold_temp_schedule = f'cold_temp schedules {thermal_zone.usage_name}'
    file = self._files['dhw']
    self._write_to_idf_format(file, idf_cte.DHW)
    self._write_to_idf_format(file, zone_name, 'Name')
    self._write_to_idf_format(file, zone_name, 'EndUse Subcategory')
    self._write_to_idf_format(file, peak_flow_rate, 'Peak Flow Rate')
    self._write_to_idf_format(file, flow_rate_schedule, 'Flow Rate Fraction Schedule Name')
    self._write_to_idf_format(file, dhw_schedule, 'Target Temperature Schedule Name')
    self._write_to_idf_format(file, dhw_schedule, 'Hot Water Supply Temperature Schedule Name')
    self._write_to_idf_format(file, cold_temp_schedule, 'Cold Water Supply Temperature Schedule Name')
    self._write_to_idf_format(file, zone_name, 'Zone Name', ';')
