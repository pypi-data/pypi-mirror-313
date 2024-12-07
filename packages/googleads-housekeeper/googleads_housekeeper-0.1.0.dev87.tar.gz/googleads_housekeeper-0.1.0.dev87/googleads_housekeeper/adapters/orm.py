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

# pylint: disable=C0330
from __future__ import annotations

from sqlalchemy import (
  Boolean,
  Column,
  DateTime,
  Enum,
  ForeignKey,
  Integer,
  MetaData,
  String,
  Table,
  Text,
)
from sqlalchemy.orm import mapper, relationship

from googleads_housekeeper.domain.core import (
  execution,
  preview_task,
  settings,
  task,
)
from googleads_housekeeper.domain.external_parsers import (
  website_parser,
  youtube_data_parser,
)
from googleads_housekeeper.domain.placement_handler import (
  entities as placement_entities,
)
from googleads_housekeeper.services import enums

metadata = MetaData()

tasks = Table(
  'tasks',
  metadata,
  Column('_id', Integer, autoincrement=True),
  Column('id', String(36), primary_key=True),
  Column('name', String(255)),
  Column('exclusion_rule', String(255)),
  Column('customer_ids', String(255)),
  Column('date_range', Integer),
  Column('exclusion_level', Enum(enums.ExclusionLevelEnum)),
  Column('output', Enum(task.TaskOutput)),
  Column('from_days_ago', Integer),
  Column('placement_types', String(255)),
  Column('creation_date', DateTime),
  Column('status', Enum(task.TaskStatus)),
  Column('schedule', String(255)),
)

old_tasks = Table(
  'old_tasks',
  metadata,
  Column('_id', Integer, autoincrement=True),
  Column('customer_id', String(36)),
  Column('date_created', String(255)),
  Column('email_alerts', Boolean),
  Column('from_days_ago', String(36)),
  Column('gads_data_display', Boolean),
  Column('gads_data_youtube', Boolean),
  Column('gads_filter', String(255)),
  Column('include_youtube', Boolean),
  Column('lookback_days', String(36)),
  Column('schedule', String(36)),
  Column('task_id', String(36), primary_key=True),
  Column('task_name', String(255)),
  Column('yt_country_operator', String(255)),
  Column('yt_country_value', String(255)),
  Column('yt_language_operator', String(255)),
  Column('yt_language_value', String(255)),
  Column('yt_std_character', String(255)),
  Column('yt_subscriber_operator', String(255)),
  Column('yt_subscriber_value', String(255)),
  Column('yt_video_operator', String(255)),
  Column('yt_video_value', String(255)),
  Column('yt_view_operator', String(255)),
  Column('yt_view_value', String(255)),
)

executions = Table(
  'executions',
  metadata,
  Column('_id', Integer, autoincrement=True),
  Column('id', String(36), primary_key=True, nullable=False),
  Column('task', ForeignKey('tasks.id'), nullable=False),
  Column('start_time', DateTime, nullable=False),
  Column('end_time', DateTime, nullable=False),
  Column('type', Enum(execution.ExecutionTypeEnum)),
  Column('placements_excluded', Integer),
)

execution_details = Table(
  'execution_details',
  metadata,
  Column('_id', Integer, autoincrement=True),
  Column('id', String(36), primary_key=True, nullable=False),
  Column('execution_id', ForeignKey('executions.id'), nullable=False),
  Column('placement', String(255), nullable=False),
  Column('placement_type', String(255), nullable=False),
  Column('reason', String(255), nullable=False),
)

preview_task_and_results = Table(
  'preview_task_and_results',
  metadata,
  Column('_id', Integer, autoincrement=True),
  Column('id', String(36), primary_key=True, nullable=False),
  Column('status', Enum(preview_task.PreviewTaskStatus)),
  Column('creation_time', DateTime, nullable=False),
  Column('preview_command', Text, nullable=True),
  Column('results', Text, nullable=True),
)

