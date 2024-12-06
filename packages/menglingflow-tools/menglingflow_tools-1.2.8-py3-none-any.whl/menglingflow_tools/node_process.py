import json
import base64
import subprocess
try:
    from menglingtool_redis.redis_tool import RedisExecutor
    from menglingtool.thread import thread_auto_run
except ModuleNotFoundError:
    subprocess.check_call(['pip','install', "menglingtool_redis", "menglingtool"])
    from menglingtool_redis.redis_tool import RedisExecutor
    from menglingtool.thread import thread_auto_run


def getEncode(data) -> str:
    js = json.dumps(data, ensure_ascii=False)
    return base64.b64encode(js.encode('utf-8')).decode('utf-8')


def getDecode(enc):
    decoded_data = base64.b64decode(enc).decode('utf-8')
    return json.loads(decoded_data)


class Node:
    def __init__(self, name, last_node, dt_func_ls,
                 thread_num=3):
        self.name = name
        self.last_node = last_node
        self.func = dt_func_ls
        self.getR = last_node.getR
        self.thread_num = thread_num

    def getInEncs(self):
        return self.last_node.getOutEncs()

    def getOutEncs(self) -> set:
        rst = set()
        with self.getR() as r:
            for enc in r.hvals(self.name):
                rst.update(enc.split('\n'))
        return rst

    def _ceil(self, enc):
        datas = self.func(getDecode(enc))
        value = '\n'.join(getEncode(data) for data in datas)
        with self.getR() as r:
            r.hset(self.name, enc, value)

    def run(self, restart=False):
        # 获取上节点的全部值
        encs_all = self.getInEncs()
        print(f'节点-{self.name} 输入数据量:{len(encs_all)}')
        with self.getR() as r:
            if restart:
                print('删除节点记录数据,重新开始任务...')
                r.delete(self.name)
            else:
                encs_have = set(r.hkeys(self.name))
                print(f'已完成数据量:{len(encs_have)}')
        thread_auto_run(self._ceil, encs_all - encs_have,
                        threadnum=self.thread_num, max_error_num=3)


# 首节点
class FNode(Node):
    def __init__(self, name, datas, dt_func_ls, r_connect,
                 thread_num=3):
        self.getR = lambda: RedisExecutor(**r_connect)
        super().__init__(name, self, dt_func_ls, thread_num=thread_num)
        self.datas = datas

    def getInEncs(self):
        return set(getEncode(data) for data in self.datas)


# 尾结点
class LNode(Node):
    def __init__(self, last_node):
        super().__init__(Node, last_node, None)

    def resultsit(self, num=10_000) -> list:
        encs = list(self.getInEncs())
        for i in range(0, len(encs), num):
            yield [getDecode(enc) for enc in encs[i: i + num]]

    def getOutEncs(self):
        return []

    def run(self):
        pass
