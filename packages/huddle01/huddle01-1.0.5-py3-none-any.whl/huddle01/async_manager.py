import asyncio
from enum import Enum
from typing import Any, Dict, Generic, Optional, TypeVar, Union

from .log import base_logger

logger = base_logger.getChild("AsyncOperationManager")

T = TypeVar("T")


class OperationStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class PendingOperation(Generic[T]):
    def __init__(self, operation_id: str):
        self.operation_id = operation_id
        self.future: asyncio.Future[T] = asyncio.Future()


class OperationsType(Dict[str, str]):
    CREATE_ROOM = "create_room"
    CONNECT_ROOM = "connect_room"
    CREATE_TRANSPORT = "create_transport"
    CONNECT_TRANSPORT = "connect_transport"
    PRODUCE = "produce"
    CONSUME = "consume"
    RESUME_CONSUMER = "resume_consumer"


class AsyncOperationManager:
    """
    A manager for handling asynchronous operations.

    This class is used to create, resolve, and wait for asynchronous operations.

    Attributes:
        operations: A dictionary of pending operations.
    """

    def __init__(self):
        self.operations: Dict[str, PendingOperation[Any]] = {}

    def has_operation(self, operation_id: str):
        """
        Check if an operation exists.
        """
        return operation_id in self.operations

    def get_operation(self, operation_id: str) -> Union[PendingOperation, None]:
        """
        Get a pending operation.
        """
        return self.operations.get(operation_id)

    def create_operation(self, operation_id: str) -> PendingOperation:
        """
        Create a new pending operation.
        """
        if operation_id in self.operations:
            raise ValueError(f"Operation with id {operation_id} already exists")

        operation = PendingOperation(operation_id)

        self.operations[operation_id] = operation

        logger.info(f"Created operation: {operation_id}")

        return operation

    def resolve_operation(
        self,
        operation_id: str,
        result: Optional[T] = None,
        error: Optional[Exception] = None,
    ) -> Optional[T]:
        """
        Resolve a pending operation with a result or an error.
        """
        operation = self.operations.get(operation_id)
        try:
            if not operation:
                logger.warning(
                    f"Attempted to resolve non-existent operation: {operation_id}"
                )
                return None

            if error:
                operation.future.set_exception(error)
            else:
                operation.future.set_result(result)

            logger.info(f"Resolved operation: {operation_id}")

        except Exception as e:
            logger.error(f"Error while resolving operation: {e}")
            raise

        finally:
            del self.operations[operation_id]

    async def wait_for_operation(
        self,
        operation_id: str,
    ) -> Any:
        """
        Wait for an operation to be resolved and return its result.
        """
        operation = self.operations.get(operation_id)
        if not operation:
            raise ValueError(f"No operation found with id: {operation_id}")

        try:
            result = await asyncio.wait_for(operation.future, timeout=None)
            return result
        except Exception:
            del self.operations[operation_id]
            raise

    def operation_id(self, type: str, id: str) -> str:
        """
        Get the operation id.

        The operation id is a unique identifier for an operation.

        type: Operation type.
        id: Operation id.
        """
        return f"{type}_{id}"
