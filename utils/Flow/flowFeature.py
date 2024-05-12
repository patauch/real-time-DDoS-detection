'''
This class is designed to store info about packets and flow
'''

class FlowFeatures:
    def __init__(self):
        self.dest_port = 0
        self.flow_dur = 0
        self.p_len = PacketLength()
        self.p_stats = PacketStats()
        self.iat = IAT()  
        self.p_time = PacketTime()
        self.flow_bytes = FlowBytes()
        self.active_stats = ActiveStats()
        self.idle_stats = IdleStats()
        self.flags = FlagCount()
        self.subflow = SubflowInfo()
        self.init_win = InitWinBytes()

    def getDestPort(self):
        return self.dest_port

    def setDestPort(self, value):
        self.dest_port = value

    def getFlowDuration(self):
        return self.flow_dur

    def setFlowDuration(self, value):
        self.flow_dur = int(round(value))    
 

class PacketLength():
    '''
    This class is used to store info consisting of packet quantity
    '''
    def __init__(self) -> None:
        self.total_fwd_packets = 0
        self.total_bwd_packets = 0

    def getTotalFwdPacketsNum(self):
        return self.total_fwd_packets
    
    def setTotalFwdPacketsNum(self, value):
        self.total_fwd_packets = value

    def getTotalBwdPacketsNum(self):
        return self.total_bwd_packets
    
    def setTotalBwdPacketsNum(self, value):
        self.total_bwd_packets = value


class PacketStats():
    '''
    This class is used to store PacketStats info
    '''
    def __init__(self) -> None:
        self.flStats = FlowPacketStats()
        self.fwdStats = FwdPacketStats()
        self.bwdStats = BwdPacketStats()


class FlowPacketStats():
    '''
    This class is used to store info about overall packet stats
    '''
    def __init__(self) -> None:
        self.avg_packet_size = 0
        self.max_packet_len = 0
        self.mean_packet_len = 0
        self.std_packet_len = 0
        self.var_packet_len = 0
    
    def getMaxPacketLen(self):
        return self.max_packet_len

    def setMaxPacketLen(self, value):
        self.max_packet_len = value

    def getPacketLenMean(self):
        return self.mean_packet_len

    def setPacketLenMean(self, value):
        self.mean_packet_len = value

    def getPacketLenStd(self):
        return self.std_packet_len

    def setPacketLenStd(self, value):
        self.std_packet_len = value

    def getPacketLenVar(self):
        return self.var_packet_len

    def setPacketLenVar(self, value):
        self.var_packet_len = value
 
    def getAvgPacketSize(self):
        return self.avg_packet_size

    def setAvgPacketSize(self, value):
        self.avg_packet_size = value


class FwdPacketStats():
    '''
    This class is used to store stats of forward packets
    '''
    def __init__(self) -> None:
        self.max_packet_length = 0
        self.mean_packet_length = 0
        self.std_packet_length = 0
    
    def getFwdPacketLenMax(self):
        return self.max_packet_length

    def setFwdPacketLenMax(self, value):
        self.max_packet_length = value

    def getFwdPacketLenMean(self):
        return self.mean_packet_length
    
    def setFwdPacketLenMean(self, value):
        self.mean_packet_length = value

    def getFwdPacketLenStd(self):
        return self.std_packet_length

    def setFwdPacketLenStd(self, value):
        self.std_packet_length = value


class BwdPacketStats():
    '''
    This class is used to store stats of backward packets
    '''
    def __init__(self) -> None:
        self.max_packet_len = 0
        self.min_packet_len = 0
        self.mean_packet_len = 0
        self.std_packet_len = 0
    
    def getBwdPacketLenMax(self):
        return self.max_packet_len

    def setBwdPacketLenMax(self, value):
        self.max_packet_len = value

    def getBwdPacketLenMin(self):
        return self.min_packet_len
    
    def setBwdPacketLenMin(self, value):
        self.min_packet_len = value

    def getBwdPacketLenMean(self):
        return self.mean_packet_len

    def setBwdPacketLenMean(self, value):
        self.mean_packet_len = value

    def getBwdPacketLenStd(self):
        return self.std_packet_len

    def setBwdPacketLenStd(self, value):
        self.std_packet_len = value


class IAT():
    '''
    This class is used to store info of IAT
    '''
    def __init__(self) -> None:
        self.flowIAT = FlowIAT()
        self.fwdIAT = FwdIAT()
        self.bwdIAT = BwdIAT()

    
