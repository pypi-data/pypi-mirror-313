# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module for defining preview_results objects."""

# pylint: disable=C0330,
from __future__ import annotations

import dataclasses
import datetime
import enum
import uuid
from typing import Optional


class PreviewTaskStatus(enum.Enum):
  """Holds type of Task execution."""

  RUNNING = 'RUNNING'
  DONE = 'DONE'
  ERROR = 'ERROR'


@dataclasses.dataclass
class PreviewTaskAndResults:
  """Holds information of a particular preview result set.

  Attributes:
    status: execution status
    creation_time: Time when execution started.
    preview_command: The preview command
    results: Optional result details as a text field.
    id: Unique identifier of execution.
  """

  preview_command: str
  creation_time: datetime = dataclasses.field(
    default_factory=datetime.datetime.now
  )
  status: PreviewTaskStatus = PreviewTaskStatus.RUNNING
  results: Optional[str] = None
  id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))

  DATETIME_FORMAT = '%d-%b-%Y %H:%M'

  def to_serializable_dict(self):
    """Returns a JSON-serializable dictionary representation of the object."""

    def serialize(value):
      if isinstance(value, datetime.datetime):
        return value.strftime(self.DATETIME_FORMAT)
      if isinstance(value, PreviewTaskStatus):
        return value.value
      return value

    return {
      field.name: serialize(getattr(self, field.name))
      for field in dataclasses.fields(self)
    }
