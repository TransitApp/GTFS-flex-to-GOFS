from gtfs_flex_to_gofs.gofs_data import GofsData
import gtfs_loader
from .files import operation_rules


def patch_gtfs(args, gtfs):
    clean_up_gtfs(gtfs)

    if len(gtfs.stop_times) != 0:
        gtfs_loader.patch(gtfs, args.gtfs_dir, args.out_gtfs_dir)
    else:
        # we have no data, nothing to export
        print("No data to export, not exporting GTFS")


def clean_up_gtfs(gtfs):
    for trip_id, stop_times in list(gtfs.stop_times.items()):
        type_of_trip = operation_rules.get_type_of_trip(trip_id, stop_times)
        if type_of_trip == operation_rules.TripType.OTHER:
            print(f"WARNING : Trip {trip_id} is not a normal gtfs trip, not microtransit and not deviated service only. We are not supproting this yet, it will be removed from the GTFS and not shown anywhere")

        if type_of_trip == operation_rules.TripType.OTHER or type_of_trip == operation_rules.TripType.PURE_MICROTRANSIT:
            del gtfs.stop_times[trip_id]
