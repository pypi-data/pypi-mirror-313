from __future__ import annotations

from digitalhub.entities._base.runtime_entity.builder import RuntimeEntityBuilder
from digitalhub.entities.task._base.utils import build_task_actions

from digitalhub_runtime_kfp.entities._commons.enums import EntityKinds, TaskActions


class RuntimeEntityBuilderKfp(RuntimeEntityBuilder):
    EXECUTABLE_KIND = EntityKinds.WORKFLOW_KFP.value
    TASKS_KINDS = build_task_actions(
        [
            (
                EntityKinds.TASK_KFP_PIPELINE.value,
                TaskActions.PIPELINE.value,
            ),
            (
                EntityKinds.TASK_KFP_BUILD.value,
                TaskActions.BUILD.value,
            ),
        ]
    )
    RUN_KIND = EntityKinds.RUN_KFP.value
