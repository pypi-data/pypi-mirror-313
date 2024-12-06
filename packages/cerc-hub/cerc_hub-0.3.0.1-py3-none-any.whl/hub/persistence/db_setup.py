"""
Database setup
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

import logging
from hub.persistence.repository import Repository
from hub.persistence.models import Application
from hub.persistence.models import City
from hub.persistence.models import CityObject
from hub.persistence.models import User
from hub.persistence.models import UserRoles
from hub.persistence.models import SimulationResults
from hub.persistence.repositories.user import User as UserRepository
from hub.persistence.repositories.application import Application as ApplicationRepository


class DBSetup:
  """
  Creates a Persistence database structure
  """

  def __init__(self, db_name, app_env, dotenv_path, admin_password, application_uuid):
    """
    Creates database tables a default admin user and a default admin app with the given password and uuid
    :param db_name: database name
    :param app_env: application environment type [TEST|PROD]
    :param dotenv_path: .env file path
    :param admin_password: administrator password for the application uuid
    :application_uuid: application uuid
    """
    repository = Repository(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)

    # Create the tables using the models
    Application.__table__.create(bind=repository.engine, checkfirst=True)
    User.__table__.create(bind=repository.engine, checkfirst=True)
    City.__table__.create(bind=repository.engine, checkfirst=True)
    CityObject.__table__.create(bind=repository.engine, checkfirst=True)
    SimulationResults.__table__.create(bind=repository.engine, checkfirst=True)

    self._user_repo = UserRepository(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    self._application_repo = ApplicationRepository(db_name=db_name, app_env=app_env, dotenv_path=dotenv_path)
    application_id = self._create_admin_app(self._application_repo, application_uuid)
    self._create_admin_user(self._user_repo, admin_password, application_id)

  @staticmethod
  def _create_admin_app(application_repo, application_uuid):
    name = 'AdminTool'
    description = 'Admin tool to control city persistence and to test the API v1.4'
    logging.info('Creating default admin tool application...')
    application = application_repo.insert(name, description, application_uuid)

    if isinstance(application, dict):
      logging.info(application)
    else:
      msg = f'Created Admin tool with application_uuid: {application_uuid}'
      logging.info(msg)
    return application.id

  @staticmethod
  def _create_admin_user(user_repo, admin_password, application_id):
    password = admin_password
    logging.info('Creating default admin user...')
    user = user_repo.insert('Administrator', password, UserRoles.Admin, application_id)
    if isinstance(user, dict):
      logging.info(user)
    else:
      logging.info('Created Admin user')
