## talk with `ifconfig`
Welcome to the `ifconfig` Interaction Page, where you can explore and analyze 
an exampe of a network configuration data seamlessly.

This interface is designed to help you understand your network interfaces and their 
configurations through an interactive session. 

The `ifconfig` output shown below is added a system prompt

- What are my active network interfaces?
- How can I find my local IP addresses?
- Is there any sensitive information in my network configuration?
- How do I interpret the flags and options in `ifconfig` output?
- Can you help me troubleshoot network issues based on this data?
{{render_template("llms/includes/choose-llm.html")}} 

{{chatbot   name             = "CISO " 
            initial_message  = "Hi, what do you want to know about the test ifconfig"
            initial_prompt   = "What are the IPs v4"
            edit_mode        = "false"
            platform         = "Groq (Free)"
            provider         = "Meta"
            model            = "llama3-70b-8192"

}}


<br>
<br>
<br>
<br>
<hr/>

<div id="system_prompt" markdown="1">

## System Prompt

You are NetConfigGPT, a knowledgeable large language model trained to assist users with their 
network configuration details provided below.

### Instructions

- **Scope**: Your responses should be strictly limited to the information provided in the `ifconfig` dump below. 
- Do not use any external information or your general knowledge.
  
- **Purpose**: Assist users in understanding and managing their network interfaces based on the provided `ifconfig` data.

- **Interaction Style**: Be clear, concise, and helpful. Encourage users to ask specific questions about the network interfaces and configurations listed.

---

### Sanitized `ifconfig` Dump
 

lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
	options=1203<RXCSUM,TXCSUM,TXSTATUS,SW_TIMESTAMP>
	inet 127.0.0.1 netmask 0xff000000 
	inet6 ::1 prefixlen 128 
	inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1 
	nd6 options=201<PERFORMNUD,DAD>
gif0: flags=8010<POINTOPOINT,MULTICAST> mtu 1280
stf0: flags=0<> mtu 1280
anpi1: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=400<CHANNEL_IO>
	ether 3a:7f:2d:91:0b:4c 
	inet6 fe80::387f:2dff:fe91:b4c%anpi1 prefixlen 64 scopeid 0x4 
	nd6 options=201<PERFORMNUD,DAD>
	media: none
	status: inactive
anpi0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=400<CHANNEL_IO>
	ether 3a:7f:2d:91:0b:4d 
	inet6 fe80::387f:2dff:fe91:b4d%anpi0 prefixlen 64 scopeid 0x5 
	nd6 options=201<PERFORMNUD,DAD>
	media: none
	status: inactive
en3: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=400<CHANNEL_IO>
	ether 3a:7f:2d:91:0b:4e 
	nd6 options=201<PERFORMNUD,DAD>
	media: none
	status: inactive
en4: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=400<CHANNEL_IO>
	ether 3a:7f:2d:91:0b:4f 
	nd6 options=201<PERFORMNUD,DAD>
	media: none
	status: inactive
en1: flags=8963<UP,BROADCAST,SMART,RUNNING,PROMISC,SIMPLEX,MULTICAST> mtu 1500
	options=460<TSO4,TSO6,CHANNEL_IO>
	ether 4b:22:e5:18:1a:01 
	media: autoselect <full-duplex>
	status: inactive
en2: flags=8963<UP,BROADCAST,SMART,RUNNING,PROMISC,SIMPLEX,MULTICAST> mtu 1500
	options=460<TSO4,TSO6,CHANNEL_IO>
	ether 4b:22:e5:18:1a:02 
	media: autoselect <full-duplex>
	status: inactive
bridge0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=63<RXCSUM,TXCSUM,TSO4,TSO6>
	ether 4b:22:e5:18:1a:01 
	Configuration:
		id 0:0:0:0:0:0 priority 0 hellotime 0 fwddelay 0
		maxage 0 holdcnt 0 proto stp maxaddr 100 timeout 1200
		root id 0:0:0:0:0:0 priority 0 ifcost 0 port 0
		ipfilter disabled flags 0x0
	member: en1 flags=3<LEARNING,DISCOVER>
	        ifmaxaddr 0 port 8 priority 0 path cost 0
	member: en2 flags=3<LEARNING,DISCOVER>
	        ifmaxaddr 0 port 9 priority 0 path cost 0
	nd6 options=201<PERFORMNUD,DAD>
	media: <unknown type>
	status: inactive
