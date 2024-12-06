from datetime import timedelta

from bpkio_api.exceptions import BroadpeakIoHelperError
from bpkio_cli.core.exceptions import UnexpectedContentError
from bpkio_cli.writers.colorizer import Colorizer as CL
from bpkio_cli.writers.xml_formatter import XMLFormatter
from media_muncher.handlers import XMLHandler
from mpd_inspector import MPDInspector, Scte35BinaryEventInspector

COMMON_NAMESPACES = {
    "mpd": "urn:mpeg:dash:schema:mpd:2011",
    "scte35": "http://www.scte.org/schemas/35/2016",
    "cenc": "urn:mpeg:cenc:2013",
}

NS_MPD = "{" + COMMON_NAMESPACES["mpd"] + "}"


class MPDFormatter(XMLFormatter):
    def __init__(self, handler: XMLHandler) -> None:
        super().__init__(handler=handler)
        self.ad_pattern = "/bpkio-jitt"

    def format(self, mode="standard", top: int = 0, tail: int = 0, **kwargs):
        try:
            match mode:
                case "raw":
                    output = self.raw()
                case "standard":
                    root = self.handler.xml_document
                    filter_mpd(root, **kwargs)

                    decorate_mpd(root, self.handler.inspector, **kwargs)

                    output = self.pretty_print(
                        namespaces=COMMON_NAMESPACES,
                        root=root,
                        uri_attributes=self.handler.uri_attributes,
                        uri_elements=self.handler.uri_elements,
                        ad_pattern=self.ad_pattern,
                        **kwargs,
                    )

            output = self.trim(output, top, tail)
            return output

        except BroadpeakIoHelperError as e:
            out = self.handler.content.decode()
            out += "\n\n"
            out += CL.error(f"Error - {e.message}: {e.original_message}")
            return out

        except Exception as e:
            raise UnexpectedContentError(
                message="Error formatting the content. "
                "It does not appear to be a valid MPEG-DASH MPD. {}\n"
                "Raw content: \n{}".format(e, self.handler.content)
            )


def filter_mpd(mpd, **kwargs):
    # Select periods to return
    selected_periods = kwargs.get("mpd_period")
    mpd_level = kwargs.get("mpd_level")

    for i, period in enumerate(mpd.findall(f"{NS_MPD}Period")):
        if selected_periods is not None and i not in selected_periods:
            mpd.remove(period)
        else:
            if mpd_level is not None and mpd_level <= 1:
                for child in period:
                    period.remove(child)
            else:
                _filter_mpd_adaptationsets(period, **kwargs)


def _filter_mpd_adaptationsets(period, **kwargs):
    # Select adaptation sets to return
    selected_adaptation_sets = kwargs.get("mpd_adaptation_set")
    mpd_level = kwargs.get("mpd_level")

    for adaptation_set in period.findall(f"{NS_MPD}AdaptationSet"):
        if (
            selected_adaptation_sets
            and selected_adaptation_sets not in adaptation_set.get("mimeType", "")
            # and selected_adaptation_sets not in adaptation_set.get("id", "")
            # and selected_adaptation_sets not in adaptation_set.get("contentType", "")
        ):
            period.remove(adaptation_set)
        else:
            if mpd_level is not None and mpd_level <= 2:
                for child in adaptation_set:
                    adaptation_set.remove(child)
            else:
                _filter_mpd_adaptationset_content(adaptation_set, **kwargs)


def _filter_mpd_adaptationset_content(adaptation_set, **kwargs):
    mpd_level = kwargs.get("mpd_level")

    for child in adaptation_set:
        if mpd_level is not None and mpd_level <= 3:
            if child.tag != f"{NS_MPD}Representation":
                adaptation_set.remove(child)


def decorate_mpd(mpd, inspector: MPDInspector, **kwargs):
    COMMON_NAMESPACES["bic"] = "urn:broadpeak:bic"
    BIC_NS = "{" + COMMON_NAMESPACES["bic"] + "}"

    for i, period in enumerate(mpd.findall(f"{NS_MPD}Period")):
        period_inspect = inspector.periods[i]

        start = (
            str(period_inspect.start_time.value) if period_inspect.start_time else ""
        )
        duration = str(period_inspect.duration.value) if period_inspect.duration else ""
        period.set(f"{BIC_NS}start", start)
        period.set(f"{BIC_NS}duration", duration)

        for j, eventstream in enumerate(period.findall(f"{NS_MPD}EventStream")):
            for k, event in enumerate(eventstream.findall(f"{NS_MPD}Event")):
                event_inspect = period_inspect.event_streams[j].events[k]
                if isinstance(event_inspect, Scte35BinaryEventInspector):
                    event.set(
                        f"{BIC_NS}pt",
                        str(event_inspect.presentation_time),
                    )
                    event.set(
                        f"{BIC_NS}pt_rel",
                        format_timedelta(event_inspect.relative_presentation_time),
                    )


def format_timedelta(td: timedelta) -> str:
    total_seconds = td.total_seconds()
    abs_seconds = abs(total_seconds)

    hours, remainder = divmod(abs_seconds, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, milliseconds = divmod(remainder, 1)

    sign = "-" if total_seconds < 0 else ""
    return f"{sign}{int(hours):01}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds * 1000):03}"
