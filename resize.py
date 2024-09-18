import argparse
from pathlib import Path
from utils.image_resizer import ImageResizer, ResizeMode


def main() -> None:
    parser = argparse.ArgumentParser(description="Resize images")
    parser.add_argument("-i", "--input", type=str,
                        default="/kaggle/working/ESRGAN_Upscale/output", help="Ścieżka wejściowa")
    parser.add_argument("-o", "--output", type=str,
                        default="/kaggle/working/ESRGAN_Upscale_Output", help="Ścieżka wyjściowa")
    parser.add_argument("-mb", "--max_size_mb", type=float,
                        default=8.0, help="Maksymalny rozmiar pliku w MB")
    parser.add_argument("-px", "--max_size_px", type=int, default=4096,
                        help="Maksymalna długość krawędzi w pikselach")
    parser.add_argument("-m", "--mode", type=str, default="LONGEST_EDGE",
                        choices=["LONGEST_EDGE", "WIDTH", "HEIGHT"], help="Tryb zmiany rozmiaru")
    args = parser.parse_args()

    input_path: Path = Path(args.input)
    output_path: Path = Path(args.output)
    max_size_mb: float = args.max_size_mb
    max_size_px: int = args.max_size_px
    resize_mode: ResizeMode = ResizeMode[args.mode]

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
