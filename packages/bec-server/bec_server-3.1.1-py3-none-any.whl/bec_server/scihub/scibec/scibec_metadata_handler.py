from __future__ import annotations

import json
import time
from typing import TYPE_CHECKING, Any

import numpy as np
import py_scibec
import py_scibec_openapi_client.models as py_scibec_models

from bec_lib.endpoints import MessageEndpoints
from bec_lib.logger import bec_logger
from bec_lib.serialization import json_ext

logger = bec_logger.logger

if TYPE_CHECKING:
    from bec_lib import messages
    from bec_server.scihub.scibec import SciBecConnector


class SciBecMetadataHandler:
    """
    The SciBecMetadataHandler class is responsible for handling metadata sent to SciBec.
    """

    MAX_DATA_SIZE = 1e6  # max data size for the backend; currently set to 1 MB

    def __init__(self, scibec_connector: SciBecConnector) -> None:
        self.scibec_connector = scibec_connector
        self._scan_status_register = None
        self._start_scan_subscription()
        self._file_subscription = None
        self._start_file_subscription()

    def _start_scan_subscription(self):
        self._scan_status_register = self.scibec_connector.connector.register(
            MessageEndpoints.scan_status(), cb=self._handle_scan_status, parent=self
        )

    def _start_file_subscription(self):
        self._file_subscription = self.scibec_connector.connector.register(
            MessageEndpoints.file_content(), cb=self._handle_file_content, parent=self
        )

    @staticmethod
    def _handle_scan_status(msg, *, parent, **_kwargs) -> None:
        msg = msg.value
        try:
            scan = parent.update_scan_status(msg)
        except Exception as exc:
            logger.exception(f"Failed to update scan status: {exc}")
            logger.warning("Failed to write to SciBec")
            return

        # if msg.content["status"] != "open":
        #     parent.update_event_data(scan)

    def update_scan_status(self, msg: messages.ScanStatusMessage) -> dict:
        """
        Update the scan status in SciBec

        Args:
            msg(messages.ScanStatusMessage): The message containing the scan data

        Returns:
            dict: The updated scan data
        """
        scibec = self.scibec_connector.scibec
        if not scibec:
            return
        scibec_info = self.scibec_connector.scibec_info
        experiment_id = scibec_info["activeExperiment"].id
        # session_id = scibec_info["activeSession"][0]["id"]
        # experiment_id = scibec_info["activeSession"][0]["experimentId"]
        logger.debug(f"Received new scan status {msg}")
        scan_filter = py_scibec.bec.ScanFilterWhere(where={"scanId": msg.content["scan_id"]})
        scan = scibec.scan.scan_controller_find(scan_filter)
        if not scan:
            info = msg.content["info"]
            dataset_number = info.get("dataset_number")
            dataset_filter = py_scibec.bec.DatasetFilterWhere(
                where={"number": dataset_number, "experimentId": experiment_id}
            )
            dataset = scibec.dataset.dataset_controller_find(dataset_filter)
            if dataset:
                dataset = dataset[0]
            else:
                new_dataset = py_scibec.bec.NewDataset(
                    **{
                        "readACL": scibec_info["activeExperiment"].read_acl,
                        "writeACL": scibec_info["activeExperiment"].read_acl,
                        "owner": scibec_info["activeExperiment"].owner,
                        "number": dataset_number,
                        "experimentId": experiment_id,
                        "name": info.get("dataset_name", ""),
                    }
                )
                dataset = scibec.dataset.dataset_controller_create(new_dataset)

            new_scan = py_scibec.bec.NewScan(
                **{
                    "readACL": scibec_info["activeExperiment"].read_acl,
                    "writeACL": scibec_info["activeExperiment"].read_acl,
                    "owner": scibec_info["activeExperiment"].owner,
                    "scanType": info.get("scan_name", ""),
                    "scanId": info.get("scan_id", ""),
                    "queueId": info.get("queue_id", ""),
                    "requestId": info.get("RID", ""),
                    "exitStatus": msg.content["status"],
                    # "queue": info.get("stream", ""),
                    "metadata": info,
                    # "sessionId": session_id,
                    "experimentId": experiment_id,
                    "datasetId": dataset.id,
                    "scanNumber": info.get("scan_number", 0),
                }
            )
            scan = scibec.scan.scan_controller_create(new_scan)
            # scan = scibec.add_scan(scan_data)
        else:
            info = msg.content["info"]
            scan = scibec.scan.scan_controller_update_by_id(
                id=scan[0].id,
                scan_partial=py_scibec.bec.ScanPartial(
                    metadata=info, exitStatus=msg.content["status"]
                ),
            )
        return scan

    @staticmethod
    def _handle_file_content(msg, *, parent, **_kwargs) -> None:
        msg = msg.value
        try:
            logger.debug(f"Received new file content {msg}")
            if not msg.content["data"]:
                return
            parent.update_scan_data(**msg.content)
        except Exception as exc:
            logger.exception(f"Failed to update scan data: {exc}")
            logger.warning("Failed to write to SciBec")
            return

    def serialize_special_data(self, data: Any) -> dict:
        """
        Serialize special data in the scan data.
        This method is recursively called for each key in the data dictionary and
        checks if the data is serializable. If not, the data is serialized using
        the json_ext.dumps method.

        Args:
            data(dict): The scan data

        Returns:
            dict: The serialized scan data
        """
        if isinstance(data, (int, float, str, bool)):
            return data
        if isinstance(data, dict):
            return {key: self.serialize_special_data(value) for key, value in data.items()}
        if isinstance(data, list):
            return [self.serialize_special_data(item) for item in data]
        if isinstance(data, tuple):
            return tuple(self.serialize_special_data(item) for item in data)
        if isinstance(data, set):
            return {self.serialize_special_data(item) for item in data}
        if isinstance(data, np.generic):
            return self.serialize_special_data(data.tolist())
        return json_ext.dumps(data)

    def update_scan_data(self, file_path: str, data: dict, scan_info: dict):
        """
        Update the scan data in SciBec

        Args:
            file_path(str): The path to the original NeXuS file
            data(dict): The scan data
            scan_info(dict): The scan information
        """
        scibec = self.scibec_connector.scibec
        if not scibec:
            return
        scan_filter = py_scibec.bec.ScanFilterWhere(where={"scanId": scan_info["bec"]["scan_id"]})
        scan = scibec.scan.scan_controller_find(scan_filter)
        if not scan:
            logger.warning(
                f"Could not find scan with scan_id {scan_info['bec']['scan_id']}. Cannot write scan"
                " data to SciBec."
            )
            return
        scan = scan[0]
        data_bec = self.serialize_special_data(data)
        data_size = len(json.dumps(data_bec)) / self.MAX_DATA_SIZE

        start = time.time()
        logger.info(f"Data size: {data_size} MB")
        if data_size > 1:
            logger.info(
                f"Data size is larger than {self.MAX_DATA_SIZE/1e6} MB. Splitting data into chunks."
            )
            self._write_scan_data_chunks(file_path, data_bec, scan)
        else:
            new_scan_data = py_scibec.bec.NewScanData(
                **{
                    "readACL": scan.read_acl,
                    "writeACL": scan.read_acl,
                    "owner": scan.owner,
                    "scanId": scan.id,
                    "filePath": file_path,
                    "data": data_bec,
                }
            )
            scibec.scan_data.scan_data_controller_create_many(new_scan_data)
        logger.info(
            f"Wrote scan data to SciBec for scan_id {scan_info['bec']['scan_id']} in {time.time() - start} seconds."
        )

    def _write_scan_data_chunks(
        self, file_path: str, data_bec: dict, scan: py_scibec_models.ScanWithRelations
    ):
        """
        Write the scan data to SciBec in chunks. This method is called if the scan data is larger
        than 1 MB. The method loops through all keys in the data dictionary and creates chunks of
        max 1 MB size. The chunks are then written to SciBec.

        Args:
            file_path(str): The path to the original NeXuS file
            data_bec(dict): The serialized scan data
            scan(dict): The scan data
        """
        scibec = self.scibec_connector.scibec
        if not scibec:
            return
        chunk = {}
        for key, value in data_bec.items():
            if len(json.dumps({key: value})) > self.MAX_DATA_SIZE:
                logger.warning(
                    f"Data size of key {key} is larger than {self.MAX_DATA_SIZE/1e6} MB. Cannot write this key to SciBec."
                )
                continue
            if len(json.dumps(chunk)) + len(json.dumps({key: value})) > self.MAX_DATA_SIZE:
                new_scan_data = py_scibec.bec.NewScanData(
                    **{
                        "readACL": scan.read_acl,
                        "writeACL": scan.read_acl,
                        "owner": scan.owner,
                        "scanId": scan.id,
                        "filePath": file_path,
                        "data": chunk,
                    }
                )
                scibec.scan_data.scan_data_controller_create_many(new_scan_data)
                chunk = {}
            chunk[key] = value

        # Write the last chunk
        if chunk:
            new_scan_data = py_scibec.bec.NewScanData(
                **{
                    "readACL": scan.read_acl,
                    "writeACL": scan.read_acl,
                    "owner": scan.owner,
                    "scanId": scan.id,
                    "filePath": file_path,
                    "data": chunk,
                }
            )
            scibec.scan_data.scan_data_controller_create_many(new_scan_data)

    def shutdown(self):
        """
        Shutdown the metadata handler
        """
        if self._scan_status_register:
            self._scan_status_register.shutdown()
        if self._file_subscription:
            self._file_subscription.shutdown()
