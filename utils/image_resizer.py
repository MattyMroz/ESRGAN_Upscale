from dataclasses import dataclass
from enum import Enum
from os import stat
from pathlib import Path
from PIL import Image
from typing import List, Tuple


class ResizeMode(Enum):
    VERTICAL: str = "vertical"
    HORIZONTAL: str = "horizontal"
    LONGEST_EDGE: str = "longest_edge"
    SHORTEST_EDGE: str = "shortest_edge"


@dataclass(slots=True)
class ImageResizer:
    input_filename: str
    input_path: Path
    output_path: Path
    max_size_mb: float
    max_size_px: int
    resize_mode: ResizeMode
    supported_extensions: List[str] = (
        '.jpg', '.jpeg', '.png', '.webp', '.bmp', '.eps', '.gif',
        '.ico', '.msp', '.pcx', '.ppm', '.spider', '.tif', '.tiff', '.xbm', '.xpm'
    )

    def resize_image(self) -> None:
        try:
            input_file: Path = self.input_path / self.input_filename
            if not input_file.exists():
                raise FileNotFoundError(f"Plik {input_file} nie istnieje.")

            if input_file.suffix.lower() not in self.supported_extensions:
                raise ValueError(
                    f"Nieobsługiwane rozszerzenie pliku: {input_file.suffix}")

            image: Image.Image = self._load_image(input_file)
            resized_image: Image.Image = self._resize_to_max_dimensions(image)
            output_file: Path = self.output_path / self.input_filename
            self._reduce_file_size_and_save(resized_image, output_file)

            print(
                f"Obraz został pomyślnie zmniejszony i zapisany jako {output_file}")
        except Exception as e:
            print(f"Wystąpił błąd podczas przetwarzania obrazu: {str(e)}")

    def _load_image(self, file_path: Path) -> Image.Image:
        return Image.open(file_path).convert("RGB")

    def _resize_to_max_dimensions(self, image: Image.Image) -> Image.Image:
        width: int
        height: int
        width, height = image.size
        target_size: Tuple[int, int] = self._calculate_target_size(
            width, height)

        if width > target_size[0] or height > target_size[1]:
            return image.resize(target_size, Image.Resampling.LANCZOS)
        return image

    def _calculate_target_size(self, width: int, height: int) -> Tuple[int, int]:
        aspect_ratio: float = width / height
        max_size: int = self.max_size_px

        new_width: int
        new_height: int

        if self.resize_mode == ResizeMode.VERTICAL:
            new_height = max_size
            new_width = int(new_height * aspect_ratio)
        elif self.resize_mode == ResizeMode.HORIZONTAL:
            new_width = max_size
            new_height = int(new_width / aspect_ratio)
        elif self.resize_mode == ResizeMode.LONGEST_EDGE:
            if width > height:
                new_width = max_size
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_size
                new_width = int(new_height * aspect_ratio)
        else:  # ResizeMode.SHORTEST_EDGE
            if width < height:
                new_width = max_size
                new_height = int(new_width / aspect_ratio)
            else:
                new_height = max_size
                new_width = int(new_height * aspect_ratio)

        return (new_width, new_height)

    def _reduce_file_size_and_save(self, image: Image.Image, output_file: Path) -> None:
        quality: int = 95
        while True:
            image.save(output_file, format="JPEG", quality=quality)
            if stat(output_file).st_size <= self.max_size_mb * 1024 * 1024:
                break
            quality -= 5
            if quality < 20:
                raise ValueError(
                    "Nie można zmniejszyć rozmiaru pliku do żądanej wielkości.")


def main() -> None:
    input_path: Path = Path("../input")
    output_path: Path = Path("../output")
    max_size_mb: float = float(
        input("Podaj ile MB nie może przekroczyć plik np.: 8: ") or 8)
    max_size_px: int = int(input(
        "Podaj długość największej krawędzi w px np.: 1024, 2048, 4096, 8192: ") or 4096)
    resize_mode: ResizeMode = ResizeMode.LONGEST_EDGE

    if not output_path.exists():
        output_path.mkdir(parents=True)

    for file in input_path.iterdir():
        if file.is_file() and file.suffix.lower() in ImageResizer("", Path(), Path(), 0, 0, ResizeMode.LONGEST_EDGE).supported_extensions:
            resizer: ImageResizer = ImageResizer(
                input_filename=file.name,
                input_path=input_path,
                output_path=output_path,
                max_size_mb=max_size_mb,
                max_size_px=max_size_px,
                resize_mode=resize_mode
            )
            resizer.resize_image()

    print("Zakończono przetwarzanie wszystkich obrazów.")


if __name__ == "__main__":
    main()
