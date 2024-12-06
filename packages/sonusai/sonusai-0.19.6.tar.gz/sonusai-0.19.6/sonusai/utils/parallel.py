import warnings
from collections.abc import Callable
from collections.abc import Iterable
from multiprocessing import current_process
from multiprocessing import get_context
from typing import Any

from tqdm import TqdmExperimentalWarning
from tqdm.rich import tqdm

warnings.filterwarnings(action="ignore", category=TqdmExperimentalWarning)

track = tqdm

CONTEXT = "fork"


def par_track(
    func: Callable,
    *iterables: Iterable,
    initializer: Callable[..., None] | None = None,
    initargs: Iterable[Any] | None = None,
    progress: tqdm | None = None,
    num_cpus: int | float | None = None,
    total: int | None = None,
    no_par: bool = False,
) -> list[Any]:
    """Performs a parallel ordered imap with tqdm progress."""
    from collections.abc import Sized

    from psutil import cpu_count

    if total is None:
        _total = min(len(iterable) for iterable in iterables if isinstance(iterable, Sized))
    else:
        _total = int(total)

    results: list[Any] = [None] * _total
    if no_par or current_process().daemon:
        if initializer is not None:
            if initargs is not None:
                initializer(*initargs)
            else:
                initializer()

        for n, result in enumerate(map(func, *iterables)):
            results[n] = result
            if progress is not None:
                progress.update()
    else:
        if num_cpus is None:
            _num_cpus = max(cpu_count() - 2, 1)
        elif isinstance(num_cpus, float):
            _num_cpus = int(round(num_cpus * cpu_count()))
        else:
            _num_cpus = int(num_cpus)

        _num_cpus = min(_num_cpus, _total)

        if initargs is None:
            initargs = []

        with get_context(CONTEXT).Pool(processes=_num_cpus, initializer=initializer, initargs=initargs) as pool:
            n = 0
            for result in pool.imap(func, *iterables):  # type: ignore[arg-type]
                results[n] = result
                n += 1
                if progress is not None:
                    progress.update()
            pool.close()
            pool.join()

    if progress is not None:
        progress.close()
    return results
