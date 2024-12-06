import threefive
from bpkio_cli.writers.colorizer import Colorizer as CL


def summarize(payload, separator="  "):
    if isinstance(payload, threefive.Cue):
        cue = payload
    else:
        cue = threefive.Cue(payload)
        cue.decode()

    lines = []

    extracted = None
    match cue.info_section.splice_command_type:
        case 5:
            extracted = dict(
                command=f"{cue.command.name} ({cue.command.command_type})",
                event_id=cue.command.splice_event_id,
                duration=cue.command.break_duration,
                avail=f"{cue.command.avail_num}/{cue.command.avails_expected}",
            )
        case 6:
            extracted = dict(command=f"{cue.command.name} ({cue.command.command_type})")
    if extracted:
        lines.append(
            separator.join(
                [
                    CL.labeled(v, label=label, label_style=CL.bic_label)
                    for label, v in extracted.items()
                ]
            )
        )

    for d in cue.descriptors:
        if d.tag != 0:
            extracted = dict()

            extracted["descriptor"] = (
                f"{CL.high3_rev(d.segmentation_message) or '(Unknown)'} "
                f"({d.segmentation_type_id} | {hex(d.segmentation_type_id)})"
            )

            extracted["event_id"] = int(d.segmentation_event_id, 16)
            if d.segmentation_duration_flag:
                extracted["duration"] = d.segmentation_duration

            if d.segmentation_upid_type > 0:
                if d.segmentation_upid_type == 12:
                    extracted["upid_fmt"] = d.segmentation_upid["format_identifier"]
                    extracted["upid"] = d.segmentation_upid["private_data"]
                else:
                    extracted["upid"] = d.segmentation_upid

                # decode it from hex
                try:
                    extracted["upid"] = bytes.fromhex(extracted["upid"][2:]).decode(
                        "utf-8"
                    )
                except UnicodeDecodeError:
                    pass

            if hasattr(d, "segments_expected"):
                extracted["segments"] = f"{d.segment_num}/{d.segments_expected}"

            lines.append(
                separator.join(
                    [CL.labeled(v, label=label) for label, v in extracted.items()]
                )
            )

    return lines
