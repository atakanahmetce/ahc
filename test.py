import networkx as nx
import time

from adhoccomputing.GenericModel import GenericModel
from adhoccomputing.Generics import Event, EventTypes, ConnectorTypes
from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Networking.LinkLayer.GenericLinkLayer import GenericLinkLayer
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel
from node_model import *
from node_model.GenericNode import UsrpNode

"""class AdHocNode(GenericModel):
  def on_message_from_top(self, eventobj: Event):
    self.send_down(Event(self, EventTypes.MFRT, eventobj.eventcontent))

  def on_message_from_bottom(self, eventobj: Event):
    self.send_up(Event(self, EventTypes.MFRB, eventobj.eventcontent))

  def __init__(self, componentname, componentinstancenumber):
    super().__init__(componentname, componentinstancenumber)"""


def main():
  topo = Topology()
  topo.construct_winslab_topology_with_channels(4, UsrpNode, GenericChannel)

  topo.start()
  for i in range(500):
    #from_id = random.randint(0, 3)
    from_id = 1
    #dest_id = random.randint(0, 3)
    dest_id = 2
    message = "hw!"

    topo.nodes[from_id].appl.send_down(message, dest_id)

    time.sleep(0.33)

if __name__ == '__main__':
  main()