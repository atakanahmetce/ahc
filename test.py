from adhoccomputing.Experimentation.Topology import Topology
from adhoccomputing.Networking.LogicalChannels.GenericChannel import GenericChannel
from node_model.GenericNode import UsrpNode

def main():
  topo = Topology()
  topo.construct_winslab_topology_with_channels(4, UsrpNode, GenericChannel)
  print(topo)
  """
  topo.start()
  
  from_id = 1
  dest_id = 2
  message = "hw!"

  topo.nodes[from_id].appl.send_down(message, dest_id)
  """
if __name__ == '__main__':
  main()