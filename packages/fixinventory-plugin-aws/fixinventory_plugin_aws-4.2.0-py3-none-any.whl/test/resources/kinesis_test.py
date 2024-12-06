from fix_plugin_aws.resource.kinesis import AwsKinesisStream
from fix_plugin_aws.aws_client import AwsClient
from fixlib.graph import Graph
from test.resources import round_trip_for
from typing import Any, cast
from types import SimpleNamespace


def test_kinesis_stream() -> None:
    res, builder = round_trip_for(AwsKinesisStream, "kinesis_policy")
    assert len(builder.resources_of(AwsKinesisStream)) == 1
    assert len(res.tags) == 1


def test_tagging() -> None:
    stream, _ = round_trip_for(AwsKinesisStream, "kinesis_policy")

    def validate_update_args(**kwargs: Any) -> None:
        assert kwargs["action"] == "add-tags-to-stream"
        assert kwargs["StreamName"] == stream.name
        assert kwargs["Tags"] == {"foo": "bar"}

    def validate_delete_args(**kwargs: Any) -> None:
        assert kwargs["action"] == "remove-tags-from-stream"
        assert kwargs["StreamName"] == stream.name
        assert kwargs["TagKeys"] == ["foo"]

    client = cast(AwsClient, SimpleNamespace(call=validate_update_args))
    stream.update_resource_tag(client, "foo", "bar")

    client = cast(AwsClient, SimpleNamespace(call=validate_delete_args))
    stream.delete_resource_tag(client, "foo")


def test_deletion() -> None:
    stream, _ = round_trip_for(AwsKinesisStream, "kinesis_policy")

    def validate_delete_args(**kwargs: Any) -> None:
        assert kwargs["action"] == "delete-stream"
        assert kwargs["StreamName"] == stream.name

    client = cast(AwsClient, SimpleNamespace(call=validate_delete_args))
    stream.delete_resource(client, Graph())
