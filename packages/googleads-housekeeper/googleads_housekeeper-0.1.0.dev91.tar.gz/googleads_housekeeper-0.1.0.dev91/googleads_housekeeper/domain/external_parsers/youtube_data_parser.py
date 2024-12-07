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
"""Module for extracting meta data about YouTube channels and videos."""

from __future__ import annotations

import collections
import dataclasses
import os
from typing import Any, Literal

from googleapiclient.discovery import build

from googleads_housekeeper.domain.external_parsers import base_parser


class YouTubeDataConnector:
  """Specifies connections to YouTube.

  Attributes:
      service: Build YouTube service.
  """

  def __init__(
    self,
    api_version: str = 'v3',
    developer_key: str = os.getenv('YOUTUBE_DATA_API_KEY'),
  ):
    """Initializes YouTubeDataConnector.

    Args:
        api_version: Version of YouTube Data API.
        developer_key: API key to access YouTube Data API.

    Returns:
        Description of return.
    """
    self.service = build('youtube', api_version, developerKey=developer_key)

  def get_response(
    self,
    type_: Literal['videos', 'channels'],
    elements: str,
    placements: collections.abc.Sequence[str],
  ):
    """Gets API response for a correct type.

    Args:
        type_: Service type.
        elements: Elements to return in response.
        placements: Identifiers for videos/channels.

    Returns:
        Description of return.
    """
    if type_ == 'videos':
      service = self.service.videos()
    elif type_ == 'channels':
      service = self.service.channels()
    else:
      raise ValueError(f'Unsupported resource {type_}')
    return service.list(part=elements, id=placements).execute()


@dataclasses.dataclass
class ChannelInfo(base_parser.EntityInfo):
  """Contains meta information of YouTube Channel.

  Attributes:
      placement: Id of YouTube channel.
      title: Title of the channel.
      description: Channel description.
      viewCount: Number of channel views.
      subscriberCount: Number of channel subscribers.
      videoCount: Number of videos on the channel.
      topicCategories: Categories associated with the channel.
      is_processed: Whether YouTube channel was successfully parsed.
  """

  placement: str
  title: str | None = None
  description: str | None = None
  country: str | None = None
  viewCount: int = 0
  subscriberCount: int = 0
  videoCount: int = 0
  topicCategories: str = ''
  is_processed: bool = True


@dataclasses.dataclass
class VideoInfo(base_parser.EntityInfo):
  """Contains meta information of YouTube Video.

  Attributes:
      placement: Id of YouTube video.
      title: Title of the video.
      description: Channel description.
      defaultLanguage: Language of the video.
      defaultAudioLanguage: Audio language of the video.
      commentCount: Number of video comments.
      favouriteCount: Number of times video is added to favorites.
      likeCount: Number of video likes.
      viewCount: Number of videos views.
      madeForKids: Whether is the video is made for kids.
      tags: Tags associated with the video.
      topicCategories: Categories associated with the video.
      is_processed: Whether YouTube video was successfully parsed.
  """

  placement: str
  title: str | None = None
  description: str | None = None
  defaultLanguage: str | None = None
  defaultAudioLanguage: str | None = None
  commentCount: int = 0
  favouriteCount: int = 0
  likeCount: int = 0
  viewCount: int = 0
  madeForKids: bool = False
  tags: str = ''
  topicCategories: str = ''
  is_processed: bool = True


