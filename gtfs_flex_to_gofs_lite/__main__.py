import gtfs_loader
import sys

gtfs = gtfs_loader.load(sys.argv[1])

print(gtfs.stop_times)