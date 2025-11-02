from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

CACHE_KEY = "all_properties"

@receiver(post_save,sender=Property)
def invalidate_cache_on_save(sender,instance,**kwargs):
    """Invalidates all properties when a Property is created or deleted"""
    cache.delete(CACHE_KEY)
    print(f"Cache invalidated property: '{instance.title}' was saved ")

@receiver(post_delete,sender=Property)
def invalidate_cache_on_delete(sender,instance,**kwargs):
    cache.delete(CACHE_KEY)
    print(f"Cache invalidated: Property '{instance.title}' was deleted")