class ChannelInfoParser(base_parser.BaseParser):
  """Performs YouTube channel parsing."""

  def __init__(
    self, data_connector: type[YouTubeDataConnector] = YouTubeDataConnector
  ):
    """Initializes ChannelInfoParser.

    Args:
        data_connector: Connector to get data from YouTube.
    """
    self.data_connector = data_connector

  def parse(
    self, placements: collections.abc.Sequence[str]
  ) -> list[ChannelInfo]:
    """Parses provided YouTube channels.

    Args:
        placements: Sequence of YouTube channel ids.

    Returns:
        Parsed information in ChannelInfo format.
    """
    response = self.data_connector().get_response(
      'channels', 'id,snippet,statistics,topicDetails', placements
    )
    if not (items := response.get('items')):
      return [
        ChannelInfo(placement=channel_id, is_processed=False)
        for channel_id in placements
      ]
    results: list[ChannelInfo] = []
    for item in items:
      if snippet := item.get('snippet'):
        title = snippet.get('title')
        description = snippet.get('description')
        country = snippet.get('country')
      else:
        title = None
        description = None
        country = None
      if statistics := item.get('statistics'):
        subscriberCount = safe_cast(int, statistics.get('subscriberCount'))
        viewCount = safe_cast(int, statistics.get('viewCount'))
        videoCount = safe_cast(int, statistics.get('videoCount'))
      else:
        subscriberCount = 0
        viewCount = 0
        videoCount = 0
      topics = parse_topic_details(item.get('topicDetails'))
      results.append(
        ChannelInfo(
          placement=item.get('id'),
          title=title,
          description=description,
          country=country,
          viewCount=viewCount,
          subscriberCount=subscriberCount,
          videoCount=videoCount,
          topicCategories=topics,
        )
      )
    return results


class VideoInfoParser(base_parser.BaseParser):
  """Performs YouTube video parsing."""

  def __init__(
    self, data_connector: type[YouTubeDataConnector] = YouTubeDataConnector
  ):
    """Initializes VideoInfoParser.

    Args:
        data_connector: Connector to get data from YouTube.
    """
    self.data_connector = data_connector

  def parse(self, placements: collections.abc.Sequence[str]) -> list[VideoInfo]:
    """Parses provided YouTube videos.

    Args:
        placements: Sequence of YouTube video ids.

    Returns:
        Parsed information in VideoInfo format.
    """
    response = self.data_connector().get_response(
      'videos',
      'id,status,snippet,statistics,contentDetails,topicDetails',
      placements,
    )
    if not (items := response.get('items')):
      return [
        VideoInfo(placement=video_id, is_processed=False)
        for video_id in placements
      ]
    results: list[VideoInfo] = []
    for item in items:
      if snippet := item.get('snippet'):
        title = snippet.get('title')
        description = snippet.get('description')
        defaultLanguage = snippet.get('defaultLanguage')
        defaultAudioLanguage = snippet.get('defaultAudioLanguage')
        tags = snippet.get('tags')
      else:
        title = None
        description = None
        defaultLanguage = None
        defaultAudioLanguage = None
        tags = ''
      if statistics := item.get('statistics'):
        commentCount = safe_cast(int, statistics.get('commentCount'))
        favouriteCount = safe_cast(int, statistics.get('favouriteCount'))
        likeCount = safe_cast(int, statistics.get('likeCount'))
        viewCount = safe_cast(int, statistics.get('viewCount'))
      else:
        commentCount = 0
        favouriteCount = 0
        likeCount = 0
        viewCount = 0
      if status := item.get('status'):
        madeForKids = safe_cast(bool, status.get('madeForKids'))
      else:
        madeForKids = False
      topics = parse_topic_details(item.get('topicDetails'))
      if tags:
        tags = ','.join(tags)
      results.append(
        VideoInfo(
          placement=item.get('id'),
          title=title,
          description=description,
          defaultLanguage=defaultLanguage,
          defaultAudioLanguage=defaultAudioLanguage,
          commentCount=commentCount,
          favouriteCount=favouriteCount,
          likeCount=likeCount,
          viewCount=viewCount,
          madeForKids=madeForKids,
          tags=tags,
          topicCategories=topics,
        )
      )
    return results


def parse_topic_details(
  topic_details: collections.abc.Mapping[str, Any] | None,
) -> str:
  """Converts Wikipedia URLs to topic names."""
  if not topic_details:
    return ''
  if not (topic_categories := topic_details.get('topicCategories')):
    return ''
  return ','.join(list({topic.split('/')[-1] for topic in topic_categories}))


def safe_cast(callable_, value: str | None):
  if value:
    return callable_(value)
  return callable_()
