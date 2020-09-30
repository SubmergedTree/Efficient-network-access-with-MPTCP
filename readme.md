# Effizienter Netzzugang mit MPTCP
(Efficient network access with MPTCP)

# Testbeds
- Kernel Parameter Testbed: mptcp_net.py and no_mptcp_net.py
- Socket Options Testbed: so_testbed.py

# NGINX config
Example config for Reverse Proxy configuration to be used in the testbeds.

# Setup:
- VirtualBox
- install Ubuntu 18.04.5 LTS Server Image (20 should also work) as VM (or two VMs if you want to use the Kernel Parameters testbed.)
- install mininet http://mininet.org/download (from source or packet manager)
- install MPTCP. https://multipath-tcp.org/pmwiki.php/Users/AptRepository
- Use apply routing config scripts: https://multipath-tcp.org/pmwiki.php/Users/ConfigureRouting
- Configuration options can be found here: https://multipath-tcp.org/pmwiki.php/Users/ConfigureMPTCP