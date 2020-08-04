# _*_encoding:utf-8_*_

from websocket_server import WebsocketServer
import json

HOST = '127.0.0.1'
PORT = 8989

'''
data:数据结构
{
    'send_client':'',           # 发送客户端id
    'send_type':'',             # 发送类型：msg-聊天，new_connect-连接提示，client_count-连接数量
    'msg':'',                   # 消息内容
    'client_count':''           # 在线数量
}

'''


# 处理消息
def message_received(client, server, message):
    # if len(message) > 200:
    #     message = message[:200]+'..'
    print("Client(%d) speak: %s" % (client['id'], message))
    try:
        data = {'send_client': client['id'],
                'send_type': 'msg',
                'msg':message
                }
        # 发送消息给所有连接
        server.send_message_to_all(json.dumps(data))
    except:
        pass

# 有新连接时，执行的方法
def new_client(client, server):
    client_set.add(client['id'])
    data = {'send_client': client['id'],
            'send_type':'new_connect',
            }
    # 给当前客户端发送消息
    server.send_message(client,json.dumps(data))
    # 用来给所有客户端更新在线人数
    client_close(client, server, False)

# 客户端断开连接
def client_close(client, server,flag=True):
    if flag:
        # 删除断开连接的客户端id
        client_set.discard(client['id'])
    data = {
        'send_client': client['id'],
        'send_type': 'client_count',
        'client_count': len(client_set)
    }
    server.send_message_to_all(json.dumps(data))

def start_websocket_server():
    server = WebsocketServer(PORT, HOST)
    # 有设备连接上，
    server.set_fn_new_client(new_client)
    # 有设备断开连接
    server.set_fn_client_left(client_close)
    # 接收到信息
    server.set_fn_message_received(message_received)
    # 开始监听
    server.run_forever()


if __name__ == '__main__':
    # 存储客户端连接id
    client_set = set()
    start_websocket_server()
