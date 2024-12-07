from redis import Redis

from .schemas import ProgressTask, ProgressReport
import logging
logger = logging.getLogger(__name__)

class ProgressHandler:

    def __init__(self, redis: Redis):
        self._redis = redis

    def new(self, *,

            key: str,
            model_key: str | None = None
            ) -> ProgressTask:
        """
        Build a progress task object, you can provide 2 key
        :param key: to save this task progress, key can be used to retrieve progress percentage
        :param model_key:
        :return:
        """

        root = ProgressTask(redis=self._redis, key=key, model_key=model_key)
        if model_key is not None:
            prebuilt_tasks = ProgressTask.get_prebuilt_subtasks_model(root=root,
                                                                      redis=self._redis, model_key=model_key)
            root.subtasks = prebuilt_tasks
        logger.info(f'[Helper] Progress task inited, and initialized state: {str(root)}')
        return root

    def get(self, *, key: str) -> ProgressReport | None:
        t = ProgressTask.get_from_redis(redis=self._redis, key=key)
        if t is None: return None
        return t.progress_report
