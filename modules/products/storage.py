import os
import uuid

from supabase import create_client


BUCKET_NAME = "product_url"

ALLOWED_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


def upload_product_image(file_bytes, content_type):
    """
    Upload an image to Supabase Storage and return its public URL.
    """

    if content_type not in ALLOWED_TYPES:
        raise ValueError("Unsupported image type.")

    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SECRET_KEY")

    if not supabase_url or not supabase_key:
        raise RuntimeError(
            "Supabase Storage environment variables are missing."
        )

    supabase = create_client(
        supabase_url,
        supabase_key
    )

    extension = ALLOWED_TYPES[content_type]
    filename = f"{uuid.uuid4().hex}{extension}"

    supabase.storage.from_(BUCKET_NAME).upload(
        path=filename,
        file=file_bytes,
        file_options={
            "content-type": content_type,
            "upsert": "false",
            "cache-control": "3600",
        },
    )

    return supabase.storage.from_(
        BUCKET_NAME
    ).get_public_url(filename)
