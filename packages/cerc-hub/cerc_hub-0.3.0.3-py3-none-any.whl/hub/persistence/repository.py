"""
Base repository class to establish db connection
SPDX - License - Identifier: LGPL - 3.0 - or -later
Copyright © 2022 Concordia CERC group
Project Coder Peter Yefi peteryefi@gmail.com
"""
import logging
from sqlalchemy import create_engine
from hub.persistence.configuration import Configuration


class Repository:
  """
  Base repository class to establish db connection
  """

  def __init__(self, db_name, dotenv_path: str, app_env='TEST'):
    try:
      self.configuration = Configuration(db_name, dotenv_path, app_env)
      self.engine = create_engine(self.configuration.connection_string)
    except ValueError as err:
      logging.error('Missing value for credentials: %s', err)
