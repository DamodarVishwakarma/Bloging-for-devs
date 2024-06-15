import uuid


def unique_media_upload(instance, filename):
    ext = filename.split('.').pop()

    return f"images/{instance._meta.model_name}/{instance.id}/{uuid.uuid4().hex[:6]}.{ext}"

def icon_media_upload(instance, filename):
    ext = filename.split('.').pop()

    return f"images/{instance._meta.model_name}_icon/{instance.slug}-{uuid.uuid4().hex[:6]}.{ext}"



