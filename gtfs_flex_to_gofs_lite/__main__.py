import argparse
import gtfs_loader
import os
from pathlib import Path

from .gofs_lite_converter import convert_to_gofs_lite
from .utils import YELLOW_STRING

DEFAULT_TTL = 86400


def main(args):
    gtfs = gtfs_loader.load(args.gtfs_dir)
    gofs_dir = Path(args.gofs_dir)

    if not gofs_dir.exists():
        os.mkdir(gofs_dir)

    convert_to_gofs_lite(gtfs, gofs_dir, args.ttl, args.url)


def print_args_warnings(args):
    if args.url is None:
        print(YELLOW_STRING.format(
            "[WARNING]") + ' No url given. \'gofs.json\' and \'gofs_versions.json\' will not be created. Consider adding a url with the --url parameter')

    if args.ttl == DEFAULT_TTL:
        print(YELLOW_STRING.format(
            "[WARNING]") + ' No ttl given. Will be using the default value of {}'.format(DEFAULT_TTL))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert GTFS-flex on-demand format to GOFS-lite')
    parser.add_argument(
        '--gtfs_dir', help='input gtfs directory', metavar='Dir', required=True)
    parser.add_argument(
        '--gofs_dir', help='output gofs directory', metavar='Dir', required=True)
    parser.add_argument(
        '--url', help='auto-discovery url. Base URL indicate for where each files will be uploaded (and downloadable)')
    parser.add_argument(
        '--ttl', help='time to live of the generated gofs files in seconds (default: 86400)', type=int, default=DEFAULT_TTL)
    parser.add_argument(
        '--no_warning', help='Silence warnings', action='store_true')

    args = parser.parse_args()

    if not args.no_warning:
        print_args_warnings(args)

    main(args)
