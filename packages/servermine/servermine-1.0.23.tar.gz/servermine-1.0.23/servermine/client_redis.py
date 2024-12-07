import datetime
import asyncio
import threading
import traceback
import time
import json
import uuid
import sys
import os
import importlib
import redis

import servermine.lib.redis_lib as redis_lib
import servermine.lib.acl as acl

project = "sm"
session_id = str(uuid.uuid4())
heartbeat_interval = 5
retry_delay = 5

imported_files = {}
methods_map = {}

# ssh -R 80:localhost:9001 serveo.net
# autossh -M 0 -R servermine.serveo.net:80:localhost:9001 serveo.net
# autossh -M 0 -R servermine:80:localhost:9001 serveo.net
# ssh -R servermine.serveo.net:443:localhost:9001 serveo.net
# ssh -R 443:localhost:9001 serveo.net

# def import_directories():
#     files = os.listdir('./plugins')
#     # print(files)
#     sys.path.append('./plugins')
#     for file in files:
#         if file.endswith(".py"):
#             try:
#                 file = file[:-3]
#                 imported_files.setdefault(file, importlib.import_module(file))
#             except ImportError as err:
#                 print('Error:', err)
#     # print(imported_files)


def set_project(p):
    global project
    project = p


def set_user(u):
    redis_lib.set_redis_user(u)


def set_password(p):
    redis_lib.set_redis_password(p)


def set_redis_url(url):
    redis_lib.set_redis_url(url)


def set_redis_api_key(key):
    acl.set_api_key(key)


def set_redis_api_secret(secret):
    acl.set_api_secret(secret)


async def start():
    # print("Start")
    sub_server()
    await asyncio.to_thread(queue())


def import_directories(path):
    files = os.listdir(path)
    # print(files)
    sys.path.append(path)
    for file in files:
        if file.endswith(".py"):
            try:
                file = file[:-3]
                imported_files.setdefault(file, importlib.import_module(file))
                print(f"Imported {file}")
            except ImportError as err:
                print('Error:', err)


def sub_server():
    print("Sub Server")
    # r = await redis.from_url("redis://admin:V!6xU8Kf*sQqJS@redis-10264.c277.us-east-1-3.ec2.redns.redis-cloud.com:10264")

    # acl.create_acl("test2", "test123")
    ev = {
        "channel": f'{project}:bl',
        "action": "server_up",
        "created": time.time_ns()
    }
    # get_redis_connection().hset(
    #     f'pp1:servers:{session_id}', mapping=session_data)
    # get_redis_connection().expire(
    #     f'pp1:servers:{session_id}', heartbeat_interval)
    # ev = {
    #     "channel": f'{project}:bl',
    #     "action": "server_up",
    #     "created": time.time_ns()
    # }
    redis_lib.get_redis_connection().publish(f'{project}:bl', json.dumps(ev))
    pubsub = redis_lib.get_redis_connection().pubsub()
    subscribe_channel(pubsub, f'{project}:br')

    # update_redis_hash()
    # Run the update_redis_hash function in a separate thread
    interval_thread = threading.Thread(target=update_redis_hash)
    interval_thread.daemon = True  # Daemon thread will exit when the main program exits
    interval_thread.start()

# while True:
#     try:
#         # Listen for messages
#         for message in pubsub.listen():
#             if message['type'] == 'message':
#                 print(f"Message received: {message['data']}")

#     except Exception as e:
#         time.sleep(5)
#         pubsub = get_redis_connection().pubsub()
#         subscribe_channel(pubsub, f'{project}:br')


def update_redis_hash():
    while True:
        session_data = {
            "type": "plugin",
            "sessionId": session_id,
            "project": project
        }
        try:
            redis_lib.get_redis_connection().hset(
                f'pp1:servers:{session_id}', mapping=session_data)
            redis_lib.get_redis_connection().expire(
                f'pp1:servers:{session_id}', heartbeat_interval)
            # print("Ping Redis", session_id)
            time.sleep(heartbeat_interval-1)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            print(e)
        except Exception as e:
            print(e)


