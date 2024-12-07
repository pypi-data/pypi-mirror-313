from motor.motor_asyncio import AsyncIOMotorCollection
from functools import wraps
from pymongo.errors import DuplicateKeyError


class MongoMiddleware:
    def __init__(self):
        self.insert_success_count = 0
        self.insert_repeat_count = 0
        self.insert_fail_count = 0
        self.update_success_count = 0
        self.update_fail_count = 0
        self._patch_methods()

    def _patch_methods(self):
        original_insert_one = AsyncIOMotorCollection.insert_one
        original_update_one = AsyncIOMotorCollection.update_one

        @wraps(original_insert_one)
        async def patched_insert_one(collection, document, *args, **kwargs):
            """
            插入补丁
            """
            try:
                result = await original_insert_one(collection, document, *args, **kwargs)
                self.insert_success_count += 1
                return result
            except DuplicateKeyError:
                self.insert_repeat_count += 1
                raise
            except Exception:
                self.insert_fail_count += 1
                raise

        @wraps(original_update_one)
        async def patched_update_one(filter, update, *args, **kwargs):
            """
            更新补丁
            """
            try:
                result = await original_update_one(filter, update, *args, **kwargs)
                self.update_success_count += 1
                return result
            except Exception:
                self.update_fail_count += 1
                raise

        AsyncIOMotorCollection.insert_one = patched_insert_one
        AsyncIOMotorCollection.update_one = patched_update_one

    def get_count(self):
        result = self.insert_success_count, self.insert_repeat_count, self.insert_fail_count, \
                 self.update_success_count, self.update_fail_count
        self.insert_success_count = self.insert_repeat_count = self.insert_fail_count = \
            self.update_success_count = self.update_fail_count = 0
        return result
