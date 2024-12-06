from robot_base import func_decorator

from .spark_api import *


@func_decorator
def spark_api(appid, api_secret, api_key, domain, query, **kwargs):
    api = SparkApi(
        appid=appid,
        api_secret=api_secret,
        api_key=api_key,
        domain=domain,
        query=query,
    )
    return api.get_response()
