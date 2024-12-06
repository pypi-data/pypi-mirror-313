def get_frames_per_batch(batch_size: int, timesteps: int) -> int:
    return batch_size if timesteps == 0 else batch_size * timesteps
