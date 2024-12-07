"""
Model representation of a User
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

import datetime
import enum

from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import DateTime, Enum

from hub.persistence.configuration import Models


class UserRoles(enum.Enum):
  """
  User roles enum
  """
  Admin = 'Admin'
  Hub_Reader = 'Hub_Reader'


class User(Models):
  """
  A model representation of a city
  """
  __tablename__ = 'user'
  id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
  name = Column(String, nullable=False)
  password = Column(String, nullable=False)
  role = Column(Enum(UserRoles), nullable=False, default=UserRoles.Hub_Reader)
  application_id = Column(Integer, nullable=False)
  created = Column(DateTime, default=datetime.datetime.utcnow)
  updated = Column(DateTime, default=datetime.datetime.utcnow)

  def __init__(self, name, password, role, application_id):
    self.name = name
    self.password = password
    self.role = role
    self.application_id = application_id
