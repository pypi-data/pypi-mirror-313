"""
Idf exports one building to idf format
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Guillermo.GutierrezMorote@concordia.ca
Code contributors: Pilar Monsalvete Alvarez de Uribarri pilar.monsalvete@concordia.ca
                   Oriol Gavalda Torrellas oriol.gavalda@concordia.ca
"""
import copy
import datetime
import glob
import os
from pathlib import Path
from geomeppy import IDF
import hub.helpers.constants as cte
from hub.city_model_structure.attributes.schedule import Schedule
from hub.city_model_structure.building_demand.thermal_zone import ThermalZone
from hub.helpers.configuration_helper import ConfigurationHelper


class Idf:
  """
  Exports city to IDF
  """
  _BUILDING = 'BUILDING'
  _ZONE = 'ZONE'
  _LIGHTS = 'LIGHTS'
  _APPLIANCES = 'OTHEREQUIPMENT'
  _PEOPLE = 'PEOPLE'
  _DHW = 'WATERUSE:EQUIPMENT'
  _THERMOSTAT = 'HVACTEMPLATE:THERMOSTAT'
  _IDEAL_LOAD_AIR_SYSTEM = 'HVACTEMPLATE:ZONE:IDEALLOADSAIRSYSTEM'
  _SURFACE = 'BUILDINGSURFACE:DETAILED'
  _SHADING = 'SHADING:BUILDING:DETAILED'
  _SHADING_PROPERTY = 'SHADINGPROPERTY:REFLECTANCE'
  _BUILDING_SURFACE = 'BuildingSurfaceDetailed'
  _CONSTRUCTION = 'CONSTRUCTION'
  _MATERIAL = 'MATERIAL'
  _MATERIAL_NOMASS = 'MATERIAL:NOMASS'
  _MATERIAL_ROOFVEGETATION = 'MATERIAL:ROOFVEGETATION'

  _WINDOW = 'FENESTRATIONSURFACE:DETAILED'
  _WINDOW_MATERIAL_SIMPLE = 'WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM'
  _ROUGHNESS = 'MediumRough'
  _INFILTRATION = 'ZONEINFILTRATION:DESIGNFLOWRATE'
  _VENTILATION = 'ZONEVENTILATION:DESIGNFLOWRATE'

  _HOURLY_SCHEDULE = 'SCHEDULE:DAY:HOURLY'
  _COMPACT_SCHEDULE = 'SCHEDULE:COMPACT'
  _FILE_SCHEDULE = 'SCHEDULE:FILE'
  _SCHEDULE_LIMIT = 'SCHEDULETYPELIMITS'
  _ON_OFF = 'On/Off'
  _FRACTION = 'Fraction'
  _ANY_NUMBER = 'Any Number'
  _CONTINUOUS = 'Continuous'
  _DISCRETE = 'Discrete'
  _SIZING_PERIODS = 'SIZINGPERIOD:DESIGNDAY'
  _LOCATION = 'SITE:LOCATION'
  _SIMPLE = 'Simple'

  idf_surfaces = {
    cte.WALL: 'wall',
    cte.GROUND: 'floor',
    cte.ROOF: 'roof'
  }
  idf_type_limits = {
    cte.ON_OFF: 'on/off',
    cte.FRACTION: 'Fraction',
    cte.ANY_NUMBER: 'Any Number',
    cte.CONTINUOUS: 'Continuous',
    cte.DISCRETE: 'Discrete'
  }
  idf_day_types = {
    cte.MONDAY: 'Monday',
    cte.TUESDAY: 'Tuesday',
    cte.WEDNESDAY: 'Wednesday',
    cte.THURSDAY: 'Thursday',
    cte.FRIDAY: 'Friday',
    cte.SATURDAY: 'Saturday',
    cte.SUNDAY: 'Sunday',
    cte.HOLIDAY: 'Holidays',
    cte.WINTER_DESIGN_DAY: 'WinterDesignDay',
    cte.SUMMER_DESIGN_DAY: 'SummerDesignDay'
  }

  def __init__(self, city, output_path, idf_file_path, idd_file_path, epw_file_path, export_type="Surfaces",
               target_buildings=None):
    self._city = city
    self._sanity_check()
    self._output_path = str(output_path.resolve())
    self._output_file = str((output_path / f'{city.name}.idf').resolve())
    self._export_type = export_type
    self._idd_file_path = str(idd_file_path)
    self._idf_file_path = str(idf_file_path)
    self._epw_file_path = str(epw_file_path)
    IDF.setiddname(self._idd_file_path)
    self._idf = IDF(self._idf_file_path, self._epw_file_path)
    self._idf.newidfobject(self._SCHEDULE_LIMIT, Name=self._ANY_NUMBER)
    self._idf.newidfobject(self._SCHEDULE_LIMIT, Name=self._FRACTION, Lower_Limit_Value=0.0, Upper_Limit_Value=1.0,
                           Numeric_Type=self._CONTINUOUS)
    self._idf.newidfobject(self._SCHEDULE_LIMIT, Name=self._ON_OFF, Lower_Limit_Value=0, Upper_Limit_Value=1,
                           Numeric_Type=self._DISCRETE)
    self._target_buildings = target_buildings
    self._adjacent_buildings = []
    if target_buildings is None:
      self._target_buildings = [building.name for building in self._city.buildings]
    else:
      for building_name in target_buildings:
        building = city.city_object(building_name)
        print('Name: ', building_name)
        if building.neighbours is not None:
          self._adjacent_buildings += building.neighbours
    self._export()

  def _sanity_check(self):
    levels_of_detail = self._city.level_of_detail
    if levels_of_detail.geometry is None:
      raise AttributeError('Level of detail of geometry not assigned')
    if levels_of_detail.geometry < 1:
      raise AttributeError(f'Level of detail of geometry = {levels_of_detail.geometry}. Required minimum level 1')
    if levels_of_detail.construction is None:
      raise AttributeError('Level of detail of construction not assigned')
    if levels_of_detail.construction < 2:
      raise AttributeError(f'Level of detail of construction = {levels_of_detail.construction}. Required minimum level 2')
    if levels_of_detail.usage is None:
      raise AttributeError('Level of detail of usage not assigned')
    if levels_of_detail.usage < 2:
      raise AttributeError(f'Level of detail of usage = {levels_of_detail.usage}. Required minimum level 2')
    if levels_of_detail.weather is None:
      raise AttributeError('Level of detail of weather not assigned')
    if levels_of_detail.weather < 2:
      raise AttributeError(f'Level of detail of weather = {levels_of_detail.weather}. Required minimum level 2')

  @staticmethod
  def _matrix_to_list(points, lower_corner):
    lower_x = lower_corner[0]
    lower_y = lower_corner[1]
    lower_z = lower_corner[2]
    points_list = []
    for point in points:
      point_tuple = (point[0] - lower_x, point[1] - lower_y, point[2] - lower_z)
      points_list.append(point_tuple)
    return points_list

  @staticmethod
  def _matrix_to_2d_list(points):
    points_list = []
    for point in points:
      point_tuple = (point[0], point[1])
      points_list.append(point_tuple)
    return points_list

  def _add_material(self, layer):
    for material in self._idf.idfobjects[self._MATERIAL]:
      if material.Name == layer.material_name:
        return
    for material in self._idf.idfobjects[self._MATERIAL_NOMASS]:
      if material.Name == layer.material_name:
        return
    if layer.no_mass:
      self._idf.newidfobject(self._MATERIAL_NOMASS,
                             Name=layer.material_name,
                             Roughness=self._ROUGHNESS,
                             Thermal_Resistance=layer.thermal_resistance
                             )
    else:
      self._idf.newidfobject(self._MATERIAL,
                             Name=layer.material_name,
                             Roughness=self._ROUGHNESS,
                             Thickness=layer.thickness,
                             Conductivity=layer.conductivity,
                             Density=layer.density,
                             Specific_Heat=layer.specific_heat,
                             Thermal_Absorptance=layer.thermal_absorptance,
                             Solar_Absorptance=layer.solar_absorptance,
                             Visible_Absorptance=layer.visible_absorptance
                             )

  @staticmethod
  def _create_infiltration_schedules(thermal_zone):
    _infiltration_schedules = []
    if thermal_zone.thermal_control is None:
      return []
    for hvac_availability_schedule in thermal_zone.thermal_control.hvac_availability_schedules:
      _schedule = Schedule()
      _schedule.type = cte.INFILTRATION
      _schedule.data_type = cte.FRACTION
      _schedule.time_step = cte.HOUR
      _schedule.time_range = cte.DAY
      _schedule.day_types = copy.deepcopy(hvac_availability_schedule.day_types)
      _infiltration_values = []
      for hvac_value in hvac_availability_schedule.values:
        if hvac_value == 0:
          _infiltration_values.append(1.0)
        else:
          if thermal_zone.infiltration_rate_system_off == 0:
            _infiltration_values.append(0.0)
          else:
            _infiltration_values.append(
              thermal_zone.infiltration_rate_system_on / thermal_zone.infiltration_rate_system_off)
      _schedule.values = _infiltration_values
      _infiltration_schedules.append(_schedule)
    return _infiltration_schedules

  @staticmethod
  def _create_ventilation_schedules(thermal_zone):
    _ventilation_schedules = []
    if thermal_zone.thermal_control is None:
      return []
    for hvac_availability_schedule in thermal_zone.thermal_control.hvac_availability_schedules:
      _schedule = Schedule()
      _schedule.type = cte.VENTILATION
      _schedule.data_type = cte.FRACTION
      _schedule.time_step = cte.HOUR
      _schedule.time_range = cte.DAY
      _schedule.day_types = copy.deepcopy(hvac_availability_schedule.day_types)
      _ventilation_schedules = thermal_zone.thermal_control.hvac_availability_schedules
    return _ventilation_schedules

  @staticmethod
  def _create_yearly_values_schedules(schedule_type, values):
    _schedule = Schedule()
    _schedule.type = schedule_type
    _schedule.data_type = cte.ANY_NUMBER
    _schedule.time_step = cte.HOUR
    _schedule.time_range = cte.YEAR
    _schedule.day_types = ['monday',
                           'tuesday',
                           'wednesday',
                           'thursday',
                           'friday',
                           'saturday',
                           'sunday',
                           'holiday',
                           'winter_design_day',
                           'summer_design_day']
    _schedule.values = values
    return [_schedule]

  @staticmethod
  def _create_constant_value_schedules(schedule_type, value):
    _schedule = Schedule()
    _schedule.type = schedule_type
    _schedule.data_type = cte.ANY_NUMBER
    _schedule.time_step = cte.HOUR
    _schedule.time_range = cte.DAY
    _schedule.day_types = ['monday',
                           'tuesday',
                           'wednesday',
                           'thursday',
                           'friday',
                           'saturday',
                           'sunday',
                           'holiday',
                           'winter_design_day',
                           'summer_design_day']
    _schedule.values = [value for _ in range(0, 24)]
    return [_schedule]

  def _add_standard_compact_hourly_schedule(self, usage, schedule_type, schedules):
    for schedule in self._idf.idfobjects[self._COMPACT_SCHEDULE]:
      if schedule.Name == f'{schedule_type} schedules {usage}':
        return
    _kwargs = {'Name': f'{schedule_type} schedules {usage}',
               'Schedule_Type_Limits_Name': self.idf_type_limits[schedules[0].data_type],
               'Field_1': 'Through: 12/31'}
    counter = 1
    for j, schedule in enumerate(schedules):
      _val = schedule.values
      _new_field = ''
      for day_type in schedule.day_types:
        _new_field += f' {self.idf_day_types[day_type]}'
      _kwargs[f'Field_{j * 25 + 2}'] = f'For:{_new_field}'
      counter += 1
      for i, _ in enumerate(_val):
        _kwargs[f'Field_{j * 25 + 3 + i}'] = f'Until: {i + 1:02d}:00,{_val[i]}'
        counter += 1
    _kwargs[f'Field_{counter + 1}'] = 'For AllOtherDays'
    _kwargs[f'Field_{counter + 2}'] = 'Until: 24:00,0.0'
    self._idf.newidfobject(self._COMPACT_SCHEDULE, **_kwargs)

  def _write_schedules_file(self, schedule, usage):
    file_name = str((Path(self._output_path) / f'{schedule.type} schedules {usage.replace("/","_")}.csv').resolve())
    if not Path(file_name).exists():
      with open(file_name, 'w', encoding='utf8') as file:
        for value in schedule.values:
          file.write(f'{str(value)},\n')
    return Path(file_name).name

  def _add_file_schedule(self, usage, schedule, file_name):
    _schedule = self._idf.newidfobject(self._FILE_SCHEDULE, Name=f'{schedule.type} schedules {usage}')
    _schedule.Schedule_Type_Limits_Name = self.idf_type_limits[schedule.data_type]
    _schedule.File_Name = file_name
    _schedule.Column_Number = 1
    _schedule.Rows_to_Skip_at_Top = 0
    _schedule.Number_of_Hours_of_Data = 8760
    _schedule.Column_Separator = 'Comma'
    _schedule.Interpolate_to_Timestep = 'No'
    _schedule.Minutes_per_Item = 60

  def _add_schedules(self, usage, schedule_type, new_schedules):
    if len(new_schedules) < 1:
      return
    schedule_from_file = False
    for schedule in new_schedules:
      if len(schedule.values) > 168:  # Hours in one week
        schedule_from_file = True
    if schedule_from_file:
      for schedule in self._idf.idfobjects[self._FILE_SCHEDULE]:
        if schedule.Name == f'{schedule_type} schedules {usage}':
          return
      file_name = self._write_schedules_file(new_schedules[0], usage)
      self._add_file_schedule(usage, new_schedules[0], file_name)
      return

    for schedule in self._idf.idfobjects[self._HOURLY_SCHEDULE]:
      if schedule.Name == f'{schedule_type} schedules {usage}':
        return
    self._add_standard_compact_hourly_schedule(usage, schedule_type, new_schedules)
    return

  def _add_construction(self, thermal_boundary):
    for construction in self._idf.idfobjects[self._CONSTRUCTION]:
      if thermal_boundary.parent_surface.vegetation is not None:
        vegetation_name = f'{thermal_boundary.construction_name}_{thermal_boundary.parent_surface.vegetation.name}'
        if construction.Name == vegetation_name:
          return
      else:
        if construction.Name == f'{thermal_boundary.construction_name} {thermal_boundary.parent_surface.type}':
          return
    if thermal_boundary.layers is None:
      for material in self._idf.idfobjects[self._MATERIAL]:
        if material.Name == "DefaultMaterial":
          return

      self._idf.set_default_constructions()
      return
    for layer in thermal_boundary.layers:
      self._add_material(layer)
    layers = thermal_boundary.layers
    # The constructions should have at least one layer
    if thermal_boundary.parent_surface.vegetation is not None:
      vegetation_name = f'{thermal_boundary.construction_name}_{thermal_boundary.parent_surface.vegetation.name}'
      _kwargs = {'Name': vegetation_name,
                 'Outside_Layer': thermal_boundary.parent_surface.vegetation.name}
      for i in range(0, len(layers) - 1):
        _kwargs[f'Layer_{i + 2}'] = layers[i].material_name
    else:
      _kwargs = {'Name': f'{thermal_boundary.construction_name} {thermal_boundary.parent_surface.type}',
                 'Outside_Layer': layers[0].material_name}
      for i in range(1, len(layers) - 1):
        _kwargs[f'Layer_{i + 1}'] = layers[i].material_name
    self._idf.newidfobject(self._CONSTRUCTION, **_kwargs)

  def _add_window_construction_and_material(self, thermal_opening):
    for window_material in self._idf.idfobjects[self._WINDOW_MATERIAL_SIMPLE]:
      if window_material['UFactor'] == thermal_opening.overall_u_value and \
         window_material['Solar_Heat_Gain_Coefficient'] == thermal_opening.g_value:
        return

    order = str(len(self._idf.idfobjects[self._WINDOW_MATERIAL_SIMPLE]) + 1)
    material_name = 'glazing_' + order
    _kwargs = {'Name': material_name, 'UFactor': thermal_opening.overall_u_value,
               'Solar_Heat_Gain_Coefficient': thermal_opening.g_value}
    self._idf.newidfobject(self._WINDOW_MATERIAL_SIMPLE, **_kwargs)

    window_construction_name = 'window_construction_' + order
    _kwargs = {'Name': window_construction_name, 'Outside_Layer': material_name}
    self._idf.newidfobject(self._CONSTRUCTION, **_kwargs)

  def _add_zone(self, thermal_zone, name):
    for zone in self._idf.idfobjects['ZONE']:
      if zone.Name == name:
        return
    self._idf.newidfobject(self._ZONE, Name=name, Volume=thermal_zone.volume)
    self._add_heating_system(thermal_zone, name)

  def _add_thermostat(self, thermal_zone):
    thermostat_name = f'Thermostat {thermal_zone.usage_name}'
    for thermostat in self._idf.idfobjects[self._THERMOSTAT]:
      if thermostat.Name == thermostat_name:
        return thermostat
    return self._idf.newidfobject(
      self._THERMOSTAT,
      Name=thermostat_name,
      Heating_Setpoint_Schedule_Name=f'Heating thermostat schedules {thermal_zone.usage_name}',
      Cooling_Setpoint_Schedule_Name=f'Cooling thermostat schedules {thermal_zone.usage_name}'
    )

  def _add_heating_system(self, thermal_zone, zone_name):
    for air_system in self._idf.idfobjects[self._IDEAL_LOAD_AIR_SYSTEM]:
      if air_system.Zone_Name == zone_name:
        return
    thermostat = self._add_thermostat(thermal_zone)
    self._idf.newidfobject(self._IDEAL_LOAD_AIR_SYSTEM,
                           Zone_Name=zone_name,
                           System_Availability_Schedule_Name=f'Thermostat_availability schedules {thermal_zone.usage_name}',
                           Heating_Availability_Schedule_Name=f'Thermostat_availability schedules {thermal_zone.usage_name}',
                           Cooling_Availability_Schedule_Name=f'Thermostat_availability schedules {thermal_zone.usage_name}',
                           Template_Thermostat_Name=thermostat.Name)

  def _add_occupancy(self, thermal_zone, zone_name):
    number_of_people = thermal_zone.occupancy.occupancy_density * thermal_zone.total_floor_area
    fraction_radiant = 0
    total_sensible = (
      thermal_zone.occupancy.sensible_radiative_internal_gain + thermal_zone.occupancy.sensible_convective_internal_gain
    )
    if total_sensible != 0:
      fraction_radiant = thermal_zone.occupancy.sensible_radiative_internal_gain / total_sensible

    self._idf.newidfobject(self._PEOPLE,
                           Name=f'{zone_name}_occupancy',
                           Zone_or_ZoneList_or_Space_or_SpaceList_Name=zone_name,
                           Number_of_People_Schedule_Name=f'Occupancy schedules {thermal_zone.usage_name}',
                           Number_of_People_Calculation_Method="People",
                           Number_of_People=number_of_people,
                           Fraction_Radiant=fraction_radiant,
                           Activity_Level_Schedule_Name=f'Activity Level schedules {thermal_zone.usage_name}'
                           )

  def _add_lighting(self, thermal_zone: ThermalZone, zone_name: str):
    fraction_radiant = thermal_zone.lighting.radiative_fraction
    method = 'Watts/Area'
    storeys_number = int(thermal_zone.total_floor_area / thermal_zone.footprint_area)
    watts_per_zone_floor_area = thermal_zone.lighting.density * storeys_number
    subcategory = f'ELECTRIC EQUIPMENT#{zone_name}#GeneralLights'

    self._idf.newidfobject(self._LIGHTS,
                           Name=f'{zone_name}_lights',
                           Zone_or_ZoneList_or_Space_or_SpaceList_Name=zone_name,
                           Schedule_Name=f'Lighting schedules {thermal_zone.usage_name}',
                           Design_Level_Calculation_Method=method,
                           Watts_per_Zone_Floor_Area=watts_per_zone_floor_area,
                           Fraction_Radiant=fraction_radiant,
                           EndUse_Subcategory=subcategory
                           )

  def _add_appliances(self, thermal_zone, zone_name):
    fuel_type = 'Electricity'
    fraction_radiant = thermal_zone.appliances.radiative_fraction
    fraction_latent = thermal_zone.appliances.latent_fraction
    method = 'Watts/Area'
    storeys_number = int(thermal_zone.total_floor_area / thermal_zone.footprint_area)
    watts_per_zone_floor_area = thermal_zone.appliances.density * storeys_number
    subcategory = f'ELECTRIC EQUIPMENT#{zone_name}#InteriorEquipment'
    self._idf.newidfobject(self._APPLIANCES,
                           Fuel_Type=fuel_type,
                           Name=zone_name,
                           Zone_or_ZoneList_or_Space_or_SpaceList_Name=zone_name,
                           Schedule_Name=f'Appliance schedules {thermal_zone.usage_name}',
                           Design_Level_Calculation_Method=method,
                           Power_per_Zone_Floor_Area=watts_per_zone_floor_area,
                           Fraction_Latent=fraction_latent,
                           Fraction_Radiant=fraction_radiant,
                           EndUse_Subcategory=subcategory
                           )

  def _add_infiltration(self, thermal_zone, zone_name):
    schedule = f'INF_CONST schedules {thermal_zone.usage_name}'
    _infiltration = thermal_zone.infiltration_rate_system_off * cte.HOUR_TO_SECONDS
    self._idf.newidfobject(self._INFILTRATION,
                           Name=f'{zone_name}_infiltration',
                           Zone_or_ZoneList_or_Space_or_SpaceList_Name=zone_name,
                           Schedule_Name=schedule,
                           Design_Flow_Rate_Calculation_Method='AirChanges/Hour',
                           Air_Changes_per_Hour=_infiltration
                           )

  def _add_infiltration_surface(self, thermal_zone, zone_name):
    schedule = f'INF_CONST schedules {thermal_zone.usage_name}'
    _infiltration = thermal_zone.infiltration_rate_area_system_off* cte.INFILTRATION_75PA_TO_4PA
    self._idf.newidfobject(self._INFILTRATION,
                           Name=f'{zone_name}_infiltration',
                           Zone_or_ZoneList_or_Space_or_SpaceList_Name=zone_name,
                           Schedule_Name=schedule,
                           Design_Flow_Rate_Calculation_Method='Flow/ExteriorWallArea',
                           Flow_Rate_per_Exterior_Surface_Area=_infiltration
                           )

  def _add_ventilation(self, thermal_zone, zone_name):
    schedule = f'Ventilation schedules {thermal_zone.usage_name}'
    _air_change = thermal_zone.mechanical_air_change * cte.HOUR_TO_SECONDS
    self._idf.newidfobject(self._VENTILATION,
                           Name=f'{zone_name}_ventilation',
                           Zone_or_ZoneList_or_Space_or_SpaceList_Name=zone_name,
                           Schedule_Name=schedule,
                           Design_Flow_Rate_Calculation_Method='AirChanges/Hour',
                           Air_Changes_per_Hour=_air_change
                           )

  def _add_dhw(self, thermal_zone, zone_name, usage):
    peak_flow_rate = thermal_zone.domestic_hot_water.peak_flow * thermal_zone.total_floor_area
    self._idf.newidfobject(self._DHW,
                           Name=f'DHW {zone_name}',
                           Peak_Flow_Rate=peak_flow_rate,
                           Flow_Rate_Fraction_Schedule_Name=f'DHW_prof schedules {thermal_zone.usage_name}',
                           Target_Temperature_Schedule_Name=f'DHW_temp schedules {thermal_zone.usage_name}',
                           Hot_Water_Supply_Temperature_Schedule_Name=f'DHW_temp schedules {thermal_zone.usage_name}',
                           Cold_Water_Supply_Temperature_Schedule_Name=f'cold_temp schedules {usage}',
                           EndUse_Subcategory=f'DHW {zone_name}',
                           Zone_Name=zone_name
                           )

  def _rename_building(self, city_name):
    name = str(city_name.encode("utf-8"))
    for building in self._idf.idfobjects[self._BUILDING]:
      building.Name = f'Buildings in {name}'
      building['Solar_Distribution'] = 'FullExterior'

  def _remove_sizing_periods(self):
    while len(self._idf.idfobjects[self._SIZING_PERIODS]) > 0:
      self._idf.popidfobject(self._SIZING_PERIODS, 0)

  def _remove_location(self):
    self._idf.popidfobject(self._LOCATION, 0)

  def _export(self):
    """
    Export the idf file into the given path.

    If buildings to calculate are provided, only those will appear in the output variables, otherwise all the city
    buildings will be calculated.
    If adjacent buildings are provided those buildings will be calculated, but will not appear in the output variables.

    export type = "Surfaces|Block"
    """

    self._remove_location()
    self._remove_sizing_periods()
    self._rename_building(self._city.name)
    self._lod = self._city.level_of_detail.geometry
    for building in self._city.buildings:
      is_target = building.name in self._target_buildings or building.name in self._adjacent_buildings
      for internal_zone in building.internal_zones:
        if internal_zone.thermal_zones_from_internal_zones is None:
          self._target_buildings.remove(building.name)
          is_target = False
          continue
        for thermal_zone in internal_zone.thermal_zones_from_internal_zones:

          for thermal_boundary in thermal_zone.thermal_boundaries:
            self._add_construction(thermal_boundary)
            if thermal_boundary.parent_surface.vegetation is not None:
              self._add_vegetation_material(thermal_boundary.parent_surface.vegetation)
            for thermal_opening in thermal_boundary.thermal_openings:
              self._add_window_construction_and_material(thermal_opening)

          if is_target:
            start = datetime.datetime.now()
            service_temperature = thermal_zone.domestic_hot_water.service_temperature
            usage = thermal_zone.usage_name
            _new_schedules = self._create_infiltration_schedules(thermal_zone)
            self._add_schedules(usage, 'Infiltration', _new_schedules)
            _new_schedules = self._create_ventilation_schedules(thermal_zone)
            self._add_schedules(usage, 'Ventilation', _new_schedules)
            self._add_schedules(usage, 'Occupancy', thermal_zone.occupancy.occupancy_schedules)
            self._add_schedules(usage, 'HVAC AVAIL', thermal_zone.thermal_control.hvac_availability_schedules)
            self._add_schedules(usage, 'Heating thermostat', thermal_zone.thermal_control.heating_set_point_schedules)
            self._add_schedules(usage, 'Cooling thermostat', thermal_zone.thermal_control.cooling_set_point_schedules)
            self._add_schedules(usage, 'Lighting', thermal_zone.lighting.schedules)
            self._add_schedules(usage, 'Appliance', thermal_zone.appliances.schedules)
            self._add_schedules(usage, 'DHW_prof', thermal_zone.domestic_hot_water.schedules)
            _new_schedules = self._create_yearly_values_schedules('cold_temp', building.cold_water_temperature[cte.HOUR])
            self._add_schedules(usage, 'cold_temp', _new_schedules)
            _new_schedules = self._create_constant_value_schedules('DHW_temp', service_temperature)
            self._add_schedules(usage, 'DHW_temp', _new_schedules)
            _new_schedules = self._create_constant_value_schedules('INF_CONST', 1)
            self._add_schedules(usage, 'INF_CONST', _new_schedules)
            _new_schedules = self._create_constant_value_schedules('Thermostat_availability', 1)
            self._add_schedules(usage, 'Thermostat_availability', _new_schedules)
            _occ = thermal_zone.occupancy
            if _occ.occupancy_density == 0:
              _total_heat = 0
            else:
              _total_heat = (_occ.sensible_convective_internal_gain + _occ.sensible_radiative_internal_gain
                             + _occ.latent_internal_gain) / _occ.occupancy_density
            _new_schedules = self._create_constant_value_schedules('Activity Level', _total_heat)
            self._add_schedules(usage, 'Activity Level', _new_schedules)
            self._add_zone(thermal_zone, building.name)
            self._add_heating_system(thermal_zone, building.name)
            self._add_infiltration_surface(thermal_zone, building.name)
            self._add_ventilation(thermal_zone, building.name)
            self._add_occupancy(thermal_zone, building.name)
            self._add_lighting(thermal_zone, building.name)
            self._add_appliances(thermal_zone, building.name)
            self._add_dhw(thermal_zone, building.name, usage)
      if self._export_type == "Surfaces":
        if is_target:
          if building.thermal_zones_from_internal_zones is not None:
            self._add_surfaces(building, building.name)
          else:
            self._add_pure_geometry(building, building.name)
        else:
          self._add_shading(building)
      else:
        self._add_block(building)

    self._idf.newidfobject(
      "OUTPUT:VARIABLE",
      Variable_Name="Zone Ideal Loads Supply Air Total Heating Energy",
      Reporting_Frequency="Hourly",
    )

    self._idf.newidfobject(
      "OUTPUT:VARIABLE",
      Variable_Name="Zone Ideal Loads Supply Air Total Cooling Energy",
      Reporting_Frequency="Hourly",
    )

    self._idf.newidfobject(
      "OUTPUT:VARIABLE",
      Variable_Name="Water Use Equipment Heating Rate",
      Reporting_Frequency="Hourly",
    )

    self._idf.newidfobject(
      "OUTPUT:VARIABLE",
      Variable_Name="Zone Lights Electricity Rate",
      Reporting_Frequency="Hourly",
    )

    self._idf.newidfobject(
      "OUTPUT:VARIABLE",
      Variable_Name="Other Equipment Electricity Rate",
      Reporting_Frequency="Hourly",
    )

    self._idf.newidfobject(
      "OUTPUT:VARIABLE",
      Variable_Name="Zone Air Temperature",
      Reporting_Frequency="Hourly",
    )

    self._idf.newidfobject(
      "OUTPUT:VARIABLE",
      Variable_Name="Zone Air Relative Humidity",
      Reporting_Frequency="Hourly",
    )

    # post-process to erase windows associated to adiabatic walls
    windows_list = []
    for window in self._idf.idfobjects[self._WINDOW]:
      found = False
      for surface in self._idf.idfobjects[self._SURFACE]:
        if window.Building_Surface_Name == surface.Name:
          found = True
      if not found:
        windows_list.append(window)
    for window in windows_list:
      self._idf.removeidfobject(window)

    self._idf.saveas(str(self._output_file))
    for building in self._city.buildings:
      if self._export_type == "Surfaces":
        if is_target and building.thermal_zones_from_internal_zones is not None:
          self._add_surfaces(building, building.name)
    return self._idf

  def run(self):
    """
    Start the energy plus simulation
    """
    self._idf.run(expandobjects=False, readvars=True, output_directory=self._output_path,
                  output_prefix=f'{self._city.name}_')

  def _add_block(self, building):
    _points = self._matrix_to_2d_list(building.foot_print.coordinates)
    self._idf.add_block(name=building.name, coordinates=_points, height=building.max_height,
                        num_stories=int(building.storeys_above_ground))

    for surface in self._idf.idfobjects[self._SURFACE]:
      for thermal_zone in building.thermal_zones_from_internal_zones:
        for boundary in thermal_zone.thermal_boundaries:
          if surface.Type == self.idf_surfaces[boundary.surface.type]:
            surface.Construction_Name = boundary.construction_name
            break
        for usage in thermal_zone.usages:
          surface.Zone_Name = usage.id
          break
        break
    self._idf.intersect_match()

  def _add_shading(self, building):
    for i, surface in enumerate(building.surfaces):
      shading = self._idf.newidfobject(self._SHADING, Name=f'{building.name}_{i}')
      coordinates = self._matrix_to_list(surface.solid_polygon.coordinates,
                                         self._city.lower_corner)
      shading.setcoords(coordinates)
      solar_reflectance = surface.short_wave_reflectance
      if solar_reflectance is None:
        solar_reflectance = ConfigurationHelper().short_wave_reflectance
      self._idf.newidfobject(self._SHADING_PROPERTY,
                             Shading_Surface_Name=f'{building.name}_{i}',
                             Diffuse_Solar_Reflectance_of_Unglazed_Part_of_Shading_Surface=solar_reflectance,
                             Fraction_of_Shading_Surface_That_Is_Glazed=0)

  def _add_pure_geometry(self, building, zone_name):
    for index, surface in enumerate(building.surfaces):
      outside_boundary_condition = 'Outdoors'
      sun_exposure = 'SunExposed'
      wind_exposure = 'WindExposed'
      idf_surface_type = self.idf_surfaces[surface.type]
      _kwargs = {'Name': f'Building_{building.name}_surface_{index}',
                 'Surface_Type': idf_surface_type,
                 'Zone_Name': zone_name}
      if surface.type == cte.GROUND:
        outside_boundary_condition = 'Ground'
        sun_exposure = 'NoSun'
        wind_exposure = 'NoWind'
      if surface.percentage_shared is not None and surface.percentage_shared > 0.5:
        outside_boundary_condition = 'Surface'
        outside_boundary_condition_object = f'Building_{building.name}_surface_{index}'
        sun_exposure = 'NoSun'
        wind_exposure = 'NoWind'
        _kwargs['Outside_Boundary_Condition_Object'] = outside_boundary_condition_object

      _kwargs['Outside_Boundary_Condition'] = outside_boundary_condition
      _kwargs['Sun_Exposure'] = sun_exposure
      _kwargs['Wind_Exposure'] = wind_exposure
      idf_surface = self._idf.newidfobject(self._SURFACE, **_kwargs)

      coordinates = self._matrix_to_list(surface.solid_polygon.coordinates,
                                         self._city.lower_corner)
      idf_surface.setcoords(coordinates)
    if self._lod >= 3:
      for internal_zone in building.internal_zones:
        for thermal_zone in internal_zone.thermal_zones_from_internal_zones:
          for boundary in thermal_zone.thermal_boundaries:
            self._add_windows_by_vertices(boundary)
    else:
      # idf only allows setting wwr for external walls
      wwr = 0
      try:
        self._idf.set_wwr(wwr, construction='window_construction_1')
      except ValueError:
        self._idf.set_wwr(0, construction='window_construction_1')

  def _add_surfaces(self, building, zone_name):
    for thermal_zone in building.thermal_zones_from_internal_zones:
      for index, boundary in enumerate(thermal_zone.thermal_boundaries):
        idf_surface_type = self.idf_surfaces[boundary.parent_surface.type]
        outside_boundary_condition = 'Outdoors'
        sun_exposure = 'SunExposed'
        wind_exposure = 'WindExposed'
        _kwargs = {'Name': f'Building_{building.name}_surface_{index}',
                   'Surface_Type': idf_surface_type,
                   'Zone_Name': zone_name}
        if boundary.parent_surface.type == cte.GROUND:
          outside_boundary_condition = 'Ground'
          sun_exposure = 'NoSun'
          wind_exposure = 'NoWind'
        if boundary.parent_surface.percentage_shared is not None and boundary.parent_surface.percentage_shared > 0.5:
          outside_boundary_condition = 'Surface'
          outside_boundary_condition_object = f'Building_{building.name}_surface_{index}'
          sun_exposure = 'NoSun'
          wind_exposure = 'NoWind'
          _kwargs['Outside_Boundary_Condition_Object'] = outside_boundary_condition_object
        _kwargs['Outside_Boundary_Condition'] = outside_boundary_condition
        _kwargs['Sun_Exposure'] = sun_exposure
        _kwargs['Wind_Exposure'] = wind_exposure

        if boundary.parent_surface.vegetation is not None:
          construction_name = f'{boundary.construction_name}_{boundary.parent_surface.vegetation.name}'
        else:
          construction_name = f'{boundary.construction_name} {boundary.parent_surface.type}'
        _kwargs['Construction_Name'] = construction_name
        start = datetime.datetime.now()
        surface = self._idf.newidfobject(self._SURFACE, **_kwargs)
        coordinates = self._matrix_to_list(boundary.parent_surface.solid_polygon.coordinates,
                                           self._city.lower_corner)
        surface.setcoords(coordinates)
    if self._lod >= 3:
      for internal_zone in building.internal_zones:
        for thermal_zone in internal_zone.thermal_zones_from_internal_zones:
          for boundary in thermal_zone.thermal_boundaries:
            self._add_windows_by_vertices(boundary)
    else:
      # idf only allows setting wwr for external walls
      wwr = 0
      for surface in building.surfaces:
        if surface.type == cte.WALL:
          wwr = surface.associated_thermal_boundaries[0].window_ratio
      try:
        self._idf.set_wwr(wwr, construction='window_construction_1')
      except ValueError:
        self._idf.set_wwr(0, construction='window_construction_1')

  def _add_windows_by_vertices(self, boundary):
    raise NotImplementedError

  def _compare_window_constructions(self, window_construction, opening):
    glazing = window_construction['Outside_Layer']
    for material in self._idf.idfobjects[self._WINDOW_MATERIAL_SIMPLE]:
      if material['Name'] == glazing:
        if material['UFactor'] == opening.overall_u_value and material[
          'Solar_Heat_Gain_Coefficient'] == opening.g_value:
          return True
    return False

  def _add_vegetation_material(self, vegetation):
    for vegetation_material in self._idf.idfobjects[self._MATERIAL_ROOFVEGETATION]:
      if vegetation_material.Name == vegetation.name:
        return
    soil = vegetation.soil
    height = 0
    leaf_area_index = 0
    leaf_reflectivity = 0
    leaf_emissivity = 0
    minimal_stomatal_resistance = 0
    for plant in vegetation.plants:
      height += plant.percentage * plant.height
      leaf_area_index += plant.percentage * plant.leaf_area_index
      leaf_reflectivity += plant.percentage * plant.leaf_reflectivity
      leaf_emissivity += plant.percentage * plant.leaf_emissivity
      minimal_stomatal_resistance += plant.percentage * plant.minimal_stomatal_resistance
    self._idf.newidfobject(
      self._MATERIAL_ROOFVEGETATION,
      Name=vegetation.name,
      Height_of_Plants=height,
      Leaf_Area_Index=leaf_area_index,
      Leaf_Reflectivity=leaf_reflectivity,
      Leaf_Emissivity=leaf_emissivity,
      Minimum_Stomatal_Resistance=minimal_stomatal_resistance,
      Soil_Layer_Name=soil.name,
      Roughness=soil.roughness,
      Thickness=vegetation.soil_thickness,
      Conductivity_of_Dry_Soil=soil.dry_conductivity,
      Density_of_Dry_Soil=soil.dry_density,
      Specific_Heat_of_Dry_Soil=soil.dry_specific_heat,
      Thermal_Absorptance=soil.thermal_absorptance,
      Solar_Absorptance=soil.solar_absorptance,
      Visible_Absorptance=soil.visible_absorptance,
      Saturation_Volumetric_Moisture_Content_of_the_Soil_Layer=soil.saturation_volumetric_moisture_content,
      Residual_Volumetric_Moisture_Content_of_the_Soil_Layer=soil.residual_volumetric_moisture_content,
      Initial_Volumetric_Moisture_Content_of_the_Soil_Layer=soil.initial_volumetric_moisture_content,
      Moisture_Diffusion_Calculation_Method=self._SIMPLE
    )
