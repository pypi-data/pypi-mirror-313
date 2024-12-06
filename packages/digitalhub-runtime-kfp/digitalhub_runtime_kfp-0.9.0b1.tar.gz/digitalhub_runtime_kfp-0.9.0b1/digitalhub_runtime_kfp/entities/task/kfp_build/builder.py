from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_kfp.entities._base.runtime_entity.builder import RuntimeEntityBuilderKfp
from digitalhub_runtime_kfp.entities._commons.enums import EntityKinds
from digitalhub_runtime_kfp.entities.task.kfp_build.entity import TaskKfpBuild
from digitalhub_runtime_kfp.entities.task.kfp_build.spec import TaskSpecKfpBuild, TaskValidatorKfpBuild
from digitalhub_runtime_kfp.entities.task.kfp_build.status import TaskStatusKfpBuild


class TaskKfpBuildBuilder(TaskBuilder, RuntimeEntityBuilderKfp):
    """
    TaskKfpBuildBuilder builder.
    """

    ENTITY_CLASS = TaskKfpBuild
    ENTITY_SPEC_CLASS = TaskSpecKfpBuild
    ENTITY_SPEC_VALIDATOR = TaskValidatorKfpBuild
    ENTITY_STATUS_CLASS = TaskStatusKfpBuild
    ENTITY_KIND = EntityKinds.TASK_KFP_BUILD.value
