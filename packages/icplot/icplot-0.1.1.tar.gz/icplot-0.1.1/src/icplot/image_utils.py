"""
This module has functions for converting between image
formats
"""

import logging
import os
from pathlib import Path

from wand.image import Image
from wand.color import Color
import cairosvg


logger = logging.getLogger(__name__)


def _get_out_filename(source: Path, target: Path | None, extension: str) -> Path:
    if target:
        return target
    return source.parent / f"{source.stem}.{extension}"


def pdf_to_png(source: Path, target: Path | None = None, resolution: int = 300):
    """
    Convert a pdf to png with white background
    """

    outfile = _get_out_filename(source, target, "png")
    os.makedirs(outfile.parent, exist_ok=True)

    with Image(filename=source, resolution=resolution) as img:
        img.format = "png"
        img.background_color = Color("white")
        img.alpha_channel = "remove"
        img.save(filename=outfile)


def svg_to_png(source: Path, target: Path | None = None):
    """
    Convert an svg to png
    """

    outfile = _get_out_filename(source, target, "png")
    os.makedirs(outfile.parent, exist_ok=True)
    cairosvg.svg2png(url=str(source), write_to=str(outfile))


def svg_to_pdf(source: Path, target: Path | None = None):
    """
    Convert an svg to pdf
    """

    outfile = _get_out_filename(source, target, "pdf")
    os.makedirs(outfile.parent, exist_ok=True)
    cairosvg.svg2pdf(url=str(source), write_to=str(outfile))
