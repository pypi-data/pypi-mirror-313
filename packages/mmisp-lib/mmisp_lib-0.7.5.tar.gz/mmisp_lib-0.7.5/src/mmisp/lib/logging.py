from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.models.log import Log
from ..db.models.workflow import Workflow


class ApplicationLogger:
    db_session: AsyncSession

    def __init__(self: Self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    def log_workflow_debug_message(self: Self, workflow: Workflow, message: str) -> Log | None:
        """
        If debugging is enabled, logs a message for the given workflow.

        Arguments:
            workflow:       The workflow a log entry is created for.
            message:        The message to log.
        """

        if workflow.debug_enabled:
            log_entry = self.__create_workflow(workflow.id, message)
            self.db_session.add(log_entry)

            return log_entry

        return None

    def log_workflow_execution_error(self: Self, workflow: Workflow, message: str) -> Log:
        """
        Logs a message in case of an error for the given workflow.

        Arguments:
            workflow:       The workflow a log entry is created for.
            message:        The message to log.
        """

        log_entry = self.__create_workflow(workflow.id, message)
        self.db_session.add(log_entry)

        return log_entry

    def __create_workflow(self: Self, id: int, message: str) -> Workflow:
        return Log(
            title=message,
            action="execute_workflow",
            model="Workflow",
            model_id=id,
            user_id=0,
            email="SYSTEM",
            org="SYSTEM",
            description="",
            change="",
            ip="",
        )
