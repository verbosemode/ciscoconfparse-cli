#ciscoconfparse-cli

* Grep-like tool for Cisco IOS configs
* Based on [ciscoconfparse](https://pypi.python.org/pypi/ciscoconfparse/)

#Installation

	sudo cp ciscoconfparse-cli.py /usr/local/bin/ciscoconfparse-cli.py
	sudo ln -s /usr/local/bin/ciscoconfparse-cli.py /usr/local/bin/cigrep

#Examples

##Find all VLAN tagged interfaces

	$ cigrep interface "encapsulation dot1q" example.txt 
	interface Ethernet0/1.10
	interface Ethernet0/1.20


##Find all PPP and VLAN tagged interfaces

Right, regular expressions are supported ;-)

	$ cigrep ^interface "encapsulation (dot1q|ppp)" example.txt 
	interface Ethernet0/1.10
	interface Ethernet0/1.20
	interface Serial1/0
	interface Serial1/1


##Find all interfaces *without* an IP helper configuration

	$ cigrep -v ^interface "ip helper-address" example.txt 
	interface Ethernet0/0
	interface Ethernet0/1
	interface Ethernet0/1.10
	interface Serial1/0
	interface Serial1/1
	interface Serial1/2


##Use the -A option to display the complete configuration section of a matching pattern

	$ cigrep -A "^interface" "ip helper-address" example.txt 
	interface Ethernet0/1.20
	 encapsulation dot1q 20
	 ip address 172.16.20.1 255.255.255.0
	 ip helper-address 172.16.30.100

# TODO

* Multiple input filenames -> glob
  - filename: matched-pattern output
  - -l for grep-like behaviour -> List matching file names w/o matched lines
* Add setup.cfg
* Switch to argparse


## example.txt

	policy-map QOS_1
	 class GOLD
	  priority percent 10
	 class SILVER
	  bandwidth 30
	  random-detect
	 class default
	!
	interface Ethernet0/0
	 ip address 192.0.2.1 255.255.255.252
	 no cdp enable
	!
	interface Ethernet0/1
	 no ip address
	!
	interface Ethernet0/1.10
	 encapsulation dot1q 10
	 ip address 172.16.10.1 255.255.255.0
	!
	interface Ethernet0/1.20
	 encapsulation dot1q 20
	 ip address 172.16.20.1 255.255.255.0
	 ip helper-address 172.16.30.100
	!
	interface Serial1/0
	 encapsulation ppp
	 ip address 192.0.2.5 255.255.255.252
	!
	interface Serial1/1
	 encapsulation ppp
	 ip address 192.0.2.9 255.255.255.252
	 service-policy output QOS_1
	!
	interface Serial1/2
	 encapsulation hdlc
	 ip address 192.0.2.13 255.255.255.252
	!
	class-map GOLD
	 match access-group 102
	class-map SILVER
	 match protocol tcp
	!
	access-list 101 deny tcp any any eq 25 log
	access-list 101 permit ip any any
	!
	access-list 102 permit tcp any host 192.0.2.100 eq www
	access-list 102 deny ip any any
