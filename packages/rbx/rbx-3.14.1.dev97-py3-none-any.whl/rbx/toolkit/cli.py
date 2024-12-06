import datetime
import logging
import logging.config
import os

import click

from . import Options, run


class ColourFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        colours = {
            logging.INFO: {"bold": True},
            logging.WARNING: {"fg": "yellow"},
            logging.ERROR: {"fg": "bright_red"},
            logging.CRITICAL: {"fg": "bright_white", "bg": "red"},
        }
        try:
            message = click.style(message, **colours[record.levelno])
        except KeyError:
            pass
        return message


@click.group()
@click.version_option(message="%(version)s")
def cli():
    """Toolkit Creative Converter."""


def validate_filename(ctx, param, value):
    if value is None:
        return

    if ctx.params["format"] == "image" and not value.endswith(".png"):
        raise click.BadParameter(f"{param.name} must use the '.png' extension")
    elif ctx.params["format"] == "video" and not value.endswith(".mp4"):
        raise click.BadParameter(f"{param.name} must use the '.mp4' extension")

    return value


@cli.command(context_settings={"show_default": True})
@click.argument("url")
@click.option("--width", "-w", type=click.INT, default=1080)
@click.option("--height", "-h", type=click.INT, default=1920)
@click.option(
    "--format",
    type=click.Choice(["image", "video"], case_sensitive=False),
    default="image",
)
@click.option("--duration", "-d", type=click.INT, default=6)
@click.option("--fps", type=click.INT, default=30)
@click.option("--path", "-p", default="/tmp")
@click.option("--output-dir", "-o", type=click.Path(file_okay=False), default=".")
@click.option("--filename", "-f", callback=validate_filename)
def export(url, width, height, format, duration, fps, path, output_dir, filename):
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.config.dictConfig(
        {
            "version": 1,
            "formatters": {
                "coloured": {
                    "class": "rbx.toolkit.cli.ColourFormatter",
                    "format": "[%(asctime)s] %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "coloured",
                },
            },
            "loggers": {
                "rbx.toolkit": {
                    "level": log_level,
                    "handlers": ["console"],
                    "propagate": False,
                },
            },
        }
    )

    start_timestamp = datetime.datetime.now()

    try:
        run(
            options=Options(
                url=url,
                width=width,
                height=height,
                format=format,
                duration=duration,
                fps=fps,
                path=path,
                output=output_dir,
                filename=filename,
            )
        )
    except RuntimeError as e:
        click.secho(e, fg="red", bold=True)

    click.secho(f"Finished in {datetime.datetime.now() - start_timestamp}", bold=True)
