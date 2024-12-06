import os
import subprocess
import tempfile
from datetime import datetime, timedelta
from urllib.parse import urlparse

import ffmpeg
import requests
from bpkio_cli.core.config_provider import CONFIG
from bpkio_cli.core.logging import logger
from bpkio_cli.monitor.hls_segment_map import SYMBOLS
from bpkio_cli.monitor.store import SegmentMapRecord
from chafa import Canvas, CanvasConfig, PixelMode, PixelType, TermDb
from PIL import Image


class FrameExtractor:
    def __init__(self, output_folder) -> None:
        self.output_folder = output_folder

    def _download_video(self, url):
        """
        Downloads a video from a remote URL to a temporary file.
        Returns the path to the temporary file.
        """
        response = requests.get(
            url, stream=True, verify=CONFIG.get("verify-ssl", cast_type=bool)
        )
        # in case of redirection
        actual_url = response.request.url
        filename = urlparse(actual_url).path.split("/")[-1]

        if response.status_code == 200:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            for chunk in response.iter_content(chunk_size=1024):
                temp_file.write(chunk)
            temp_file.close()
            return filename, temp_file.name
        else:
            response.raise_for_status()

    def _extract_middle_frame(
        self,
        video_path: str,
        start_pdt: datetime,
        base_name: str,
        media_sequence: int,
        content_type: str,
        text_color: str = "white",
    ):
        # Ensure the video file exists
        if not os.path.isfile(video_path):
            return

        # Get the total number of frames
        probe = ffmpeg.probe(video_path)
        video_stream = next(
            (stream for stream in probe["streams"] if stream["codec_type"] == "video"),
            None,
        )
        duration = float(video_stream["duration"])
        # Calculate the time position for the middle frame
        middle_time = duration / 2
        middle_pdt = start_pdt + timedelta(seconds=middle_time)

        # Use a temporary file for the output
        output_filename = f"{middle_pdt.strftime('%Y%m%dT%H%M%S%f')[:-3]}_ms{media_sequence}__{base_name}.jpg"
        output_file = os.path.join(self.output_folder, output_filename)

        try:
            # Extract the frame at the middle time as a JPEG
            output = (
                ffmpeg.input(video_path)
                .filter("scale", "-1", "180")
                .drawtext(
                    text=str(media_sequence),
                    x="20",
                    y="(text_h+2)",
                    fontsize=12,
                    fontcolor="white",
                    box=1,
                    boxcolor="black@0.5",
                    boxborderw=3,
                )
                .drawtext(
                    text=str(duration),
                    x="20",
                    y="(text_h*2+10)",
                    fontsize=12,
                    fontcolor="white",
                    box=1,
                    boxcolor="black@0.5",
                    boxborderw=3,
                )
                .drawtext(
                    text=content_type,
                    x="(w-text_w-20)",
                    y="(text_h+2)",
                    fontsize=12,
                    fontcolor="white",
                    box=1,
                    boxcolor=f"{text_color}@0.8",
                    boxborderw=3,
                )
                .output(output_file, ss=middle_time, vframes=1)
            )

            logger.debug("FFMPEG command: " + " ".join(output.compile()))

            output.run(capture_stdout=True, capture_stderr=True, overwrite_output=True)
            return output_file
        except ffmpeg.Error as e:
            logger.error(f"An error occurred: {e.stderr.decode()}")

    def _make_image_for_terminal_viu(self, image_path):
        # Run viu and capture its output
        result = subprocess.run(
            ["viu", image_path, "-w", "32"], capture_output=True, text=True
        )

        # Check if the command was executed successfully
        if result.returncode == 0:
            vert_cusor_moves = 8
            return result.stdout, vert_cusor_moves
        else:
            # Print error message if something went wrong
            logger.error("Error running viu:", result.stderr)

    def _make_image_for_terminal_chafa(self, image_path):
        config = CanvasConfig()

        # Get terminal capabilities
        term_db = TermDb()
        term_info = term_db.detect()
        capabilities = term_info.detect_capabilities()
        config.canvas_mode = capabilities.canvas_mode
        config.pixel_mode = capabilities.pixel_mode

        terminal = os.getenv("TERM_PROGRAM")
        if terminal == "iTerm.app":
            config.pixel_mode = PixelMode.CHAFA_PIXEL_MODE_ITERM2
        else:
            config.pixel_mode = PixelMode.CHAFA_PIXEL_MODE_SYMBOLS

        # Calculate the appropriate geometry for the canvas, based on font aspect ratio
        config.calc_canvas_geometry(src_width=32, src_height=20, font_ratio=8 / 20)

        # Open image with PIL
        image = Image.open(image_path)
        width = image.width
        height = image.height
        bands = len(image.getbands())
        pixels = image.tobytes()

        # Init the canvas
        canvas = Canvas(config)

        # Draw to canvas
        canvas.draw_all_pixels(
            PixelType.CHAFA_PIXEL_RGB8, pixels, width, height, width * bands
        )
        # Write picture
        output = canvas.print(fallback=True).decode()
        vert_cursor_moves = 7  # found experimentally
        return output, vert_cursor_moves

    def extract_frame_and_show(self, segment: SegmentMapRecord):
        orig_filename, video_file = self._download_video(segment.segment.absolute_uri)
        image_file = self._extract_middle_frame(
            video_file,
            start_pdt=segment.segment.current_program_date_time,
            media_sequence=segment.segment.media_sequence,
            base_name=orig_filename,
            content_type=segment.type.value,
            text_color=SYMBOLS[segment.type]["color"],
        )
        if CONFIG.get("image-processor", section="monitor") == "viu":
            image, vert_cursor_moves = self._make_image_for_terminal_viu(image_file)
        elif CONFIG.get("image-processor", section="monitor") == "chafa":
            image, vert_cursor_moves = self._make_image_for_terminal_chafa(image_file)
        else:
            logger.error("No compatible image processor")

        return orig_filename, image, vert_cursor_moves
