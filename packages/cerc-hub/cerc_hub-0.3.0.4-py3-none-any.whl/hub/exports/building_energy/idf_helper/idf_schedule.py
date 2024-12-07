import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfSchedule(IdfBase):
  @staticmethod
  def add(self, usage, schedule_type, schedules):
    if len(schedules) < 1:
      return
    schedule_name = f'{schedule_type} schedules {usage}'
    if schedule_name not in self._schedules_added_to_idf:
      self._schedules_added_to_idf[schedule_name] = True
      file = self._files['schedules']
      self._write_to_idf_format(file, idf_cte.COMPACT_SCHEDULE)
      self._write_to_idf_format(file, schedule_name, 'Name')
      self._write_to_idf_format(file, idf_cte.idf_type_limits[schedules[0].data_type], 'Schedule Type Limits Name')
      self._write_to_idf_format(file, 'Through: 12/31', 'Field 1')
      counter = 1
      for j, schedule in enumerate(schedules):
        _val = schedule.values
        _new_field = ''
        for day_type in schedule.day_types:
          _new_field += f' {idf_cte.idf_day_types[day_type]}'
        self._write_to_idf_format(file, f'For:{_new_field}', f'Field {j * 25 + 2}')
        counter += 1
        for i, _ in enumerate(_val):
          self._write_to_idf_format(file, f'Until: {i + 1:02d}:00,{_val[i]}', f'Field {j * 25 + 3 + i}')
          counter += 1
      self._write_to_idf_format(file, 'For AllOtherDays', f'Field {counter + 1}')
      self._write_to_idf_format(file, 'Until: 24:00,0.0', f'Field {counter + 2}', ';')
