# from loguru import logger
# import os
# import typing
# from typing import Optional

# import boto3
# import jsonlines
# import orjson
# import parse


# from good_common.dependencies import BaseProvider

# class S3Object:
#     def __init__(self, client, obj):
#         self._client = client
#         self._obj = obj

#         properties = parse.parse(
#             "Batch_Results_{batch_id}_{result_id}_Page_{page_id}.jsonl", self.key
#         )
#         if properties:
#             self.batch_id = properties["batch_id"]
#             self.result_id = properties["result_id"]
#             self.page_id = properties["page_id"]

#     @property
#     def obj(self):
#         return self._obj

#     @property
#     def key(self):
#         return self.obj.key

#     def read(self):
#         return orjson.loads(self._obj.get()["Body"].read())

#     def read_jsonlines(self) -> jsonlines.Reader:
#         # iter_lines
#         # return jsonlines.Reader(io.BytesIO(self.read()), loads=orjson.loads)
#         return jsonlines.Reader(
#             self._obj.get()["Body"].iter_lines(), loads=orjson.loads
#         )

#     def __repr__(self):
#         return f"<S3Object key={self.key}>"


# class S3Bucket:
#     def __init__(
#         self,
#         bucket_name: str,
#         aws_access_key_id: Optional[str] = None,
#         aws_secret_access_key: Optional[str] = None,
#     ):
#         self._cache = {}

#         self._client = boto3.resource(
#             "s3",
#             aws_access_key_id=aws_access_key_id or os.environ.get("AWS_ACCESS_TOKEN"),
#             aws_secret_access_key=aws_secret_access_key
#             or os.environ.get("AWS_SECRET_KEY"),
#         )

#         self._bucket = self._client.Bucket(bucket_name)

#     def get_object(self, key) -> S3Object:
#         return self._cache.get(key, S3Object(self, self._bucket.Object(key)))

#     def iter_items(self, prefix=None):
#         for obj in (
#             self._bucket.objects.filter(Prefix=prefix)
#             if prefix
#             else self._bucket.objects.all()
#         ):
#             obj = S3Object(self, obj)
#             self._cache[obj.key] = obj
#             yield obj


# class S3BucketProvider(BaseProvider[S3Bucket], S3Bucket):
#     def initializer(
#         self,
#         cls_args: typing.Tuple[typing.Any, ...],
#         cls_kwargs: typing.Dict[str, typing.Any],
#         fn_kwargs: typing.Dict[str, typing.Any],
#     ):
#         logger.info((cls_kwargs, fn_kwargs))

#         return cls_args, {
#             **cls_kwargs,
#             **fn_kwargs,
#         }
