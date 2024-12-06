from sonusai.mixture.datatypes import Truth
from sonusai.mixture.truth_functions.datatypes import TruthFunctionConfig
from sonusai.mixture.truth_functions.datatypes import TruthFunctionData


def phoneme_validate(_config: dict) -> None:
    raise NotImplementedError("Truth function phoneme is not supported yet")


def phoneme_parameters(_config: TruthFunctionConfig) -> int:
    raise NotImplementedError("Truth function phoneme is not supported yet")


def phoneme(_data: TruthFunctionData, _config: TruthFunctionConfig) -> Truth:
    """Read in .txt transcript and run a Python function to generate text grid data
    (indicating which phonemes are active). Then generate truth based on this data and put
    in the correct classes based on the index in the config.
    """
    raise NotImplementedError("Truth function phoneme is not supported yet")
