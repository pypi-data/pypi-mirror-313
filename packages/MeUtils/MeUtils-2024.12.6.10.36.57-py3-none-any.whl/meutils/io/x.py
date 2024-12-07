#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2024/9/25 15:27
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : 

from meutils.pipe import *
# from minio import Minio
from meutils.oss.minio_oss import Minio

# MinIO client setup
# minio_client = Minio(
#     "minio-server-url:9000",
#     access_key="your-access-key",
#     secret_key="your-secret-key",
#     secure=True  # set to False if not using HTTPS
# )
minio_client = Minio()


async def download_and_upload(video_url, bucket_name, object_name):
    buffer_size = 5 * 1024 * 1024  # 5MB buffer to meet MinIO's minimum part size

    async with httpx.AsyncClient() as client:
        try:
            async with client.stream("GET", video_url) as response:
                response.raise_for_status()

                total_size = int(response.headers.get('content-length', 0))
                buffer = io.BytesIO()
                uploaded = 0

                async for chunk in response.aiter_bytes(chunk_size=buffer_size):
                    buffer.write(chunk)
                    buffer_size = buffer.tell()
                    buffer.seek(0)

                    if buffer_size >= 5 * 1024 * 1024 or response.is_closed:
                        try:
                            minio_client.put_object(
                                bucket_name,
                                object_name,
                                buffer,
                                length=buffer_size,
                                part_size=5 * 1024 * 1024,
                                content_type='video/mp4'
                            )
                            uploaded += buffer_size
                            print(f"Uploaded {uploaded}/{total_size} bytes")

                        except Exception as upload_error:
                            print(f"Unexpected upload error: {upload_error}")
                            raise

                        buffer = io.BytesIO()  # Reset buffer after upload

                print("Upload completed")
        except httpx.HTTPStatusError as http_error:
            print(f"HTTP error occurred: {http_error}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    # Usage
    url = "https://s22-def.ap4r.com/bs2/upload-ylab-stunt-sgp/se/ai_portal_sgp_queue_m2v_txt2video_camera/b7eded0c-452c-4282-ad0a-02d96bd97f3e/0.mp4"
    bucket_name = "videos"
    object_name = "video11.mp4"

    with timer():
        arun(download_and_upload(url, bucket_name, object_name))