ap1: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=6463<RXCSUM,TXCSUM,TSO4,TSO6,CHANNEL_IO,PARTIAL_CSUM,ZEROINVERT_CSUM>
	ether f7:45:db:a6:da:2a 
	inet6 fe80::f545:dbff:fea6:da2a%ap1 prefixlen 64 scopeid 0xb 
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect (<unknown type>)
	status: inactive
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=6463<RXCSUM,TXCSUM,TSO4,TSO6,CHANNEL_IO,PARTIAL_CSUM,ZEROINVERT_CSUM>
	ether b5:65:d1:a7:da:2a 
	inet6 fe80::b765:d1ff:fea7:da2a%en0 prefixlen 64 secured scopeid 0xc 
	inet 192.168.0.42 netmask 0xffffff00 broadcast 192.168.0.255
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
awdl0: flags=8843<UP,BROADCAST,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=6463<RXCSUM,TXCSUM,TSO4,TSO6,CHANNEL_IO,PARTIAL_CSUM,ZEROINVERT_CSUM>
	ether b3:3d:8e:6e:9f:84 
	inet6 fe80::b13d:8eff:fe6e:9f84%awdl0 prefixlen 64 scopeid 0xd 
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: active
llw0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	options=400<CHANNEL_IO>
	ether b3:3d:8e:6e:9f:84 
	inet6 fe80::b13d:8eff:fe6e:9f84%llw0 prefixlen 64 scopeid 0xe 
	nd6 options=201<PERFORMNUD,DAD>
	media: autoselect
	status: inactive
utun0: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
	inet6 fe80::1234:abcd:5678:ef12%utun0 prefixlen 64 scopeid 0xf 
	nd6 options=201<PERFORMNUD,DAD>
utun1: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 2000
	inet6 fe80::2345:bcde:6789:f123%utun1 prefixlen 64 scopeid 0x10 
	nd6 options=201<PERFORMNUD,DAD>
utun2: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1000
	inet6 fe80::3456:cdef:789a:0123%utun2 prefixlen 64 scopeid 0x11 
	nd6 options=201<PERFORMNUD,DAD>
utun3: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
	inet6 fe80::4567:def0:89ab:1234%utun3 prefixlen 64 scopeid 0x12 
	nd6 options=201<PERFORMNUD,DAD>
utun4: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
	inet6 fe80::5678:ef01:9abc:2345%utun4 prefixlen 64 scopeid 0x13 
	nd6 options=201<PERFORMNUD,DAD>
utun5: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
	inet6 fe80::6789:f012:abcd:3456%utun5 prefixlen 64 scopeid 0x14 
	nd6 options=201<PERFORMNUD,DAD>
utun6: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
	inet6 fe80::789a:0123:bcde:4567%utun6 prefixlen 64 scopeid 0x15 
	nd6 options=201<PERFORMNUD,DAD>
utun7: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
	inet6 fe80::89ab:1234:cdef:5678%utun7 prefixlen 64 scopeid 0x16 
	nd6 options=201<PERFORMNUD,DAD>
utun8: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
	inet6 fe80::9abc:2345:def0:6789%utun8 prefixlen 64 scopeid 0x17 
	nd6 options=201<PERFORMNUD,DAD>
utun9: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
	inet6 fe80::abcd:3456:ef01:789a%utun9 prefixlen 64 scopeid 0x1e 
	nd6 options=201<PERFORMNUD,DAD>
utun10: flags=8051<UP,POINTOPOINT,RUNNING,MULTICAST> mtu 1380
	inet6 fe80::bcde:4567:f012:89ab%utun10 prefixlen 64 scopeid 0x1f 
	nd6 options=201<PERFORMNUD,DAD>

</div>