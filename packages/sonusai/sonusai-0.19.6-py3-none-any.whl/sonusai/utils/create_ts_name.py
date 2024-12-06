def create_ts_name(base: str) -> str:
    """Create a timestamped name based on 'base'."""
    from datetime import datetime
    from os.path import exists

    ts = datetime.now()

    # First try just date
    dir_name = base + "-" + ts.strftime("%Y%m%d")
    if exists(dir_name):
        # add hour-min-sec if necessary
        dir_name = base + "-" + ts.strftime("%Y%m%d-%H%M%S")

    return dir_name
