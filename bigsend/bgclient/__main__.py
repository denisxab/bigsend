import argparse
import asyncio

from .lib_clients import FileSender


def main():
    parser = argparse.ArgumentParser(
        description="Send a large file to a remote server."
    )
    parser.add_argument("url", type=str, help="URL of the remote server. Example: http://192.168.10.63:8083")
    parser.add_argument("file_path", type=str, help="Path to the local file to be sent")
    parser.add_argument(
        "remote_path",
        type=str,
        help="Path to the remote directory where the file will be saved",
    )
    args = parser.parse_args()
    #
    ##
    #
    sender = FileSender(
        url=args.url,
        file_path=args.file_path,
        remote_path=args.remote_path,
    )
    asyncio.run(sender.send())


if __name__ == "__main__":
    main()