def message_handler(message):
    print("message_handler")
    print(message.get("data"))
    job = json.loads(message.get("data"))
    job["connected"] = True
    if "action" in job and job["action"] == "ping":
        print("PING")
        if "ws" in job:
            redis_lib.get_redis_connection().rpush(
                job["ws"], json.dumps(job))
            redis_lib.get_redis_connection().expire(
                job["ws"], 60)
        # redis_lib.get_redis_connection().publish(f'{project}:bl', json.dumps(job))

    elif "plugin" in job and job["plugin"] in imported_files:
        if hasattr(imported_files[job["plugin"]], job["action"]):
            mtd = getattr(
                imported_files[job["plugin"]], job["action"])
            ret = mtd(job["data"])
            job["data"] = ret
            print('job with data')
            print(job)
            if "ws" in job:
                redis_lib.get_redis_connection().rpush(
                    job["ws"], json.dumps(job))
                redis_lib.get_redis_connection().expire(
                    job["ws"], 60)


def subscribe_channel(pubsub, channel):
    print("Subscribe", channel)
    # pubsub.subscribe(channel)
    pubsub.subscribe(**{channel: message_handler})
    pubsub.run_in_thread(sleep_time=0.001)


def add_method(plugin, action, fn):
    print("Adding method", plugin, action)
    methods_map.setdefault(plugin, {})
    methods_map[plugin].setdefault(action, fn)


def error_handler(job, error):
    job["data"] = {"error": {
        "message": error.content[0]['message'], "code": error.content[0]['errorCode']}}


def set_error_handler(fn):
    global error_handler
    error_handler = fn


def queue():
    # print('Queue')
    # r = await redis.from_url("redis://admin:V!6xU8Kf*sQqJS@redis-10264.c277.us-east-1-3.ec2.redns.redis-cloud.com:10264")
    while True:
        # print(f'{project}:r')
        try:
            val = redis_lib.get_redis_connection().blpop(f'{project}:r', 5)
            if val:
                job = json.loads(val[1])
                try:
                    mtd = None
                    if job["plugin"] in methods_map and job["action"] in methods_map[job["plugin"]]:
                        mtd = methods_map[job["plugin"]][job["action"]]
                    elif job["plugin"] in imported_files:
                        if hasattr(imported_files[job["plugin"]], job["action"]):
                            mtd = getattr(
                                imported_files[job["plugin"]], job["action"])
                    if mtd:
                        ret = None
                        if "data" in job:
                            ret = mtd(job["data"])
                        else:
                            ret = mtd(job)
                        job["data"] = ret
                    else:
                        job["data"] = {
                            "error": f"no server actions found for {job['plugin']}:{job['action']}"
                        }
                except Exception as error:
                    print("ERROR")
                    print(traceback.format_exc())
                    # print(error)
                    error_handler(job, error)
                if "ws" in job:
                    redis_lib.get_redis_connection().rpush(
                        job["ws"], json.dumps(job))
                    redis_lib.get_redis_connection().expire(
                        job["ws"], 60)
        except (redis.exceptions.ConnectionError, redis.exceptions.TimeoutError) as e:
            print("Redis connection lost. Reconnecting...")
            print(e)
            time.sleep(retry_delay)

        except redis.exceptions.RedisError as e:
            # Catch other general Redis-related exceptions
            print("General Redis error")
            print(e)
            # traceback.print_exc()

        except Exception as error:
            print("Unexpected error on brpop queue")
            print(error)

def queue_ws():
    print("Queue WS")

if __name__ == '__main__':
    print('start')
    # redis.set_user("Teste")
#     try:
#         # loop = asyncio.get_event_loop()
#         # loop.run_until_complete(start())
#         asyncio.run(start())
#     except Exception as error:
#         print(error)
#         traceback.print_exc()
#     # asyncio.run(start())
