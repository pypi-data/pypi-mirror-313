from collections.abc import Sequence

from onnx import ModelProto
from onnx import ValueInfoProto
from onnxruntime import InferenceSession
from onnxruntime import NodeArg
from onnxruntime import SessionOptions

REQUIRED_HPARAMS = (
    "feature",
    "batch_size",
    "timesteps",
    "flatten",
    "add1ch",
    "truth_mutex",
)


def _extract_shapes(io: list[ValueInfoProto]) -> list[list[int] | str]:
    shapes: list[list[int] | str] = []

    # iterate through inputs of the graph to find shapes
    for item in io:
        # get tensor type: 0, 1, 2, etc.
        tensor_type = item.type.tensor_type
        # check if it has a shape
        if tensor_type.HasField("shape"):
            tmp_shape = []
            # iterate through dimensions of the shape
            for d in tensor_type.shape.dim:
                if d.HasField("dim_value"):
                    # known dimension, int value
                    tmp_shape.append(d.dim_value)
                elif d.HasField("dim_param"):
                    # dynamic dim with symbolic name of d.dim_param; set size to 0
                    tmp_shape.append(0)
                else:
                    # unknown dimension with no name; also set to 0
                    tmp_shape.append(0)
            # add as a list
            shapes.append(tmp_shape)
        else:
            shapes.append("unknown rank")

    return shapes


def get_and_check_inputs(
    model: ModelProto,
) -> tuple[list[ValueInfoProto], list[list[int] | str]]:
    from sonusai import logger

    # ignore initializer inputs (only seen in older ONNX < v1.5)
    initializer_names = [x.name for x in model.graph.initializer]
    inputs = [i for i in model.graph.input if i.name not in initializer_names]
    if len(inputs) != 1:
        logger.warning(f"Warning: ONNX model has {len(inputs)} inputs; expected only 1")

    # This one-liner works only if input has type and shape, returns a list
    # shape0 = [d.dim_value for d in inputs[0].type.tensor_type.shape.dim]
    shapes = _extract_shapes(inputs)

    return inputs, shapes


def get_and_check_outputs(
    model: ModelProto,
) -> tuple[list[ValueInfoProto], list[list[int] | str]]:
    from sonusai import logger

    outputs = list(model.graph.output)
    if len(outputs) != 1:
        logger.warning(f"Warning: ONNX model has {len(outputs)} outputs; expected only 1")

    shapes = _extract_shapes(outputs)

    return outputs, shapes


def add_sonusai_metadata(model: ModelProto, hparams: dict) -> ModelProto:
    """Add SonusAI hyperparameters as metadata to an ONNX model using 'hparams' key

    :param model: ONNX model
    :param hparams: dictionary of hyperparameters to add
    :return: ONNX model

    Note SonusAI conventions require models to have:
        feature: Model feature type
        batch_size: Model batch size
        timesteps: Size of timestep dimension (0 for no dimension)
        flatten: Model input feature data is flattened (stride + bins combined)
        add1ch: Model input has channel dimension
        truth_mutex: Model label output is mutually exclusive
    """
    from sonusai import logger

    # Note hparams should be a dict (i.e., extracted from checkpoint)
    if eval(str(hparams)) != hparams:  # noqa: S307
        raise TypeError("hparams is not a dict")
    for key in REQUIRED_HPARAMS:
        if key not in hparams:
            logger.warning(f"Warning: SonusAI hyperparameters are missing: {key}")

    meta = model.metadata_props.add()
    meta.key = "hparams"
    meta.value = str(hparams)

    return model


def get_sonusai_metadata(session: InferenceSession) -> dict | None:
    """Get SonusAI hyperparameter metadata from an ONNX Runtime session."""
    from sonusai import logger

    meta = session.get_modelmeta()
    if "hparams" not in meta.custom_metadata_map:
        logger.warning("Warning: ONNX model metadata does not contain 'hparams'")
        return None

    hparams = eval(meta.custom_metadata_map["hparams"])  # noqa: S307
    for key in REQUIRED_HPARAMS:
        if key not in hparams:
            logger.warning(f"Warning: ONNX model does not have required SonusAI hyperparameters: {key}")

    return hparams


def load_ort_session(
    model_path: str, providers: Sequence[str | tuple[str, dict]] | None = None
) -> tuple[InferenceSession, SessionOptions, str, dict | None, list[NodeArg], list[NodeArg]]:
    from os.path import basename
    from os.path import exists
    from os.path import isfile
    from os.path import splitext

    import onnxruntime as ort

    from sonusai import logger

    if providers is None:
        providers = ["CPUExecutionProvider"]

    if exists(model_path) and isfile(model_path):
        model_basename = basename(model_path)
        model_root = splitext(model_basename)[0]
        logger.info(f"Importing model from {model_basename}")
        try:
            session = ort.InferenceSession(model_path, providers=providers)
            options = ort.SessionOptions()
        except Exception as e:
            logger.exception(f"Error: could not load ONNX model from {model_path}: {e}")
            raise SystemExit(1) from e
    else:
        logger.exception(f"Error: model file does not exist: {model_path}")
        raise SystemExit(1)

    logger.info(f"Opened session with provider options: {session._provider_options}.")
    hparams = get_sonusai_metadata(session)
    if hparams is not None:
        for key in REQUIRED_HPARAMS:
            logger.info(f"  {key:12} {hparams[key]}")

    inputs = session.get_inputs()
    outputs = session.get_outputs()

    # in_names = [n.name for n in session.get_inputs()]
    # out_names = [n.name for n in session.get_outputs()]

    return session, options, model_root, hparams, inputs, outputs
