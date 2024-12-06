"""
Model representation of a City
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""

import datetime

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy import DateTime

from hub.persistence.configuration import Models


class City(Models):
  """A model representation of a city
  """
  __tablename__ = 'city'
  id = Column(Integer, Sequence('city_id_seq'), primary_key=True)
  pickle_path = Column(String, nullable=False)
  name = Column(String, nullable=False)
  scenario = Column(String, nullable=False)
  application_id = Column(Integer, ForeignKey('application.id', ondelete='CASCADE'), nullable=False)
  user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=True)
  hub_release = Column(String, nullable=False)
  created = Column(DateTime, default=datetime.datetime.utcnow)
  updated = Column(DateTime, default=datetime.datetime.utcnow)

  def __init__(self, pickle_path, name, scenario, application_id, user_id, hub_release):
    self.pickle_path = str(pickle_path)
    self.name = name
    self.scenario = scenario
    self.application_id = application_id
    self.user_id = user_id
    self.hub_release = hub_release
