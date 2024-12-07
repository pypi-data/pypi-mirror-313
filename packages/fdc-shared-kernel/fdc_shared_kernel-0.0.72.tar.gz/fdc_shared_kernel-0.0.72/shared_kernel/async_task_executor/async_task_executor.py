import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from shared_kernel.enums.async_task_executor import AsyncTaskStatus
from shared_kernel.logger import Logger
from shared_kernel.config import Config


config = Config()
logger = Logger(config.get("APP_NAME"))


class AsyncTaskExecutor:
    """
    Singleton class for managing the execution of asynchronous tasks.
    It uses a thread pool to manage concurrency and a status tracker to monitor task execution.
    """

    _instance = None
    # lock to ensure thread safety
    _lock = Lock()

    def __new__(self, concurrency: int):
        """
        Singleton method that ensures only one instance of AsyncTaskExecutor is created.
        Uses double-checked locking to ensure thread safety.

        Args:
            concurrency (int): The maximum number of threads allowed to run concurrently.

        Returns:
            AsyncTaskExecutor: A single instance of AsyncTaskExecutor.
        """
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = super(AsyncTaskExecutor, self).__new__(self)
                    self._instance._initialized = False
        return self._instance

    def __init__(self, concurrency: int):
        """
        Initializes the AsyncTaskExecutor. This method will only run once for the singleton instance.

        Args:
            concurrency (int): The number of threads that can be run concurrently in the pool.
        """
        if self._initialized:
            return
        # dictionary to track the status of tasks
        self.status_tracker: dict = {}
        self.queue = ThreadPoolExecutor(max_workers=int(concurrency))
        # mark as initialized to prevent re-initialization
        self._initialized = True
        logger.debug(
            f"AsyncTaskExecutor initialized with concurrency level: {concurrency}"
        )

    def task_execute_wrapper(self, task_to_execute, job_payload: dict):
        """
        Wrapper method to execute a task and handle its status updates.
        Updates the task's status to STARTED, SUCCESS, or FAILURE depending on the outcome.

        Args:
            task_to_execute (callable): The function representing the task to be executed.
            job_payload (dict): The payload containing job-related information, including the execution ID.
        """
        execution_id = job_payload["execution_id"]
        self.status_tracker[execution_id]["status"] = AsyncTaskStatus.STARTED.value
        logger.debug(f"Task started for execution ID: {execution_id}")
        try:
            result = task_to_execute(job_payload)
            self.status_tracker[execution_id]["status"] = AsyncTaskStatus.SUCCESS.value
            self.status_tracker[execution_id]["data"] = result
            logger.debug(
                f"Task completed successfully for execution ID: {execution_id}"
            )
        except Exception as e:
            self.status_tracker[execution_id]["status"] = AsyncTaskStatus.FAILURE.value
            self.status_tracker[execution_id]["reason"] = str(e)
            logger.error(
                f"Task failed for execution ID: {execution_id}, Reason: {str(e)}"
            )

    def submit_job(self, task_to_execute, job_payload: dict):
        """
        Submits a new task to be executed asynchronously. Generates a unique execution ID and tracks the job status.

        Args:
            task_to_execute (callable): The function to be executed asynchronously.
            job_payload (dict): The payload to pass to the task, excluding the execution ID.

        Returns:
            str: The unique execution ID of the submitted job.
        """
        execution_id = str(uuid.uuid4())
        job_payload["execution_id"] = execution_id
        self.status_tracker[execution_id] = {"status": AsyncTaskStatus.QUEUED.value}
        logger.info(f"Job submitted with execution ID: {execution_id}")
        self.queue.submit(self.task_execute_wrapper, task_to_execute, job_payload)
        return execution_id

    def track_status(self, execution_id: str) -> dict:
        """
        Polls the current status of a task using its execution ID.

        Args:
            execution_id (str): The unique identifier for the task to track.

        Returns:
            dict: The current status of the task (QUEUED, STARTED, SUCCESS, FAILURE, or NA).
        """
        status = self.status_tracker.get(
            execution_id, {"status": AsyncTaskStatus.NA.value}
        )
        logger.debug(
            f"Tracking status for task with execution ID: {execution_id}, Status: {status['status']}"
        )
        return status
