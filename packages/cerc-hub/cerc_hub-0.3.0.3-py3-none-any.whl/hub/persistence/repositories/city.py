"""
City repository with database CRUD operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
import datetime
import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from hub.city_model_structure.city import City as CityHub
from hub.persistence.repository import Repository
from hub.persistence.models import City as Model
from hub.persistence.models import CityObject
from hub.version import __version__


class City(Repository):
  """
  City repository
  """
  _instance = None

  def __init__(self, db_name: str, dotenv_path: str, app_env: str):
    super().__init__(db_name, dotenv_path, app_env)

  def __new__(cls, db_name, dotenv_path, app_env):
    """
    Implemented for a singleton pattern
    """
    if cls._instance is None:
      cls._instance = super(City, cls).__new__(cls)
    return cls._instance

  def insert(self, city: CityHub, pickle_path, scenario, application_id, user_id: int):
    """
    Inserts a city
    :param city: The complete city instance
    :param pickle_path: Path to the pickle
    :param scenario: Simulation scenario name
    :param application_id: Application id owning the instance
    :param user_id: User id owning the instance
    :return: Identity id
    """
    city.save_compressed(pickle_path)
    try:
      db_city = Model(
        pickle_path,
        city.name,
        scenario,
        application_id,
        user_id,
        __version__)
      with Session(self.engine) as session:
        session.add(db_city)
        session.flush()
        session.commit()
        for building in city.buildings:
          db_city_object = CityObject(db_city.id,
                                      building)
          session.add(db_city_object)
          session.flush()
        session.commit()
        session.refresh(db_city)
        return db_city.id
    except SQLAlchemyError as err:
      logging.error('An error occurred while creating a city %s', err)
      raise SQLAlchemyError from err

  def update(self, city_id: int, city: CityHub):
    """
    Updates a city name (other updates makes no sense)
    :param city_id: the id of the city to be updated
    :param city: the city object
    :return: None
    """
    try:
      now = datetime.datetime.utcnow()
      with Session(self.engine) as session:
        session.query(Model).filter(Model.id == city_id).update({'name': city.name, 'updated': now})
        session.commit()
    except SQLAlchemyError as err:
      logging.error('Error while updating city %s', err)
      raise SQLAlchemyError from err

  def delete(self, city_id: int):
    """
    Deletes a City with the id
    :param city_id: the city id
    :return: None
    """
    try:
      with Session(self.engine) as session:
        session.query(CityObject).filter(CityObject.city_id == city_id).delete()
        session.query(Model).filter(Model.id == city_id).delete()
        session.commit()
    except SQLAlchemyError as err:
      logging.error('Error while fetching city %s', err)
      raise SQLAlchemyError from err

  def get_by_user_id_application_id_and_scenario(self, user_id, application_id, scenario) -> [Model]:
    """
    Fetch city based on the user who created it
    :param user_id: the user id
    :param application_id: the application id
    :param scenario: simulation scenario name
    :return: [ModelCity]
    """
    try:
      with Session(self.engine) as session:
        result_set = session.execute(select(Model).where(Model.user_id == user_id,
                                                         Model.application_id == application_id,
                                                         Model.scenario == scenario
                                                         )).all()
        return result_set
    except SQLAlchemyError as err:
      logging.error('Error while fetching city by name %s', err)
      raise SQLAlchemyError from err

  def get_by_user_id_and_application_id(self, user_id, application_id) -> [Model]:
    """
    Fetch city based on the user who created it
    :param user_id: the user id
    :param application_id: the application id
    :return: ModelCity
    """
    try:
      with Session(self.engine) as session:
        result_set = session.execute(
          select(Model).where(Model.user_id == user_id, Model.application_id == application_id)
        )
        return [r[0] for r in result_set]
    except SQLAlchemyError as err:
      logging.error('Error while fetching city by name %s', err)
      raise SQLAlchemyError from err

  def get_by_id(self, city_id) -> Model:
    with Session(self.engine) as session:
      return session.execute(select(Model).where(Model.id == city_id)).first()[0]