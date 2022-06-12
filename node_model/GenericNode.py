from enum import Enum
from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import *

from adhoccomputing.Networking.PhysicalLayer.UsrpB210OfdmFlexFramePhy import  UsrpB210OfdmFlexFramePhy
from adhoccomputing.Networking.MacProtocol.CSMA import MacCsmaPPersistent, MacCsmaPPersistentConfigurationParameters

class SlottedAlohaMessageTypes(Enum):
    SAD = "DATA"

class SlottedAlohaMessageHeader(GenericMessageHeader):
    def __init__(self, messagetype, messagefrom, messageto, message):
        super().__init__(messagetype, messagefrom, messageto)
        self.message = message

class SlottedAlohaMessagePayload(GenericMessagePayload):
    pass

class SlottedAlohaMessage(GenericMessage):
    pass

class SlottedAlohaLayer(GenericModel):
    def __init__(self, componentname, componentinstancenumber, context=None, configurationparameters=None, num_worker_threads=1, topology=None):
        super().__init__(componentname, componentinstancenumber, context, configurationparameters, num_worker_threads, topology)

    def on_init(self, eventobj: Event):
        pass
    
    def on_message_from_top(self, eventobj: Event):
        self.send_down(Event(self, EventTypes.MFRT, eventobj.eventcontent))

    def on_message_from_bottom(self, eventobj: Event):
        # self.send_up(Event(self, EventTypes.MFRB, eventobj.eventcontent))
        print("Message is: ", eventobj.eventcontent.header.message)
    
    def send_down(self, message, dest_id):
        header = SlottedAlohaMessageHeader(SlottedAlohaMessageTypes.SAD, self.componentinstancenumber, dest_id, message)
        payload = SlottedAlohaMessagePayload(None)
        message = SlottedAlohaMessage(header, payload)
        event = Event(self, EventTypes.MFRT, message)
        return super().send_down(event)

class UsrpNode(GenericModel):
    counter = 0
    def on_init(self, eventobj: Event):
        pass
    
    def __init__(self, componentname, componentinstancenumber, context=None, configurationparameters=None, num_worker_threads=1, topology=None):
        super().__init__(componentname, componentinstancenumber, context, configurationparameters, num_worker_threads, topology)
        # SUBCOMPONENTS
        
        macconfig = MacCsmaPPersistentConfigurationParameters(0.5, -51)
        #usrpconfig = SDRConfiguration(freq =900000000.0, bandwidth = 250000, chan = 0, hw_tx_gain = 50.0, hw_rx_gain = 20.0, sw_tx_gain = -12.0)
        #sdrconfig = SDRConfiguration(freq =915000000.0, bandwidth = 2000000, chan = 0, hw_tx_gain = 70, hw_rx_gain = 70, sw_tx_gain = -12.0)
        #sdrconfig = SDRConfiguration(freq =915000000.0, bandwidth = 20000000, chan = 0, hw_tx_gain = 76, hw_rx_gain = 20, sw_tx_gain = -12.0)
        
        sdrconfig = SDRConfiguration(freq =2484000000.0, bandwidth = 20000000, chan = 0, hw_tx_gain = 76, hw_rx_gain = 20, sw_tx_gain = -12.0)
        bladerfconfig = SDRConfiguration(freq =900000000.0, bandwidth = 250000, chan = 0, hw_tx_gain = 50.0, hw_rx_gain = 20.0, sw_tx_gain = -12.0)
        
        self.appl = SlottedAlohaLayer("SlottedAlohaLayer", componentinstancenumber, topology=topology)
        self.phy = UsrpB210OfdmFlexFramePhy("UsrpB210OfdmFlexFramePhy", componentinstancenumber, usrpconfig=sdrconfig, topology=topology)
        print(self.phy.sdrdev)
        self.mac = MacCsmaPPersistent("MacCsmaPPersistent", componentinstancenumber,  configurationparameters=macconfig, sdr=self.phy.sdrdev,topology=topology)
        
        self.components.append(self.appl)
        self.components.append(self.phy)
        self.components.append(self.mac)

        # CONNECTIONS AMONG SUBCOMPONENTS
        # self.appl.connect_me_to_component(ConnectorTypes.UP, self) #Not required if nodemodel will do nothing
        self.appl.connect_me_to_component(ConnectorTypes.DOWN, self.mac)
        
        self.mac.connect_me_to_component(ConnectorTypes.UP, self.appl)
        self.mac.connect_me_to_component(ConnectorTypes.DOWN, self.phy)
        
        # Connect the bottom component to the composite component....
        self.phy.connect_me_to_component(ConnectorTypes.UP, self.mac)
        self.phy.connect_me_to_component(ConnectorTypes.DOWN, self)
        
        # self.phy.connect_me_to_component(ConnectorTypes.DOWN, self)
        # self.connect_me_to_component(ConnectorTypes.DOWN, self.appl)