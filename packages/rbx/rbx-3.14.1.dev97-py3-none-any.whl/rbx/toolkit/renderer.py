from pathlib import Path
import tempfile
from typing import Optional

import sh

from .upload import upload


def render(
    path: str,
    fps: int,
    width: int,
    height: int,
    output: str,
    bg: Optional[str] = "white",
) -> None:
    frames = sorted(list(Path(path).glob("*.png")))

    # ffmpg filter to ensure width and height are divisible by 2.
    #
    # The .h264 codec needs even dimensions so this filter will:
    #   - Divide the original height and width by 2
    #   - Round it up to the nearest pixel
    #   - Multiply it by 2 again, thus making it an even number
    #   - Add black padding pixels up to this number
    #
    # You can change the color of the padding by adding filter parameter :color=white.
    # > See the documentation of pad: https://ffmpeg.org/ffmpeg-filters.html#pad
    f_filter = f"pad=ceil(iw/2)*2:ceil(ih/2)*2:color={bg}"

    # fmt: off
    args = [
        "-r", fps,
        "-f", "image2",
        "-s", f"{width}x{height}",
        "-start_number", 0,
        "-i", f"{path}/frame_%d.png",
        "-frames:v", len(frames),
        "-vcodec", "libx264",  # H264.AVC codec
        "-vf", f_filter,
        "-crf", 5,  # less is better quality 0-51
        "-pix_fmt", "yuv420p",  # pixel format
        "-y",  # overwrite
    ]
    # fmt: on

    if output.startswith("s3://"):
        with tempfile.NamedTemporaryFile(suffix=".mp4") as fp:
            ffmpg(args, fp.name)
            upload(fp.name, output)
    else:
        ffmpg(args, output)


def ffmpg(args, output):
    try:
        sh.ffmpeg(*args, output)
    except sh.ErrorReturnCode as e:
        raise RuntimeError(
            f"Command {e.full_cmd} exited with {e.exit_code}\n\n{e.stderr.decode()}"
        )
