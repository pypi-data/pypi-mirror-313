"""
EnergyBuildingsExportsFactory exports a city into several formats related to energy in buildings
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Pilar Monsalvete Alvarez de uribarri pilar.monsalvete@concordia.ca
"""

from pathlib import Path

import requests

from hub.exports.building_energy.energy_ade import EnergyAde
from hub.exports.building_energy.idf import Idf
from hub.exports.building_energy.cerc_idf import CercIdf
from hub.exports.building_energy.insel.insel_monthly_energy_balance import InselMonthlyEnergyBalance
from hub.helpers.utils import validate_import_export_type
from hub.imports.weather.helpers.weather import Weather as wh


class EnergyBuildingsExportsFactory:
  """
  Energy Buildings exports factory class
  """

  def __init__(self, handler, city, path, custom_insel_block='d18599', target_buildings=None, weather_file=None):
    self._city = city
    self._export_type = '_' + handler.lower()
    self._weather_file = weather_file
    validate_import_export_type(EnergyBuildingsExportsFactory, handler)
    if isinstance(path, str):
      path = Path(path)
    self._path = path
    self._custom_insel_block = custom_insel_block
    self._target_buildings = target_buildings

  @property
  def _energy_ade(self):
    """
    Export to citygml with application domain extensions
    :return: None
    """
    return EnergyAde(self._city, self._path)

  @property
  def _idf(self):
    """
    Export the city to Energy+ idf format

    When target_buildings is set, only those will be calculated and their energy consumption output, non-adjacent
    buildings will be considered shading objects and adjacent buildings will be considered adiabatic.

    Adjacent buildings are provided they will be considered heated so energy plus calculations are more precise but
    no results will be calculated to speed up the calculation process.

    :return: None
    """
    idf_data_path = (Path(__file__).parent / './building_energy/idf_files/').resolve()
    url = wh().epw_file(self._city.region_code)
    if self._weather_file is None:
      self._weather_file = (Path(__file__).parent.parent / f'data/weather/epw/{url.rsplit("/", 1)[1]}').resolve()
    if not self._weather_file.exists():
      with open(self._weather_file, 'wb') as epw_file:
        epw_file.write(requests.get(url, allow_redirects=True).content)
    return Idf(self._city, self._path, (idf_data_path / 'Minimal.idf'), (idf_data_path / 'Energy+.idd'),
               self._weather_file, target_buildings=self._target_buildings)

  @property
  def _cerc_idf(self):
    idf_data_path = (Path(__file__).parent / './building_energy/idf_files/').resolve()
    url = wh().epw_file(self._city.region_code)
    weather_path = (Path(__file__).parent.parent / f'data/weather/epw/{url.rsplit("/", 1)[1]}').resolve()
    if not weather_path.exists():
      with open(weather_path, 'wb') as epw_file:
        epw_file.write(requests.get(url, allow_redirects=True).content)
    return CercIdf(self._city, self._path, (idf_data_path / 'base.idf'), (idf_data_path / 'Energy+.idd'), weather_path,
                   target_buildings=self._target_buildings)

  @property
  def _insel_monthly_energy_balance(self):
    """
    Export to Insel MonthlyEnergyBalance
    :return: None
    """
    return InselMonthlyEnergyBalance(self._city, self._path, self._custom_insel_block)

  def export(self):
    """
    Export the city given to the class using the given export type handler
    :return: None
    """
    return getattr(self, self._export_type, lambda: None)
