#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf

def emptyNet():
    NODE1_IP='192.168.56.101'
    NODE2_IP='192.168.56.102'
    CONTROLLER_IP='192.168.56.102'

    net = Mininet( topo=None,
                   build=False)

    net.addController( 'c0',
                      controller=RemoteController,
                      ip=CONTROLLER_IP,
                      port=6633)

    h3 = net.addHost( 'h3', ip='10.0.2.3' )
    h4 = net.addHost( 'h4', ip='10.0.2.4' )
    s2 = net.addSwitch( 's2' )
    net.addLink( h3, s2 )
    net.addLink( h4, s2 )

    s2.cmd('ip tun del s2-gre1')
    s2.cmd('ip li ad s2-gre1 type gretap local '+NODE2_IP+' remote '+NODE1_IP+' ttl 64')
    s2.cmd('ip li se dev s2-gre1 up')
    Intf( 's2-gre1', node=s2 )

    net.start()
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    emptyNet()
