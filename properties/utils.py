from django.core.cache import cache
from django.http import request
from .models import Property
from django_redis import get_redis_connection
import logger
import uuid
from django_redis import get_redis_connection

def get_all_properties():
    """
    Fetch all properties from cache or database.
    Caches the queryset in Redis for 1 hour (3600 seconds).

    Returns:
        QuerySet: All Property objects
    """
    cached_properties=cache.get("all_properties")
    if cached_properties is not None:
        print("Returning cached properites")
        return cached_properties
    
    """If there is no cached properties it fetches from the database"""
    print("fetching data from the database")
    properties=Property.objects.all()

    """convert to list to make it serializable for Redis"""
    list_properties=list(properties.values('property_id', 'title', 'description', 'price', 'location', 'created_at'))
    if not list_properties:
        print("oops there is no data in the database. Adding sample data ...")
        sample_data=[
            {
                'property_id': str(uuid.uuid4()),
                'title': 'pr1',
                'description': 'sample property1.',
                'price': 999.99,
                'location': 'Bremen'
            },
             {
                'property_id': str(uuid.uuid4()),
                'title': 'pr2',
                'description': 'sample property2.',
                'price': 110000.99,
                'location': 'London'
            },
               {
                'property_id': str(uuid.uuid4()),
                'title': 'pr3',
                'description': 'sample property3.',
                'price': 876.99,
                'location': 'Berlin'
            }



        ]

        for p in sample_data:
            Property.objects.create(**p)
        properties=Property.objects.all()
        properties_list=list(properties.values('property_id', 'title', 'description', 'price', 'location', 'created_at'))

    cache.set("all_properties",properties_list,3600)
    return {
        "status": "success",
        "status_code": 200,
        "message": "Properties fetched successfully",
        "data": properties_list
    }


def get_redis_cache_metrics():
    """
    connect to Redis and retrieve cache hit/miss metrics 
    Returned a dictionary with hits,misses and hit_ratio

    """
    try:
        redis_conn=get_redis_connection("default")
        info=redis_conn.info("stats")
        hits=info.get("keyspace_hits",0)
        misses=info.get("keyspace_misses",0)

        total_requests=hits+misses
        if total_requests > 0:
            hit_ratio = (hits / total_requests) * 100
        else:
            hit_ratio = 0.0

        metrics={
            "hits":hits,
            "misses":misses,
            "hit_ratio":round(hit_ratio,2)
        }
        logger.info(f"Redis Cache Metrics: {metrics}")

        return metrics
    except Exception as e:
        logger.error(f"Failed to retrieve Redis metrics: {e}")
        return {"hits": 0, "misses": 0, "hit_ratio": 0.0}


