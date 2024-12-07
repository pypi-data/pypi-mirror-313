import hub.exports.building_energy.idf_helper as idf_cte
import hub.helpers.constants as cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfInfiltration(IdfBase):
  @staticmethod
  def add(self, thermal_zone, zone_name):
    IdfInfiltration._add_infiltration(self, thermal_zone, zone_name, 'AirChanges/Hour', cte.HOUR_TO_SECONDS)

  @staticmethod
  def add_surface(self, thermal_zone, zone_name):
    IdfInfiltration._add_infiltration(self, thermal_zone, zone_name, 'Flow/ExteriorWallArea', cte.INFILTRATION_75PA_TO_4PA)

  @staticmethod
  def _add_infiltration(self, thermal_zone, zone_name, calculation_method, multiplier):
    schedule_name = f'Infiltration schedules {thermal_zone.usage_name}'
    infiltration = thermal_zone.infiltration_rate_system_off * multiplier
    file = self._files['infiltration']
    self._write_to_idf_format(file, idf_cte.INFILTRATION)
    self._write_to_idf_format(file, zone_name, 'Name')
    self._write_to_idf_format(file, zone_name, 'Zone or ZoneList or Space or SpaceList Name')
    self._write_to_idf_format(file, schedule_name, 'Schedule Name')
    self._write_to_idf_format(file, calculation_method, 'Design Flow Rate Calculation Method')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Design Flow Rate')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Flow Rate per Floor Area')
    self._write_to_idf_format(file, infiltration, 'Flow Rate per Exterior Surface Area')
    self._write_to_idf_format(file, infiltration, 'Air Changes per Hour')
    self._write_to_idf_format(file, 1, 'Constant Term Coefficient')
    self._write_to_idf_format(file, 0, 'Temperature Term Coefficient')
    self._write_to_idf_format(file, 0, 'Velocity Term Coefficient')
    self._write_to_idf_format(file, 0, 'Velocity Squared Term Coefficient', ';')
