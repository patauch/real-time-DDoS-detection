from PyQt6.QtCore import QRunnable, QObject, pyqtSlot, pyqtSignal

import time
import traceback, sys
import os
import pickle

from scapy.sendrecv import AsyncSniffer

from ..Sniffer.model import Model
from ..Flow.flow import Flow
from ..Flow.packetInfo import PacketInfo

FlowTimeout = 600


class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    prints = pyqtSignal(str)


class Worker(QRunnable):
    
    def __init__(self) -> None:
        super(Worker, self).__init__()
        self.is_stopped = False
        self.model_name = None
        self.model_path = None
        self.model = None
        self.mode = None
        self.interface = None
        self.pcap_path = None
        self.current_flows = {}
        self.normalization = pickle.load(open(os.path.join("model/utils/scaler.sav"), 'rb'))
        self.signals = WorkerSignals()
        self.sniffer = None

    @pyqtSlot()
    def run(self):
        try:
            if self.mode == "Live":
                self.sniffer = AsyncSniffer(iface=self.interface, prn=self.newPacket)
            else:
                self.sniffer  = AsyncSniffer(offline=self.pcap_path, prn=self.newPacket)
            self.sniffer.start()
        except:
            traceback.print_exc()
            print(sys.exc_info()[:2])

            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
            
    def stop(self):
        
        self.is_stopped = True
        self.sniffer.stop()
        try:
            for flow in self.current_flows.values():
                self.classify(flow.terminated())
        except Exception as e:
            print(e)
        self.signals.prints.emit('Stop Sniffer')
        self.signals.finished.emit()
        
    
    def test(self, p):
        self.signals.prints.emit('test')
        pass

    def classify(self, features):
        # preprocess
        f = features
        features = self.normalization.transform([f])
        result = self.model.predict(features)

        feature_string = [str(i) for i in f]
        classification = [str(result[0])]
        
        #if result !='BENIGN':
        self.signals.prints.emit(*classification)

        return feature_string + classification   
    
    def newPacket(self, p):
        try:
            packet = PacketInfo(p)
            packet.setDest(p)
            packet.setSrc(p)
            packet.setSrcPort(p)
            packet.setDestPort(p)
            packet.setProtocol(p)
            packet.setTimestamp(p)
            packet.setPSHFlag(p)
            packet.setFINFlag(p)
            packet.setSYNFlag(p)
            packet.setACKFlag(p)
            packet.setURGFlag(p)
            packet.setRSTFlag(p)
            packet.setPayloadBytes(p)
            packet.setHeaderBytes(p)
            packet.setPacketSize(p)
            packet.setWinBytes(p)
            packet.setFwdID()
            packet.setBwdID()
            
            if packet.getFwdID() in self.current_flows.keys():
                #self.signals.prints.emit('found flow fwd')
                flow = self.current_flows[packet.getFwdID()]

                # check for timeout
                if (packet.getTimestamp() - flow.getFlowStartTime()) > FlowTimeout:
                    self.classify(flow.terminated())
                    del self.current_flows[packet.getFwdID()]
                    flow = Flow(packet)
                    self.current_flows[packet.getFwdID()] = flow

                # check for fin flag
                elif packet.getFINFlag() or packet.getRSTFlag():
                    flow.new(packet, 'fwd')
                    self.classify(flow.terminated())
                    del self.current_flows[packet.getFwdID()]
                    del flow

                else:
                    flow.new(packet, 'fwd')
                    self.current_flows[packet.getFwdID()] = flow

            elif packet.getBwdID() in self.current_flows.keys():
                #self.signals.prints.emit('found flow bwd')
                flow = self.current_flows[packet.getBwdID()]

                # check for timeout
                if (packet.getTimestamp() - flow.getFlowStartTime()) > FlowTimeout:
                    self.classify(flow.terminated())
                    del self.current_flows[packet.getBwdID()]
                    del flow
                    flow = Flow(packet)
                    self.current_flows[packet.getFwdID()] = flow

                elif packet.getFINFlag() or packet.getRSTFlag():
                    flow.new(packet, 'bwd')
                    self.classify(flow.terminated())
                    del self.current_flows[packet.getBwdID()]
                    del flow
                else:
                    flow.new(packet, 'bwd')
                    self.current_flows[packet.getBwdID()] = flow
            else:
                #self.signals.prints.emit('new flow')
                flow = Flow(packet)
                self.current_flows[packet.getFwdID()] = flow
                # current flows put id, (new) flow

        except AttributeError:
            # not IP or TCP
            return

        except:
            traceback.print_exc()

    def set_params(self, **kwargs):
        self.__dict__.update(kwargs)

    def set_model(self):
        self.model = Model(model_name=self.model_name, model_path=self.model_path)

    