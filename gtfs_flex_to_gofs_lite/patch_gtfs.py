import gtfs_loader


def patch_gtfs(args, gtfs, gofs_data):
    clean_up_gtfs(gtfs, gofs_data)
    gtfs_loader.patch(gtfs, args.gtfs_dir, args.out_gtfs_dir)


def clean_up_gtfs(gtfs, gofs_data):
    # TODO : Implement me
    pass
