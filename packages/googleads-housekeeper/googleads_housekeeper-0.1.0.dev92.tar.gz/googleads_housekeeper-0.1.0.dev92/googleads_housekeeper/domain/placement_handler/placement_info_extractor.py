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
"""Extracts extra info on placements from DB."""

from __future__ import annotations

import gaarf

from googleads_housekeeper.adapters import repository
from googleads_housekeeper.domain.external_parsers import base_parser
from googleads_housekeeper.services import unit_of_work


class PlacementInfoExtractor:
  """Responsible for getting parsed placement information from DB.

  Attributes:
      website_info: Repository containing parsed website data.
      youtube_channel_info: Repository containing parsed YouTube channel data.
      youtube_video_info: Repository containing parsed YouTube video data.
  """

  def __init__(self, uow: unit_of_work.AbstractUnitOfWork) -> None:
    """Creates PlacementInfoExtractor repositories.

    Args:
        uow: An instance of Unit of Work.
    """
    self.website_info = uow.website_info
    self.youtube_channel_info = uow.youtube_channel_info
    self.youtube_video_info = uow.youtube_video_info

  def extract_placement_info(
    self, placement_info: gaarf.report.GaarfRow
  ) -> dict[str, base_parser.EntityInfo]:
    """Fetches parsed information for a given placement.

    Args:
        placement_info:
            A row from report containing placement info from Google Ads.

    Returns:
        Mapping between placement parsed into type (i.e. 'website_info')
        and actual information fetched from DB.
    """
    if placement_info.placement_type == 'WEBSITE':
      return {
        'website_info': self._get_placement_from_repo(
          self.website_info, placement_info.placement
        )
      }
    if placement_info.placement_type == 'YOUTUBE_CHANNEL':
      return {
        'youtube_channel_info': self._get_placement_from_repo(
          self.youtube_channel_info, placement_info.placement
        )
      }

    if placement_info.placement_type == 'YOUTUBE_VIDEO':
      return {
        'youtube_video_info': self._get_placement_from_repo(
          self.youtube_video_info, placement_info.placement
        )
      }
    return {}

  def _get_placement_from_repo(
    self, repo: repository.AbstractRepository, placement: str
  ) -> base_parser.EntityInfo | dict:
    """Helper method for getting data from repository.

    Args:
        repository: Repository to get data from.
        placement: Placement identifier (website_url, channel_id, video_id).

    Returns:
        Parsed placement info.
    """
    if parsed_placement_info := repo.get_by_condition('placement', placement):
      return parsed_placement_info[0]
    return {}
