"""
DBFactory performs read related operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project CoderPeter Yefi peteryefi@gmail.com
"""
from typing import Dict

from hub.persistence.repositories.application import Application
from hub.persistence.repositories.city import City
from hub.persistence.repositories.city_object import CityObject
from hub.persistence.repositories.simulation_results import SimulationResults
from hub.persistence.repositories.user import User
from hub.persistence.repositories.user import UserRoles


class DBControl:
  """
  DBFactory class
  """

  def __init__(self, db_name, app_env, dotenv_path):
    self._city = City(db_name=db_name, dotenv_path=dotenv_path, app_env=app_env)
    self._application = Application(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._user = User(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._city_object = CityObject(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._simulation_results = SimulationResults(db_name=db_name, dotenv_path=dotenv_path, app_env=app_env)

  def application_info(self, application_uuid) -> Application:
    """
    Retrieve the application info for the given uuid from the database
    :param application_uuid: the uuid for the application
    :return: Application
    """
    return self._application.get_by_uuid(application_uuid)

  def user_info(self, name, password, application_id) -> User:
    """
    Retrieve the user info for the given name and password and application_id from the database
    :param name: the username
    :param password: the user password
    :param application_id: the application id
    :return: User
    """
    return self._user.get_by_name_application_id_and_password(name, password, application_id)

  def user_login(self, name, password, application_uuid) -> User:
    """
    Retrieve the user info from the database
    :param name: the username
    :param password: the user password
    :param application_uuid: the application uuid
    :return: User
    """
    return self._user.get_by_name_application_uuid_and_password(name, password, application_uuid)

  def cities_by_user_and_application(self, user_id, application_id) -> [City]:
    """
    Retrieve the cities belonging to the user and the application from the database
    :param user_id: User id
    :param application_id: Application id
    :return: [City]
    """
    return self._city.get_by_user_id_and_application_id(user_id, application_id)

  def building(self, name, user_id, application_id, scenario) -> CityObject:
    """
    Retrieve the building from the database
    :param name: Building name
    :param user_id: User id
    :param application_id: Application id
    :param scenario: Scenario
    :
    """
    cities = self._city.get_by_user_id_application_id_and_scenario(user_id, application_id, scenario)
    c = [c[0].id for c in cities]
    result = self._city_object.building_in_cities_info(name, c)
    if result is not None:
      return result
    return None

  def building_info(self, name, city_id) -> CityObject:
    """
    Retrieve the building info from the database
    :param name: Building name
    :param city_id: City ID
    :return: CityObject
    """
    return self._city_object.get_by_name_or_alias_and_city(name, city_id)

  def building_info_in_cities(self, name, cities) -> CityObject:
    """
    Retrieve the building info from the database
    :param name: Building name
    :param cities: [City ID]
    :return: CityObject
    """
    return self._city_object.get_by_name_or_alias_in_cities(name, cities)

  def buildings_info(self, user_id, application_id, names_or_aliases) -> [CityObject]:
    """
    Retrieve the buildings info from the database
    :param user_id: User ID
    :param application_id: Application ID
    :param names_or_aliases: A list of names or alias for the buildings
    :return: [CityObject]
    """
    results = self._city_object.get_by_name_or_alias_for_user_app(user_id, application_id, names_or_aliases)
    if results is None:
      return []
    return results

  def results(self, user_id, application_id, request_values, result_names=None) -> Dict:
    """
    Retrieve the simulation results for the given cities from the database
    :param user_id: the user id owning the results
    :param application_id: the application id owning the results
    :param request_values: dictionary containing the scenario and building names to grab the results
    :param result_names: if given, filter the results to the selected names
    """
    if result_names is None:
      result_names = []
    results = {}
    for scenario in request_values['scenarios']:
      for scenario_name in scenario.keys():
        result_sets = self._city.get_by_user_id_application_id_and_scenario(
          user_id,
          application_id,
          scenario_name
        )
        if result_sets is None:
          continue
        results[scenario_name] = []
        city_ids = [r[0].id for r in result_sets]
        for building_name in scenario[scenario_name]:
          _building = self._city_object.get_by_name_or_alias_in_cities(building_name, city_ids)
          if _building is None:
            continue
          city_object_id = _building.id
          _ = self._simulation_results.get_simulation_results_by_city_object_id_and_names(
            city_object_id,
            result_names)

          for value in _:
            values = value.values
            values["building"] = building_name
            results[scenario_name].append(values)
    return results

  def persist_city(self, city: City, pickle_path, scenario, application_id: int, user_id: int):
    """
    Creates a city into the database
    :param city: City to be stored
    :param pickle_path: Path to save the pickle file
    :param scenario: Simulation scenario name
    :param application_id: Application id owning this city
    :param user_id: User who create the city
    return identity_id
    """
    return self._city.insert(city, pickle_path, scenario,  application_id, user_id)

  def update_city(self, city_id, city):
    """
   Update an existing city in the database
   :param city_id: the id of the city to update
   :param city: the updated city object
    """
    return self._city.update(city_id, city)

  def persist_application(self, name: str, description: str, application_uuid: str):
    """
    Creates information for an application in the database
   :param name: name of application
   :param description: the description of the application
   :param application_uuid: the uuid of the application to be created
    """
    return self._application.insert(name, description, application_uuid)

  def update_application(self, name: str, description: str, application_uuid: str):
    """
    Update the application information stored in the database
   :param name: name of application
   :param description: the description of the application
   :param application_uuid: the uuid of the application to be created
    """
    return self._application.update(application_uuid, name, description)

  def add_simulation_results(self, name, values, city_id=None, city_object_id=None):
    """
    Add simulation results to the city or to the city_object to the database
    :param name: simulation and simulation engine name
    :param values: simulation values in json format
    :param city_id: city id or None
    :param city_object_id: city object id or None
    """
    return self._simulation_results.insert(name, values, city_id, city_object_id)

  def create_user(self, name: str, application_id: int, password: str, role: UserRoles):
    """
    Creates a new user in the database
    :param name: the name of the user
    :param application_id: the application id of the user
    :param password: the password of the user
    :param role: the role of the user
    """
    return self._user.insert(name, password, role, application_id)

  def update_user(self, user_id: int, name: str, password: str, role: UserRoles):
    """
    Updates a user in the database
    :param user_id: the id of the user
    :param name: the name of the user
    :param password: the password of the user
    :param role: the role of the user
    """
    return self._user.update(user_id, name, password, role)

  def get_by_name_and_application(self, name: str, application: int):
    """
    Retrieve a single user from the database
    :param name: username
    :param application: application accessing hub
    """
    return self._user.get_by_name_and_application(name, application)

  def delete_user(self, user_id):
    """
    Delete a single user from the database
    :param user_id: the id of the user to delete
    """
    self._user.delete(user_id)

  def delete_city(self, city_id):
    """
    Deletes a single city from the database
    :param city_id: the id of the city to get
    """
    self._city.delete(city_id)

  def delete_results_by_name(self, name, city_id=None, city_object_id=None):
    """
    Deletes city object simulation results from the database
    :param name: simulation name
    :param city_id: if given, delete delete the results for the city with id city_id
    :param city_object_id: if given, delete delete the results for the city object with id city_object_id
    """
    self._simulation_results.delete(name, city_id=city_id, city_object_id=city_object_id)

  def delete_application(self, application_uuid):
    """
    Deletes a single application from the database
    :param application_uuid: the id of the application to get
    """
    self._application.delete(application_uuid)

  def get_city(self, city_id):
    return self._city.get_by_id(city_id)
