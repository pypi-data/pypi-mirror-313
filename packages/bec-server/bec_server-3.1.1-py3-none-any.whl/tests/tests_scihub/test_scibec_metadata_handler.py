from unittest import mock

import numpy as np
import pytest
from py_scibec_openapi_client.models import NewScanData, ScanPartial

from bec_lib import messages
from bec_lib.redis_connector import MessageObject
from bec_server.scihub.scibec.scibec_metadata_handler import SciBecMetadataHandler


@pytest.fixture
def md_handler():
    inst = SciBecMetadataHandler(mock.Mock())
    yield inst


def test_handle_scan_status(md_handler):
    # pylint: disable=protected-access
    msg = messages.ScanStatusMessage(scan_id="scan_id", status="open", info={})
    with mock.patch.object(md_handler, "update_scan_status") as mock_update_scan_status:
        md_handler._handle_scan_status(
            MessageObject(value=msg, topic="scan_status"), parent=md_handler
        )
        mock_update_scan_status.assert_called_once_with(msg)


def test_handle_scan_status_ignores_errors(md_handler):
    # pylint: disable=protected-access
    msg = messages.ScanStatusMessage(scan_id="scan_id", status="open", info={})
    with mock.patch("bec_server.scihub.scibec.scibec_metadata_handler.logger") as mock_logger:
        with mock.patch.object(md_handler, "update_scan_status") as mock_update_scan_status:
            mock_update_scan_status.side_effect = Exception("test")
            md_handler._handle_scan_status(
                MessageObject(value=msg, topic="scan_status"), parent=md_handler
            )
            mock_update_scan_status.assert_called_once_with(msg)
            mock_logger.exception.assert_called_once_with(
                f"Failed to update scan status: {Exception('test')}"
            )


def test_update_scan_status_returns_without_scibec(md_handler):
    # pylint: disable=protected-access
    msg = messages.ScanStatusMessage(scan_id="scan_id", status="open", info={})
    md_handler.scibec_connector.scibec = None
    md_handler.update_scan_status(msg)


def test_update_scan_status(md_handler, active_experiment, dataset_document):
    # pylint: disable=protected-access
    msg = messages.ScanStatusMessage(scan_id="scan_id", status="open", info={"dataset_number": 12})
    scibec = mock.Mock()
    md_handler.scibec_connector.scibec = scibec
    scibec_info = {"activeExperiment": active_experiment}
    md_handler.scibec_connector.scibec_info = scibec_info
    scibec.scan.scan_controller_find = mock.MagicMock(return_value=[])
    scibec.dataset.dataset_controller_find = mock.MagicMock(return_value=[])
    scibec.dataset.dataset_controller_create = mock.MagicMock(return_value=dataset_document)
    md_handler.update_scan_status(msg)


def test_update_scan_status_patch(md_handler, active_experiment, scan_document):
    # pylint: disable=protected-access
    msg = messages.ScanStatusMessage(
        scan_id="scan_id", status="closed", info={"dataset_number": 12}
    )
    scibec = mock.Mock()
    md_handler.scibec_connector.scibec = scibec
    scibec_info = {"activeExperiment": active_experiment}
    md_handler.scibec_connector.scibec_info = scibec_info
    scibec.scan.scan_controller_find = mock.MagicMock(return_value=[scan_document])
    md_handler.update_scan_status(msg)
    scibec.scan.scan_controller_update_by_id.assert_called_once_with(
        id="dummy_id",
        scan_partial=ScanPartial(exit_status="closed", metadata={"dataset_number": 12}),
    )


def test_handle_file_content(md_handler):
    # pylint: disable=protected-access
    msg = messages.FileContentMessage(file_path="my_file.h5", data={"data": {}}, scan_info={})
    msg_raw = MessageObject(value=msg, topic="file_content")
    with mock.patch.object(md_handler, "update_scan_data") as mock_update_scan_data:
        md_handler._handle_file_content(msg_raw, parent=md_handler)
        mock_update_scan_data.assert_called_once_with(**msg.content)


def test_handle_file_content_ignores_errors(md_handler):
    # pylint: disable=protected-access
    msg = messages.FileContentMessage(file_path="my_file.h5", data={"data": {}}, scan_info={})
    msg_raw = MessageObject(value=msg, topic="file_content")
    with mock.patch("bec_server.scihub.scibec.scibec_metadata_handler.logger") as mock_logger:
        with mock.patch.object(md_handler, "update_scan_data") as mock_update_scan_data:
            mock_update_scan_data.side_effect = Exception("test")
            md_handler._handle_file_content(msg_raw, parent=md_handler)
            mock_update_scan_data.assert_called_once_with(**msg.content)
            mock_logger.exception.assert_called_once_with(
                f"Failed to update scan data: {Exception('test')}"
            )


