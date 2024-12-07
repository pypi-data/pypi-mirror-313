import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfZone(IdfBase):
  @staticmethod
  def add(self, thermal_zone, zone_name):
    file = self._files['zones']
    self._write_to_idf_format(file, idf_cte.ZONE)
    self._write_to_idf_format(file, zone_name, 'Name')
    self._write_to_idf_format(file, 0, 'Direction of Relative North')
    self._write_to_idf_format(file, 0, 'X Origin')
    self._write_to_idf_format(file, 0, 'Y Origin')
    self._write_to_idf_format(file, 0, 'Z Origin')
    self._write_to_idf_format(file, 1, 'Type')
    self._write_to_idf_format(file, 1, 'Multiplier')
    self._write_to_idf_format(file, idf_cte.AUTOCALCULATE, 'Ceiling Height')
    self._write_to_idf_format(file, thermal_zone.volume, 'Volume')
    self._write_to_idf_format(file, idf_cte.AUTOCALCULATE, 'Floor Area')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Zone Inside Convection Algorithm')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Zone Outside Convection Algorithm')
    self._write_to_idf_format(file, 'Yes', 'Part of Total Floor Area', ';')