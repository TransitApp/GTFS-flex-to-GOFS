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
            if transfer.is_pure_microtransit_trip:
                del gtfs.stop_times[transfer.trip_id]
            else:
                gtfs.stop_times[transfer.trip_id] = [stop_time for stop_time in gtfs.stop_times[transfer.trip_id]
                     if stop_time.stop_id != transfer.from_stop_id and stop_time.stop_id != transfer.to_stop_id
                ]
                
        if transfer.is_pure_microtransit_trip and transfer.trip_id in gtfs.trips:
            # Only delete trip if there's no stop_times.txt that still reference it, which only happen for pure microtransit trip
            del gtfs.trips[transfer.trip_id]
