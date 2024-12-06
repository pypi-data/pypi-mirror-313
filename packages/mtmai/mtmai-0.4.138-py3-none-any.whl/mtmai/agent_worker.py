"""
功能：通过 grpc 连接主服务，获取
"""

import asyncio
import json

import nsq
import redis
import structlog

from mtmai.agents.phiagents.workbrench_agent import workbrench_agent

LOG = structlog.get_logger()
# 消息服务地址（也是总后端）
mtm_backend_url = "http://localhost:8383"

redis_url = "redis://localhost:6379"

task_run_stream = "taskrun"

# 死信队列
topic_dlq = "deal"
topic_run_task = "taskrun"
nsqd_tcp_addresses = ["localhost:4150"]


class AgentWorker:
    """完全靠消息队列传递消息 的 agent 服务"""

    def __init__(self):
        self.pool = redis.ConnectionPool(host="localhost", port=6379, db=0)
        self.r = redis.Redis(connection_pool=self.pool)
        self.group_name = "my_consumer_group"  # 消费组名称
        self.consumer_name = "my_consumer"  # 消费者名称

        # 确保消费组存在
        try:
            self.r.xgroup_create(
                task_run_stream, self.group_name, id="0", mkstream=True
            )
        except redis.exceptions.ResponseError as e:
            if "BUSYGROUP Consumer Group name already exists" not in str(e):
                raise
        # 创建 NSQ 消费者
        # r = nsq.Reader(
        #     message_handler=Handler,
        #     nsqd_tcp_addresses=['127.0.0.1:4150'],  # NSQ 的 TCP 地址
        #     topic='test_topic',  # 订阅的主题
        #     channel='test_channel',  # 订阅的频道
        # )

    async def start(self):
        """从消息队列中获取任务，并执行"""
        try:
            LOG.info("start agent worker", topic=topic_run_task)

            self.publisher = nsq.Writer(nsqd_tcp_addresses=nsqd_tcp_addresses)
            self.publisher.connect()

            reader = nsq.Reader(
                topic=topic_run_task,
                channel="default-channel",
                message_handler=self.message_handler,
                lookupd_connect_timeout=10,
                requeue_delay=10,
                nsqd_tcp_addresses=nsqd_tcp_addresses,
                max_in_flight=5,
                snappy=False,
            )

        except Exception as e:
            LOG.error(f"An error occurred: {e}")

        # while True:
        #     # 从消费组中读取消息
        #     tasks = self.r.xreadgroup(
        #         self.group_name,
        #         self.consumer_name,
        #         {task_run_stream: ">"},
        #         count=1,
        #         block=0,
        #     )
        #     for task in tasks:
        #         stream_key = task[0]
        #         stream_data = task[1]
        #         msg_id, msg_data = stream_data[0]
        #         payload_data = msg_data.get("data")  # 解码任务名称
        #         # task_params = msg_data.get("task_params")
        #         task_payload = TaskPayload.model_validate(payload_data)
        #         # reply_to = msg_data.get(b"reply_to").decode("utf-8")  # 解码回复地址
        #         LOG.info(
        #             f"Received task: {msg_id}, data: {stack_data}, task_name: {task_name}, reply_to: {reply_to}"
        #         )

        #         # 处理任务
        #         await self.execute_task(task_name, reply_to)

        #         # 确认消息
        #         self.r.xack(task_run_stream, self.group_name, msg_id)

    async def stop(self):
        LOG.info("stop agent worker")

    async def execute_task(self, task_name, reply_to):
        """执行任务"""
        # phi_data_hello = PhiHelloAgent()

        async def fake_runner():
            """模拟任务执行"""
            LOG.info(f"Executing task with name: {task_name} and reply_to: {reply_to}")

            await asyncio.sleep(1)
            # LOG.info(f"Task executed: {task}")

    # 定义消息处理函数
    async def message_handler(self, message: nsq.Message):
        LOG.info(f"Received message: {message.body}")
        try:
            msg_obj = json.loads(str(message.body.decode("utf-8")))
            reply_to = msg_obj.get("reply_to", "deal")
            result = await workbrench_agent.arun(messages=[], stream=True)

            for i in range(10):
                # LOG.info(f"Executing task with name: {task_name} and reply_to: {reply_to}")
                result = f"result{i}"
                await asyncio.sleep(0.1)

            await self.publish_message(reply_to, result)
        except json.JSONDecodeError as e:
            LOG.error(f"Failed to decode JSON: {e}, message body: {message.body}")
            return False  # 返回 False 表示消息处理失败
        except Exception as e:
            LOG.error(f"An error occurred: {e}")
            return False  # 返回 False 表示消息处理失败

        return True  # 返回 True 表示消息处理成功

    async def publish_message(self, topic, message: str | bytes):
        """发送消息到指定的NSQ主题"""
        msg_bytes = message if isinstance(message, bytes) else message.encode("utf-8")

        LOG.info(f"Published message to topic: {topic}")
        self.publisher.pub(topic, msg_bytes, self.on_finnished_publish)

    def on_finnished_publish(self, conn, data):
        """发布完成回调"""
        LOG.info(f"Published message to topic: {data}")
