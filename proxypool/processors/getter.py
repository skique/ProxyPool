

from loguru import logger
from proxypool.storages.redis import RedisClient
import requests
from proxypool.schemas.proxy import Proxy
from proxypool.setting import GENERATE_PROXY_API

class Getter(object):
    """
    getter of proxypool
    """
    
    def __init__(self):
        """
        init db and crawlers
        """
        self.redis = RedisClient()
    
    @logger.catch
    def run(self):
        """
        run crawlers to get proxy
        :return:
        """
        response = requests.get(GENERATE_PROXY_API)
        result = response.json()
        code = result['code']
        if code == 0:
            data = result['data']
            for item in data:
                proxy = Proxy(host=item['ip'], port=item['port'])
                # proxtStr = proxy.string()
                self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
