from __future__ import annotations

from digitalhub.entities.workflow._base.spec import WorkflowSpec, WorkflowValidator

from digitalhub_runtime_kfp.entities.workflow.kfp.models import BuildValidator, SourceValidator


class WorkflowSpecKfp(WorkflowSpec):
    """
    WorkflowSpecKfp specifications.
    """

    def __init__(
        self,
        source: dict | None = None,
        build: dict | None = None,
        image: str | None = None,
        tag: str | None = None,
        workflow: str | None = None,
    ) -> None:
        super().__init__()

        self.source = source
        self.build = build
        self.image = image
        self.tag = tag
        self.workflow = workflow


class WorkflowValidatorKfp(WorkflowValidator):
    """
    WorkflowValidatorKfp validator.
    """

    source: SourceValidator
    """Source code validator."""

    build: BuildValidator = None
    """Build validator."""

    image: str = None
    """Name of the Workflow's container image."""

    tag: str = None
    """Tag of the Workflow's container image."""

    workflow: str = None
    """YAML of the Workflow."""
