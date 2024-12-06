import sys

from robot_desktop.extract_icon import extract_icon

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_icon.py <executable_path>")
        sys.exit(1)
    result = extract_icon(sys.argv[1])
    print(result)
