from pathlib import Path
from utils.image_resizer import ImageResizer, ResizeMode


def main() -> None:
    input_path: Path = Path("/kaggle/working/ESRGAN_Upscale/output")
    output_path: Path = Path("/kaggle/working/ESRGAN_Upscale_Output")
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
