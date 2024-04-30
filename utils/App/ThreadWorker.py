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
    
    def __init__(self, model_name, model_path, mode, interface=None, pcapPath=None) -> None:
        super(Worker, self).__init__()
        self.is_stopped = False
        self.model_name = model_name
        self.model = Model(model_path, model_name)
        self.mode = mode
        self.interface = interface
        self.pcap_path = pcapPath
        self.current_flows = {}
        self.normalization = pickle.load(open(os.path.join("model/scalar.sav"), 'rb'))
        self.signals = WorkerSignals()
        self.sniffer = None

    @pyqtSlot()
    def run(self):
        try:
            if self.mode == "Live":
                self.sniffer = AsyncSniffer(iface=self.interface, prn=self.test)
            else:
                self.sniffer  = AsyncSniffer(offline=self.pcap_path, prn=self.test)
            self.sniffer.start()
            for flow in self.current_flows.values():
                    self.classify(flow.terminated())

            for i in range(1000):
                if self.is_stopped:
                    break                              
                string = f"Time slept {i+1}"
                self.signals.prints.emit(string)
            time.sleep(2)  
            self.sniffer.stop()
        except:
            traceback.print_exc()
            print(sys.exc_info()[:2])

            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        finally:
            self.signals.finished.emit()

    def stop(self):
        self.signals.prints.emit('Stop Sniffer')
        self.is_stopped = True
    
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
        if result !='BENIGN':
            self.signals.prints.emit(classification)

        return feature_string + classification   
    
    def newPacket(self, p):
        try:
            packet = PacketInfo()
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

            if packet.getFwdID() in self.self.current_flows.keys():
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

                flow = Flow(packet)
                self.current_flows[packet.getFwdID()] = flow
                # current flows put id, (new) flow

        except AttributeError:
            # not IP or TCP
            return

        except:
            traceback.print_exc()
            