allowlisted_placements = Table(
  'allowlisted_placements',
  metadata,
  Column('_id', Integer, autoincrement=True),
  Column('id', String(36), primary_key=True, nullable=False),
  Column('type', Enum(enums.PlacementTypeEnum)),
  Column('name', String(255), unique=True),
  Column('account_id', String(255)),
)

config = Table(
  'config',
  metadata,
  Column('_id', Integer, autoincrement=True),
  Column('id', String(36), primary_key=True, nullable=False),
  Column('mcc_id', String(10)),
  Column('always_fetch_youtube_preview_mode', Boolean),
  Column('save_to_db', Boolean),
  Column('email_address', String(50)),
)

customer_ids = Table(
  'customer_ids',
  metadata,
  Column('mcc_id', String(10), primary_key=True),
  Column('account_name', String(255)),
  Column('id', String(10), primary_key=True),
)

mcc_ids = Table(
  'mcc_ids',
  metadata,
  Column('id', String(10), primary_key=True),
  Column('account_name', String(255)),
)

website_info = Table(
  'external_parser.website_info',
  metadata,
  Column('_id', Integer, autoincrement=True),
  Column('id', String(36), primary_key=True, nullable=False),
  Column('placement', String(255)),
  Column('title', String(255), nullable=True),
  Column('description', String(1000), nullable=True),
  Column('keywords', String(1000), nullable=True),
  Column('last_processed_time', DateTime),
  Column('is_processed', Boolean),
)

youtube_channel_info = Table(
  'external_parser.youtube_channel_info',
  metadata,
  Column('_id', Integer, autoincrement=True),
  Column('id', String(36), primary_key=True, nullable=False),
  Column('placement', String(255)),
  Column('title', String(255), nullable=True),
  Column('country', String(255), nullable=True),
  Column('description', String(1000), nullable=True),
  Column('viewCount', Integer),
  Column('subscriberCount', Integer),
  Column('videoCount', Integer),
  Column('topicCategories', String(1000), nullable=True),
  Column('last_processed_time', DateTime),
  Column('is_processed', Boolean),
)

youtube_video_info = Table(
  'external_parser.youtube_video_info',
  metadata,
  Column('_id', Integer, autoincrement=True),
  Column('id', String(36), primary_key=True, nullable=False),
  Column('placement', String(255)),
  Column('title', String(255), nullable=True),
  Column('description', String(1000), nullable=True),
  Column('defaultLanguage', String(10), nullable=True),
  Column('defaultAudioLanguage', String(10), nullable=True),
  Column('commentCount', Integer),
  Column('favouriteCount', Integer),
  Column('likeCount', Integer),
  Column('viewCount', Integer),
  Column('madeForKids', Boolean),
  Column('tags', String(1000)),
  Column('topicCategories', String(1000)),
  Column('last_processed_time', DateTime),
  Column('is_processed', Boolean),
)


def start_mappers(engine):
  execution_details_mapper = mapper(
    execution.ExecutionDetails, execution_details
  )
  execution_mapper = mapper(
    execution.Execution,
    executions,
    properties={
      'details': relationship(execution_details_mapper, collection_class=list)
    },
  )
  mapper(
    task.Task,
    tasks,
    properties={
      'executions': relationship(execution_mapper, collection_class=list)
    },
  )
  mapper(task.OldTask, old_tasks)
  mapper(settings.Config, config)
  mapper(placement_entities.AllowlistedPlacement, allowlisted_placements)
  mapper(settings.MccIds, mcc_ids)
  mapper(settings.CustomerIds, customer_ids)
  mapper(website_parser.WebsiteInfo, website_info)
  mapper(youtube_data_parser.ChannelInfo, youtube_channel_info)
  mapper(youtube_data_parser.VideoInfo, youtube_video_info)
  mapper(preview_task.PreviewTaskAndResults, preview_task_and_results)
  if engine:
    metadata.create_all(engine)
