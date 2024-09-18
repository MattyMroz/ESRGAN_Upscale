import logging
import sys
from enum import Enum
from pathlib import Path
from typing import List, Tuple

from PIL import Image
import typer
from rich import print
from rich.logging import RichHandler
from rich.progress import BarColumn, Progress, TimeRemainingColumn


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
    supported_extensions: List[str] = [
        '.jpg', '.jpeg', '.png', '.webp', '.bmp', '.eps', '.gif',
        '.ico', '.msp', '.pcx', '.ppm', '.spider', '.tif', '.tiff', '.xbm', '.xpm'
    ]

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

        images = list(self.input.rglob("*.*"))
        images = [img for img in images if img.suffix.lower() in self.supported_extensions]

        with Progress(
            "[progress.description]{task.description}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
        ) as progress:
            task_resizing = progress.add_task("Resizing", total=len(images))
            for idx, img_path in enumerate(images, 1):
                self.process_image(img_path, idx, len(images))
                progress.advance(task_resizing)

    def process_image(self, img_path: Path, idx: int, total: int) -> None:
        img_input_path_rel = img_path.relative_to(self.input)
        output_dir = self.output.joinpath(img_input_path_rel).parent
        img_output_path = output_dir.joinpath(img_path.name)
        output_dir.mkdir(parents=True, exist_ok=True)

        self.log.info(f'Processing {str(idx).zfill(len(str(total)))}: "{img_input_path_rel}"')
        
        if self.skip_existing and img_output_path.is_file():
            self.log.warning("Already exists, skipping")
            if self.delete_input:
                img_path.unlink(missing_ok=True)
            return

        try:
            image = Image.open(img_path).convert("RGB")
            resized_image = self._resize_to_max_dimensions(image)
            self._reduce_file_size_and_save(resized_image, img_output_path)

            if self.delete_input:
                img_path.unlink(missing_ok=True)

            self.log.info(f"Image successfully resized and saved as {img_output_path}")
        except Exception as e:
            self.log.error(f"An error occurred while processing the image: {str(e)}")

    def _resize_to_max_dimensions(self, image: Image.Image) -> Image.Image:
        width, height = image.size
        target_size = self._calculate_target_size(width, height)

        if width > target_size[0] or height > target_size[1]:
            return image.resize(target_size, Image.LANCZOS)
        return image

    def _calculate_target_size(self, width: int, height: int) -> Tuple[int, int]:
        aspect_ratio = width / height
        max_size = self.max_size_px

        if self.resize_mode == ResizeMode.LONGEST_EDGE:
            if width > height:
                new_width = max_size
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_size
                new_width = int(new_height * aspect_ratio)
        elif self.resize_mode == ResizeMode.SHORTEST_EDGE:
            if width < height:
                new_width = max_size
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_size
                new_width = int(new_height * aspect_ratio)
        elif self.resize_mode == ResizeMode.WIDTH:
            new_width = max_size
            new_height = int(new_width / aspect_ratio)
        else:  # ResizeMode.HEIGHT
            new_height = max_size
            new_width = int(new_height * aspect_ratio)

        return (new_width, new_height)

    def _reduce_file_size_and_save(self, image: Image.Image, output_path: Path) -> None:
        quality = 95
        while True:
            image.save(output_path, format="JPEG", quality=quality)
            if output_path.stat().st_size <= self.max_size_mb * 1024 * 1024:
                break
            quality -= 5
            if quality < 20:
                raise ValueError("Cannot reduce file size to the desired size.")


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