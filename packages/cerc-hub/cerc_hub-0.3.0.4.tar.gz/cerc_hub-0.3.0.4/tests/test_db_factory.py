"""
Test db factory
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
import distutils
import glob
import os
import subprocess
import unittest
from pathlib import Path
from unittest import TestCase

import sqlalchemy
import sqlalchemy.exc
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

import hub.helpers.constants as cte
from hub.exports.energy_building_exports_factory import EnergyBuildingsExportsFactory
from hub.exports.exports_factory import ExportsFactory
from hub.helpers.data.montreal_function_to_hub_function import MontrealFunctionToHubFunction
from hub.imports.construction_factory import ConstructionFactory
from hub.imports.energy_systems_factory import EnergySystemsFactory
from hub.imports.geometry_factory import GeometryFactory
from hub.imports.results_factory import ResultFactory
from hub.imports.usage_factory import UsageFactory
from hub.imports.weather_factory import WeatherFactory
from hub.persistence.db_control import DBControl
from hub.persistence.models import City, Application, CityObject, SimulationResults, UserRoles
from hub.persistence.models import User
from hub.persistence.repository import Repository


class Control:
  _skip_test = False
  _skip_reason = 'PostgreSQL not properly installed in host machine'

  def __init__(self):
    """
    Test
    setup
    :return: None
    """
    self._skip_test = False
    # Create test database
    dotenv_path = Path("{}/.local/etc/hub/.env".format(os.path.expanduser('~'))).resolve()
    if not dotenv_path.exists():
      self._skip_test = True
      self._skip_reason = f'.env file missing at {dotenv_path}'
      return
    dotenv_path = str(dotenv_path)
    repository = Repository(db_name='persistence_test_db', app_env='TEST', dotenv_path=dotenv_path)
    engine = create_engine(repository.configuration.connection_string)
    if database_exists(engine.url):
      drop_database(engine.url)
    create_database(engine.url)
    Application.__table__.create(bind=engine, checkfirst=True)
    User.__table__.create(bind=engine, checkfirst=True)
    City.__table__.create(bind=engine, checkfirst=True)
    CityObject.__table__.create(bind=engine, checkfirst=True)
    SimulationResults.__table__.create(bind=engine, checkfirst=True)

    self._database = DBControl(
      db_name=repository.configuration.db_name,
      app_env='TEST',
      dotenv_path=dotenv_path)

    example_path = (Path(__file__).parent / 'tests_data').resolve()
    city_file = (example_path / 'test.geojson').resolve()
    output_path = (Path(__file__).parent / 'tests_outputs').resolve()
    self._application_uuid = '60b7fc1b-f389-4254-9ffd-22a4cf32c7a3'
    self._application_id = 1
    self._user_id = 1
    self._pickle_path = 'tests_data/pickle_path.bz2'
    self._city = GeometryFactory('geojson',
                                 city_file,
                                 height_field='citygml_me',
                                 year_of_construction_field='ANNEE_CONS',
                                 aliases_field=['ID_UEV', 'CIVIQUE_DE', 'NOM_RUE'],
                                 function_field='CODE_UTILI',
                                 function_to_hub=MontrealFunctionToHubFunction().dictionary).city

    ConstructionFactory('nrcan', self._city).enrich()
    UsageFactory('nrcan', self._city).enrich()
    WeatherFactory('epw', self._city).enrich()
    ExportsFactory('sra', self._city, output_path).export()
    sra_file = str((output_path / f'{self._city.name}_sra.xml').resolve())
    subprocess.run([self.sra, sra_file], stdout=subprocess.DEVNULL)
    ResultFactory('sra', self._city, output_path).enrich()

    for building in self._city.buildings:
      building.energy_systems_archetype_name = 'system 1 gas pv'
    EnergySystemsFactory('montreal_custom', self._city).enrich()
    EnergyBuildingsExportsFactory('insel_monthly_energy_balance', self._city, output_path).export()
    _insel_files = glob.glob(f'{output_path}/*.insel')
    for insel_file in _insel_files:
      subprocess.run([self.insel, str(insel_file)], stdout=subprocess.DEVNULL)
    ResultFactory('insel_monthly_energy_balance', self._city, output_path).enrich()

    self._database = DBControl(
      db_name=repository.configuration.db_name,
      app_env='TEST',
      dotenv_path=dotenv_path)

    self._application_uuid = 'b9e0ce80-1218-410c-8a64-9d9b7026aad8'
    self._application_id = 1
    self._user_id = 1
    try:
      self._application_id = self._database.persist_application(
        'test',
        'test',
        self.application_uuid
      )
    except sqlalchemy.exc.SQLAlchemyError:
      self._application_id = self._database.application_info(self.application_uuid).id

    try:
      self._user_id = self._database.create_user('test', self._application_id, 'test', UserRoles.Admin)
    except sqlalchemy.exc.SQLAlchemyError:
      self._user_id = self._database.user_info(name='test', password='test', application_id=self._application_id).id

    self._pickle_path = (example_path / 'pickle_path.bz2').resolve()

    self._city

  @property
  def database(self):
    return self._database

  @property
  def application_uuid(self):
    return self._application_uuid

  @property
  def application_id(self):
    return self._application_id

  @property
  def user_id(self):
    return self._user_id

  @property
  def skip_test(self):
    return self._skip_test

  @property
  def insel(self):
    return distutils.spawn.find_executable('insel')

  @property
  def sra(self):
    return distutils.spawn.find_executable('sra')

  @property
  def skip_insel_test(self):
    return self.insel is None

  @property
  def skip_reason(self):
    return self._skip_reason

  @property
  def message(self):
    return self._skip_reason

  @property
  def pickle_path(self):
    return self._pickle_path

  @property
  def city(self):
    return self._city


control = Control()


class TestDBFactory(TestCase):
  """
