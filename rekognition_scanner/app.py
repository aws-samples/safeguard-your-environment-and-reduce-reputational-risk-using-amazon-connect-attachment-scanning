# Invoke Amazon Rekognition moderate_content API and passing the attachment
from __future__ import annotations
from enum import Enum
from re import sub
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.parser import event_parser, BaseModel
from aws_lambda_powertools import Logger
from aws_lambda_powertools import Tracer
from aws_lambda_powertools import Metrics
import boto3

tracer = Tracer()
logger = Logger()
metrics = Metrics(namespace="AttachmentScanner")

def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))

class S3Location(BaseModel):
    key: str
    bucket: str
    arn: str

    class Config:
        alias_generator = to_camel


class FileLocation(BaseModel):
    s3_location: "S3Location"

    class Config:
        alias_generator = to_camel


class File(BaseModel):
    file_id: str
    file_creation_time: int
    file_name: str
    file_size_in_bytes: int
    file_location: "FileLocation"

    class Config:
        alias_generator = to_camel


class ScanningRequest(BaseModel):
    version: str
    instance_id: str
    file: "File"

    class Config:
        alias_generator = to_camel


class Status(str, Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
@metrics.log_metrics(capture_cold_start_metric=True)
@event_parser(model=ScanningRequest)
def lambda_handler(scanning_request: ScanningRequest, context: LambdaContext) -> dict:
    attachment_bucket = scanning_request.file.file_location.s3_location.bucket
    attachment_key = scanning_request.file.file_location.s3_location.key
    s3_client = boto3.client("s3")
    head_object_result = s3_client.head_object(
        Bucket=attachment_bucket, Key=attachment_key
    )
    content_type = head_object_result["ContentType"]
    if content_type in ["image/jpeg", "image/png"]:
        try:
            labels = moderate_content(attachment_bucket, attachment_key)
        except Exception as e:
            logger.error(f"Unable to get moderation labels due to: {e}")
            return {"Status": Status.REJECTED}
        if len(labels) > 0:
            logger.info("This image may have unsafe content, rejecting it")
            return {"Status": Status.REJECTED}
        else:
            return {"Status": Status.APPROVED}
    else:
        return {"Status": Status.APPROVED}


def moderate_content(bucket: str, key: str) -> list:
    client = boto3.client("rekognition")
    response = client.detect_moderation_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": key}}
    )
    logger.info(
        f"Detected following labels for {bucket}/{key}: {response['ModerationLabels']}"
    )
    return response["ModerationLabels"]

