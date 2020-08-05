ssh debug hangs at
```
debug1: expecting SSH2_MSG_KEX_ECDH_REPLY
```

Controls TCP Packetization-Layer Path MTU Discovery. 
```
echo 1 > /proc/sys/net/ipv4/tcp_mtu_probing

0 - Disabled
1 - Disabled by default, enabled when an ICMP black hole detected
2 - Always enabled, use initial MSS of tcp_base_mss.
```

changing the kex algorithms
```
ssh -o KexAlgorithms=ecdh-sha2-nistp52
```
