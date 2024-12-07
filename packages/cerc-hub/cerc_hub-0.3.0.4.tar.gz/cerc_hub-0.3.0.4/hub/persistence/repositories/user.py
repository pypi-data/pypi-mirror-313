"""
User repository with database CRUD operations
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
import datetime
import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from hub.helpers.auth import Auth
from hub.persistence.repository import Repository
from hub.persistence.models import User as Model, Application as ApplicationModel, UserRoles


class User(Repository):
  """
  User class
  """
  _instance = None

  def __init__(self, db_name: str, dotenv_path: str, app_env: str):
    super().__init__(db_name, dotenv_path, app_env)

  def __new__(cls, db_name, dotenv_path, app_env):
    """
    Implemented for a singleton pattern
    """
    if cls._instance is None:
      cls._instance = super(User, cls).__new__(cls)
    return cls._instance

  def insert(self, name: str, password: str, role: UserRoles, application_id: int):
    """
    Inserts a new user
    :param name: username
    :param password: user password
    :param role: user rol [Admin or Hub_Reader]
    :param application_id: user application id
    :return: Identity id
    """
    try:
      user = self.get_by_name_and_application(name, application_id)
      if user is not None:
        raise SQLAlchemyError(f'A user named {user.name} already exists for that application')
    except TypeError:
      pass
    try:
      user = Model(name=name, password=Auth.hash_password(password), role=role, application_id=application_id)
      with Session(self.engine) as session:
        session.add(user)
        session.flush()
        session.commit()
        session.refresh(user)
      return user.id
    except SQLAlchemyError as err:
      logging.error('An error occurred while creating user %s', err)
      raise SQLAlchemyError from err

  def update(self, user_id: int, name: str, password: str, role: UserRoles):
    """
    Updates a user
    :param user_id: the id of the user to be updated
    :param name: the name of the user
    :param password: the password of the user
    :param role: the role of the user
    :return: None
    """
    try:
      with Session(self.engine) as session:
        session.query(Model).filter(Model.id == user_id).update({
          'name': name,
          'password': Auth.hash_password(password),
          'role': role,
          'updated': datetime.datetime.utcnow()
        })
        session.commit()
    except SQLAlchemyError as err:
      logging.error('Error while updating user: %s', err)
      raise SQLAlchemyError from err

  def delete(self, user_id: int):
    """
    Deletes a user with the id
    :param user_id: the user id
    :return: None
    """
    try:
      with Session(self.engine) as session:
        session.query(Model).filter(Model.id == user_id).delete()
        session.commit()
    except SQLAlchemyError as err:
      logging.error('Error while fetching user: %s', err)
      raise SQLAlchemyError from err

  def get_by_name_and_application(self, name: str, application_id: int) -> Model:
    """
    Fetch user based on the email address
    :param name: Username
    :param application_id: User application name
    :return: User matching the search criteria or None
    """
    try:
      with Session(self.engine) as session:
        user = session.execute(
          select(Model).where(Model.name == name, Model.application_id == application_id)
        ).first()
        session.commit()
        return user[0]
    except SQLAlchemyError as err:
      logging.error('Error while fetching user by name and application: %s', err)
      raise SQLAlchemyError from err
    except TypeError as err:
      logging.error('Error while fetching user, empty result %s', err)
      raise TypeError from err

  def get_by_name_application_id_and_password(self, name: str, password: str, application_id: int) -> Model:
    """
    Fetch user based on the name, password and application id
    :param name: Username
    :param password: User password
    :param application_id: Application id
    :return: User
    """
    try:
      with Session(self.engine) as session:
        user = session.execute(
          select(Model).where(Model.name == name, Model.application_id == application_id)
        ).first()
        if user:
          if Auth.check_password(password, user[0].password):
            return user[0]
    except SQLAlchemyError as err:
      logging.error('Error while fetching user by name: %s', err)
      raise SQLAlchemyError from err
    raise ValueError('Unauthorized')

  def get_by_name_application_uuid_and_password(self, name: str, password: str, application_uuid: str) -> Model:
    """
    Fetch user based on the email and password
    :param name: Username
    :param password: User password
    :param application_uuid: Application uuid
    :return: User
    """
    try:
      with Session(self.engine) as session:
        application = session.execute(
          select(ApplicationModel).where(ApplicationModel.application_uuid == application_uuid)
        ).first()
        return self.get_by_name_application_id_and_password(name, password, application[0].id)
    except SQLAlchemyError as err:
      logging.error('Error while fetching user by name: %s', err)
      raise SQLAlchemyError from err
    except ValueError as err:
      raise ValueError from err
