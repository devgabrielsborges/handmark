from dissector import ImageDissector
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: handmark <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]

    try:
        sample = ImageDissector(image_path=image_path)
        sample.write_response()
        print(f"Response written to response.md for image: {image_path}")
    except FileNotFoundError:
        print("File not found")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()