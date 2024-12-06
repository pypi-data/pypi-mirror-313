from __future__ import annotations

import shutil
from typing import Callable

from digitalhub.context.api import get_context
from digitalhub.runtimes._base import Runtime
from digitalhub.utils.logger import LOGGER

from digitalhub_runtime_kfp.entities._commons.enums import TaskActions
from digitalhub_runtime_kfp.utils.configurations import (
    get_dhcore_workflow,
    get_kfp_pipeline,
    parse_workflow_specs,
    save_workflow_source,
)
from digitalhub_runtime_kfp.utils.functions import run_kfp_build
from digitalhub_runtime_kfp.utils.outputs import build_status


class RuntimeKfp(Runtime):
    """
    RuntimeKfp class.
    """

    def __init__(self, project: str) -> None:
        super().__init__(project)
        ctx = get_context(self.project)
        self.runtime_dir = ctx.root / "runtime_kfp"
        self.runtime_dir.mkdir(parents=True, exist_ok=True)

    def build(self, workflow: dict, task: dict, run: dict) -> dict:
        """
        Build run spec.

        Parameters
        ----------
        workflow : dict
            The workflow.
        task : dict
            The task.
        run : dict
            The run.

        Returns
        -------
        dict
            The run spec.
        """
        return {
            **workflow.get("spec", {}),
            **task.get("spec", {}),
            **run.get("spec", {}),
        }

    def run(self, run: dict) -> dict:
        """
        Run workflow.

        Returns
        -------
        dict
            Status of the executed run.
        """
        LOGGER.info("Validating task.")
        action = self._validate_task(run)
        executable = self._get_executable(action)

        LOGGER.info(f"Starting task {action}.")
        spec = run.get("spec")

        LOGGER.info("Collecting inputs.")
        workflow_args = self._collect_inputs(spec)

        LOGGER.info("Configure execution.")
        kfp_workflow = self._configure_execution(spec)

        LOGGER.info("Executing workflow.")
        results = self._execute(executable, kfp_workflow, workflow_args)

        LOGGER.info("Collecting outputs.")
        status = build_status(results)

        LOGGER.info("Cleanup")
        self._cleanup()

        LOGGER.info("Task completed, returning run status.")
        return status

    @staticmethod
    def _get_executable(action: str) -> Callable:
        """
        Select workflow according to action.

        Parameters
        ----------
        action : str
            Action to execute.

        Returns
        -------
        Callable
            Workflow to execute.
        """
        if action == TaskActions.BUILD.value:
            return run_kfp_build
        raise NotImplementedError

    ##############################
    # Helpers
    ##############################
    def _collect_inputs(self, spec: dict) -> dict:
        """
        Collect inputs.

        Parameters
        ----------
        spec : dict
            Run specs.
        project : str
            Name of the project.

        Returns
        -------
        dict
            Parameters.
        """
        LOGGER.info("Getting inputs.")
        inputs = spec.get("inputs", {})
        parameters = spec.get("parameters", {})
        return {**parameters, **inputs}

    ##############################
    # Configuration
    ##############################

    def _configure_execution(self, spec: dict):
        """
        Create KFP pipeline and prepare parameters.

        Parameters
        ----------
        spec : dict
            Run specs.
        action : str
            Action to execute.
        project : str
            Name of the project.

        Returns
        -------
        tuple
            KFP pipeline to execute and parameters.
        """
        # Setup function source and specs
        LOGGER.info("Getting workflow source and specs.")
        dhcore_workflow = get_dhcore_workflow(spec.get("workflow"))
        workflow_source = save_workflow_source(self.runtime_dir, dhcore_workflow.spec.to_dict().get("source"))
        workflow_specs = parse_workflow_specs(dhcore_workflow.spec)

        # Create kfp project
        LOGGER.info("Creating KFP project and workflow.")
        return get_kfp_pipeline(dhcore_workflow.name, workflow_source, workflow_specs)

    ##############################
    # Cleanup
    ##############################

    def _cleanup(self) -> None:
        """
        Cleanup root folder.

        Returns
        -------
        None
        """
        shutil.rmtree(self.runtime_dir, ignore_errors=True)
