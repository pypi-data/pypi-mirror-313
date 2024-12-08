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
from __future__ import annotations

# pylint: disable=C0330, g-bad-import-order
import dataclasses
from collections import abc

from googleads_housekeeper.domain.core import execution, task


class Command: ...


@dataclasses.dataclass
class RunTask(Command):
  id: int
  type: execution.ExecutionTypeEnum
  exclusion_rule: str = ''
  save_to_db: bool = True


@dataclasses.dataclass
class SaveTask(Command):
  exclusion_rule: str
  customer_ids: str | list[str]
  from_days_ago: int = 0
  date_range: int = 7
  exclusion_level: str = 'AD_GROUP'
  output: str = task.TaskOutput.EXCLUDE_AND_NOTIFY.name
  name: str | None = None
  schedule: str | None = None
  placement_types: str | None = None
  task_id: str | None = None

  def __post_init__(self):
    self.customer_ids = (
      ','.join(self.customer_ids)
      if isinstance(self.customer_ids, abc.MutableSequence)
      else self.customer_ids
    )


@dataclasses.dataclass
class DeleteTask(Command):
  task_id: int


@dataclasses.dataclass
class RunManualExclusion(Command):
  customer_ids: str
  placements: list[list]
  header: list[str]
  exclusion_level: str


def ensure_tuple(value):
  if isinstance(value, str):
    return tuple(value.split(','))
  return value


@dataclasses.dataclass
class PreviewPlacements(Command):
  exclusion_rule: str
  placement_types: tuple[str, ...] | None
  customer_ids: str | list[str]
  from_days_ago: int
  date_range: int
  exclusion_level: str = 'AD_GROUP'
  exclude_and_notify: str = 'EXCLUDE_AND_NOTIFY'
  save_to_db: bool = True
  preview_pagination_index_one_based: int = 1

  def __post_init__(self):
    self.placement_types = ensure_tuple(self.placement_types)
    self.from_days_ago = int(self.from_days_ago)
    self.date_range = int(self.date_range)

  def to_dict(self):
    return dataclasses.asdict(self)


@dataclasses.dataclass
class AddToAllowlisting(Command):
  type: str
  name: str
  account_id: str


@dataclasses.dataclass
class RemoveFromAllowlisting(Command):
  type: str
  name: str
  account_id: str


@dataclasses.dataclass
class SaveConfig(Command):
  id: str
  mcc_id: str
  email_address: str
  always_fetch_youtube_preview_mode: bool = True
  save_to_db: bool = False


@dataclasses.dataclass
class GetCustomerIds(Command):
  mcc_id: str


@dataclasses.dataclass
class GetMccIds(Command):
  root_mcc_id: int


@dataclasses.dataclass
class SaveWebsiteInfo(Command):
  website_info: dict


@dataclasses.dataclass
class SaveChannelInfo(Command):
  channel_info: dict


@dataclasses.dataclass
class SaveVideoInfo(Command):
  video_info: dict


@dataclasses.dataclass
class MigrateFromOldTasks(Command):
  pass


@dataclasses.dataclass
class GetPreviewTasksTable(Command):
  pass


@dataclasses.dataclass
class GetResultsForSpecificPreviewTask(Command):
  preview_task_id: str
  preview_pagination_index_one_based: int = 1
