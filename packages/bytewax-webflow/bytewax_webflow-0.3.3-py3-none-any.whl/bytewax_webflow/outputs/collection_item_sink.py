from logging import getLogger
from typing import Sequence

from bytewax.outputs import (
    StatelessSinkPartition,
    DynamicSink,
)

from ..webflow_client import WebflowClient
from ..types import CollectionItem, CollectionField


logger = getLogger(__name__)


class CollectionItemSinkPartition(StatelessSinkPartition[CollectionItem]):
    def __init__(
        self,
        client: WebflowClient,
        collection_id: str,
        is_publishing: bool = False,
    ):
        self._client = client
        self._collection_id = collection_id
        self._is_publishing = is_publishing

    @staticmethod
    def _is_valid(schema: Sequence[CollectionField], value: CollectionItem):
        valid_fields = set(
            [f.slug for f in schema if f.is_editable and f.slug not in ["slug", "name"]]
        )
        required_fields = set(
            [f.slug for f in schema if f.is_required and f.slug not in ["slug", "name"]]
        )

        value_fields = set(value.fields.keys())

        if (
            not value.is_draft
            and len(required_fields) > 0
            and not required_fields <= value_fields
        ):
            logger.warning(
                f"Item with slug {value.slug} missing required fields: {", ".join(required_fields.difference(value_fields))}"
            )
            return False

        if not value_fields <= valid_fields:
            logger.warning(
                f"Item with slug {value.slug} has invalid fields: {", ".join(value_fields.difference(valid_fields))}"
            )
            return False

        return True

    def write_batch(self, items: Sequence[CollectionItem]) -> None:
        if len(items) == 0:
            return

        schema = self._client.get_collection_schema(self._collection_id)

        inserts: list[CollectionItem] = []
        updates: list[CollectionItem] = []

        for item in items:
            if not self._is_valid(schema, item):
                continue

            existing_item = self._client.get_item_by_slug(
                self._collection_id, item.slug
            )

            if existing_item is not None:
                existing_item.is_archived = item.is_archived
                existing_item.is_draft = item.is_draft
                existing_item.name = item.name

                # Update only set values
                for key, value in item.fields.items():
                    existing_item.fields[key] = value

                item = existing_item

            if item.id is not None:
                updates.append(item)
            else:
                inserts.append(item)

        touched_items = []

        if len(inserts) > 0:
            logger.info(f"Inserted {len(inserts)} collection items")

            touched_items += self._client.insert_collection_items(
                self._collection_id, inserts
            )

        if len(updates) > 0:
            logger.info(f"Updated {len(updates)} collection items")

            touched_items += self._client.update_collection_items(
                self._collection_id, updates
            )

        if self._is_publishing and len(touched_items) > 0:
            # Only publish collection items that aren't draft - the publish
            # endpoint will change the state of draft items to published
            # even if it's not what we want
            publish_items = [item for item in touched_items if not item.is_draft]
            self._client.publish_collection_items(self._collection_id, publish_items)

            # And un-publish items that should be draft now
            draft_items = [item for item in touched_items if item.is_draft]
            for item in draft_items:
                self._client.unpublish_collection_item(self._collection_id, item)


class CollectionItemSink(DynamicSink[CollectionItem]):
    """Fixed partitioned sink for writing data to a Webflow Collection."""

    def __init__(
        self,
        access_token: str,
        collection_id: str,
        is_publishing: bool = False,
        base_url: str | None = None,
    ) -> None:
        """Initialize the WebflowCollectionSink."""
        self._access_token = access_token
        self._collection_id = collection_id
        self._is_publishing = is_publishing
        self._base_url = base_url

    def build(
        self,
        step_id: str,
        worker_index: int,
        worker_count: int,
    ) -> CollectionItemSinkPartition:
        """Build or resume a partition."""
        if worker_count != 1:
            raise ValueError("only supports 1 worker")

        client = WebflowClient(
            access_token=self._access_token,
            base_url=self._base_url,
        )

        return CollectionItemSinkPartition(
            client=client,
            collection_id=self._collection_id,
            is_publishing=self._is_publishing,
        )


__all__ = ("CollectionItemSinkPartition", "CollectionItemSink")
