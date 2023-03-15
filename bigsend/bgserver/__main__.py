import argparse
from .lib_server import run


def main():
    parser = argparse.ArgumentParser(description="Big file sender")
    parser.add_argument(
        "host", nargs="?", default="0.0.0.0", type=str, help="Server host"
    )
    parser.add_argument(
        "port", nargs="?", default=8083, type=int, help="Server port"
    )
    args = parser.parse_args()

    run(args.host, args.port)


if __name__ == "__main__":
    main()
