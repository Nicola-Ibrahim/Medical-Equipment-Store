import random

from django.utils.text import slugify


def slugify_instance_name(instance, new_slug=None):
    """
    Create a unique slug value
    -----
    Checking slug existence by apply recursion
    """

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    # Check if the new slug is existed
    klass = instance.__class__
    qs = klass.objects.filter(slug=slug).exclude(id=instance.id)
    if qs.exists():
        slug = f"{slug}-{random.randint(300_000, 500_000)}"
        return slugify_instance_name(instance, slug)

    instance.slug = slug

    return instance


def send_msg(value):
    msg = f"Your order has been {value}"
    print(msg)
