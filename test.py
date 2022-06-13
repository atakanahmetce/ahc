from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel
from node_model.GenericNode import UsrpNode

def main():
  topo = Topology()
  topo.construct_winslab_topology_with_channels(4, UsrpNode, GenericChannel)
  topo.start()
  
  source = 1
  dest = 2
  message = "hw!"

  topo.nodes[source].appl.send_down(message, dest)
  
if __name__ == '__main__':
  main()