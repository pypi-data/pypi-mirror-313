"""
Model representation of simulation results
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""

import datetime

from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from hub.persistence.configuration import Models


class SimulationResults(Models):
  """
  A model representation of an application
  """
  __tablename__ = 'simulation_results'
  id = Column(Integer, Sequence('simulation_results_id_seq'), primary_key=True)
  city_id = Column(Integer, ForeignKey('city.id', ondelete='CASCADE'), nullable=True)
  city_object_id = Column(Integer, ForeignKey('city_object.id', ondelete='CASCADE'), nullable=True)
  name = Column(String, nullable=False)
  values = Column(JSONB, nullable=False)
  created = Column(DateTime, default=datetime.datetime.utcnow)
  updated = Column(DateTime, default=datetime.datetime.utcnow)

  def __init__(self, name, values, city_id=None, city_object_id=None):
    self.name = name
    self.values = values
    self.city_id = city_id
    self.city_object_id = city_object_id
