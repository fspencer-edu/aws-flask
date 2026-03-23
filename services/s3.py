import json
import mimetypes
import uuid
from datetime import datetime, timezone

import boto3
from botocore.config import Config as BotoConfig
from werkzeug.utils import secure_filename

from config import Config

s3 = boto3.client(
    "s3",
    region_name=Config.AWS_REGION,
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    config=BotoConfig(signature_version="s3v4"),
)


def upload_image(file):
    if not file or not file.filename:
        return None

    key = f"uploads/{uuid.uuid4()}-{secure_filename(file.filename)}"

    content_type, _ = mimetypes.guess_type(file.filename)
    if not content_type:
        content_type = "application/octet-stream"

    s3.upload_fileobj(
        file,
        Config.S3_BUCKET,
        key,
        ExtraArgs={"ContentType": content_type},
    )

    return key


def generate_image_url(key):
    if not key:
        return None

    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": Config.S3_BUCKET, "Key": key},
        ExpiresIn=3600,
    )


def save_entry(title, content, image_key):
    entry_id = str(uuid.uuid4())
    entry_key = f"entries/{entry_id}.json"

    entry = {
        "id": entry_id,
        "title": title,
        "content": content,
        "image_key": image_key,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    s3.put_object(
        Bucket=Config.S3_BUCKET,
        Key=entry_key,
        Body=json.dumps(entry).encode("utf-8"),
        ContentType="application/json",
    )


def get_all_entries():
    response = s3.list_objects_v2(Bucket=Config.S3_BUCKET, Prefix="entries/")
    contents = response.get("Contents", [])

    entries = []

    for obj in contents:
        key = obj["Key"]
        if not key.endswith(".json"):
            continue

        file_obj = s3.get_object(Bucket=Config.S3_BUCKET, Key=key)
        data = json.loads(file_obj["Body"].read().decode("utf-8"))

        image_key = data.get("image_key")
        data["image_url"] = generate_image_url(image_key) if image_key else None

        print("ENTRY:", data)

        entries.append(data)

    entries.sort(key=lambda x: x["created_at"], reverse=True)
    return entries