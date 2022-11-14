#!/usr/bin/env python3
from google.cloud import storage
import socket
import os
import json

# new imports
import firebase_admin
from firebase_admin import credentials, firestore
# new imports end

# initiating firebase
cred = credentials.Certificate("prashasti-karlekar-fall2022-firebase.json")
firebase_admin.initialize_app(cred)

# fetching server ip
serverip = 0
with open('server-ip.txt', 'r') as f:
    serverip = f.readlines()[0].rstrip()

# HOST = "localhost"  # Standard loopback interface address (localhost)
HOST = serverip
PORT = 9889        # Port to listen on (non-privileged ports are > 1023)


# Native storage
def getItem(key):
    try:
        with open('data/' + (str(key[1])+'.json'), 'r') as fr:
            data = json.load(fr)
        conn.send(
            ("VALUE "+str(key[1])+" "+str(len(data[key[1]]))+" \r\n"+data[key[1]] + "\r\n").encode())
    except FileNotFoundError as f:
        return "CLIENT_ERROR : THERE IS NO SUCH KEY IN KV STORE.\r\n".encode()
    except Exception as e:
        print("Exception in get:", e)
        pass


def setItem(key):
    if not(isValidKey(key[1])):
        return "CLIENT_ERROR INVALID KEY\r\n".encode()
    else:
        value = conn.recv(9542).decode()
        if int(key[2]) != len(value):
            return 'CLIENT_ERROR : THE LENGTH OF THE VALUE DO NOT MATCH.\r\n'.encode()
        elif len(key) != 4:
            return 'CLIENT_ERROR: COMMAND PROTOCOL WAS NOT FOLLOWED.\r\n'.encode()
        else:
            try:
                with open('data/' + (str(key[1])+'.json'), 'w') as fw:
                    data = {key[1]: value}
                    json.dump(data, fw)
                    return "STORED\r\n".encode()
            except Exception as e:
                print(e)
                return "NOT_STORED\r\n".encode()


# Firestore storage
def getItem1(key):
    # print(f"In getitem1 key is  ====={key}")
    db = firestore.client()  # this connects to our Firestore database
    collection = db.collection('KVStore')  # opens 'places' collection
    doc = collection.document('test')  # test is key
    res = doc.get().to_dict()
    print(res)
    return res[key]


def setItem1(key):
    if not(isValidKey(key[1])):
        return "CLIENT_ERROR INVALID KEY\r\n".encode()
    else:
        value = conn.recv(9542).decode()
        if int(key[2]) != len(value):
            return 'CLIENT_ERROR : THE LENGTH OF THE VALUE DO NOT MATCH.\r\n'.encode()
        elif len(key) != 4:
            return 'CLIENT_ERROR: COMMAND PROTOCOL WAS NOT FOLLOWED.\r\n'.encode()
        else:
            try:
                db = firestore.client()  # this connects to our Firestore database
                collection = db.collection('KVStore')
                collection.document('test').update({key[1]: value})
                return "STORED\r\n".encode()
            except Exception as e:
                print(e)
                return "NOT STORED\r\n".encode()


# Bucket Storage
def getItem2(key):
    # print("---in GET Bucket storage")
    storage_client = storage.Client.from_service_account_json(
        'prashasti-karlekar-fall2022-firebase.json')
    bucket_name = "prashasti_kvstore"
    bucket = storage_client.get_bucket(bucket_name)
    filename = "bucket_data.json"
    get_newBlob = bucket.get_blob(filename)
    dictionary = {}
    if get_newBlob.exists():
        dictionary = json.loads(get_newBlob.download_as_string())
        value = dictionary[key]
    else:
        value = "OBJECT NOT FOUND"
    print(value)
    return value


def setItem2(key):
    # print("In SET bucket storage")
    if not(isValidKey(key[1])):
        return "CLIENT_ERROR INVALID KEY\r\n".encode()
    else:
        value = conn.recv(9542).decode()
        if int(key[2]) != len(value):
            return 'CLIENT_ERROR : THE LENGTH OF THE VALUE DO NOT MATCH.\r\n'.encode()
        elif len(key) != 4:
            return 'CLIENT_ERROR: COMMAND PROTOCOL WAS NOT FOLLOWED.\r\n'.encode()
        else:
            try:
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'prashasti-karlekar-fall2022-firebase.json'
                storage_client = storage.Client(
                    project='prashasti-karlekar-fall2022')
                bucket_name = "prashasti_kvstore"
                bucket = storage_client.get_bucket(bucket_name)
                filename = "bucket_data.json"

                dictionary = {}
                blob = bucket.get_blob(filename)
                if(not blob.exists()):
                    blob = bucket.blob(filename)
                    blob.upload_from_string(json.dumps(
                        dictionary), content_type='application/json')

                if(blob.exists()):
                    dictionary = json.loads(blob.download_as_string())

                dictionary[key[1]] = value
                blob.upload_from_string(json.dumps(
                    dictionary), content_type='application/json')
                ret_val = "STORED\r\n"
                return ret_val.encode()
            except Exception as e:
                print(e)
                return "NOT STORED\r\n".encode()


def isValidKey(key):
    if not key.isalnum() or len(key) > 250:
        # print("Invalid key.")
        return False
    return True


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as myServer:
    try:
        myServer.bind(('', PORT))
        myServer.listen(1)
        # print("Started listening")
        while True:
            conn, addr = myServer.accept()
            # with conn:
            # print('Connected by', addr)
            # while True:
            cmd1 = conn.recv(9542).decode()
            data = cmd1.split()

            if data[0] == "set":
                if data[3] == "1":
                    result = setItem(data)
                elif data[3] == "2":
                    result = setItem1(data)
                elif data[3] == '3':
                    result = setItem2(data)

                conn.send(result)
            elif data[0] == "get":
                if data[2] == "1":
                    result = getItem(data)
                elif data[2] == "2":
                    result = getItem1(data[1])
                elif data[2] == '3':
                    result = getItem2(data[1])
                conn.send(result.encode())

                conn.send('\nEND\r\n'.encode())
                # conn.close()
            else:
                conn.send('ERROR\r\n'.encode())
    except Exception as e:
        # conn.send('ERROR OCCURED\r\n'.encode())
        pass
