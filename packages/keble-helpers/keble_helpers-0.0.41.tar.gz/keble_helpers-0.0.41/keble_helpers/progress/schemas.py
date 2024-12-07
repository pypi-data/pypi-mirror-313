import json
import uuid
from enum import Enum
from functools import reduce
from typing import List, Optional
import logging
from pydantic import BaseModel, computed_field, ConfigDict, Field
from keble_helpers import PydanticModelConfig
from redis import Redis

logger = logging.getLogger(__name__)


class ProgressTaskStage(str, Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class ProgressReport(BaseModel):
    model_config = PydanticModelConfig.default()
    progress_key: Optional[str] = None
    progress: float
    is_root_success: bool
    success: int
    failure: int
    pending: int
    assigned: int
    total: int
    errors: List[str] = []


class ProgressTask(BaseModel):

    model_config = ConfigDict(**PydanticModelConfig.default_dict(), arbitrary_types_allowed=True)
    stage: ProgressTaskStage = ProgressTaskStage.PENDING
    subtasks: List["ProgressTask"] = []
    error: Optional[str] = None
    redis: Optional[Redis] = None
    key: Optional[str] = None
    model_key: Optional[str] = None
    root: Optional["ProgressTask"] = None
    # if the task is assigned to a task
    # it will be marked as True
    # otherwise, it will be marked as False (by default)
    assigned: bool = False

    # @property
    # def root_key(self) -> str:
    #     if self.root is not None:
    #         return self.root.root_key
    #     return self.key


    def __str__(self):
        report = self.progress_report
        return f"[Helper] Progress {f'{round(report.progress * 100, 2)}%' if report.progress is not None else '-%'}(total={report.total}, assigned={report.assigned}, success={report.success}, failure={report.failure}, pending={report.pending})"

    @property
    def is_root_success(self) -> bool:
        if self.root is not None:
            return self.root.is_root_success
        # self is root
        return self.stage == ProgressTaskStage.SUCCESS

    @property
    def total_assigned(self) -> int:
        if self.root is not None:
            return self.root.total_assigned
        # is root, 1 is for root, root is assumed as assigned
        return 1 + len([s for s in self.subtasks if s.assigned is True])

    @classmethod
    def get_from_redis(cls, redis: Redis, *, key: str) -> Optional["ProgressTask"]:
        h = redis.get(key)
        if h is None: return None
        return ProgressTask(**json.loads(h))

    @classmethod
    def get_prebuilt_subtasks_model(cls, root: "ProgressTask", redis: Redis, *, model_key: str) -> List["ProgressTask"]:
        """number of subtasks will be stored in redis,
        so each time when a new object is initialized,
         a certain amount of subtasks will be prebuilt into the list"""
        h = redis.get(model_key)
        if h is None: return []
        return [ProgressTask(
            root=root,
        ) for _ in range(max(int(h) - 1 , 0))]

    def _refresh_redis(self, update_model: bool):
        if self.root is not None:
            self.root._refresh_redis(update_model=update_model)
        else:
            # now self is root
            assert self.key is not None and self.redis is not None, "[Helpers] You must provide redis and key for progress task to refresh redis cache"
            self.redis.set(
                self.key,
                json.dumps(self.model_dump_circular_reference_safe()),
                ex=48 * 60 * 60 # expire after 48 hours
            )
            if self.model_key is not None and update_model:
                # we will update how many subtask it requires to complete
                logger.info(f"[Helper] Progress model update as total assigned={self.total_assigned}, model_key={self.model_key}")
                self.redis.set(
                    self.model_key,
                    self.total_assigned,
                    ex=30 * 24 * 60 * 60  # expire after 30 days
                )

    def new_subtask(self) -> "ProgressTask":
        # Avoid setting root to self, set it only to the rootmost instance
        if self.root is not None:
            self.root.new_subtask()
        else:
            # is root, handle subtask by itself
            # before creating any new subtask
            # we first search unassigned task object
            unassigned_list = [s for s in self.subtasks if not s.assigned]
            if len(unassigned_list) > 0:
                subtask = unassigned_list[0]
            else:
                subtask = ProgressTask(root=self)
                self.subtasks.append(subtask) # append this new subtask to list

            subtask.assigned = True # mark as assigned
            self._refresh_redis(update_model=self.is_root_success)
            return subtask


    def success(self):
        self.stage = ProgressTaskStage.SUCCESS
        self._refresh_redis(update_model=self.is_root_success)

    def failure(self, error: Optional[str] = None):
        self.stage = ProgressTaskStage.FAILURE
        self.error = error
        # all pending subtask need to mark as failure
        for s in self.subtasks:
            if s.stage == ProgressTaskStage.PENDING:
                s.failure()
        self._refresh_redis(update_model=self.is_root_success)

    @property
    def progress_report(self) -> ProgressReport:
        if self.root is not None: return self.progress_report
        total = 1 + len(self.subtasks)
        success_counts = len([s for s in [self] + self.subtasks if s.stage in [ProgressTaskStage.SUCCESS]])
        failure_counts = len([s for s in [self] + self.subtasks if s.stage in [ProgressTaskStage.FAILURE]])
        pending_counts = len([s for s in [self] + self.subtasks if s.stage in [ProgressTaskStage.PENDING]])
        errors = [s.error for s in [self] + self.subtasks if s.stage in [ProgressTaskStage.FAILURE] if s.error is not None]
        progress_floats = success_counts / total if total > 0 else 0
        return ProgressReport(
            progress_key=self.key,
            progress=progress_floats ,
            is_root_success=self.is_root_success,
            success=success_counts,
            failure=failure_counts,
            pending=pending_counts,
            assigned=self.total_assigned,
            total=total,
            errors=errors
        )

        # subtask_progress = [s.progress_report for s in self.subtasks]
        # total = 1 + len(self.subtasks)
        # progress_floats = [p.progress * (1 / total) for p in subtask_progress]
        #
        # success = sum([p.success for p in subtask_progress]) if len(subtask_progress) > 0 else 0
        # failure = sum([p.failure for p in subtask_progress]) if len(subtask_progress) > 0 else 0
        # pending = sum([p.pending for p in subtask_progress]) if len(subtask_progress) > 0 else 0
        # errors = reduce(lambda a, b: a + b, [p.errors for p in subtask_progress]) if len(subtask_progress) > 0 else []
        # if self.stage == ProgressTaskStage.SUCCESS:
        #     success += 1
        #     progress_floats.append(1 / total)
        # if self.stage == ProgressTaskStage.FAILURE:
        #     failure += 1
        #     if self.error is not None:
        #         errors.append(self.error)
        # if self.stage == ProgressTaskStage.PENDING:
        #     pending += 1

        # return ProgressReport(
        #     progress_key=self.key,
        #     progress=sum(progress_floats) if len(progress_floats) > 0 else 0,
        #     is_root_success=self.is_root_success,
        #     success=success,
        #     failure=failure,
        #     pending=pending,
        #     errors=errors
        # )

    def model_dump_circular_reference_safe(self) -> dict:
        """Custom model dump that excludes circular references."""
        return {
            "stage": self.stage,
            "error": self.error,
            "key": self.key,
            "subtasks": [s.model_dump_circular_reference_safe() for s in self.subtasks]
        }
        # return self.model_dump(exclude={"root", "subtasks", "redis"}, mode="json")
