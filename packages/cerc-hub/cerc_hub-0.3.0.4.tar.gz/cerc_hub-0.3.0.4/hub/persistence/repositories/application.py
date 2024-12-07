"""
Application repository with database CRUD operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""

import datetime
import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.session import Session

from hub.persistence.repository import Repository
from hub.persistence.models import Application as Model


class Application(Repository):
  """
  Application repository
  """
  _instance = None

  def __init__(self, db_name: str, dotenv_path: str, app_env: str):
    super().__init__(db_name, dotenv_path, app_env)

  def __new__(cls, db_name, dotenv_path, app_env):
    """
    Implemented for a singleton pattern
    """
    if cls._instance is None:
      cls._instance = super(Application, cls).__new__(cls)
    return cls._instance

  def insert(self, name: str, description: str, application_uuid: str):
    """
    Inserts a new application
    :param name: Application name
    :param description: Application description
    :param application_uuid: Unique identifier for the application
    :return: Identity id
    """
    try:
      application = self.get_by_uuid(application_uuid)
      if application is not None:
        raise SQLAlchemyError('application already exists')
    except TypeError:
      pass
    try:
      application = Model(name=name, description=description, application_uuid=application_uuid)
      with Session(self.engine) as session:
        session.add(application)
        session.commit()
        session.refresh(application)
        return application.id
    except SQLAlchemyError as err:
      logging.error('An error occurred while creating application %s', err)
      raise SQLAlchemyError from err

  def update(self, application_uuid: str, name: str, description: str):
    """
    Updates an application
    :param application_uuid: the application uuid of the application to be updated
    :param name: the application name
    :param description: the application description
    :return: None
    """
    try:
      with Session(self.engine) as session:
        session.query(Model).filter(
          Model.application_uuid == application_uuid
        ).update({'name': name, 'description': description, 'updated': datetime.datetime.utcnow()})
        session.commit()
    except SQLAlchemyError as err:
      logging.error('Error while updating application %s', err)
      raise SQLAlchemyError from err

  def delete(self, application_uuid: str):
    """
    Deletes an application with the application_uuid
    :param application_uuid: The application uuid
    :return: None
    """
    try:
      with Session(self.engine) as session:
        session.query(Model).filter(Model.application_uuid == application_uuid).delete()
        session.flush()
        session.commit()
    except SQLAlchemyError as err:
      logging.error('Error while deleting application %s', err)
      raise SQLAlchemyError from err

  def get_by_uuid(self, application_uuid: str) -> Model:
    """
    Fetch Application based on the application uuid
    :param application_uuid: the application uuid
    :return: Application with the provided application_uuid
    """
    try:
      with Session(self.engine) as session:
        result_set = session.execute(select(Model).where(
          Model.application_uuid == application_uuid)
        ).first()
        return result_set[0]
    except SQLAlchemyError as err:
      logging.error('Error while fetching application by application_uuid %s', err)
      raise SQLAlchemyError from err
    except TypeError as err:
      logging.error('Error while fetching application, empty result %s', err)
      raise TypeError from err
