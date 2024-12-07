# Copyright 2024 Google LLC
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
"""Module for performing parsing of external entities.

External entity represents a YouTube Channel or Video, Webpage,
Mobile Application or anything that requires connection to external
(non Google Ads) system in order to get information from it.
"""

from __future__ import annotations

import dataclasses
import itertools
import logging

from gaarf import report

from googleads_housekeeper.adapters import repository
from googleads_housekeeper.domain import external_parsers
from googleads_housekeeper.domain.core import exclusion_specification
from googleads_housekeeper.services import unit_of_work

PARSER_MAPPING = {
  'youtube_channel_info': external_parsers.youtube_data_parser.ChannelInfoParser,
  'youtube_video_info': external_parsers.youtube_data_parser.VideoInfoParser,
  'website_info': external_parsers.website_parser.WebSiteParser,
}


@dataclasses.dataclass
class ParseOptions:
  """Specifies options regarding parsing behaviour.

  Attributes:
      save_to_db: Whether to save parsing results to DB.
      batch_size: Maximum number of entities in response.
  """

  save_to_db: bool = True
  batch_size: int = 50


class ExternalEntitiesParser:
  """Performance parsing of external entities (YouTube, Websites, etc.).

  Attributes:
      uow: Unit of work to handle transaction.
  """

  def __init__(self, uow: unit_of_work.AbstractUnitOfWork) -> None:
    """Initializes an instance of ExternalEntitiesParser.

    Args:
        uow: Unit of work to handle transaction.
    """
    self.uow = uow

  def parse_specification_chain(
    self,
    entities: report.GaarfReport,
    specification: exclusion_specification.ExclusionSpecification,
    parse_options: ParseOptions = ParseOptions(),
  ) -> None:
    """Performance parsing of entities via all parsers in specification.

    Args:
        entities:
            Report containing entities that should be parsed.
        specifications:
            All possible non Ads specifications. Entities within a report
            can be parsed via different parsers (YouTube, Website, etc.)
        parse_options:
            Options for performing parsing.
    """
    uow = self.uow
    with uow:
      for specification_entries in specification.specifications:
        for specification_entry in specification_entries:
          self._parse_via_external_parser(
            entities=entities,
            specification_entry=specification_entry,
            uow=uow,
            parse_options=parse_options,
          )

  def _parse_via_external_parser(
    self,
    entities: report.GaarfReport,
    specification_entry: exclusion_specification.BaseExclusionSpecificationEntry,
    uow: unit_of_work.AbstractUnitOfWork,
    parse_options: ParseOptions,
  ) -> None:
    """Performance parsing of entities via a single parser in specification.

    Args:
        entities:
            Report containing entities that should be parsed.
        specification:
            Single non Ads specifications. Entities will be parsed via
            a single parsers (YouTube, Website, etc.
        uow:
            Unit of work to handle transaction.
        parse_options:
            Options for performing parsing.
    """
    repo = getattr(uow, specification_entry.repository_name)
    parser = PARSER_MAPPING.get(specification_entry.repository_name)
    if not_parsed_entities := self._get_not_parsed_entities(
      entities, specification_entry, repo
    ):
      i = 0
      while batch := list(
        itertools.islice(not_parsed_entities, i, i + parse_options.batch_size)
      ):
        parsed_entities_info = parser().parse(batch)
        i += parse_options.batch_size
        if parse_options.save_to_db:
          for parsed_placement in parsed_entities_info:
            logging.debug('saving placement: %s to db', parsed_placement)
            repo.add(parsed_placement)
          uow.commit()

  def _get_not_parsed_entities(
    self,
    entities: report.GaarfReport,
    specification_entry: exclusion_specification.BaseExclusionSpecificationEntry,
    repo: repository.AbstractRepository,
  ) -> list[str]:
    """Get all entities not parsed and saved in DB.

    Args:
        entities:
            Report containing entities that should be parsed.
        specification_entry:
            Single non Ads specifications. Entities will be parsed via
            a single parsers (YouTube, Website, etc.).
        repo:
            Repository to get data from.

    Returns:
        Non-parsed placements.
    """
    not_parsed_entities: list[str] = []
    for entity_info in entities:
      if (
        entity_info.placement_type
        == specification_entry.corresponding_placement_type.name
      ):
        if not repo.get_by_conditions(
          {
            'placement': entity_info.placement,
          }
        ):
          not_parsed_entities.append(str(entity_info.placement))
    return not_parsed_entities
