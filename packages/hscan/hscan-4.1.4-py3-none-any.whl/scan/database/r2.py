import io
import boto3
import botocore.exceptions
from scan.common import logger


class CFR2:
    def __init__(self, **kwargs):
        self.account_id = kwargs.get('account_id')
        self.aws_access_key_id = kwargs.get('aws_access_key_id')
        self.aws_secret_access_key = kwargs.get('aws_secret_access_key')
        self.r2_client = boto3.client('s3', endpoint_url=f'https://{self.account_id}.r2.cloudflarestorage.com',
                                      aws_access_key_id=self.aws_access_key_id,
                                      aws_secret_access_key=self.aws_secret_access_key)

    async def upload(self, bucket_name, resp, file_name):
        """
        :param bucket_name:
        :param resp:
        :param file_name:
        :return:
        小文件上传
        """
        content = resp.content()
        byte_stream_file_obj = io.BytesIO(content)
        try:
            # 上传字节流文件对象到S3存储桶中
            self.r2_client.upload_fileobj(byte_stream_file_obj, bucket_name, file_name)
            logger.info(f'Uploaded {file_name} to {bucket_name}')
            return True
        except botocore.exceptions.ClientError as e:
            logger.error(f'Error uploading {file_name}: {e}')
        return False

    async def upload_bytes(self, bucket_name, file_bytes, file_name):
        """
        :param bucket_name:
        :param file_bytes:
        :param file_name:
        :return:
        小文件上传
        """
        byte_stream_file_obj = io.BytesIO(file_bytes)
        try:
            # 上传字节流文件对象到S3存储桶中
            self.r2_client.upload_fileobj(byte_stream_file_obj, bucket_name, file_name)
            logger.info(f'Uploaded {file_name} to {bucket_name}')
            return True
        except botocore.exceptions.ClientError as e:
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
            # 逐块上传流数据到S3存储桶中
            self.r2_client.create_multipart_upload(Bucket=bucket_name, Key=file_name)
            upload_id = self.r2_client.create_multipart_upload(Bucket=bucket_name, Key=file_name)['UploadId']

            part_number = 1
            uploaded_parts = []
            part_size = 5 * 1024 * 1024  # 每块5MB，小了要报错

            async for chunk in resp.response.aiter_bytes(chunk_size=part_size):
                if chunk:
                    part = self.r2_client.upload_part(
                        Body=chunk,
                        Bucket=bucket_name,
                        Key=file_name,
                        PartNumber=part_number,
                        UploadId=upload_id
                    )
                    uploaded_parts.append({'PartNumber': part_number, 'ETag': part['ETag']})
                    part_number += 1

            self.r2_client.complete_multipart_upload(
                Bucket=bucket_name,
                Key=file_name,
                UploadId=upload_id,
                MultipartUpload={'Parts': uploaded_parts}
            )
            logger.info(f'Uploaded {file_name} from stream to {bucket_name}')
            return True
        except Exception as e:
            logger.error(f'Error uploading {file_name}: {e}')
        return False
