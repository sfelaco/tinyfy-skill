#!/usr/bin/env python3
"""CLI per la compressione e il resizing di immagini tramite TinyPNG API."""

import argparse
import os
import sys

from dotenv import load_dotenv
import tinify

load_dotenv()


def get_api_key(args_key: str | None) -> str:
    key = args_key or os.environ.get("TINIFY_API_KEY")
    if not key:
        print(
            "Errore: API key non trovata. "
            "Usa --api-key oppure imposta la variabile TINIFY_API_KEY.",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def resolve_output(input_path: str, output_path: str | None, suffix: str = "_optimized") -> str:
    if output_path:
        return output_path
    base, ext = os.path.splitext(input_path)
    return f"{base}{suffix}{ext}"


def cmd_compress(args: argparse.Namespace) -> None:
    tinify.key = get_api_key(args.api_key)
    output = resolve_output(args.input, args.output)

    print(f"Compressione: {args.input} -> {output}")
    source = tinify.from_file(args.input)
    source.to_file(output)

    input_size = os.path.getsize(args.input)
    output_size = os.path.getsize(output)
    saving = (1 - output_size / input_size) * 100
    print(f"  Prima: {input_size:,} byte")
    print(f"  Dopo:  {output_size:,} byte  ({saving:.1f}% di risparmio)")


def cmd_resize(args: argparse.Namespace) -> None:
    tinify.key = get_api_key(args.api_key)
    output = resolve_output(args.input, args.output, suffix="_resized")

    if args.width and args.height:
        print("Errore: specifica solo --width oppure --height, non entrambi.", file=sys.stderr)
        sys.exit(1)

    if not args.width and not args.height:
        print("Errore: devi specificare almeno --width oppure --height.", file=sys.stderr)
        sys.exit(1)

    resize_opts: dict = {"method": "scale"}
    if args.width:
        resize_opts["width"] = args.width
        dim_info = f"larghezza={args.width}px (proporzioni conservate)"
    else:
        resize_opts["height"] = args.height
        dim_info = f"altezza={args.height}px (proporzioni conservate)"

    print(f"Resize + compressione: {args.input} -> {output}  [{dim_info}]")
    source = tinify.from_file(args.input)
    source.resize(**resize_opts).to_file(output)

    input_size = os.path.getsize(args.input)
    output_size = os.path.getsize(output)
    saving = (1 - output_size / input_size) * 100
    print(f"  Prima: {input_size:,} byte")
    print(f"  Dopo:  {output_size:,} byte  ({saving:.1f}% di risparmio)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="image-cli",
        description="Compressione e resizing di immagini tramite TinyPNG API.",
    )
    parser.add_argument(
        "--api-key",
        metavar="KEY",
        help="TinyPNG API key (in alternativa usa la variabile TINIFY_API_KEY).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- compress ---
    p_compress = subparsers.add_parser("compress", help="Comprimi un'immagine.")
    p_compress.add_argument("input", help="Percorso dell'immagine di input.")
    p_compress.add_argument(
        "-o", "--output", metavar="FILE", help="Percorso dell'immagine di output (opzionale)."
    )
    p_compress.set_defaults(func=cmd_compress)

    # --- resize ---
    p_resize = subparsers.add_parser(
        "resize",
        help="Ridimensiona (e comprimi) un'immagine conservando le proporzioni.",
    )
    p_resize.add_argument("input", help="Percorso dell'immagine di input.")
    p_resize.add_argument(
        "-o", "--output", metavar="FILE", help="Percorso dell'immagine di output (opzionale)."
    )

    dim_group = p_resize.add_mutually_exclusive_group(required=True)
    dim_group.add_argument(
        "--width", type=int, metavar="PX", help="Larghezza target in pixel."
    )
    dim_group.add_argument(
        "--height", type=int, metavar="PX", help="Altezza target in pixel."
    )

    p_resize.set_defaults(func=cmd_resize)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
