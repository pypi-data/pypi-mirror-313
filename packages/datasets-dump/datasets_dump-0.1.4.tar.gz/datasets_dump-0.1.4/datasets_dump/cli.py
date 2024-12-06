import argparse
from datasets import load_dataset
from .api import dump


def main():
    parser = argparse.ArgumentParser(
        description="Dump Hugging Face datasets to audio or image folders"
    )

    parser.add_argument(
        "dataset",
        help="Dataset name or path",
    )

    parser.add_argument(
        "dist",
        help="Destination folder path",
    )

    parser.add_argument(
        "--config",
        help="Dataset configuration",
    )

    parser.add_argument(
        "--audio-column",
        help="Column name containing audio data",
    )

    parser.add_argument(
        "--image-column",
        help="Column name containing image data",
    )

    parser.add_argument(
        "--metadata-format",
        choices=["jsonl", "csv"],
        default="jsonl",
        help="Format for metadata file",
    )

    parser.add_argument(
        "--audio-format",
        help="Output audio format (e.g., WAV, MP3, FLAC)",
        default=None,
    )

    parser.add_argument(
        "--image-format",
        help="Output image format (e.g., PNG, JPEG, WEBP)",
        choices=["PNG", "JPEG", "WEBP", "GIF", "BMP", "TIFF"],
        default=None,
    )

    args = parser.parse_args()

    dataset = load_dataset(args.dataset, args.config)

    dump(
        dataset=dataset,
        dist=args.dist,
        audio_column=args.audio_column,
        image_column=args.image_column,
        metadata_format=args.metadata_format,
        audio_format=args.audio_format,
        image_format=args.image_format,
    )


if __name__ == "__main__":
    main()
