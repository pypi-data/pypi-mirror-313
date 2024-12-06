import json
from pathlib import Path
from typing import Optional

from classiq.interface.model.model import Model, SerializedModel

from classiq.qmod.native.pretty_printer import DSLPrettyPrinter
from classiq.qmod.utilities import DEFAULT_DECIMAL_PRECISION

_QMOD_SUFFIX = "qmod"
_SYNTHESIS_OPTIONS_SUFFIX = "synthesis_options.json"


def write_qmod(
    serialized_model: SerializedModel,
    name: str,
    directory: Optional[Path] = None,
    decimal_precision: int = DEFAULT_DECIMAL_PRECISION,
) -> None:
    """
    Creates a native Qmod file from a serialized model and outputs the synthesis options (Preferences and Constraints) to a file.
    The native Qmod file may be uploaded to the Classiq IDE.

    Args:
        serialized_model: The serialized model to write as a native Qmod file and synthesis options file.
        name: The name to save the file by.
        directory: The directory to save the files in. If None, the current working directory is used.
        decimal_precision: The number of decimal places to use for numbers, set to 4 by default.

    Returns:
        None
    """

    model = Model.model_validate_json(serialized_model)
    pretty_printed_model = DSLPrettyPrinter(decimal_precision=decimal_precision).visit(
        model
    )

    synthesis_options = model.model_dump(
        include={"constraints", "preferences"}, exclude_none=True
    )

    synthesis_options_path = Path(f"{name}.{_SYNTHESIS_OPTIONS_SUFFIX}")
    if directory is not None:
        synthesis_options_path = directory / synthesis_options_path

    synthesis_options_path.write_text(json.dumps(synthesis_options, indent=2))

    native_qmod_path = Path(f"{name}.{_QMOD_SUFFIX}")
    if directory is not None:
        native_qmod_path = directory / native_qmod_path

    native_qmod_path.write_text(pretty_printed_model)