def test_update_scan_data_return_without_scibec(md_handler):
    # pylint: disable=protected-access
    md_handler.scibec_connector.scibec = None
    md_handler.update_scan_data(file_path="my_file.h5", data={"data": {}}, scan_info={})


def test_update_scan_data_without_scan(md_handler):
    # pylint: disable=protected-access
    scibec = mock.Mock()
    md_handler.scibec_connector.scibec = scibec
    scibec.scan.scan_controller_find = mock.MagicMock(return_value=[])
    md_handler.update_scan_data(
        file_path="my_file.h5", data={"data": {}}, scan_info={"bec": {"scan_id": "scan_id"}}
    )


def test_update_scan_data(md_handler, scan_document):
    # pylint: disable=protected-access
    scibec = mock.Mock()
    md_handler.scibec_connector.scibec = scibec
    scibec.scan.scan_controller_find = mock.MagicMock(return_value=[scan_document])
    md_handler.update_scan_data(
        file_path="my_file.h5", data={"data": {}}, scan_info={"bec": {"scan_id": "scan_id"}}
    )
    scibec.scan_data.scan_data_controller_create_many.assert_called_once_with(
        NewScanData(
            **{
                "readACL": ["readACL"],
                "writeACL": ["readACL"],
                "owner": ["owner"],
                "scanId": "dummy_id",
                "filePath": "my_file.h5",
                "data": {"data": {}},
                "scaninfo": {"bec": {"scan_id": "scan_id"}},
            }
        )
    )


def test_update_scan_data_exceeding_limit(md_handler, scan_document):
    # pylint: disable=protected-access
    scibec = mock.Mock()
    md_handler.MAX_DATA_SIZE = 1000
    md_handler.scibec_connector.scibec = scibec
    scibec.scan.scan_controller_find = mock.MagicMock(return_value=[scan_document])
    data_block = {f"key_{i}": {"signal": list(range(100))} for i in range(10)}
    md_handler.update_scan_data(
        file_path="my_file.h5", data=data_block, scan_info={"bec": {"scan_id": "scan_id"}}
    )
    num_calls = scibec.scan_data.scan_data_controller_create_many.call_count
    assert num_calls == 5


@pytest.mark.parametrize(
    "data, expected_result",
    [
        (
            {"int": 123, "float": 3.14, "str": "hello", "bool": True},
            {"int": 123, "float": 3.14, "str": "hello", "bool": True},
        ),
        (
            {"nested": {"int": 123, "float": 3.14, "str": "hello", "bool": True}},
            {"nested": {"int": 123, "float": 3.14, "str": "hello", "bool": True}},
        ),
        ([1, 2, 3, 4, 5], [1, 2, 3, 4, 5]),
        ((1, 2, 3, 4, 5), (1, 2, 3, 4, 5)),
        ({1, 2, 3, 4, 5}, {1, 2, 3, 4, 5}),
        (
            np.array([1, 2, 3, 4, 5]),
            '{"nd": true, "type": "<i8", "kind": "", "shape": [5], "data": [1, 2, 3, 4, 5]}',
        ),
        # Integer types
        ({"signal": np.int8(123)}, {"signal": 123}),
        ({"signal": np.int16(123)}, {"signal": 123}),
        ({"signal": np.int32(123)}, {"signal": 123}),
        ({"signal": np.int64(123)}, {"signal": 123}),
        ({"signal": np.uint8(123)}, {"signal": 123}),
        ({"signal": np.uint16(123)}, {"signal": 123}),
        ({"signal": np.uint32(123)}, {"signal": 123}),
        ({"signal": np.uint64(123)}, {"signal": 123}),
        # Float types
        ({"signal": np.float16(3.14)}, {"signal": np.float16(3.14).tolist()}),
        ({"signal": np.float32(3.14)}, {"signal": np.float32(3.14).tolist()}),
        ({"signal": np.float64(3.14)}, {"signal": np.float64(3.14).tolist()}),
        ({"signal": np.str_("hello")}, {"signal": "hello"}),
        ({"signal": np.bool_(True)}, {"signal": True}),
    ],
)
def test_serialize_special_data(md_handler, data, expected_result):
    # pylint: disable=protected-access
    assert md_handler.serialize_special_data(data) == expected_result
