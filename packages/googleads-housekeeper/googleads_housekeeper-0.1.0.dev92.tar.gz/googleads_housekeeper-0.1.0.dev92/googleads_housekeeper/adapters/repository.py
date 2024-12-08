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
# pylint: disable=C0330, g-bad-import-order, protected-access
from __future__ import annotations

import abc
from dataclasses import asdict
from typing import Any, Generic, TypeVar

from google.cloud.firestore_v1.base_query import FieldFilter

from googleads_housekeeper.domain.core import task

T = TypeVar('T')


class AbstractRepository(abc.ABC, Generic[T]):
  """An Abstract Repository."""

  def __init__(self):
    self.seen: set[T] = set()

  def add(self, entity: T) -> None:
    """Adds an entity to the repository."""
    self._add(entity)

  def delete(self, entity_id: str) -> None:
    """Deletes an entity by its ID."""
    self._delete(entity_id)

  def get(self, entity_id: str) -> T:
    """Retrieves an entity by its ID."""
    return self._get(entity_id)

  def get_by_conditions(self, conditions: dict[str, Any]) -> T:
    """Retrieves an entity based on specific conditions."""
    return self._get_by_conditions(conditions)

  def get_by_condition(self, condition_name: str, condition_value: str) -> T:
    """Retrieves an entity based on specific conditions."""
    return self._get_by_conditions({condition_name: condition_value})

  def list(self) -> list[T]:
    """Retrieves all entities as a list."""
    return self._list()

  def update(self, entity_id: str, update_dict: dict[str, str]) -> T:
    return self._update(entity_id, update_dict)

  @abc.abstractmethod
  def _add(self, entity: T): ...

  @abc.abstractmethod
  def _get(self, entity_id) -> T: ...

  @abc.abstractmethod
  def _get_by_conditions(self, conditions: dict[str, Any]) -> T: ...

  @abc.abstractmethod
  def _list(self) -> list[T]: ...

  @abc.abstractmethod
  def list_with_creation_time_paginated(
    self, limit=20, offset=0
  ) -> (list)[T]: ...

  @abc.abstractmethod
  def _update(self, entity_id, update_dict) -> None: ...

  @abc.abstractmethod
  def _delete(self, entity_id) -> None: ...


class SqlAlchemyRepository(AbstractRepository[T]):
  """An Sql Alchemy Repository."""

  def __init__(self, session, entity=task.Task):
    super().__init__()
    self.session = session
    self.entity = entity

  def _add(self, entity) -> None:
    self.session.add(entity)

  def _get(self, entity_id) -> T:
    return self.session.query(self.entity).filter_by(id=entity_id).first()

  def _get_by_conditions(self, conditions: dict[str, Any]) -> list[T]:
    query = self.session.query(self.entity)
    for condition_name, condition_value in conditions.items():
      query = query.filter(
        getattr(self.entity, condition_name) == condition_value
      )
    return query.all()

  def _list(self) -> list[T]:
    return self.session.query(self.entity).all()

  def list_with_creation_time_paginated(self, limit=20, offset=0) -> list[T]:
    """Returns a paginated list of entities, ordered by creation time.

    Args:
      limit: The maximum number of entities to retrieve.
      offset: The number of entities to skip before starting retrieval.
    """
    return (
      self.session.query(self.entity)
      .order_by(self.entity.creation_time.desc())
      .offset(offset)
      .limit(limit)
      .all()
    )

  def _update(self, entity_id, update_dict) -> T:
    return (
      self.session.query(self.entity)
      .filter_by(id=entity_id)
      .update(update_dict)
    )

  def _delete(self, entity_id) -> T:
    return self.session.query(self.entity).filter_by(id=entity_id).delete()


class FirestoreRepository(AbstractRepository[T]):
  """A Firestore Repository Repository."""

  def __init__(self, client, entity=T):
    super().__init__()
    self.client = client
    self.entity = entity
    self.collection_name = entity.__name__

  def _add(self, entity) -> None:
    if hasattr(entity, 'id'):
      element_id = entity.id
    else:
      element_id = entity._id
    element_dict = {}
    for key, value in asdict(entity).items():
      if hasattr(value, 'name'):
        value = value.name
      element_dict[key] = value
    self.client.collection(self.collection_name).document(str(element_id)).set(
      element_dict
    )

  def _get(self, entity_id: str) -> T:
    doc = self.client.collection(self.collection_name).document(entity_id).get()
    if doc.exists:
      return self.entity(**doc.to_dict())
    return None

  def _get_by_conditions(self, conditions: dict[str, Any]) -> list[T]:
    try:
      query = self.client.collection(self.collection_name)
      for condition_name, condition_value in conditions.items():
        query = query.where(
          filter=FieldFilter(condition_name, '==', condition_value)
        )
      results = [self.entity(**result.to_dict()) for result in query.stream()]
      return results
    except Exception:
      return []

  def _list(self):
    results = self.client.collection(self.collection_name).stream()
    entities = [self.entity(**result.to_dict()) for result in results]
    return entities

  def list_with_creation_time_paginated(self, limit=20, offset=0) -> (list)[T]:
    """Returns a paginated list of entities, ordered by creation time.

    Args:
      limit: The maximum number of entities to retrieve.
       offset: The number of entities to skip before starting retrieval.
    """
    results = (
      self.client.collection(self.collection_name)
      .order_by('creation_time', direction='DESCENDING')
      .offset(offset)
    )
    if limit is not None:
      results = results.limit(limit)
    entities = [self.entity(**result.to_dict()) for result in results.stream()]
    return entities

  def _update(self, entity_id: str, update_dict: dict[str, Any]) -> None:
    if doc := self.client.collection(self.collection_name).document(entity_id):
      doc.update(update_dict)

  def _delete(self, entity_id: str) -> None:
    self.client.collection(self.collection_name).document(entity_id).delete()
