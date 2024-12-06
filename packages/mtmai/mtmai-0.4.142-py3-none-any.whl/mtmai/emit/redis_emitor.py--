import json
import time

import redis

# 连接到 Redis
r = redis.Redis(host="localhost", port=6379, db=0)


class RedisEmitor:
    def send_message(session_id, thread_id, message):
        message_id = f"{session_id}:{thread_id}:{int(time.time())}"
        message_data = {
            "sessionID": session_id,
            "threadID": thread_id,
            "message": message,
            "timestamp": time.time(),
        }

        # 存储消息
        r.hset(message_id, mapping=message_data)

        # 发布消息
        r.publish(f"chat:{session_id}:{thread_id}", json.dumps(message_data))

    def subscribe_messages(session_id, thread_id):
        pubsub = r.pubsub()
        pubsub.subscribe(f"chat:{session_id}:{thread_id}")

        for message in pubsub.listen():
            if message["type"] == "message":
                print("Received message:", json.loads(message["data"]))

    # 示例用法
    # send_message("session123", "thread456", "Hello, world!")
    # subscribe_messages("session123", "thread456")
