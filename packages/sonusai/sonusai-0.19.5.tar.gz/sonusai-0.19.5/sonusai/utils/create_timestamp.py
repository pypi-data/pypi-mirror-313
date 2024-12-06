def create_timestamp() -> str:
    """Create a timestamp."""
    from datetime import datetime

    return datetime.now().strftime("%Y%m%d-%H%M%S")
