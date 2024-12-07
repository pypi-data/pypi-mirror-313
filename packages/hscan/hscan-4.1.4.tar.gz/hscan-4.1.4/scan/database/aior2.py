import io
import asyncio
from contextlib import AsyncExitStack
from aiobotocore.session import AioSession
from scan.common import logger


class AioCFR2:
    def __init__(self, **kwargs):
        self.account_id = kwargs.get('account_id')
        self.aws_access_key_id = kwargs.get('aws_access_key_id')
        self.aws_secret_access_key = kwargs.get('aws_secret_access_key')
        self.session = AioSession()
        self.client = None
        self.lock = asyncio.Lock()

    async def create_s3_client(self):
        exit_stack = AsyncExitStack()
        client = await exit_stack.enter_async_context(
            self.session.create_client('s3',
                                       aws_access_key_id=self.aws_access_key_id,
                                       aws_secret_access_key=self.aws_secret_access_key,
                                       endpoint_url=f'https://{self.account_id}.r2.cloudflarestorage.com')
        )
        return client

    async def initialize(self):
        async with self.lock:
            if not self.client:
                self.client = await self.create_s3_client()

    async def close(self):
        if self.client:
            await self.client.close()

    async def upload(self, bucket_name, resp, file_name):
        """
        :param bucket_name:
        :param resp:
        :param file_name:
        :return:
        小文件上传
        """
        try:
            if not self.client:
                await self.initialize()
            content = resp.content()
            if not content:
                return False
            byte_stream_file_obj = io.BytesIO(content)
            try:
                # 上传字节流文件对象到S3存储桶中
                res = await self.client.put_object(Body=byte_stream_file_obj, Bucket=bucket_name, Key=file_name)
                await resp.aclose()
                if not res:
                    logger.error(f'Uploaded {file_name} to {bucket_name} fail')
                    return False
                if res.get('ResponseMetadata', {}).get('HTTPStatusCode') != 200:
                    logger.error(f'Uploaded {file_name} to {bucket_name} fail')
                    return False
                logger.info(f'Uploaded {file_name} to {bucket_name}')
                return True
            except Exception as e:
                logger.error(f'Error uploading {file_name}: {e}')
            return False
        except Exception as e:
            logger.error(f'Upload process error: {e}')
            await resp.aclose()

    async def upload_bytes(self, bucket_name, file_bytes, file_name):
        """
        :param bucket_name:
        :param file_bytes:
        :param file_name:
        :return:
        小文件上传
        """
        try:
            if not self.client:
                await self.initialize()
            byte_stream_file_obj = io.BytesIO(file_bytes)
            # 上传字节流文件对象到S3存储桶中
            res = await self.client.put_object(Body=byte_stream_file_obj, Bucket=bucket_name, Key=file_name)
            if not res:
                logger.error(f'Uploaded {file_name} to {bucket_name} fail')
                return False
            if res.get('ResponseMetadata', {}).get('HTTPStatusCode') != 200:
                logger.error(f'Uploaded {file_name} to {bucket_name} fail')
                return False
            logger.info(f'Uploaded {file_name} to {bucket_name}')
            return True
        except Exception as e:
            logger.error(f'Error uploading {file_name}: {e}')
        return False

    async def upload_large(self, bucket_name, resp, file_name):
        """
        :param bucket_name:  桶名
        :param resp: 流式请求的响应
        :param file_name: 保存的文件名
        :return: 上传成功或失败
        用于处理大文件上传，不过小文件也可以上传
        """
        try:
            if not self.client:
                await self.initialize()
            # 逐块上传流数据到S3存储桶中
            upload_id = (await self.client.create_multipart_upload(Bucket=bucket_name, Key=file_name)).get('UploadId')
            part_number = 1
            uploaded_parts = []
            part_size = 5 * 1024 * 1024  # 每块5MB，小了要报错

            async for chunk in resp.response.aiter_bytes(chunk_size=part_size):
                if chunk:
                    part = await self.client.upload_part(
                        Body=chunk,
                        Bucket=bucket_name,
                        Key=file_name,
                        PartNumber=part_number,
                        UploadId=upload_id
                    )
                    uploaded_parts.append({'PartNumber': part_number, 'ETag': part['ETag']})
                    part_number += 1

            res = await self.client.complete_multipart_upload(
                Bucket=bucket_name,
                Key=file_name,
                UploadId=upload_id,
                MultipartUpload={'Parts': uploaded_parts}
            )
            await resp.aclose()
            if not res:
                logger.error(f'Uploaded {file_name} to {bucket_name} fail')
                return False
            if res.get('ResponseMetadata', {}).get('HTTPStatusCode') != 200:
                logger.error(f'Uploaded {file_name} to {bucket_name} fail')
                return False
            logger.info(f'Uploaded {file_name} from stream to {bucket_name}')
            return True
        except Exception as e:
            logger.error(f'Error uploading {file_name}: {e}')
            await resp.aclose()
        return False
