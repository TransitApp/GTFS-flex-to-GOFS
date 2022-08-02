from gtfs_flex_to_gofs_lite.gofs_data import GofsData
import gtfs_loader


def patch_gtfs(args, gtfs, gofs_data: GofsData):
    clean_up_gtfs(gtfs, gofs_data)
    gtfs_loader.patch(gtfs, args.gtfs_dir, args.out_gtfs_dir)


def clean_up_gtfs(gtfs, gofs_data: GofsData):
    # Clean up stop_times.txt
    for transfer in gofs_data.transfers:
        gtfs.stop_times[transfer.trip_id] = [
            stop_time for stop_time in gtfs.stop_times[transfer.trip_id] if keep_stop_time(transfer, stop_time)]


def keep_stop_time(transfer, stop_time):
    return transfer.from_stop_id != stop_time.stop_id and transfer.to_stop_id != stop_time.stop_id
