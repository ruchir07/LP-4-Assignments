from pathlib import Path
import sys

SIGNATURES = {
    "jpg": {
        "start": bytes.fromhex("FFD8FF"),
        "end": bytes.fromhex("FFD9")
    },
    "png": {
        "start": bytes.fromhex("89504E470D0A1A0A"),
        "end": bytes.fromhex("49454E44AE426082")
    },
    "pdf": {
        "start": b"%PDF-",
        "end": b"%%EOF"
    }
}


def carve_files(image_path, output_folder):
    image_path = Path(image_path)
    output_folder = Path(output_folder)

    if not image_path.is_file():
        print("Error: Disk image not found.")
        return

    output_folder.mkdir(parents=True, exist_ok=True)
    data = image_path.read_bytes()

    recovered = 0

    print("===== FILE RECOVERY REPORT =====")
    print("Image:", image_path)
    print("Image size:", len(data), "bytes")

    for extension, sig in SIGNATURES.items():
        start_sig = sig["start"]
        end_sig = sig["end"]
        position = 0

        while True:
            start = data.find(start_sig, position)

            if start == -1:
                break

            end = data.find(end_sig, start + len(start_sig))

            if end == -1:
                print(
                    f"Incomplete {extension.upper()} at offset {start}"
                )
                position = start + 1
                continue

            # Include the complete end marker
            end += len(end_sig)
            recovered += 1

            output_path = output_folder / (
                f"recovered_{recovered}.{extension}"
            )

            output_path.write_bytes(data[start:end])

            print(
                f"Recovered {extension.upper()} file: "
                f"{output_path} "
                f"(offset {start}, {end - start} bytes)"
            )

            position = end

    print("\nTotal files recovered:", recovered)
    print("Output folder:", output_folder.resolve())
    print("Validate recovered files before using them.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python file_recovery.py <disk_image_file>")
    else:
        carve_files(sys.argv[1], "recovered_files")