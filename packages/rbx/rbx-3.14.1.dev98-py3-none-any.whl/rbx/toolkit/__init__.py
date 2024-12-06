__all__ = ["Options", "run"]

import logging
import os
import shutil
import tempfile
from pathlib import Path
from typing import NamedTuple, Optional

from .aws import upload
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


def capture(options: Options, dirname: Path, filename: str) -> None:
    path = dirname / "frames"
    os.makedirs(path)
    record(
        url=options.url,
        width=options.width,
        height=options.height,
        duration=options.duration,
        fps=options.fps,
        path=path,
    )
    render(
        path=path,
        fps=options.fps,
        width=options.width,
        height=options.height,
        filename=dirname / filename,
    )


def screengrab(options: Options, dirname: Path, filename: str) -> None:
    screenshot(
        url=options.url,
        width=options.width,
        height=options.height,
        filename=dirname / filename,
    )


def run(options: Options) -> None:
    with tempfile.TemporaryDirectory() as dirname:
        path = Path(options.path) / dirname
        logger.info(f"Working directory: '{path}'")
        if options.format == "video":
            asset = options.filename or "video.mp4"
            output = filename(options.output, asset)
            logger.info(
                f"Capturing '{options.url}' [{options.width}x{options.height}]"
                f" for {options.duration}s at {options.fps}fps to '{output}'",
            )
            capture(options=options, dirname=path, filename=asset)
        else:
            asset = options.filename or "screenshot.png"
            output = filename(options.output, asset)
            logger.info(
                f"Taking screenshot of '{options.url}' [{options.width}x{options.height}]"
                f" to '{output}'"
            )
            screengrab(options=options, dirname=path, filename=asset)

        if output.startswith("s3://"):
            upload(path / asset, output)
        else:
            shutil.move(path / asset, output)
