#!/usr/bin/env python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink,Intf
from subprocess import Popen, PIPE
from mininet.log import setLogLevel
from mininet.node import Controller, RemoteController, Node

 

if '__main__' == __name__:
  setLogLevel('info')

  NODE1_IP='192.168.56.101'
  NODE2_IP='192.168.56.102'
  CONTROLLER_IP='192.168.56.102'

  net = Mininet( topo=None,
    build=False)

  net.addController( 'c0',
    controller=RemoteController,
    ip=CONTROLLER_IP,
    port=6633)


  # Client
  h1 = net.addHost('h1')
  # Proxy
  h2 = net.addHost('h2')
  # Router with static routes
  r1 = net.addHost('r1')

  s1 = net.addSwitch('s1')

  linkoptWlan={'bw':20, 'delay': 20}
  linkoptMobil={'bw':10, 'delay': 100, 'loss': 2}

  net.addLink(r1,h1,cls=TCLink, **linkoptMobil)
  net.addLink(r1,h1,cls=TCLink, **linkoptWlan)

  linkopt2={'bw':50}
  net.addLink(r1,s1,cls=TCLink, **linkopt2)
  net.addLink(s1,h2,cls=TCLink, **linkopt2)

  test = net.addHost('test', ip='10.0.0.9')
  net.addLink(s1, test, **linkopt2)
  net.build()
  
  # Reset network interfaces
  r1.cmd("ifconfig r1-eth0 0")
  r1.cmd("ifconfig r1-eth1 0")
  r1.cmd("ifconfig r1-eth2 0")
  h1.cmd("ifconfig h1-eth0 0")
  h1.cmd("ifconfig h1-eth1 0")
  h2.cmd("ifconfig h2-eth0 0")

  # enable ip forwarding
  r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
  r1.cmd("ifconfig r1-eth0 10.0.0.1 netmask 255.255.255.0")
  r1.cmd("ifconfig r1-eth1 10.0.1.1 netmask 255.255.255.0")
  r1.cmd("ifconfig r1-eth2 10.0.2.1 netmask 255.255.255.0")

  h1.cmd("ifconfig h1-eth0 10.0.0.2 netmask 255.255.255.0")
  h1.cmd("ifconfig h1-eth1 10.0.1.2 netmask 255.255.255.0")

  h2.cmd("ifconfig h2-eth0 10.0.2.2 netmask 255.255.255.0")
  
  # configure mptcp on client
  h1.cmd("ip rule add from 10.0.0.2 table 1")
  h1.cmd("ip rule add from 10.0.1.2 table 2")
  h1.cmd("ip route add 10.0.0.0/24 dev h1-eth0 scope link table 1")
  h1.cmd("ip route add default via 10.0.0.1 dev h1-eth0 table 1")
  h1.cmd("ip route add 10.0.1.0/24 dev h1-eth1 scope link table 2")
  h1.cmd("ip route add default via 10.0.1.1 dev h1-eth1 table 2")
  h1.cmd("ip route add default scope global nexthop via 10.0.0.1 dev h1-eth0")

  # configure mptcp on proxy
  h2.cmd("ip rule add from 10.0.2.2 table 1")
  h2.cmd("ip route add 10.0.2.0/24 dev h2-eth0 scope link table 1")
  h2.cmd("ip route add default via 10.0.2.1 dev h2-eth0 table 1")
  h2.cmd("ip route add default scope global nexthop via 10.0.2.1 dev h2-eth0")


  #Delete old GRE tunnel
  s1.cmd('ip tun del s1-gre1')
  # Create GRE tunnel
  s1.cmd('ip li ad s1-gre1 type gretap local '+NODE1_IP+' remote '+NODE2_IP+' ttl 64')
  s1.cmd('ip li se dev s1-gre1 up')
  Intf( 's1-gre1', node=s1 )

  net.start()
  CLI(net)

  net.stop()