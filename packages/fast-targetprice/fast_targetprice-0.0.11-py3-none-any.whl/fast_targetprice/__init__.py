import ctypes
import os
import pickle
from threading import Lock
import time



current_folder = os.path.dirname(os.path.abspath(__file__))

class CONVERTER:
    def __init__(self) -> None:
        with open(os.path.join(current_folder,"datafile.pkl"), "rb") as file:  # rb: read binary
            self.datafile = pickle.load(file)

    def getId(self,itemName):
        return self.datafile["itemToId"].get(itemName,None)
    
    def getName(self,id):
        return self.datafile["idToItem"].get(id,None)

class DB:
    sell = 0
    buyOrder = 1
    smart = 2

class SITE:
    youpin = 0
    buff163 = 1

class FAST_PRICE():
    def __init__(self,host="103.163.25.8",port=26251,api_key="") -> None:
        self.lock = Lock()
        self.host = host
        self.client_socket = None
        self.port = port
        self.api_key = api_key
        self.client = ctypes.CDLL('./client.dll')
        self.client.get_data.argtypes = [ctypes.c_uint8, ctypes.c_uint16, ctypes.c_uint8]
        self.client.get_data.restype = ctypes.c_uint32
        self.client.client_auth.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        self.client.client_auth.restype = ctypes.c_int
        self.client.client_connect.argtypes = [ctypes.c_char_p, ctypes.c_int]
        self.client.client_connect.restype = ctypes.c_int
        self.client.close.restype = None
        self.response_value = ctypes.c_uint32()
        self.conveter = CONVERTER()
        self.__connect()

    def __connect(self):
        result = self.client.client_connect(self.host.encode(), self.port)
        if result == 0:
            print("Connection established successfully!")
        else:
            print("Failed to connect.")
        buffer = ctypes.create_string_buffer(1024)
        result = self.client.client_auth(self.api_key.encode(), buffer, 1024)
        if result == 0:
            print("Auth established successfully!")
        else:
            print("Failed to auth.")

    
    def __getByIndex(self,site:SITE,itemId:int,index:int):
        with self.lock: 
            result = self.client.get_data(site,itemId,index,ctypes.byref(self.response_value))
            if result < 0:
                raise "Failed to connect."
            return self.response_value.value
        
    def get(self,site:SITE,itemId:int,index:DB=0):
        return self.__getByIndex(site,itemId,index)

    def getMoreBuyOrder(self,site:SITE,itemId:int):
        result = []
        for i in range(0, 20, 2):
            result.append({
                "price": self.__getByIndex(site,itemId,i+1),
                "itemLeft" : self.__getByIndex(site,itemId,i+2)
            })
        return result

    def __del__(self):
        if self.client_socket:
            self.client_socket.close()

# if __name__ == "__main__":
#     c = FAST_PRICE(api_key="c5466de4-001a-4e0d-b2de-6c9ae2892289")
#     print(c.get(site=SITE.buff163,itemId=0))


#     start_time = time.time()
#     for i in range(100):
#         c.get(site=SITE.buff163,itemId=0)
#     end_time = time.time()

#     print(f"Thời gian chạy: {end_time - start_time:.6f} giây")