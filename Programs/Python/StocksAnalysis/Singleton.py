# File: Singleton.py
# This is the singleton pattern class

import threading


class Singleton(object):
    _instance_lock = threading.Lock()

    # This is what the example shows me
    def __init__(self):
        pass


    def __new__(cls, *args, **kwargs):
        if not hasattr(Singleton, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(Singleton, "_instance"):
                    Singleton._instance = object.__new__(cls)  
        return Singleton._instance