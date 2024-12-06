from datetime import datetime, timezone
from enum import Enum
from json import JSONDecodeError

import click
import requests
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.writers.colorizer import Colorizer as CL


class Status(Enum):
    EXISTING = "existing"
    NEW = "new"
    REMOVED = "removed"
    ERROR = "error"
    WARNING = "warning"
    EXPIRED = "expired"
    _PENDING = "_pending"


class BkMlAdInfoStore:
    def __init__(self, manifest_handler) -> None:
        self.manifest_handler = manifest_handler
        self.adpods = {}

    def retrieve(self):
        self.reset_statuses()

        # Check that it's a valid URL
        if "bpkio_sessionid" not in self.manifest_handler.url:
            return self

        bkml_url = self.manifest_handler.url + "&bk-ml=1.0"

        response = requests.get(
            bkml_url,
            headers=self.manifest_handler.headers,
            verify=self.manifest_handler.verify_ssl,
        )
        if response.status_code == 200:
            try:
                payload = response.json()
                self.merge_adpods(payload["adpods"])
            except JSONDecodeError:
                pass

        return self

    def reset_statuses(self):
        for adpod in self.adpods.values():
            for ad in adpod.values():
                ad["_status"] = Status.REMOVED

    def merge_adpods(self, adpods):
        # merge the new information
        for adpod in adpods:
            podid = adpod["id"]
            if podid not in self.adpods:
                self.adpods[podid] = {}

            for ad in adpod["ads"]:
                uid = f"{ad['adid']}-{ad['starttime_ms']}"
                if uid in self.adpods[podid]:
                    self.adpods[podid][uid]["_status"] = Status.EXISTING
                else:
                    ad["_status"] = Status.NEW
                    self.adpods[podid][uid] = ad

    def summarize(self, highlight_time):
        for adpod in self.adpods.values():
            to_show = []
            for ad in adpod.values():
                field_to_extract = CONFIG.get("bkml-ad-metadata", section="monitor")

                if ad["adid"] == "SLATE":
                    info = click.style(ad[field_to_extract], fg="blue")
                else:
                    info = click.style(ad[field_to_extract], fg="green")

                start = datetime.fromtimestamp(
                    ad["starttime_ms"] / 1000.0, tz=timezone.utc
                )
                end = datetime.fromtimestamp(
                    (ad["starttime_ms"] + ad["duration_ms"]) / 1000.0, tz=timezone.utc
                )

                if start <= highlight_time <= end:
                    info = click.style(info, reverse=True)

                if ad["_status"] == Status.EXISTING:
                    to_show.append(info)
                if ad["_status"] == Status.NEW:
                    to_show.append(CL.high1(info))

            ads = CL.attr(" | ").join(to_show)
            if ads:
                return CL.high2("❰") + " " + ads + " " + CL.high2("❱") + "  "
