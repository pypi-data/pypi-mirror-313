from __future__ import annotations

from enum import Enum


class EntityKinds(Enum):
    """
    Entity kinds.
    """

    WORKFLOW_KFP = "kfp"
    TASK_KFP_PIPELINE = "kfp+pipeline"
    TASK_KFP_BUILD = "kfp+build"
    RUN_KFP = "kfp+run"


class TaskActions(Enum):
    """
    Task actions.
    """

    PIPELINE = "pipeline"
    BUILD = "build"
