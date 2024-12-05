from gevent import sleep
from async_dfd.node import Node

def test_node():
    func = lambda x: x * 2
    node = Node(func, no_output=True)
    node.start()
    node.put(1)
    while True:
        sleep(1)
    
if __name__ == "__main__":
    test_node()