TestDBFactory
"""

  @unittest.skipIf(control.skip_test, control.skip_reason)
  def test_save_city(self):
    control.city.name = "Montreal"
    city_id = control.database.persist_city(
      control.city,
      control.pickle_path,
      control.city.name,
      control.application_id,
      control.user_id)
    control.database.delete_city(city_id)

  @unittest.skipIf(control.skip_test, control.skip_reason)
  def test_get_update_city(self):
    city_id = control.database.persist_city(control.city,
                                            control.pickle_path,
                                            control.city.name,
                                            control.application_id,
                                            control.user_id)
    control.city.name = "Ottawa"
    control.database.update_city(city_id, control.city)
    cities = control.database.cities_by_user_and_application(
      control.user_id,
      control.application_id)
    for updated_city in cities:
      if updated_city.id == city_id:
        self.assertEqual(updated_city.name, control.city.name)
        break
    control.database.delete_city(city_id)

  @unittest.skipIf(control.skip_test, control.skip_reason)
  @unittest.skipIf(control.skip_insel_test, 'insel is not installed')
  def test_save_results(self):
    city_id = control.database.persist_city(control.city,
                                            control.pickle_path,
                                            'current status',
                                            control.application_id,
                                            control.user_id)
    city_objects_id = []
    request_values = {
      'scenarios': [{'current status': ['1']}]
    }
    for building in control.city.buildings:
      _building = control.database.building_info(building.name, city_id)
      if cte.MONTH not in building.cooling_demand:
        print(f'building {building.name} not calculated')
        continue
      monthly_cooling_peak_load = building.cooling_peak_load[cte.MONTH]
      yearly_cooling_peak_load = building.cooling_peak_load[cte.YEAR]
      monthly_heating_peak_load = building.heating_peak_load[cte.MONTH]
      yearly_heating_peak_load = building.heating_peak_load[cte.YEAR]
      monthly_lighting_peak_load = building.lighting_peak_load[cte.MONTH]
      yearly_lighting_peak_load = building.lighting_peak_load[cte.YEAR]
      monthly_appliances_peak_load = building.appliances_peak_load[cte.MONTH]
      yearly_appliances_peak_load = building.appliances_peak_load[cte.YEAR]
      monthly_cooling_demand = building.cooling_demand[cte.MONTH]
      yearly_cooling_demand = building.cooling_demand[cte.YEAR]
      monthly_heating_demand = building.heating_demand[cte.MONTH]
      yearly_heating_demand = building.heating_demand[cte.YEAR]
      monthly_lighting_electrical_demand = building.lighting_electrical_demand[cte.MONTH]
      yearly_lighting_electrical_demand = building.lighting_electrical_demand[cte.YEAR]
      monthly_appliances_electrical_demand = building.appliances_electrical_demand[cte.MONTH]
      yearly_appliances_electrical_demand = building.appliances_electrical_demand[cte.YEAR]
      monthly_domestic_hot_water_heat_demand = building.domestic_hot_water_heat_demand[cte.MONTH]
      yearly_domestic_hot_water_heat_demand = building.domestic_hot_water_heat_demand[cte.YEAR]
      monthly_heating_consumption = building.heating_consumption[cte.MONTH]
      yearly_heating_consumption = building.heating_consumption[cte.YEAR]
      monthly_cooling_consumption = building.cooling_consumption[cte.MONTH]
      yearly_cooling_consumption = building.cooling_consumption[cte.YEAR]
      monthly_domestic_hot_water_consumption = building.domestic_hot_water_consumption[cte.MONTH]
      yearly_domestic_hot_water_consumption = building._domestic_hot_water_consumption[cte.YEAR]
      monthly_distribution_systems_electrical_consumption = building.distribution_systems_electrical_consumption[
        cte.MONTH]
      yearly_distribution_systems_electrical_consumption = building.distribution_systems_electrical_consumption[
        cte.YEAR]
      monthly_on_site_electrical_production = [x * cte.WATTS_HOUR_TO_JULES
                                               for x in building.onsite_electrical_production[cte.MONTH]]
      yearly_on_site_electrical_production = [x * cte.WATTS_HOUR_TO_JULES
                                              for x in building.onsite_electrical_production[cte.YEAR]]
      results = {cte.INSEL_MEB: {
        'monthly_cooling_peak_load': monthly_cooling_peak_load,
        'yearly_cooling_peak_load': yearly_cooling_peak_load,
        'monthly_heating_peak_load': monthly_heating_peak_load,
        'yearly_heating_peak_load': yearly_heating_peak_load,
        'monthly_lighting_peak_load': monthly_lighting_peak_load,
        'yearly_lighting_peak_load': yearly_lighting_peak_load,
        'monthly_appliances_peak_load': monthly_appliances_peak_load,
        'yearly_appliances_peak_load': yearly_appliances_peak_load,
        'monthly_cooling_demand': monthly_cooling_demand,
        'yearly_cooling_demand': yearly_cooling_demand,
        'monthly_heating_demand': monthly_heating_demand,
        'yearly_heating_demand': yearly_heating_demand,
        'monthly_lighting_electrical_demand': monthly_lighting_electrical_demand,
        'yearly_lighting_electrical_demand': yearly_lighting_electrical_demand,
        'monthly_appliances_electrical_demand': monthly_appliances_electrical_demand,
        'yearly_appliances_electrical_demand': yearly_appliances_electrical_demand,
        'monthly_domestic_hot_water_heat_demand': monthly_domestic_hot_water_heat_demand,
        'yearly_domestic_hot_water_heat_demand': yearly_domestic_hot_water_heat_demand,
        'monthly_heating_consumption': monthly_heating_consumption,
        'yearly_heating_consumption': yearly_heating_consumption,
        'monthly_cooling_consumption': monthly_cooling_consumption,
        'yearly_cooling_consumption': yearly_cooling_consumption,
        'monthly_domestic_hot_water_consumption': monthly_domestic_hot_water_consumption,
        'yearly_domestic_hot_water_consumption': yearly_domestic_hot_water_consumption,
        'monthly_distribution_systems_electrical_consumption': monthly_distribution_systems_electrical_consumption,
        'yearly_distribution_systems_electrical_consumption': yearly_distribution_systems_electrical_consumption,
        'monthly_on_site_electrical_production': monthly_on_site_electrical_production,
        'yearly_on_site_electrical_production': yearly_on_site_electrical_production
      }}

      db_building_id = _building.id
      city_objects_id.append(db_building_id)
      control.database.add_simulation_results(
        cte.INSEL_MEB,
        results, city_object_id=db_building_id)
    self.assertEqual(17, len(city_objects_id), 'wrong number of results')
    self.assertIsNotNone(city_objects_id[0], 'city_object_id is None')
    results = control.database.results(control.user_id, control.application_id, request_values)
    self.assertEqual(
      28,
      len(results['current status'][0]['insel meb'].keys()),
      'wrong number of results after retrieve'
    )

    for _id in city_objects_id:
      control.database.delete_results_by_name('insel meb', city_object_id=_id)
    control.database.delete_city(city_id)

  @classmethod
  @unittest.skipIf(control.skip_test, control.skip_reason)
  def tearDownClass(cls):
    control.database.delete_application(control.application_uuid)
    control.database.delete_user(control.user_id)
    os.unlink(control.pickle_path)
    output_files = glob.glob('./tests_outputs/*')
    for output_file in output_files:
      os.unlink(output_file)
