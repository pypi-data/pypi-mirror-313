__all__ = ["Options", "run"]

import logging
import tempfile
from pathlib import Path
from typing import NamedTuple, Optional

from .browser import record, screenshot
from .renderer import render

logger = logging.getLogger(__name__)


class Options(NamedTuple):
    url: str
    width: int
    height: int
    format: str
    duration: Optional[int] = 6
    fps: Optional[int] = 30
    path: Optional[str] = "/tmp"
    output: Optional[str] = "."
    filename: Optional[str] = None


def filename(output, filename):
    if output.startswith("s3://"):
        return "s3://" + str(Path(output[5:]) / filename)

    return str(Path(output) / filename)


def run(options: Options):
    if options.format == "video":
        logger.info(
            f"Recording '{options.url}' [{options.width}x{options.height}]"
            f" for {options.duration}s at {options.fps}fps",
        )

        with tempfile.TemporaryDirectory() as dirname:
            path = Path(options.path) / dirname
            logger.info(f"Saving frames in: '{path}'")

            record(
                url=options.url,
                width=options.width,
                height=options.height,
                duration=options.duration,
                fps=options.fps,
                path=path,
            )

            output = filename(options.output, options.filename or "video.mp4")
            logger.info(f"Rendering video to '{output}'")

            render(
                path=path,
                fps=options.fps,
                width=options.width,
                height=options.height,
                output=output,
            )

    else:
        output = filename(options.output, options.filename or "screenshot.png")
        logger.info(
            f"Taking screenshot of '{options.url}' [{options.width}x{options.height}]"
            f" to '{output}'"
        )

        screenshot(
            url=options.url,
            width=options.width,
            height=options.height,
            output=output,
        )
