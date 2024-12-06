from __future__ import annotations

from digitalhub.entities.task._base.spec import TaskSpecWorkflow, TaskValidatorWorkflow


class TaskSpecKfpPipeline(TaskSpecWorkflow):
    """
    TaskSpecKfpPipeline specifications.
    """

    def __init__(
        self,
        workflow: str,
        node_selector: list[dict] | None = None,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        affinity: dict | None = None,
        tolerations: list[dict] | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        runtime_class: str | None = None,
        priority_class: str | None = None,
        schedule: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            workflow,
            node_selector,
            volumes,
            resources,
            affinity,
            tolerations,
            envs,
            secrets,
            profile,
            runtime_class,
            priority_class,
            **kwargs,
        )
        self.schedule = schedule


class TaskValidatorKfpPipeline(TaskValidatorWorkflow):
    """
    TaskValidatorKfpPipeline validator.
    """

    schedule: str = None
    """KFP schedule specifications."""
