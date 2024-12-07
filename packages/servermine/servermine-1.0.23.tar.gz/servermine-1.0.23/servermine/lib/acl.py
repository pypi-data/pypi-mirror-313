import requests
import time
import os

API_KEY = os.getenv('REDIS_API_KEY',None)
API_SECRET_KEY = os.getenv('REDIS_API_SECRET',None)

headers = {
    "x-api-key": "Ay9adtha5prx8za3413t4v9y5vptrvst1aulowgz6r30uz2oa7",
    "x-api-secret-key": "S3ctl9u1zjg5cbcyma38bgnbrq6q2ia6pud7lwvaonramcpanq9",
    "Content-Type": "application/json"
}


def set_api_key(key):
    API_KEY = key


def set_api_secret(secret):
    API_SECRET_KEY = secret


def check_task_status(task_url):
    while True:
        response = requests.get(task_url, headers=headers)
        if response.status_code == 200:
            task_status = response.json()
            status = task_status.get('status')

            if status == 'processing-completed':
                return task_status
            elif status in ['received', 'processing', 'processing-in-progress']:
                print(f"Task is still processing: {status}")
                time.sleep(5)  # Non-blocking sleep
            elif status == 'processing-error':
                raise Exception(
                    f"Task failed with status: {status}. Error details: {task_status.get('response', {}).get('error', {}).get('description', 'No details provided')}")
            else:
                raise Exception(f"Unexpected task status: {status}")
        else:
            response.raise_for_status()


def create_acl(name, password):
    rule = create_rule(name)
    role = create_role(name)
    user = create_user(name, password)
    print("ACL Created")
    print(rule)
    print(role)
    print(user)
    return {"rule": rule, "role": role, "user": user}


def delete_acl(name):
    delete_user(name)
    # create_rule(name)
    # create_role(name)


def create_rule(name):
    print('Create Rule')
    print(name)
    data = {
        "name": name,
        "redisRule": f'+hset +unlink +pubsub +subscribe +brpop +blpop +rpush +lpush ~{name}* +pubsub ~pp1:* ~ws:*'
    }
    print(data)
    response = requests.post(
        'https://api.redislabs.com/v1/acl/redisRules', json=data, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(data)
    if "links" in data and len(data["links"]) > 0:
        status = check_task_status(data["links"][0]["href"])
        print(status)
        return status.get('response').get('resourceId')


def create_role(name):
    data = {
        "name": name,
        "redisRules": [
            {
                "ruleName": name,
                "databases": [
                    {
                        "subscriptionId": 2350147,
                        "databaseId": 12364997
                    }
                ]
            }
        ]
    }
    response = requests.post(
        'https://api.redislabs.com/v1/acl/roles', json=data, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(data)
    if "links" in data and len(data["links"]) > 0:
        status = check_task_status(data["links"][0]["href"])
        print(status)
        return status.get('response').get('resourceId')


def create_user(name, password):
    if not password:
        passowrd = generate_random_password()
    data = {
        "name": name,
        "role": name,
        "password": password
    }
    response = requests.post(
        'https://api.redislabs.com/v1/acl/users', json=data, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(data)
    if "links" in data and len(data["links"]) > 0:
        status = check_task_status(data["links"][0]["href"])
        print(status)
        return status.get('response').get('resourceId')
    # return data


def delete_user(name):
    data = {
        "name": name,
        "role": name,
        "password": password
    }
    response = requests.post(
        'https://api.redislabs.com/v1/acl/users', json=data, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(data)
    if "links" in data and len(data["links"]) > 0:
        status = check_task_status(data["links"][0]["href"])
        print(status)
    return data


def generate_random_password(length=12):
    # Define the character sets to use
    characters = string.ascii_letters + string.digits + '!@$'
    # Generate a random password
    password = ''.join(random.choice(characters) for _ in range(length))
    return password
