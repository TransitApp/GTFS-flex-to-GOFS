uv run python -m gtfs_flex_to_gofs --gtfs-dir ./tests/test_simple_conversion/input  --gofs-dir ./tests/test_simple_conversion/expected_default --url "" --timestamp 0
uv run python -m gtfs_flex_to_gofs --gtfs-dir ./tests/test_non_pure_microtransit_route/input  --gofs-dir ./tests/test_non_pure_microtransit_route/expected_default --url "" --timestamp 0
uv run python -m gtfs_flex_to_gofs --gtfs-dir ./tests/test_ondemand_stops/input  --gofs-dir ./tests/test_ondemand_stops/expected_default --url "" --timestamp 0
uv run python -m gtfs_flex_to_gofs --gtfs-dir ./tests/test_added_calendar_dates/input  --gofs-dir ./tests/test_added_calendar_dates/expected_default --url "" --timestamp 0
uv run python -m gtfs_flex_to_gofs --gtfs-dir ./tests/test_removed_calendar_dates/input  --gofs-dir ./tests/test_removed_calendar_dates/expected_default --url "" --timestamp 0
