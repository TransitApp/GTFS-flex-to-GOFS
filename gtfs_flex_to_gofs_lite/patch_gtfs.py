from gtfs_flex_to_gofs_lite.gofs_data import GofsData
import gtfs_loader


def patch_gtfs(args, gtfs, gofs_data: GofsData):
    clean_up_gtfs(gtfs, gofs_data)
    gtfs_loader.patch(gtfs, args.gtfs_dir, args.out_gtfs_dir)


def clean_up_gtfs(gtfs, gofs_data: GofsData):
    for transfer in gofs_data.transfers:
        # Multiple transfers can be extracted from the same trip
        # Check if it hasn't been yet deleted for each gtfs file
        if transfer.trip_id in gtfs.stop_times:
            del gtfs.stop_times[transfer.trip_id]

        if transfer.trip_id in gtfs.trips:
            del gtfs.trips[transfer.trip_id]
