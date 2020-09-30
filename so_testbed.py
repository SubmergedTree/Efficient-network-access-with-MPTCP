#!/usr/bin/env python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink,Intf
from subprocess import Popen, PIPE
from mininet.log import setLogLevel
from mininet.node import Controller, RemoteController, Node



if '__main__' == __name__:
  setLogLevel('info')
  
  CONTROLLER_IP='192.168.56.102'

  net = Mininet( topo=None,
    build=False)


  net.addController( 'c0',
    controller=RemoteController,
    ip=CONTROLLER_IP,
    port=6633)

  client = net.addHost('h1')
  proxy = net.addHost('h2')  
  server = net.addHost('h3', ip='10.0.2.3')
  # Router with static routes
  router = net.addHost('r1')
  switch = net.addSwitch('s1')

  linkoptWlan={'bw':20, 'delay': 20}
  linkoptMobil={'bw':10, 'delay': 100, 'loss': 2}

  net.addLink(router,client,cls=TCLink, **linkoptMobil)
  net.addLink(router,client,cls=TCLink, **linkoptWlan)

  linkopt2={'bw':50}
  net.addLink(router,switch,cls=TCLink, **linkopt2)
  net.addLink(switch,proxy,cls=TCLink, **linkopt2)
  net.addLink(switch,server,cls=TCLink, **linkopt2)

  net.build()

  router.cmd("ifconfig r1-eth0 0")
  router.cmd("ifconfig r1-eth1 0")
  router.cmd("ifconfig r1-eth2 0")
  client.cmd("ifconfig h1-eth0 0")
  client.cmd("ifconfig h1-eth1 0")
  proxy.cmd("ifconfig h2-eth0 0")

  router.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
  router.cmd("ifconfig r1-eth0 10.0.0.1 netmask 255.255.255.0")
  router.cmd("ifconfig r1-eth1 10.0.1.1 netmask 255.255.255.0")
  router.cmd("ifconfig r1-eth2 10.0.2.1 netmask 255.255.255.0")

  client.cmd("ifconfig h1-eth0 10.0.0.2 netmask 255.255.255.0")
  client.cmd("ifconfig h1-eth1 10.0.1.2 netmask 255.255.255.0")

  proxy.cmd("ifconfig h2-eth0 10.0.2.2 netmask 255.255.255.0")

  client.cmd("ip rule add from 10.0.0.2 table 1")
  client.cmd("ip rule add from 10.0.1.2 table 2")
  client.cmd("ip route add 10.0.0.0/24 dev h1-eth0 scope link table 1")
  client.cmd("ip route add default via 10.0.0.1 dev h1-eth0 table 1")
  client.cmd("ip route add 10.0.1.0/24 dev h1-eth1 scope link table 2")
  client.cmd("ip route add default via 10.0.1.1 dev h1-eth1 table 2")
  client.cmd("ip route add default scope global nexthop via 10.0.0.1 dev h1-eth0")

  proxy.cmd("ip rule add from 10.0.2.2 table 1")
  proxy.cmd("ip route add 10.0.2.0/24 dev h2-eth0 scope link table 1")
  proxy.cmd("ip route add default via 10.0.2.1 dev h2-eth0 table 1")
  proxy.cmd("ip route add default scope global nexthop via 10.0.2.1 dev h2-eth0")
  
  net.start()
  CLI(net)
  net.stop()