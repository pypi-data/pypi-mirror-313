import webbrowser
from urllib.parse import urljoin

from classiq.interface.exceptions import ClassiqAnalyzerVisualizationError
from classiq.interface.generator.model.preferences.preferences import QuantumFormat
from classiq.interface.generator.quantum_program import QuantumProgram

from classiq._internals.api_wrapper import ApiWrapper
from classiq._internals.async_utils import syncify_function
from classiq.analyzer.url_utils import circuit_page_uri, client_ide_base_url


async def handle_remote_app(circuit: QuantumProgram, display_url: bool = True) -> None:
    if circuit.outputs.get(QuantumFormat.QASM) is None:
        raise ClassiqAnalyzerVisualizationError(
            "Missing QASM transpilation: visualization is only supported "
            "for QASM programs. Try adding QASM to the output formats "
            "synthesis preferences"
        )
    circuit_dataid = await ApiWrapper.call_analyzer_app(circuit)
    app_url = urljoin(
        client_ide_base_url(),
        circuit_page_uri(circuit_id=circuit_dataid.id, circuit_version=circuit.version),
    )

    if display_url:
        print(f"Opening: {app_url}")  # noqa: T201

    webbrowser.open_new_tab(app_url)


async def _show_interactive(self: QuantumProgram, display_url: bool = True) -> None:
    """
    Displays the interactive representation of the quantum program in the Classiq IDE.

    Args:
        self:
            The serialized quantum program to be displayed.
        display_url:
            Whether to print the url

    Links:
        [Visualization tool](https://docs.classiq.io/latest/reference-manual/analyzer/quantum-program-visualization-tool/)
    """
    await handle_remote_app(self, display_url)


QuantumProgram.show = syncify_function(_show_interactive)  # type: ignore[attr-defined]
QuantumProgram.show_async = _show_interactive  # type: ignore[attr-defined]