class FlowIAT():
    def __init__(self) -> None:
        self.mean_IAT = 0
        self.std_IAT = 0
        self.max_IAT = 0 # delete usage
        self.min_IAT = 0 # delete usage
    
    def getFlowIATMean(self):
        return self.mean_IAT

    def setFlowIATMean(self, value):
        self.mean_IAT = int(round(value))

    def getFlowIATStd(self):
        return self.std_IAT

    def setFlowIATStd(self, value):
        self.std_IAT = value

    def getFlowIATMax(self):
        return self.max_IAT

    def setFlowIATMax(self, value):
        self.max_IAT = int(round(value))

    def getFlowIATMin(self):
        return self.min_IAT

    def setFlowIATMin(self, value):
        self.min_IAT = int(round(value))


class FwdIAT():
    '''
    This class is used to store info about forward IAT
    '''
    def __init__(self) -> None:
        self.total_IAT = 0
        self.mean_IAT = 0
        self.std_IAT = 0
        self.max_IAT = 0
        self.min_IAT = 0 # delete usage
    
    def getFwdIATTotal(self):
        return self.total_IAT

    def setFwdIATTotal(self, value):
        self.total_IAT = int(round(value))

    def getFwdIATMean(self):
        return self.mean_IAT

    def setFwdIATMean(self, value):
        self.mean_IAT = value

    def getFwdIATStd(self):
        return self.std_IAT

    def setFwdIATStd(self, value):
        self.std_IAT = value

    def getFwdIATMax(self):
        return self.max_IAT

    def setFwdIATMax(self, value):
        self.max_IAT = int(round(value))

    def getFwdIATMin(self):
        return self.min_IAT

    def setFwdIATMin(self, value):
        self.min_IAT = int(round(value))

    
class BwdIAT():
    '''
    This class is used to store info about backward IAT
    '''
    def __init__(self) -> None:
        self.total_IAT = 0 # delete usage
        self.mean_IAT = 0 # delete usage
        self.std_IAT = 0 # delete usage
        self.max_IAT = 0 # delete usage
        self.min_IAT = 0 # delete usage
    
    def getBwdIATTotal(self):
        return self.bwd_IAT_total

    def setBwdIATTotal(self, value):
        self.bwd_IAT_total = int(round(value))

    def getBwdIATMean(self):
        return self.bwd_IAT_mean

    def setBwdIATMean(self, value):
        self.bwd_IAT_mean = value

    def getBwdIATStd(self):
        return self.bwd_IAT_std

    def setBwdIATStd(self, value):
        self.bwd_IAT_std = value

    def getBwdIATMax(self):
        return self.bwd_IAT_max

    def setBwdIATMax(self, value):
        self.bwd_IAT_max = int(round(value))

    def getBwdIATMin(self):
        return self.bwd_IAT_min

    def setBwdIATMin(self, value):
        self.bwd_IAT_min = int(round(value))


class PacketTime():
    '''
    This class is used for storing info about packet rates
    '''
    def __init__(self) -> None:
        self.bwd_packets_rate = 0
        self.fl_bytes_rate = 0
        self.fl_packets_rate = 0

    def getBwdPacketsRate(self):
        return self.bwd_packets_rate
    
    def setBwdPacketsRate(self, value):
        self.bwd_packets_rate = value

    def getFlowBytesRate(self):
        return self.fl_bytes_rate

    def setFlowBytesRate(self, value):
        self.fl_bytes_rate = value

    def getFlowPacketsRate(self):
        return self.fl_packets_rate
    
    def setFlowPacketsRate(self, value):
        self.fl_packets_rate = value

    
class FlowBytes():
    '''
    This class is used to store info about size info
    '''
    def __init__(self) -> None:
        self.total_length_of_fwd_packets = 0
        self.total_length_of_bwd_packets = 0

        self.fwd_header_length = 0
        self.bwd_header_length = 0

        self.avg_fwd_segment_size = 0
        self.avg_bwd_segment_size = 0

        self.min_seg_size_forward = 0

    def getTotalLenFwdPackets(self):
        return self.total_length_of_fwd_packets
    
    def setTotalLenFwdPackets(self, value):
        self.total_length_of_fwd_packets = value

    def getTotalLenBwdPackets(self):
        return self.total_length_of_bwd_packets
    
    def setTotalLenBwdPackets(self, value):
        self.total_length_of_bwd_packets = value

    def getFwdHeaderLength(self):
        return self.fwd_header_length
    
    def setFwdHeaderLength(self, value):
        self.fwd_header_length = value

    def getBwdHeaderLength(self):
        return self.bwd_header_length
    
    def setBwdHeaderLength(self, value):
        self.bwd_header_length = value

    def getAvgFwdSegmentSize(self):
        return self.avg_fwd_segment_size

    def setAvgFwdSegmentSize(self, value):
        self.avg_fwd_segment_size = value

    def getAvgBwdSegmentSize(self):
        return self.avg_bwd_segment_size

    def setAvgBwdSegmentSize(self, value):
        self.avg_bwd_segment_size = value
    
    def getMinSegSizeFwd(self):
        return self.min_seg_size_forward
    
    def setMinSegSizeFwd(self, value):
        self.min_seg_size_forward = value


