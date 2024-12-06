from __future__ import annotations

from digitalhub.entities.run._base.builder import RunBuilder

from digitalhub_runtime_kfp.entities._base.runtime_entity.builder import RuntimeEntityBuilderKfp
from digitalhub_runtime_kfp.entities._commons.enums import EntityKinds
from digitalhub_runtime_kfp.entities.run.kfp_run.entity import RunKfpRun
from digitalhub_runtime_kfp.entities.run.kfp_run.spec import RunSpecKfpRun, RunValidatorKfpRun
from digitalhub_runtime_kfp.entities.run.kfp_run.status import RunStatusKfpRun


class RunKfpRunBuilder(RunBuilder, RuntimeEntityBuilderKfp):
    """
    RunKfpRunBuilder runer.
    """

    ENTITY_CLASS = RunKfpRun
    ENTITY_SPEC_CLASS = RunSpecKfpRun
    ENTITY_SPEC_VALIDATOR = RunValidatorKfpRun
    ENTITY_STATUS_CLASS = RunStatusKfpRun
    ENTITY_KIND = EntityKinds.RUN_KFP.value
