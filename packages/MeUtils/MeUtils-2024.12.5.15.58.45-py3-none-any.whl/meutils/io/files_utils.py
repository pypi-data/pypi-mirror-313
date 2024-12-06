#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : MeUtils.
# @File         : file
# @Time         : 2022/7/5 下午3:31
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

import mimetypes
from meutils.pipe import *
from meutils.decorators.retry import retrying
# from fastapi import UploadFile 有点区别
from starlette.datastructures import UploadFile
from contextlib import asynccontextmanager


def file_append_firstline(line):
    with open('untitled.txt', "r+") as f:
        old = f.read()

        f.seek(0)
        f.write(line)
        f.write(old)


def base64_to_bytes(base64_image_string):
    """
    # 将字节数据写入图片文件
    image_data = base64_to_bytes(...)
    with open(filename, 'wb') as file:
        file.write(image_data)
    """
    return base64.b64decode(base64_image_string.split(",", 1)[-1])


@retrying()
async def to_bytes(file: Union[UploadFile, str, bytes], headers: Optional[dict] = None):  # plus
    """

    :param file: 文件对象、路径、base64、url
    :param headers: httpx

    :return: todo: bytes、filepath、io.BytesIO
    """
    # assert file

    logger.debug(type(file))

    if isinstance(file, bytes): return file

    file_bytes = None
    if isinstance(file, UploadFile):
        file_bytes = await file.read()

    elif isinstance(file, str) and file.startswith('http'):  # url
        resp = await httpx.AsyncClient(headers=headers or {}, timeout=60).get(file)
        file_bytes = resp.content

    elif isinstance(file, str) and len(file) > 256:  # base64
        file_bytes = base64_to_bytes(file)

    elif isinstance(file, str) and len(file) < 256 and Path(file).is_file():  # file
        file_bytes = Path(file).read_bytes()

    return file_bytes


@asynccontextmanager
async def to_tempfile(file: Union[UploadFile, str]):
    """

    :param file: 文件对象、路径、base64、url
    :return: todo: bytes、filepath、io.BytesIO
    """
    file_bytes = await to_bytes(file)

    with tempfile.NamedTemporaryFile(mode='wb+') as temp:
        temp.write(file_bytes)
        temp.seek(0)

        logger.debug(temp.name)

        yield temp.name


async def to_url(
        file: Union[UploadFile, str, bytes],
        filename: Optional[str] = None,
        headers: Optional[dict] = None,
        content_type: Optional[str] = "image/*"  # todo: 适配 mime_type = "application/octet-stream"
):
    """对象存储"""
    if not file: return

    from openai.types.file_object import FileObject
    from meutils.oss.minio_oss import Minio
    uploads = [partial(Minio().put_object_for_openai, filename=filename)]

    if isinstance(file, str) or filename:  # 不指定就自行判断 url
        content_type = mimetypes.guess_type(filename)[0] or mimetypes.guess_type(file)[0] or content_type

    if content_type and content_type.startswith("image"):
        from meutils.apis.chatglm.glm_video import upload_task as glm_upload
        from meutils.apis.hailuoai.videos import upload_for_oss as hailuo_upload

        uploads = [glm_upload, hailuo_upload] + uploads

    for upload in uploads:
        try:
            file = await to_bytes(file, headers=headers)
            url = await upload(file)
            if isinstance(url, FileObject):
                url = url.filename
            return url
        except Exception as e:
            logger.error(e)


async def to_base64(file: Union[UploadFile, str, bytes]):
    _ = base64.b64encode(await to_bytes(file)).decode('utf-8')

    content_type = isinstance(file, str) and mimetypes.guess_type(file)[0]  # str, bytes or os.PathLike
    logger.debug(content_type)

    return _


def base64_to_file(base64_image_string, filename):
    image_data = base64_to_bytes(base64_image_string)
    with open(filename, 'wb') as file:
        file.write(image_data)


def file_to_base64(file):
    _ = base64.b64encode(Path(file).read_bytes()).decode('utf-8')
    content_type = mimetypes.guess_type('img.webp')[0] or "data:image/jpeg"

    return f"data:{content_type},{_}"


async def to_file(file: Union[UploadFile, str, bytes], filename: Optional[str] = None):
    file = await to_bytes(file)
    if not filename:  # 临时文件
        with tempfile.NamedTemporaryFile(mode='wb+', delete=False) as temp:
            temp.write(file)
            temp.seek(0)
            return temp.name
    else:
        Path(filename).write_bytes(file)
        return Path(filename).resolve()


if __name__ == '__main__':
    # import tempfile
    #
    # # 使用上下文管理器自动处理文件的关闭和删除
    # with tempfile.NamedTemporaryFile(mode='wb+') as temp:
    #     temp.write(b"This is a temporary file.")
    #     temp.seek(0)
    #     print(f"文件内容: {temp.read()}")
    #     print(f"临时文件名: {temp.name}")
    # 文件在这里自动关闭和删除

    # arun(to_bytes(''))

    # arun(to_url("x.png"))

    # url = "https://storage.googleapis.com/bsp-remini-image-in-web-us-central1-autodelete/54a2d77f-3070-4a95-8a1b-906ac1c74d44/64439c90-c628-47e0-9e1b-36dbbbd06664/ba502f58/input.jpg?X-Goog-Algorithm=GOOG4-HMAC-SHA256&X-Goog-Credential=GOOG1ETQDJI557KBP4YD5TQG6FMZHVKCP3S53FHI6XLBYYMT24W3PZAZNZZWQ%2F20241014%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20241014T060335Z&X-Goog-Expires=3600&X-Goog-SignedHeaders=host&X-Goog-Signature=b7745e3639a1cb81465409bfa7ed20801c5b997945739810c32cb4af02304893"

    # arun(to_base64(url))[:100]

    url = "https://oss.ffire.cc/files/kling_watermark.png"

    # arun(to_file(url, filename='x.jpg'))

    # file = Path("/Users/betterme/PycharmProjects/AI/MeUtils/meutils/io/x.py").read_bytes()

    # arun(to_url(file, content_type=None))

    print(mimetypes.guess_type("x.jpg"))
    # print(mimetypes.guess_type("x.png"))
    print(mimetypes.guess_type("x"))

    print(mimetypes.guess_extension("x.mp4", False))

    # arun(to_url(
    #     "https://cdn.hailuoai.video/moss/prod/2024-11-11-09/video/1731287464150180347-video_raw_8ba15c5c206f8d393a9248f4f9215ed8_312186282087260162.mp4",
    #     content_type=None))
