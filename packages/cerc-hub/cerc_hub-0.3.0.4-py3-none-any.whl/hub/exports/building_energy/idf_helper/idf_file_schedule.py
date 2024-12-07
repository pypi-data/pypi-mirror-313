from pathlib import Path
import hub.helpers.constants as cte
import hub.exports.building_energy.idf_helper as idf_cte
from hub.exports.building_energy.idf_helper.idf_base import IdfBase


class IdfFileSchedule(IdfBase):
  @staticmethod
  def add(self, usage, schedule_type, schedules):
    schedule_name = f'{schedule_type} schedules {usage}'
    for schedule in schedules:
      if schedule_name not in self._schedules_added_to_idf:
        self._schedules_added_to_idf[schedule_name] = True
        file_name = str(
          (Path(self._output_path) / f'{schedule_type} schedules {usage.replace("/", "_")}.csv').resolve())
        with open(file_name, 'w', encoding='utf8') as file:
          for value in schedule.values[0]:
            file.write(f'{value},\n')
        file = self._files['file_schedules']
        self._write_to_idf_format(file, idf_cte.FILE_SCHEDULE)
        self._write_to_idf_format(file, schedule_name, 'Name')
        self._write_to_idf_format(file, idf_cte.idf_type_limits[schedule.data_type], 'Schedule Type Limits Name')
        self._write_to_idf_format(file, Path(file_name).name, 'File Name')
        self._write_to_idf_format(file, 1, 'Column Number')
        self._write_to_idf_format(file, 0, 'Rows to Skip at Top')
        self._write_to_idf_format(file, 8760, 'Number of Hours of Data')
        self._write_to_idf_format(file, 'Comma', 'Column Separator')
        self._write_to_idf_format(file, 'No', 'Interpolate to Timestep')
        self._write_to_idf_format(file, '60', 'Minutes per Item')
        self._write_to_idf_format(file, 'Yes', 'Adjust Schedule for Daylight Savings', ';')
