import os
import threading

from ..strop import restrop
from ..sc import SCError

import paho.mqtt.client as mqtt

class Mqttop:
    def __init__(self, host: str, port: int, clientid: str = '', subtopic: str = '',
                 user: str = '', passwd: str = '',
                 data_length: int = 200,
                 bool_show: bool = True, bool_clean_session: bool = False):
        """
        调用self.publish()函数发布信息

        :param host: MQTT服务器IP地址
        :param port: MQTT端口
        :param clientid: 可选, "客户端"用户名 为空将随机
        :param subtopic: 选填, 需要订阅的主题 通过self.getdata()获得接收到的信息 为空时仅连接[此时可进行发布信息]; 更换订阅主题需要使用self.retopic()函数[自动重连]

        :param user: 选填, 账号
        :param passwd: 选填, 密码

        :param data_length: 缓存数据列表的长度 默认为200

        :param bool_show: 是否打印提示
        :param bool_clean_session: 断开连接时是否删除有关此客户端的所有信息
        """
        self.__got_datas: lsit[bytes] = []  # 接收到的数据
        self.bool_show = bool_show  # 是否终端打印连接相关信息
        self.bool_con_success = False  # 是否连接成功
        self.bool_clean_session = bool_clean_session  # 在断开连接时是否删除有关此客户端的所有信息, 若clientid参数为空, 将强制为True

        if host:
            self.host = host
        else:
            raise SCError("主机地址为空")
        if port:
            self.port = int(port)
        else:
            raise SCError("端口未配置")
        self.clientid = clientid
        self.subtopic = subtopic
        self.user = user
        self.passwd = passwd

        self.data_length = data_length if data_length > 0 else 200

        if len(self.clientid) == 0 or self.clientid is None:
            self.__client = mqtt.Client(client_id="", clean_session=True)  # 创建对象, 强制clean_session=True
        else:
            self.__client = mqtt.Client(client_id=self.clientid, clean_session=self.bool_clean_session)  # 创建对象
        # self.start()

    def __del__(self):
        """
        删除对象时调用__del__()断开连接
        """
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return exc_type, exc_val, exc_tb

    def set_will(self, will_topic: str, will_msg: str):
        """
        设置遗嘱, 需要在连接前设置
        :param will_topic: 遗嘱主题
        :param will_msg: 遗嘱信息
        """
        self.__client.will_set(will_topic, will_msg, 0, False)
        print(f"遗嘱信息: will_topic[`{restrop(will_topic, f=6)}`] will_msg[`{restrop(will_msg, f=4)}`] 已设置")

    def start(self):
        """
        启动MQTT连接, 建议使用time.sleep(5)等待连接完成
        :return:
        """
        threading.Thread(target=self.__run, daemon=True).start()  # 开启线程防止阻塞主程序, 使用.close()函数自动关闭该线程

    def connect(self):
        """
        启动MQTT连接, 建议使用time.sleep(5)等待连接完成
        :return:
        """
        return self.start()

    def close(self):
        """
        断开MQTT连接
        """

        # 断开MQTT连接
        self.__client.disconnect()
        # 停止循环
        self.__client.loop_stop()

        if self.bool_show and self.bool_con_success:
            print(restrop("MQTT连接已关闭"))

        self.bool_con_success = False

    def disconnect(self):
        return self.close()

    # 断开连接回调
    def __on_disconnect(self, client, userdata, rc):
        """

        """
        if self.bool_show and self.bool_con_success:
            print(f"MQTT连接已断开")
        self.bool_con_success = False

    # 连接后事件
    def __on_connect(self, client, userdata, flags, respons_code):
        """
        respons_code的含义\n
        0:连接成功\n
        1:连接被拒绝-协议版本不正确\n
        2:连接被拒绝-客户端标识符无效\n
        3:连接被拒绝-服务器不可用\n
        4:连接被拒绝-用户名或密码错误\n
        5:连接被拒绝-未授权\n
        6-255:当前未使用\n

        :param client:
        :param userdata:
        :param flags:
        :param respons_code:
        :return:
        """
        if respons_code == 0:
            # 连接成功
            if self.bool_show:
                print(restrop('MQTT服务器 连接成功!', f=2))
            self.bool_con_success = True
        else:
            # 连接失败并显示错误代码
            if self.bool_show:
                print(restrop(f'连接出错 rc={respons_code}'))
            self.bool_con_success = False
        # 订阅信息
        if self.subtopic:
            self.__client.subscribe(self.subtopic)
            if self.bool_show:
                print(f"当前订阅的主题: `{restrop(self.subtopic, f=4)}`")

    # 接收到数据后事件
    def __on_message(self, client, userdata, msg):
        self.__got_datas.append(msg.payload)
        if len(self.__got_datas) >= self.data_length:
            self.__got_datas = self.__got_datas[-self.data_length:]  # 数据阶段

    # 启动连接
    def __run(self):
        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message
        self.__client.on_disconnect = self.__on_disconnect
        # 设置账号密码
        if self.user:
            client.username_pw_set(self.user, password=self.passwd)
        # 连接到服务器
        self.__client.connect(self.host, port=self.port, keepalive=60)
        # 守护连接状态
        self.__client.loop_forever()

    # 发布消息
    def publish(self, topic: str, msg: str, bool_show_tip: bool = True):
        """

        :param topic: 发布消息的主题
        :param msg: 需要发布的消息
        :param bool_show_tip: 是否打印是否发送成功的信息
        :return:
        """
        result = self.__client.publish(topic, msg)
        status = result[0]
        if status == 0 and bool_show_tip:
            print(f"{restrop('发送成功', f=2)} TOPIC[`{restrop(topic, f=6)}`]  MSG[`{restrop(msg, f=4)}`]")
        elif bool_show_tip:
            print(f"{restrop('发送失败')} TOPIC[`{restrop(topic, f=6)}`]  MSG[`{restrop(msg, f=4)}`]")

    def retopic(self, new_topic: str):
        """
        更换订阅的主题, 并自动尝试重连
        :param new_topic: 新的订阅主题
        :return:
        """
        if self.subtopic != new_topic:
            self.subtopic = new_topic

            if self.bool_show:
                print(restrop("已更换订阅的主题, MQTT服务器正在尝试重连. . .", f=3))

            self.reconnect()

    def reconnect(self):
        """
        尝试重连
        :return: None
        """
        self.close()
        self.start()

    def getdata(self, index: int = 0, bool_del_data: bool = True, bool_all: bool = False):
        """
        获取接收到的数据
        :param index: 获取的数据的索引 默认为0
        :param bool_del_data: 获取数据时是否删除数据
        :param bool_all: 是否获取所有数据
        :return: bytes(something) 返回bytes类型的数据
        """
        if self.__got_datas:
            # print(len(self.__got_datas))
            if not bool_all:  # 获取单个数据
                if bool_del_data:  # 获取数据并删除
                    return self.__got_datas.pop(index)
                else:  # 获取数据但不删除
                    return self.__got_datas[index]
            else:  # 获取所有数据
                if bool_del_data:  # 获取数据并删除
                    temp = self.__got_datas
                    self.__got_datas = []
                    return temp
                else:  # 获取数据但不删除
                    return self.__got_datas
        else:
            return None
