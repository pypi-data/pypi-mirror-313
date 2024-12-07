import socket
from firebase_admin import db
import datetime
import json
import os
import zlib
from firebase_admin import credentials, initialize_app
from dotenv import load_dotenv
load_dotenv()

class OVSConnection():
    def __init__(self):
        self.compressed_data = os.getenv("FIREBASE_CONFIG")
        if not self.compressed_data:
            raise ValueError("Firebase yapılandırması eksik!")

        self.encrypted_json_data = zlib.compress(self.compressed_data.encode())

        self.temp_file = "firebase_temp.json"

    def create_temp_json_file(self):
        with open(self.temp_file, "wb") as f: f.write(zlib.decompress(self.encrypted_json_data))

    def delete_temp_json_file(self):
        if os.path.exists(self.temp_file): os.remove(self.temp_file)

    def connect_to_firebase(self):
        try:
            self.create_temp_json_file()
            cred = credentials.Certificate(self.temp_file)
            initialize_app(cred, {'databaseURL': 'https://onlinevariablessystem-default-rtdb.europe-west1.firebasedatabase.app/'})
        except Exception as e: print(f"Hata: {e}")
        finally: self.delete_temp_json_file()

class OVS:
    def __init__(self, token):
        self.connection = OVSConnection()
        self.connection.connect_to_firebase()
        self.token = token
        self.tokens = db.reference("tokens").child(token)
        self.vars = self.tokens.child("variables")

    def get(self, key):
        try: 
            data = self.tokens.child("variables").child(key).child("value").get()
            if data is not None: return data
            else: raise ValueError(f"{key}, is not a variable.")
        except: ...
    def set(self, key, value):
        try: self.vars.update({key: {f"value": value, f"creationDate": datetime.datetime.now().strftime("%m/%d/%Y"), f"creationTime": datetime.datetime.now().strftime("%H:%M:%S"), "creator": socket.gethostname(), "creatorIP": socket.gethostbyname(socket.gethostname())}})
        except: ... 
    def getAll(self):
        try: return self.tokens.child("variables").get()
        except: ...

    def _generate_token(self):
        try:
            self.tokens = db.reference("tokens")
            self.tokens.update({self.token: {"creatorIP": socket.gethostbyname(socket.gethostname())}})
            return True
        except : return False

if __name__ == "__main__":
    ovs = OVS("yourToken")
    ovs.set("jack", "its jack name")
    print(ovs.get("jack"))