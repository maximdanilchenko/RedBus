import json

import redis


class RedBusExecutionError(Exception):
    pass


class RedBus:
    def __init__(self, name, r=None, j=None):
        self.name = name
        self.funcs = {}
        self.r = r or redis.StrictRedis()
        self.json = j or json
        self.sub = self.r.pubsub()
        self.sub.subscribe(self.name)

    def listen(self):
        while True:
            msg = self.sub.get_message(ignore_subscribe_messages=True)
            if msg:
                msg = self.json.loads(msg['data'])
                func, args, kwargs, from_ = msg['func'], msg.get('args', []), msg.get('kwargs', {}), msg['from']
                if func in self.funcs:
                    res = self.execute(self.funcs[func], *args, **kwargs)
                    self.r.publish(from_, res)

    def execute(self, func, *args, **kwargs):
        try:
            res = self.json.dumps({'result': func(*args, **kwargs)})
        except Exception as e:
            res = self.json.dumps({'__e': str(e), 'result': None})
        return res

    def add_func(self, func):
        self.funcs[func.__name__] = func

    def call(self, address, func, *args, **kwargs):
        self.r.publish(address, self.json.dumps({'func': func, 'args': args, 'kwargs': kwargs, 'from': self.name}))
        while True:
            msg = self.sub.get_message(ignore_subscribe_messages=True)
            if msg:
                res = self.json.loads(msg['data'])
                if res.get('__e'):
                    raise RedBusExecutionError(res['__e'])
                return res['result']


