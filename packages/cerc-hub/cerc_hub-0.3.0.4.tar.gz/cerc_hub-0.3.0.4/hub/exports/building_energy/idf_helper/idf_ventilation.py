import hub.exports.building_energy.idf_helper as idf_cte
import hub.helpers.constants as cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfVentilation(IdfBase):
  @staticmethod
  def add(self, thermal_zone, zone_name):
    schedule_name = f'Ventilation schedules {thermal_zone.usage_name}'
    air_change = thermal_zone.mechanical_air_change * cte.HOUR_TO_SECONDS
    file = self._files['ventilation']
    self._write_to_idf_format(file, idf_cte.VENTILATION)
    self._write_to_idf_format(file, f'{zone_name}_ventilation', 'Name')
    self._write_to_idf_format(file, zone_name, 'Zone or ZoneList or Space or SpaceList Name')
    self._write_to_idf_format(file, schedule_name, 'Schedule Name')
    self._write_to_idf_format(file, 'AirChanges/Hour', 'Design Flow Rate Calculation Method')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Design Flow Rate')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Flow Rate per Floor Area')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Flow Rate per Person')
    self._write_to_idf_format(file, air_change, 'Air Changes per Hour')
    self._write_to_idf_format(file, 'Natural', 'Ventilation Type')
    self._write_to_idf_format(file, 0, 'Fan Pressure Rise')
    self._write_to_idf_format(file, 1, 'Fan Total Efficiency')
    self._write_to_idf_format(file, 1, 'Constant Term Coefficient')
    self._write_to_idf_format(file, 0, 'Temperature Term Coefficient')
    self._write_to_idf_format(file, 0, 'Velocity Term Coefficient')
    self._write_to_idf_format(file, 0, 'Velocity Squared Term Coefficient')
    self._write_to_idf_format(file, -100, 'Minimum Indoor Temperature')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Minimum Indoor Temperature Schedule Name')
    self._write_to_idf_format(file, 100, 'Maximum Indoor Temperature')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Maximum Indoor Temperature Schedule Name')
    self._write_to_idf_format(file, -100, 'Delta Temperature')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Delta Temperature Schedule Name')
    self._write_to_idf_format(file, -100, 'Minimum Outdoor Temperature')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Minimum Outdoor Temperature Schedule Name')
    self._write_to_idf_format(file, 100, 'Maximum Outdoor Temperature')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Maximum Outdoor Temperature Schedule Name')
    self._write_to_idf_format(file, 40, 'Maximum Wind Speed', ';')
