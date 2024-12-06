from digitalhub_runtime_kfp.entities._commons.enums import EntityKinds
from digitalhub_runtime_kfp.entities.run.kfp_run.builder import RunKfpRunBuilder
from digitalhub_runtime_kfp.entities.task.kfp_build.builder import TaskKfpBuildBuilder
from digitalhub_runtime_kfp.entities.task.kfp_pipeline.builder import TaskKfpPipelineBuilder
from digitalhub_runtime_kfp.entities.workflow.kfp.builder import WorkflowKfpBuilder

entity_builders = (
    (EntityKinds.RUN_KFP.value, RunKfpRunBuilder),
    (EntityKinds.TASK_KFP_PIPELINE.value, TaskKfpPipelineBuilder),
    (EntityKinds.TASK_KFP_BUILD.value, TaskKfpBuildBuilder),
    (EntityKinds.WORKFLOW_KFP.value, WorkflowKfpBuilder),
)

try:
    from digitalhub_runtime_kfp.runtimes.builder import RuntimeKfpBuilder

    runtime_builders = ((kind, RuntimeKfpBuilder) for kind in [e.value for e in EntityKinds])
except ImportError:
    runtime_builders = tuple()
