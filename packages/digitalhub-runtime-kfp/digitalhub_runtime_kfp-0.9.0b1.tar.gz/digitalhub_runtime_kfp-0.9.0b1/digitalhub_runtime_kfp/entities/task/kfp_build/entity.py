from __future__ import annotations

import typing

from digitalhub.entities.task._base.entity import Task

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_kfp.entities.task.kfp_build.spec import TaskSpecKfpBuild
    from digitalhub_runtime_kfp.entities.task.kfp_build.status import TaskStatusKfpBuild


class TaskKfpBuild(Task):
    """
    TaskKfpBuild class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: TaskSpecKfpBuild,
        status: TaskStatusKfpBuild,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: TaskSpecKfpBuild
        self.status: TaskStatusKfpBuild