class ActiveStats():
    '''
    This class is used to store info about active stats
    '''
    def __init__(self) -> None:
        
        self.min = 0
        self.std = 0 # delete usage
        self.mean = 0

    def getActiveMin(self):
        return self.min

    def setActiveMin(self, value):
        self.min = value

    def getActiveSTD(self):
        return self.std
    
    def setActiveSTD(self, value):
        self.std = value

    def getActiveMean(self):
        return self.mean

    def setActiveMean(self, value):
        self.mean = value


class IdleStats():
    '''
    This class is used to store info about Idle stats
    '''
    def __init__(self) -> None:
        self.mean_ = 0 # delete usage
        self.std_ = 0 # delete usage
        self.max_ = 0 # delete usage
        self.min_ = 0 # delete usage

    def getIdleMean(self):
        return self.mean

    def setIdleMean(self, value):
        self.mean = value

    def getIdleStd(self):
        return self.std_

    def setIdleStd(self, value):
        self.std_ = value

    def getIdleMax(self):
        return self.max_

    def setIdleMax(self, value):
        self.max_ = value

    def getIdleMin(self):
        return self.min_

    def setIdleMin(self, value):
        self.min_ = value


class FlagCount():
    '''
    This class is used for storing info about flags
    '''
    def __init__(self) -> None:
        self.FIN_flag_ = 0 # delete usage
        self.SYN_flag_ = 0 # delete usage
        self.PSH_flag_ = 0
        self.ACK_flag_ = 0 # delete usage
        self.URG_flag_ = 0 # delete usage

        self.fwd_PSH_flags = 0
    
    def getFINFlag(self):
        return self.FIN_flag_

    def setFINFlag(self, value):
        self.FIN_flag_ = value

    def getSYNFlag(self):
        return self.SYN_flag_

    def setSYNFlag(self, value):
        self.SYN_flag_ = value

    def getPSHFlag(self):
        return self.PSH_flag_

    def setPSHFlag(self, value):
        self.PSH_flag_ = value

    def getACKFlag(self):
        return self.ACK_flag_

    def setACKFlag(self, value):
        self.ACK_flag_ = value

    def getURGFlag(self):
        return self.URG_flag_

    def setURGFlag(self, value):
        self.URG_flag_ = value

    def getFwdPSHFlags(self):
        return self.fwd_PSH_flags

    def setFwdPSHFlags(self, value):
        self.fwd_PSH_flags = value


class SubflowInfo():
    def __init__(self) -> None:
        self.fwd_packets = 0    
        self.fwd_bytes = 0  
        self.bwd_packets = 0
        self.bwd_bytes = 0
    
    def getSubflowFwdPackets(self):
        return self.fwd_packets
    
    def setSubflowFwdPackets(self, value):
        self.fwd_packets = value

    def getSubflowFwdBytes(self):
        return self.fwd_bytes
    
    def setSubflowFwdBytes(self, value):
        self.fwd_bytes = value

    def getSubflowBwdPackets(self):
        return self.bwd_packets
    
    def setSubflowBwdPackets(self, value):
        self.bwd_packets = value

    def getSubflowBwdBytes(self):
        return self.bwd_bytes
    
    def setSubflowBwdBytes(self, value):
        self.bwd_bytes = value


class InitWinBytes():
    def __init__(self) -> None:
        #default to -1
        self._forward = -1
        self._backward = -1
    
    def getInitWinBytesFwd(self):
        return self._forward

    def setInitBytesFwd(self, value):
        self._forward = value

    def getInitWinBytesBwd(self):
        return self._backward
    
    def setInitBytesBwd(self, value): # todo
        self._backward = value
