import pytest
from pytest_mock import MockType, MockerFixture

from bytewax_webflow.outputs.collection_item_sink import (
    WebflowCollectionItemSinkPartition,
)
from bytewax_webflow.types import WebflowCollectionItem, WebflowCollectionField
from bytewax_webflow.webflow_client import WebflowClient


class TestWebflowCollectionItemSinkPartition:
    @pytest.fixture
    def mock_client(self, mocker: MockerFixture):
        mock = mocker.create_autospec(spec=WebflowClient)

        mock.get_item_by_slug.return_value = None

        mock.get_collection_schema.return_value = [
            WebflowCollectionField(
                slug="example",
                is_required=False,
                is_editable=True,
            ),
            WebflowCollectionField(
                slug="example-two",
                is_required=True,
                is_editable=True,
            ),
            WebflowCollectionField(
                slug="example-three",
                is_required=False,
                is_editable=False,
            ),
        ]

        yield mock

    def test_inserts_valid_records_no_slug(self, mock_client: MockType):
        partition = WebflowCollectionItemSinkPartition(
            mock_client, "example-collection"
        )

        input_item = WebflowCollectionItem(
            name="Example",
            slug="example",
            fields={
                "example": "Accepted field",
                "example-two": "Required Field",
            },
        )

        partition.write_batch([input_item])

        mock_client.insert_collection_items.assert_called_with(
            "example-collection", [input_item]
        )
        mock_client.update_collection_items.assert_not_called()

    def test_updates_records_with_id(self, mock_client: MockType):
        partition = WebflowCollectionItemSinkPartition(
            mock_client, "example-collection"
        )

        input_item = WebflowCollectionItem(
            id="example-id",
            name="Example",
            slug="example",
            fields={
                "example": "Accepted field",
                "example-two": "Required Field",
            },
        )

        partition.write_batch([input_item])

        mock_client.insert_collection_items.assert_not_called()
        mock_client.update_collection_items.assert_called_with(
            "example-collection", [input_item]
        )

    def test_updates_records_when_slug_overlaps(self, mock_client: MockType):
        partition = WebflowCollectionItemSinkPartition(
            mock_client, "example-collection"
        )

        from_slug_item = WebflowCollectionItem(
            id="example-id",
            name="Example",
            slug="example",
            fields={
                "example": "Accepted field",
                "example-two": "Required Field",
            },
        )

        input_item = WebflowCollectionItem(
            name="Example",
            slug="example",
            fields={
                "example": "Overridden data",
                "example-two": "Required Field",
            },
        )

        expected = WebflowCollectionItem(
            id="example-id",
            name="Example",
            slug="example",
            fields={
                "example": "Overridden data",
                "example-two": "Required Field",
            },
        )

        mock_client.get_item_by_slug.return_value = from_slug_item

        partition.write_batch([input_item])

        mock_client.insert_collection_items.assert_not_called()
        mock_client.update_collection_items.assert_called_with(
            "example-collection", [expected]
        )

    def test_ignores_records_with_invalid_keys(self, mock_client: MockType):
        partition = WebflowCollectionItemSinkPartition(
            mock_client, "example-collection"
        )

        input_item = WebflowCollectionItem(
            name="Example",
            slug="example",
            fields={
                "example": "Accepted field",
                "example-two": "Required Field",
                "invalid": "Invalid field",
            },
        )

        partition.write_batch([input_item])

        mock_client.insert_collection_items.assert_not_called()
        mock_client.update_collection_items.assert_not_called()

    def test_ignores_records_with_missing_required_keys(self, mock_client: MockType):
        partition = WebflowCollectionItemSinkPartition(
            mock_client, "example-collection"
        )

        input_item = WebflowCollectionItem(
            name="Example",
            slug="example",
            fields={
                "example": "Accepted field",
            },
        )

        partition.write_batch([input_item])

        mock_client.insert_collection_items.assert_not_called()
        mock_client.update_collection_items.assert_not_called()

    def test_ignores_records_with_uneditable_keys(self, mock_client: MockType):
        partition = WebflowCollectionItemSinkPartition(
            mock_client, "example-collection"
        )

        input_item = WebflowCollectionItem(
            name="Example",
            slug="example",
            fields={
                "example": "Accepted field",
                "example-two": "Required Field",
                "example-three": "Uneditable Field",
            },
        )

        partition.write_batch([input_item])

        mock_client.insert_collection_items.assert_not_called()
        mock_client.update_collection_items.assert_not_called()
