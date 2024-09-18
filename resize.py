import logging
import sys
from enum import Enum
from pathlib import Path
from typing import List

import cv2
import numpy as np
import typer
from rich import print
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, TaskID, TimeRemainingColumn


class ResizeMode(str, Enum):
    LONGEST_EDGE = "LONGEST_EDGE"
    SHORTEST_EDGE = "SHORTEST_EDGE"
    WIDTH = "WIDTH"
    HEIGHT = "HEIGHT"


class Resize:
    input: Path = None
    output: Path = None
    max_size_mb: float = None
    max_size_px: int = None
    resize_mode: ResizeMode = None
    skip_existing: bool = None
    delete_input: bool = None
    log: logging.Logger = None

    def __init__(
        self,
        input: Path,
        output: Path,
        max_size_mb: float,
        max_size_px: int,
        resize_mode: ResizeMode,
        skip_existing: bool = False,
        delete_input: bool = False,
        log: logging.Logger = logging.getLogger(),
    ) -> None:
        self.input = input.resolve()
        self.output = output.resolve()
        self.max_size_mb = max_size_mb
        self.max_size_px = max_size_px
        self.resize_mode = resize_mode
        self.skip_existing = skip_existing
        self.delete_input = delete_input
        self.log = log

    def run(self) -> None:
        if not self.input.exists():
            self.log.error(f'Folder "{self.input}" does not exist.')
            sys.exit(1)
        elif self.input.is_file():
            self.log.error(f'Folder "{self.input}" is a file.')
            sys.exit(1)
        elif self.output.is_file():
            self.log.error(f'Folder "{self.output}" is a file.')
            sys.exit(1)
        elif not self.output.exists():
            self.output.mkdir(parents=True)

        images: List[Path] = []
        extensions = [
            "bmp", "dib", "jpeg", "jpg", "jpe", "jp2", "png", "webp", "pbm", "pgm", "ppm", 
            "pxm", "pnm", "pfm", "sr", "ras", "tiff", "tif", "exr", "hdr", "pic"
        ]

        for file in self.input.glob("**/*.*"):
            if file.suffix.lower()[1:] in extensions:
                images.append(file)

        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
        ) as progress:
            task_resizing = progress.add_task("Resizing", total=len(images))
            for idx, img_path in enumerate(images, 1):
                img_input_path_rel = img_path.relative_to(self.input)
                output_dir = self.output.joinpath(img_input_path_rel).parent
                img_output_path_rel = output_dir.joinpath(f"{img_path.stem}.jpg")
                output_dir.mkdir(parents=True, exist_ok=True)

                self.log.info(
                    f'Processing {str(idx).zfill(len(str(len(images))))}: "{img_input_path_rel}"'
                )
                if self.skip_existing and img_output_path_rel.is_file():
                    self.log.warning("Already exists, skipping")
                    if self.delete_input:
                        img_path.unlink(missing_ok=True)
                    progress.advance(task_resizing)
                    continue

                img = cv2.imread(str(img_path))
                resized_img = self.resize_image(img)
                self.save_image(resized_img, img_output_path_rel)

                if self.delete_input:
                    img_path.unlink(missing_ok=True)

                progress.advance(task_resizing)

    def resize_image(self, img: np.ndarray) -> np.ndarray:
        height, width = img.shape[:2]
        if self.resize_mode == ResizeMode.LONGEST_EDGE:
            if width > height:
                new_width = self.max_size_px
                new_height = int(height * (self.max_size_px / width))
            else:
                new_height = self.max_size_px
                new_width = int(width * (self.max_size_px / height))
        elif self.resize_mode == ResizeMode.SHORTEST_EDGE:
            if width < height:
                new_width = self.max_size_px
                new_height = int(height * (self.max_size_px / width))
            else:
                new_height = self.max_size_px
                new_width = int(width * (self.max_size_px / height))
        elif self.resize_mode == ResizeMode.WIDTH:
            new_width = self.max_size_px
            new_height = int(height * (self.max_size_px / width))
        else:  # ResizeMode.HEIGHT
            new_height = self.max_size_px
            new_width = int(width * (self.max_size_px / height))

        return cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    def save_image(self, img: np.ndarray, output_path: Path) -> None:
        quality = 95
        while True:
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
            _, encoded_img = cv2.imencode(".jpg", img, encode_param)
            if encoded_img.nbytes <= self.max_size_mb * 1024 * 1024:
                break
            quality -= 5
            if quality < 20:
                raise ValueError("Cannot reduce file size to the desired size.")

        cv2.imwrite(str(output_path), img, encode_param)


app = typer.Typer()


@app.command()
def main(
    input: Path = typer.Option(Path("input"), "--input", "-i", help="Input folder"),
    output: Path = typer.Option(Path("output"), "--output", "-o", help="Output folder"),
    max_size_mb: float = typer.Option(8.0, "--max-size-mb", "-mb", help="Maximum file size in MB"),
    max_size_px: int = typer.Option(4096, "--max-size-px", "-px", help="Maximum edge length in pixels"),
    resize_mode: ResizeMode = typer.Option(ResizeMode.LONGEST_EDGE, "--mode", "-m", help="Resize mode"),
    skip_existing: bool = typer.Option(False, "--skip-existing", "-se", help="Skip existing output files"),
    delete_input: bool = typer.Option(False, "--delete-input", "-di", help="Delete input files after resizing"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Verbose mode"),
):
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.ERROR,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(markup=True)],
    )

    resize = Resize(
        input=input,
        output=output,
        max_size_mb=max_size_mb,
        max_size_px=max_size_px,
        resize_mode=resize_mode,
        skip_existing=skip_existing,
        delete_input=delete_input,
    )
    resize.run()


if __name__ == "__main__":
    app()