from __future__ import annotations

from digitalhub.entities.run._base.spec import RunSpec, RunValidator


class RunSpecKfpRun(RunSpec):
    """RunSpecKfpRun specifications."""

    def __init__(
        self,
        task: str,
        local_execution: bool = False,
        function: str | None = None,
        workflow: str | None = None,
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
        source: dict | None = None,
        image: str | None = None,
        tag: str | None = None,
        handler: str | None = None,
        schedule: str | None = None,
        replicas: int | None = None,
        inputs: dict | None = None,
        outputs: dict | None = None,
        parameters: dict | None = None,
        values: list | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            task,
            local_execution,
            function,
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
        self.source = source
        self.image = image
        self.tag = tag
        self.handler = handler
        self.schedule = schedule
        self.replicas = replicas
        self.inputs = inputs
        self.outputs = outputs
        self.parameters = parameters
        self.values = values


class RunValidatorKfpRun(RunValidator):
    """RunValidatorKfpRun validator."""

    # Workflow parameters
    source: dict = None
    image: str = None
    tag: str = None
    handler: str = None

    # Pipeline parameters
    schedule: str = None

    # Run parameters
    inputs: dict = None
    outputs: dict = None
    parameters: dict = None
    values: list = None
