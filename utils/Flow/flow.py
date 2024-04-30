'''
In this file Flow class should be declared
'''
from .flowFeature import FlowFeatures
from .packetInfo import PacketInfo
from scapy.layers.inet import IP, TCP
import statistics
threshold = 5

class Flow:
    def __init__(self,  packet: PacketInfo) -> None:
        self.packetInfos = [packet]
        self.fwdPacketInfos = [packet]
        self.bwdPacketInfos = []

        self.flowFeatures = FlowFeatures()
        self.flowFeatures.setDestPort(packet.getDestPort())
        self.flowFeatures.flags.setFwdPSHFlags(0 if not packet.getURGFlag() else 1)
        self.flowFeatures.p_stats.flStats.setMaxPacketLen(packet.getPayloadBytes())
        self.flowFeatures.p_stats.flStats.setPacketLenMean(packet.getPayloadBytes())
        self.flowFeatures.flags.setFINFlag(1 if packet.getFINFlag() else 0)
        self.flowFeatures.flags.setSYNFlag(1 if packet.getSYNFlag() else 0)
        self.flowFeatures.flags.setPSHFlag(1 if packet.getPSHFlag() else 0)
        self.flowFeatures.flags.setACKFlag(1 if packet.getACKFlag() else 0)
        self.flowFeatures.flags.setURGFlag(1 if packet.getURGFlag() else 0)

        self.flowFeatures.p_stats.flStats.setAvgPacketSize(packet.getPacketSize())
        self.flowLastSeen = packet.getTimestamp()
        self.fwdLastSeen = packet.getTimestamp()
        self.bwdLastSeen = 0
        self.flowStartTime = packet.getTimestamp()
        self.startActiveTime = packet.getTimestamp()
        self.endActiveTime = packet.getTimestamp()

        self.flowIAT = []
        self.fwdIAT = []
        self.bwdIAT = []
        self.flowActive = []
        self.flowIdle = []

        self.packet_count = 1
        self.fwd_packet_count = 1
        self.bwd_packet_count = 0

    def getFlowStartTime(self):
        return self.flowLastSeen

    def new(self, packet: PacketInfo, direction: str):
        if direction == 'bwd':
            self.bwdPacketInfos.append(packet)

            if self.bwd_packet_count == 0:
                self.flowFeatures.p_stats.bwdStats.setBwdPacketLenMax(packet.getPayloadBytes())
            else:
                self.flowFeatures.p_stats.bwdStats.setBwdPacketLenMax(
                    max(self.flowFeatures.p_stats.bwdStats.getBwdPacketLenMax,
                         packet.getPayloadBytes()))
                self.bwdIAT.append((packet.getTimestamp() - self.bwdLastSeen) * 1000 * 1000)

            self.bwd_packet_count = self.bwd_packet_count + 1
            self.bwdLastSeen = packet.getTimestamp()

        else:
            self.fwdPacketInfos.append(packet)
            self.fwdIAT.append((packet.getTimestamp() - self.fwdLastSeen) * 1000 * 1000)
            self.flowFeatures.flags.setFwdPSHFlags(max(1 if packet.getURGFlag() else 0,
                                                 self.flowFeatures.getFwdPSHFlags()))
            self.fwd_packet_count = self.fwd_packet_count + 1
            self.fwdLastSeen = packet.getTimestamp()

        self.flowFeatures.p_stats.flStats.setMaxPacketLen(max(self.flowFeatures.p_stats.flStats.getMaxPacketLen(),
                                                                   packet.getPayloadBytes()))

        if packet.getFINFlag():
            self.flowFeatures.flags.setFINFlag(1)
        if packet.getSYNFlag():
            self.flowFeatures.flags.setSYNFlag(1)
        if packet.getPSHFlag():
            self.flowFeatures.flags.setPSHFlag(1)
        if packet.getACKFlag():
            self.flowFeatures.flags.setACKFlag(1)
        if packet.getURGFlag():
            self.flowFeatures.flags.setURGFlag(1)

        time = packet.getTimestamp()
        if time - self.endActiveTime > threshold:
            if self.endActiveTime - self.startActiveTime > 0:
                self.flowActive.append(float(self.endActiveTime - self.startActiveTime))
            self.flowIdle.append(time - self.endActiveTime)
            self.startActiveTime = time
            self.endActiveTime = time
        else:
            self.endActiveTime = time

        self.packet_count = self.packet_count + 1
        self.packetInfos.append(packet)
        self.flowIAT.append((packet.getTimestamp() - self.flowLastSeen) * 1000 * 1000)
        self.flowLastSeen = packet.getTimestamp()

    def terminated(self):
        duration = (self.flowLastSeen - self.flowStartTime) * 1000 * 1000
        self.flowFeatures.setFlowDuration(duration)

        fwd_packet_lens = [x.getPayloadBytes() for x in self.fwdPacketInfos]
        self.flowFeatures.p_len.setTotalFwdPacketsNum(len(fwd_packet_lens))
        self.flowFeatures.flow_bytes.setTotalLenFwdPackets(sum(fwd_packet_lens))
        if len(fwd_packet_lens) > 0:
            self.flowFeatures.p_stats.fwdStats.setFwdPacketLenMax(max(fwd_packet_lens))
            self.flowFeatures.p_stats.fwdStats.setFwdPacketLenMean(statistics.mean(fwd_packet_lens))
            if len(fwd_packet_lens) > 1:
                self.flowFeatures.p_stats.fwdStats.setFwdPacketLenStd(statistics.stdev(fwd_packet_lens))

        bwd_packet_lens = [x.getPayloadBytes() for x in self.bwdPacketInfos]
        self.flowFeatures.flow_bytes.setTotalLenBwdPackets(sum(bwd_packet_lens))
        if len(bwd_packet_lens) > 0:
            self.flowFeatures.p_stats.bwdStats.setBwdPacketLenMax(max(bwd_packet_lens))
            self.flowFeatures.p_stats.bwdStats.setBwdPacketLenMin(min(bwd_packet_lens))
            self.flowFeatures.p_stats.bwdStats.setBwdPacketLenMean(statistics.mean(bwd_packet_lens))
            if len(bwd_packet_lens) > 1:
                self.flowFeatures.p_stats.bwdStats.setBwdPacketLenStd(statistics.stdev(bwd_packet_lens))

        total_packets_len = sum([x.getPayloadBytes() for x in self.packetInfos])
        self.flowFeatures.p_time.setFlowBytesRate(total_packets_len / duration)
        self.flowFeatures.p_time.setFlowPacketsRate(self.packet_count / duration)
        self.flowFeatures.p_time.setBwdPacketsRate(sum(bwd_packet_lens) / duration)

        if len(self.flowIAT) > 0:
            self.flowFeatures.iat.flowIAT.setFlowIATMean(statistics.mean(self.flowIAT))
            self.flowFeatures.iat.flowIAT.setFlowIATMax(max(self.flowIAT))
            self.flowFeatures.iat.flowIAT.setFlowIATMin(min(self.flowIAT))
            if len(self.flowIAT) > 1:
                self.flowFeatures.iat.flowIAT.setFlowIATStd(statistics.stdev(self.flowIAT))

        if len(self.fwdIAT) > 0:
            self.flowFeatures.iat.fwdIAT.setFwdIATTotal(sum(self.fwdIAT))
            self.flowFeatures.iat.fwdIAT.setFwdIATMean(statistics.mean(self.fwdIAT))
            self.flowFeatures.iat.fwdIAT.setFwdIATMax(max(self.fwdIAT))
            self.flowFeatures.iat.fwdIAT.setFwdIATMin(min(self.fwdIAT))
            if len(self.fwdIAT) > 1:
                self.flowFeatures.iat.fwdIAT.setFwdIATStd(statistics.stdev(self.fwdIAT))

        if len(self.bwdIAT) > 0:
            self.flowFeatures.iat.bwdIAT.setBwdIATTotal(sum(self.bwdIAT))
            self.flowFeatures.iat.bwdIAT.setBwdIATMean(statistics.mean(self.bwdIAT))
            self.flowFeatures.iat.bwdIAT.setBwdIATMax(max(self.bwdIAT))
            self.flowFeatures.iat.bwdIAT.setBwdIATMin(min(self.bwdIAT))
            if len(self.bwdIAT) > 1:
                self.flowFeatures.iat.bwdIAT.setBwdIATStd(statistics.stdev(self.bwdIAT))

        packet_lens = [x.getPayloadBytes() for x in self.packetInfos]
        packet_sizes =[x.getPacketSize() for x in self.packetInfos]
        if len(packet_lens) > 0:
            self.flowFeatures.p_stats.flStats.setPacketLenMean(statistics.mean(packet_lens))
            self.flowFeatures.p_stats.flStats.setAvgPacketSize(sum(packet_sizes) / self.packet_count)
            if len(packet_lens) > 1:
                self.flowFeatures.p_stats.flStats.setPacketLenStd(statistics.stdev(packet_lens))
                self.flowFeatures.p_stats.flStats.setPacketLenVar(statistics.variance(packet_lens))

        if self.fwd_packet_count != 0:
            self.flowFeatures.flow_bytes.setMinSegSizeFwd(min(fwd_packet_lens))
            self.flowFeatures.flow_bytes.setAvgFwdSegmentSize(sum(fwd_packet_lens) / self.fwd_packet_count)

        if self.bwd_packet_count != 0:
            self.flowFeatures.flow_bytes.setAvgBwdSegmentSize(sum(bwd_packet_lens) / self.bwd_packet_count)

        if len(self.flowActive) > 0:
            self.flowFeatures.active_stats.setActiveMin(min(self.flowActive))
            if len(self.flowActive) > 1:
                self.flowFeatures.active_stats.setActiveSTD(statistics.stdev(self.flowActive))

        if len(self.flowIdle) > 0:
            self.flowFeatures.idle_stats.setIdleMean(statistics.mean(self.flowIdle))
            self.flowFeatures.idle_stats.setIdleMax(max(self.flowIdle))
            self.flowFeatures.idle_stats.setIdleMin(min(self.flowIdle))
            if len(self.flowIdle) > 1:
                self.flowFeatures.idle_stats.setIdleStd(statistics.stdev(self.flowIdle))

        fwd_header_length = sum(packet[IP].ihl*4 if TCP in packet else 8 for packet in self.fwdPacketInfos)
        bwd_header_length = sum(packet[IP].ihl*4 if TCP in packet else 8 for packet in self.bwdPacketInfos)
        self.flowFeatures.flow_bytes.setFwdHeaderLength(fwd_header_length)
        self.flowFeatures.flow_bytes.setBwdHeaderLength(bwd_header_length)

        # Duplicated features
        self.flowFeatures.subflow.setSubflowBwdBytes(self.flowFeatures.getTotalLenBwdPackets)
        self.flowFeatures.subflow.setSubflowBwdPackets(self.flowFeatures.getTotalBwdPackets)
        self.flowFeatures.subflow.setSubflowFwdBytes(self.flowFeatures.getTotalLenFwdPackets)

        #TODO: rewrite to generator (hide all function calls)
        return [self.flowFeatures.getDestPort(),
                self.flowFeatures.getFlowDuration(),
                self.flowFeatures.p_len.getTotalFwdPacketsNum(),
                self.flowFeatures.flow_bytes.getTotalLenFwdPackets(),
                self.flowFeatures.p_stats.fwdStats.getFwdPacketLenMax(),
                self.flowFeatures.p_stats.fwdStats.getFwdPacketLenMean(),
                self.flowFeatures.p_stats.fwdStats.getFwdPacketLenStd(),             
                #backward stats
                self.flowFeatures.p_stats.bwdStats.getBwdPacketLenMax(),
                self.flowFeatures.p_stats.bwdStats.getBwdPacketLenMin(),
                self.flowFeatures.p_stats.bwdStats.getBwdPacketLenMean(),
                self.flowFeatures.p_stats.bwdStats.getBwdPacketLenStd(),
                #Rates
                self.flowFeatures.p_time.getFlowBytesRate(),
                self.flowFeatures.p_time.getFlowPacketsRate(),
                
                #Flow Iat
                self.flowFeatures.iat.flowIAT.getFlowIATMean(),
                self.flowFeatures.iat.flowIAT.getFlowIATStd(),
                self.flowFeatures.iat.flowIAT.getFlowIATMax(),
                #fwd iat
                self.flowFeatures.iat.fwdIAT.getFwdIATTotal(),
                self.flowFeatures.iat.fwdIAT.getFwdIATMean(),
                self.flowFeatures.iat.fwdIAT.getFwdIATStd(),
                #headers
                self.flowFeatures.flow_bytes.getFwdHeaderLength(),
                self.flowFeatures.flow_bytes.getBwdHeaderLength(),
                self.flowFeatures.p_time.getBwdPacketsRate(),
                #flstats
                self.flowFeatures.p_stats.flStats.getMaxPacketLen(),
                self.flowFeatures.p_stats.flStats.getPacketLenMean(),
                self.flowFeatures.p_stats.flStats.getPacketLenStd(),
                self.flowFeatures.p_stats.flStats.getPacketLenVar(),
                self.flowFeatures.flags.getPSHFlag(),
                self.flowFeatures.p_stats.flStats.getAvgPacketSize(),
                #flags
                #segments
                self.flowFeatures.flow_bytes.getAvgFwdSegmentSize(),
                self.flowFeatures.flow_bytes.getAvgBwdSegmentSize(),
                
                #subflow
                self.flowFeatures.subflow.getSubflowFwdPackets(),
                self.flowFeatures.subflow.getSubflowFwdBytes(),
                self.flowFeatures.subflow.getSubflowBwdPackets(),
                self.flowFeatures.subflow.getSubflowBwdBytes(),
                #initbytes
                self.flowFeatures.init_win.getInitWinBytesFwd(),
                self.flowFeatures.init_win.getInitWinBytesBwd(),
                #active stat
                self.flowFeatures.flow_bytes.getMinSegSizeFwd(),
                #self.flowFeatures.active_stats.getActiveMean(),
                self.flowFeatures.active_stats.getActiveMin()
                ]
