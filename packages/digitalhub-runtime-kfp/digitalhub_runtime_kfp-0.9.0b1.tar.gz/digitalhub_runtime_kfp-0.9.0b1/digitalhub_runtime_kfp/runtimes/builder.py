from __future__ import annotations

from digitalhub.runtimes.builder import RuntimeBuilder

from digitalhub_runtime_kfp.runtimes.runtime import RuntimeKfp


class RuntimeKfpBuilder(RuntimeBuilder):
    """RuntaimeKfpBuilder class."""

    RUNTIME_CLASS = RuntimeKfp
