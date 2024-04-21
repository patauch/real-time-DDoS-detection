'''
this file should declare sniffer functions to be called from main
'''
import pickle
import os
import scapy

class SnifferModel():
    def __init__(self, model_name, model_path, interface) -> None:
        self.model_name = model_name
        self.model = pickle.load(open(os.path.join("model",model_path), 'rb'))
        self.interface = interface

    
    