import json

class CID:
    # Class-A
    ResetInd            = 0x01
    ResetConf           = 0x01
    LinkCheckReq        = 0x02
    LinkCheckAns        = 0x02
    LinkADRReq          = 0x03
    LinkADRAns          = 0x03
    DutyCycleReq        = 0x04
    DutyCycleAns        = 0x04
    RXParamSetupReq     = 0x05
    RXParamSetupAns     = 0x05
    DevStatusReq        = 0x06
    DevStatusAns        = 0x06
    NewChannelReq       = 0x07
    NewChannelAns       = 0x07
    RXTimingSetupReq    = 0x08
    RXTimingSetupAns    = 0x08
    TXParamSetupReq     = 0x09
    TXParamSetupAns     = 0x09
    DLChannelReq        = 0x0A
    DLChannelAns        = 0x0A
    RekeyInd            = 0x0B
    RekeyConf           = 0x0B
    ADRParamSetupReq    = 0x0C
    ADRParamSetupAns    = 0x0C
    DeviceTimeReq       = 0x0D
    DeviceTimeAns       = 0x0D
    ForceRejoinReq      = 0x0E
    RejoinParamSetupReq = 0x0F
    RejoinParamSetupAns = 0x0F

    # Class-B	
    PingSlotInfoReq     = 0x10
    PingSlotInfoAns     = 0x10
    PingSlotChannelReq  = 0x11	
    PingSlotChannelAns  = 0x11
    # 0x12 has been deprecated in 1.1
    BeaconFreqReq       = 0x13
    BeaconFreqAns       = 0x13
    
    # Class-C
    DeviceModeInd       = 0x20
    DeviceModeConf      = 0x20

    ActuatorReq         = 0x0E
    ActuatorAns         = 0x0E

    # define command type
    Req = 0x00
    Ans = 0x01

    def create_command_payload(args):
        payload = []
        payload += [args['cid']]
        # Sinknode(Network server) should respond with LinkCheckAns
        if args['cid'] == CID.LinkCheckAns:              
            payload+=args['margin']
            payload+=args['gwcnt']       # Network server knows Gateway_Count
        
        # Network server use the command to request that an end-dev performs a rate adaptation
        elif args['cid'] == CID.LinkADRReq:
            payload+=args['datarate_txpower']   # 1 Octet ([7:4]bits Datarate | [3:0]bits TXPower)
            payload+=args['chmask']             # 2 Octets 
            payload+=args['redundancy']         # 1 Octet (7bit RFU | [6:4]bits ChMaskCntl | [3:0]bits NbTrans)
        elif args['cid'] == CID.DutyCycleReq:
            payload+=args['dutycyclepl']        # 1 Octet ([7:4]bits RFU | [3:0]bits MaxDCycle)
        elif args['cid'] == CID.RXParamSetupReq:
            payload+=args['dlsettings']         # 1 Octet (7bit RFU | [6:4]bits RX1DROffset | [3:0]bits RX2DataRate)
            payload+=args['frequency']          # 3 Octets
        elif args['cid'] == CID.NewChannelReq:
            payload+=args['chindex']            # 1 Octet
            payload+=args['freq']               # 3 Octets
            payload+=args['drrange']            # 1 Octet ([7:4]bits MaxDR | [3:0]bits MinDR)
        elif args['cid'] == CID.RXTimingSetupReq:
            payload+=args['settings']           # 1 Octet ([7:4]bits RFU | [3:0]bits Del(=Delay id))
        elif args['cid'] == CID.TXParamSetupReq:
            payload+=args['eirp_dwelltime']     # 1 Octet ([7:6]bits RFU | 5bit DownlinkDwellTime | 4bit Uplink" | [3:0]MaxEIRP)
            # key => CodedValue(0~1)  |  value => DwellTime
            # 0:NoLimit, 1:400 ms
            # CodedValue(0~15) : MaxEIRP(dBm)
            # 0:8, 1:10, 2:12, 3:13, 4:14, 5:16, 6:18, 7:20, 8:21, 9:24, 10:26, 11:27, 12:29, 13:30, 14:33, 15:36
        elif args['cid'] == CID.DLChannelReq:
            payload+=args['chindex']            # 1 Octet
            payload+=args['freq']               # 3 Octets

        # Network server provides the network time to the end-dev
        elif args['cid'] == CID.DeviceTimeAns:
            payload+=args['seconds_since_epoch']    # 4 Octets (32bit unsigned int)
            payload+=args['fractional_second']      # 1 Octet (8bit unsigned int | second in (1/2)^8 sec steps)
        
        elif args['cid'] == CID.ActuatorReq:
            payload_size = 1
            payload+=[args['aid']]
            for action_value in args['values']:
                if payload_size>15:
                    print('[WARNING] MacCommand payload size exceeded 15 Bytes...')
                payload+=[action_value['value']]
                payload+=[action_value['sleep']]
                payload_size+=2

        return payload


    # Handle Uplink Commands(End-dev to GW)
    def handle_command_payload(lorawan, nodeid, payload, mqttclient): # received mac command payload(received Frame Payload)
        cid = payload[0]
        ans_payload = []
        if cid == CID.LinkCheckReq:
            margin = 0x00
            # GET request to Flask Server
            # Should not wait long
            GWCnt = 0x00
            ans_payload = create_command_payload({'cid':CID.LinkCheckAns, 'margin': margin, 'gwcnt':GWCnt})        
            return CID.Req, ans_payload
        elif cid == CID.DutyCycleAns:
            return CID.Ans, ans_payload
        elif cid == CID.RXParamSetupAns:
            return CID.Ans, ans_payload
        elif cid == CID.DevStatusAns:
            print('[MacCommand]: Received DevStatusAns...')
            battery = payload[1]
            radio_status = payload[2]
            status_dict = {'nodeid':nodeid, 'battery':battery, 'radio_status':radio_status} # Need end-device's id in this data
            mqttclient.publish('command/uplink/DevStatusAns/' + str(nodeid), json.dumps(status_dict))
            print('[MQTT]: ',status_dict," Published via MQTT...")
            return CID.Ans, ans_payload
        elif cid == CID.NewChannelAns:
            return CID.Ans, ans_payload
        elif cid == CID.RXTimingSetupAns:
            return CID.Ans, ans_payload
        elif cid == CID.TXParamSetupAns:
            return CID.Ans, ans_payload
        elif cid == CID.DLChannelAns:
            return CID.Ans, ans_payload
        elif cid == CID.DeviceTimeReq:
            ans_payload += [CID.DeviceTimeReq]
            return CID.Req, ans_payload
        elif cid == CID.ActuatorAns:
            return CID.Ans, ans_payload
