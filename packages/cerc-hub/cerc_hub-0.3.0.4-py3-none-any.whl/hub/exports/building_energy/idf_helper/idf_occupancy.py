import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfOccupancy(IdfBase):
  @staticmethod
  def add(self, thermal_zone, zone_name):
    number_of_people = thermal_zone.occupancy.occupancy_density * thermal_zone.total_floor_area
    fraction_radiant = 0
    total_sensible = (
      thermal_zone.occupancy.sensible_radiative_internal_gain + thermal_zone.occupancy.sensible_convective_internal_gain
    )
    if total_sensible != 0:
      fraction_radiant = thermal_zone.occupancy.sensible_radiative_internal_gain / total_sensible
    occupancy_schedule = f'Occupancy schedules {thermal_zone.usage_name}'
    activity_level_schedule = f'Activity Level schedules {thermal_zone.usage_name}'
    file = self._files['occupancy']
    self._write_to_idf_format(file, idf_cte.PEOPLE)
    self._write_to_idf_format(file, f'{zone_name}_occupancy', 'Name')
    self._write_to_idf_format(file, zone_name, 'Zone or ZoneList or Space or SpaceList Name')
    self._write_to_idf_format(file, occupancy_schedule, 'Number of People Schedule Name')
    self._write_to_idf_format(file, 'People', 'Number of People Calculation Method')
    self._write_to_idf_format(file, number_of_people, 'Number of People')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'People per Floor Area')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Floor Area per Person')
    self._write_to_idf_format(file, fraction_radiant, 'Fraction Radiant')
    self._write_to_idf_format(file, idf_cte.AUTOCALCULATE, 'Sensible Heat Fraction')
    self._write_to_idf_format(file, activity_level_schedule, 'Activity Level Schedule Name')
    self._write_to_idf_format(file, '3.82e-08', 'Carbon Dioxide Generation Rate')
    self._write_to_idf_format(file, 'No', 'Enable ASHRAE 55 Comfort Warnings')
    self._write_to_idf_format(file, 'EnclosureAveraged', 'Mean Radiant Temperature Calculation Type')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Surface NameAngle Factor List Name')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Work Efficiency Schedule Name')
    self._write_to_idf_format(file, 'ClothingInsulationSchedule', 'Clothing Insulation Calculation Method')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Clothing Insulation Calculation Method Schedule Name')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Clothing Insulation Schedule Name')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Air Velocity Schedule Name')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Thermal Comfort Model 1 Type')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Thermal Comfort Model 2 Type')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Thermal Comfort Model 3 Type')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Thermal Comfort Model 4 Type')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Thermal Comfort Model 5 Type')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Thermal Comfort Model 6 Type')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Thermal Comfort Model 7 Type')
    self._write_to_idf_format(file, idf_cte.EMPTY, 'Ankle Level Air Velocity Schedule Name')
    self._write_to_idf_format(file, '15.56', 'Cold Stress Temperature Threshold')
    self._write_to_idf_format(file, '30', 'Heat Stress Temperature Threshold', ';')
