"""
Test db factory
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
import distutils.spawn
import glob
import os
import subprocess
import unittest
from datetime import datetime
from pathlib import Path
from unittest import TestCase

import sqlalchemy
import sqlalchemy.exc
from hub.exports.energy_building_exports_factory import EnergyBuildingsExportsFactory
from hub.exports.exports_factory import ExportsFactory
from hub.helpers.data.montreal_function_to_hub_function import MontrealFunctionToHubFunction
from hub.imports.construction_factory import ConstructionFactory
from hub.imports.energy_systems_factory import EnergySystemsFactory
from hub.imports.geometry_factory import GeometryFactory
from hub.imports.results_factory import ResultFactory
from hub.imports.usage_factory import UsageFactory
from hub.imports.weather_factory import WeatherFactory
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

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
  def test_retrieve_results(self):
    datetime.now()
    request_values = {
      "scenarios": [
        {"current status": ["01002777", "01002773", "01036804"]},
        {"skin retrofit": ["01002777", "01002773", "01036804"]},
        {"system retrofit and pv": ["01002777", "01002773", "01036804"]},
        {"skin and system retrofit with pv": ["01002777", "01002773", "01036804"]}
      ]
    }
    results = control.database.results(control.user_id, control.application_id, request_values)
    scenarios = ['current status', 'skin retrofit', 'system retrofit and pv', 'skin and system retrofit with pv']
    for key, value in results.items():
      self.assertTrue(key in scenarios, 'Wrong key value')
      self.assertEqual(len(value), 0, 'wrong number of results')