import asyncio
import traceback
import time
import json
import uuid
import sys
import os
import rel
import websocket
import importlib
from websockets.sync.client import connect

from mako.lookup import TemplateLookup
from mako.template import Template

project = "sm"
websocket_url = "ws://localhost:9001/server"
session_id = str(uuid.uuid4())
heartbeat_interval = 5
retry_delay = 5
ws = None

imported_files = {}
methods_map = {}


def set_project(p):
    global project
    project = p


def set_websocket_url(url):
    global websocket_url
    websocket_url = url


# async def start():
    # print("Start")
    # sub_server()
    # await asyncio.get_event_loop().run_until_complete(start_ws())
    # await asyncio.to_thread(queue())

def build_header_from_message(job):
    smh = job["smh"].split(":")
    return {"d": smh[0], "session_id": smh[1].split('>'), "project": smh[2], "plugin": smh[3] or "", "action": smh[4] or ""}


def build_message_from_header(header):
    return f'{header["d"]}:{">".join(header["session_id"])}>{session_id}:{header["project"]}:{header["plugin"] or ""}:{header["action"] or ""}'


def on_message(wsapp, message):
    # print("on_message")
    # print(message)
    job = json.loads(message)
    header = build_header_from_message(job)
    job["smh"] = build_message_from_header(header)
    # print("header")
    # print(header)
    try:
        mtd = None
        if header["plugin"] in methods_map and header["action"] in methods_map[header["plugin"]]:
            mtd = methods_map[header["plugin"]][header["action"]]
        elif header["plugin"] in imported_files:
            if hasattr(imported_files[header["plugin"]], header["action"]):
                mtd = getattr(
                    imported_files[header["plugin"]], header["action"])
        if mtd:
            ret = None
            if "data" in job:
                ret = mtd(job["data"])
            else:
                ret = mtd(job)
            # print("Pre Process")
            process_dict(ret)
            # print(ret)
            # print("Post Process")
            job["data"] = ret
            # if "htmx" in job:
            #     # print("HTMX found")
            #     try:
            #         act_template = lookup.get_template(
            #             f'{header["plugin"]}/{header["action"]}.mako')
            #         # print("act_template")
            #         # print(act_template)
            #         if act_template:
            #             # print("Template Found")
            #             # print(ret)
            #             # print(job["data"])
            #             job["data"] = act_template.render(data=ret)
            #             # print(job["data"])
            #     except Exception as error:
            #         print(error)
        else:
            job["data"] = {
                "error": f"no server actions found for {header['plugin']}:{header['action']}"
            }
    except Exception as error:
        print("ERROR")
        print(traceback.format_exc())
        # print(error)
        error_handler(job, error)
    # if "ws" in job:

    job["smh"] = "<" + job["smh"][1:]
    # print("Sending job back")
    # print(job["data"])
    # job["d"] = "<"
    wsapp.send(json.dumps(job))


def on_open(ws):
    print("Opened")
    job = f'{{"smh":"+:{session_id}:{project}","channel":"{session_id},{project}"}}'
    ws.send(job)


def on_error(ws, error):
    print("Error")
    print(ws)
    print(error)
    # job = f'{{"smh":"+:{session_id}:{project}","channel":"{session_id},{project}"}}'
    # ws.send(job)


def start():
    global ws
    # with connect(websocket_url) as websocket:
    # ws = websocket
    # message = websocket.recv()
    # print(f"Received: {message}")
    # websocket.enableTrace(false)
    ws = websocket.WebSocketApp(
        websocket_url, on_message=on_message, on_open=on_open, on_error=on_error)
    ws.run_forever(dispatcher=rel, ping_interval=60, ping_timeout=10, reconnect=5,
                   ping_payload="This is an optional ping payload")

    rel.dispatch()


lookup = None


def import_directories(path):
    global lookup
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
    lookup = TemplateLookup(directories=[f'{path}/templates'])


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


def process_dict(data):
    for key, value in data.items():
        # Check if the value has a 'model_dump' method
        if hasattr(value, "model_dump") and callable(getattr(value, "model_dump")):
            # Call model_dump() if it's available and callable
            data[key] = value.model_dump()
        elif isinstance(value, dict):
            # If the value is a nested dictionary, recursively process it
            process_dict(value)
        elif isinstance(value, list):
            # If the value is a list, process each item
            for i, item in enumerate(value):
                if hasattr(item, "model_dump") and callable(getattr(item, "model_dump")):
                    value[i] = item.model_dump()
                elif isinstance(item, dict):
                    process_dict(item)


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
