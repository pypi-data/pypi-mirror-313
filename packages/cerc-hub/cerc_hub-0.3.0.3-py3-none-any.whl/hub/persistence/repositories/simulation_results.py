"""
Simulation results repository with database CRUD operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""
import datetime
import logging

from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from hub.persistence.repository import Repository
from hub.persistence.models import City
from hub.persistence.models import CityObject
from hub.persistence.models import SimulationResults as Model


class SimulationResults(Repository):
  """
  Simulation results repository
  """
  _instance = None

  def __init__(self, db_name: str, dotenv_path: str, app_env: str):
    super().__init__(db_name, dotenv_path, app_env)

  def __new__(cls, db_name, dotenv_path, app_env):
    """
    Implemented for a singleton pattern
    """
    if cls._instance is None:
      cls._instance = super(SimulationResults, cls).__new__(cls)
    return cls._instance

  def insert(self, name: str, values: str, city_id=None, city_object_id=None):
    """
    Inserts simulations results linked either with a city as a whole or with a city object
    :param name: results name
    :param values: the simulation results in json format
    :param city_id: optional city id
    :param city_object_id: optional city object id
    :return: Identity id
    """
    if city_id is not None:
      _ = self._get_city(city_id)
    else:
      _ = self._get_city_object(city_object_id)
    try:
      simulation_result = Model(name=name,
                                values=values,
                                city_id=city_id,
                                city_object_id=city_object_id)
      with Session(self.engine) as session:
        session.add(simulation_result)
        session.flush()
        session.commit()
        session.refresh(simulation_result)
        return simulation_result.id
    except SQLAlchemyError as err:
      logging.error('An error occurred while creating city_object %s', err)
      raise SQLAlchemyError from err

  def update(self, name: str, values: str, city_id=None, city_object_id=None):
    """
    Updates simulation results for a city or a city object
    :param name: The simulation results tool and workflow name
    :param values: the simulation results in json format
    :param city_id: optional city id
    :param city_object_id: optional city object id
    :return: None
    """
    try:
      with Session(self.engine) as session:
        if city_id is not None:
          session.query(Model).filter(Model.name == name, Model.city_id == city_id).update(
          {
            'values': values,
            'updated': datetime.datetime.utcnow()
          })
          session.commit()
        elif city_object_id is not None:
          session.query(Model).filter(Model.name == name, Model.city_object_id == city_object_id).update(
            {
              'values': values,
              'updated': datetime.datetime.utcnow()
            })
          session.commit()
        else:
          raise NotImplementedError('Missing either city_id or city_object_id')
    except SQLAlchemyError as err:
      logging.error('Error while updating city object %s', err)
      raise SQLAlchemyError from err

  def delete(self, name: str, city_id=None, city_object_id=None):
    """
    Deletes an application with the application_uuid
    :param name: The simulation results tool and workflow name
    :param city_id: The id for the city owning the simulation results
    :param city_object_id: the id for the city_object owning these simulation results
    :return: None
    """
    try:
      with Session(self.engine) as session:
        if city_id is not None:
          session.query(Model).filter(Model.name == name, Model.city_id == city_id).delete()
          session.commit()
        elif city_object_id is not None:
          session.query(Model).filter(Model.name == name, Model.city_object_id == city_object_id).delete()
          session.commit()
        else:
          raise NotImplementedError('Missing either city_id or city_object_id')
    except SQLAlchemyError as err:
      logging.error('Error while deleting application: %s', err)
      raise SQLAlchemyError from err

  def _get_city(self, city_id) -> City:
    """
    Fetch a city object based city id
    :param city_id: a city identifier
    :return: [City] with the provided city_id
    """
    try:
      with Session(self.engine) as session:
        return session.execute(select(City).where(City.id == city_id)).first()
    except SQLAlchemyError as err:
      logging.error('Error while fetching city by city_id: %s', err)
      raise SQLAlchemyError from err

  def _get_city_object(self, city_object_id) -> [CityObject]:
    """
    Fetch a city object based city id
    :param city_object_id: a city object identifier
    :return: [CityObject] with the provided city_object_id
    """
    try:
      with Session(self.engine) as session:
        return session.execute(select(CityObject).where(CityObject.id == city_object_id)).first()
    except SQLAlchemyError as err:
      logging.error('Error while fetching city by city_id: %s', err)
      raise SQLAlchemyError from err

  def get_simulation_results_by_city_id_city_object_id_and_names(self, city_id, city_object_id, result_names=None) -> [Model]:
    """
    Fetch the simulation results based in the city_id or city_object_id with the given names or all
    :param city_id: the city id
    :param city_object_id: the city object id
    :param result_names: if given filter the results
    :return: [SimulationResult]
    """
    try:
      with Session(self.engine) as session:
        result_set = session.execute(select(Model).where(or_(
          Model.city_id == city_id,
          Model.city_object_id == city_object_id
        )))
        results = [r[0] for r in result_set]
        if not result_names:
          return results
        filtered_results = []
        for result in results:
          if result.name in result_names:
            filtered_results.append(result)
        return filtered_results
    except SQLAlchemyError as err:
      logging.error('Error while fetching city by city_id: %s', err)
      raise SQLAlchemyError from err

  def get_simulation_results_by_city_object_id_and_names(self, city_object_id, result_names=None) -> [Model]:
    """
    Fetch the simulation results based in the city_object_id with the given names or all
    :param city_object_id: the city object id
    :param result_names: if given filter the results
    :return: [SimulationResult]
    """
    try:
      with Session(self.engine) as session:
        result_set = session.execute(select(Model).where(
          Model.city_object_id == city_object_id
        ))
        results = [r[0] for r in result_set]
        if not result_names:
          return results
        filtered_results = []
        for result in results:
          if result.name in result_names:
            filtered_results.append(result)
        return filtered_results
    except SQLAlchemyError as err:
      logging.error('Error while fetching city by city_id: %s', err)
      raise SQLAlchemyError from err