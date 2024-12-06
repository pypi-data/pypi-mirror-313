"""
Cerc Idf result import
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Guillermo.GutierrezMorote@concordia.ca
Code contributors: Saeed Ranjbar saeed.ranjbar@concordia.ca
"""
import csv

import hub.helpers.constants as cte


class EnergyPlus:
  """
  Energy plus class
  """

  def _extract_fields_from_headers(self, headers):
    for header in headers:
      header_parts = header.split(':')
      building_name = header_parts[0]
      variable = ':'.join(header_parts[1:]).strip()  # concat the rest and ensure that : it's reintroduced just in case
      if variable is '':
        continue
      if building_name not in self._summary_variables:
        self._building_energy_demands[variable] = []  # initialize the list of variables
      else:
        self._building_energy_demands[header] = []

  def __init__(self, city, file_path):
    self._city = city
    self._building_energy_demands = {}
    self._lines = []
    self._summary_variables = ['DistrictCooling:Facility [J](Hourly)',
                               'InteriorEquipment:Electricity [J](Hourly)',
                               'InteriorLights:Electricity [J](Hourly) ']

    with open(file_path, 'r', encoding='utf8') as csv_file:
      csv_output = csv.reader(csv_file)
      self._headers = next(csv_output)
      self._extract_fields_from_headers(self._headers)
      for line in csv_output:
        self._lines.append(line)

  def enrich(self):
    """
    Enrich the city by using the energy plus workflow output files (J)
    :return: None
    """
    for building in self._city.buildings:
      _energy_demands = {}
      for header in self._building_energy_demands:
        print(header)
        if header == 'Zone Ideal Loads Supply Air Total Heating Energy [J](Hourly)':
          field_name = f'{building.name} IDEAL LOADS AIR SYSTEM:{header}'
        elif header == 'Zone Ideal Loads Supply Air Total Cooling Energy [J](Hourly)':
          field_name = f'{building.name} IDEAL LOADS AIR SYSTEM:{header}'
        else:
          field_name = f'{building.name}:{header}'
        position = -1
        if field_name in self._headers:
          position = self._headers.index(field_name)
        if position == -1:
          continue
        for line in self._lines:
          if header not in _energy_demands.keys():
            _energy_demands[header] = []
          _energy_demands[header].append(line[position])
      # print(building_energy_demands['Zone Ideal Loads Supply Air Total Heating Energy [J](Hourly)'])
      EnergyPlus._set_building_demands(building, _energy_demands)

  @staticmethod
  def _set_building_demands(building, energy_demands):
    print(energy_demands.keys())
    heating = [float(x) for x in energy_demands['Zone Ideal Loads Supply Air Total Heating Energy [J](Hourly)']]
    cooling = [float(x) for x in energy_demands['Zone Ideal Loads Supply Air Total Cooling Energy [J](Hourly)']]
    dhw = [float(x) * cte.WATTS_HOUR_TO_JULES for x in energy_demands['Water Use Equipment Heating Rate [W](Hourly)']]
    appliances = [float(x) * cte.WATTS_HOUR_TO_JULES for x in energy_demands['Other Equipment Electricity Rate [W](Hourly)']]
    lighting = [float(x) * cte.WATTS_HOUR_TO_JULES for x in energy_demands['Zone Lights Electricity Rate [W](Hourly)']]
    building.heating_demand[cte.HOUR] = heating
    building.cooling_demand[cte.HOUR] = cooling
    building.domestic_hot_water_heat_demand[cte.HOUR] = dhw
    building.appliances_electrical_demand[cte.HOUR] = appliances
    building.lighting_electrical_demand[cte.HOUR] = lighting
    building.heating_demand[cte.MONTH] = []
    building.cooling_demand[cte.MONTH] = []
    building.domestic_hot_water_heat_demand[cte.MONTH] = []
    building.appliances_electrical_demand[cte.MONTH] = []
    building.lighting_electrical_demand[cte.MONTH] = []

    start = 0

    for hours in cte.HOURS_A_MONTH.values():
      end = hours + start
      building.heating_demand[cte.MONTH].append(sum(building.heating_demand[cte.HOUR][start: end]))
      building.cooling_demand[cte.MONTH].append(sum(building.cooling_demand[cte.HOUR][start: end]))
      building.domestic_hot_water_heat_demand[cte.MONTH].append(sum(dhw[start: end]))
      building.appliances_electrical_demand[cte.MONTH].append(sum(appliances[start: end]))
      building.lighting_electrical_demand[cte.MONTH].append(sum(lighting[start: end]))
      start = end
    building.heating_demand[cte.YEAR] = [sum(building.heating_demand[cte.HOUR])]
    building.cooling_demand[cte.YEAR] = [sum(building.cooling_demand[cte.HOUR])]
    building.domestic_hot_water_heat_demand[cte.YEAR] = [sum(building.domestic_hot_water_heat_demand[cte.HOUR])]
    building.appliances_electrical_demand[cte.YEAR] = [sum(building.appliances_electrical_demand[cte.HOUR])]
    building.lighting_electrical_demand[cte.YEAR] = [sum(building.lighting_electrical_demand[cte.HOUR])]
