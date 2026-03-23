import os
import uuid
import boto3
from werkzeug.utils import secure_filename
from config import Config

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION")  # now works
)


def upload_image(file):
    if not file or not file.filename:
        return None

    filename = f"{uuid.uuid4()}-{secure_filename(file.filename)}"

    s3.upload_fileobj(
        file,
        Config.S3_BUCKET,
        filename,
        ExtraArgs={"ContentType": file.content_type},
    )

    return f"https://{Config.S3_BUCKET}.s3.{Config.AWS_REGION}.amazonaws.com/{filename}"