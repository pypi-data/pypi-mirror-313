"""
Model representation of an application
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Guille Gutierrez Guillermo.GutierrezMorote@concordia.ca
"""

import datetime

from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID

from hub.persistence.configuration import Models


class Application(Models):
  """
  A model representation of an application
  """
  __tablename__ = 'application'
  id = Column(Integer, Sequence('application_id_seq'), primary_key=True)
  name = Column(String, nullable=False)
  description = Column(String, nullable=False)
  application_uuid = Column(UUID(as_uuid=True), nullable=False)
  created = Column(DateTime, default=datetime.datetime.utcnow)
  updated = Column(DateTime, default=datetime.datetime.utcnow)

  def __init__(self, name, description, application_uuid):
    self.name = name
    self.description = description
    self.application_uuid = application_uuid
