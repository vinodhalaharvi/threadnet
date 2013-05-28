##Run set of commands from a file each in a seperate thread
>"Specially helpful while running network diagnostic commands like ping, dig and such. Since these commands impose timeouts it's more efficient timewise to run them parallely."

###Simple Usage
####python threadedcommands.py -n 10 -r  < commandlist
####contents of sample input file
	ssh localhost "hostname -i"
	whois vinodhalaharvi.com
	ping -c 1 localhost
####Please see below for output
	PING localhost (127.0.0.1) 56(84) bytes of data.
	64 bytes from localhost (127.0.0.1): icmp_req=1 ttl=64 time=0.051 ms

	--- localhost ping statistics ---
	1 packets transmitted, 1 received, 0% packet loss, time 0ms
	rtt min/avg/max/mdev = 0.051/0.051/0.051/0.000 ms


	Whois Server Version 2.0

	Domain names in the .com and .net domains can now be registered
	with many different competing registrars. Go to http://www.internic.net
	for detailed information.

	   Domain Name: VINODHALAHARVI.COM
	   Registrar: GODADDY.COM, LLC
	   Whois Server: whois.godaddy.com
	   Referral URL: http://registrar.godaddy.com
	   Name Server: NS73.DOMAINCONTROL.COM
	   Name Server: NS74.DOMAINCONTROL.COM
	   Status: ok
	   Updated Date: 07-oct-2012
	   Creation Date: 08-dec-2011
	   Expiration Date: 08-dec-2014

	>>> Last update of whois database: Tue, 28 May 2013 20:08:56 UTC <<<

	NOTICE: The expiration date displayed in this record is the date the 
	registrar's sponsorship of the domain name registration in the registry is 
	currently set to expire. This date does not necessarily reflect the expiration 
	date of the domain name registrant's agreement with the sponsoring 
	registrar.  Users may consult the sponsoring registrar's Whois database to 
	view the registrar's reported date of expiration for this registration.

	TERMS OF USE: You are not authorized to access or query our Whois 
	database through the use of electronic processes that are high-volume and 
	automated except as reasonably necessary to register domain names or 
	modify existing registrations; the Data in VeriSign Global Registry 
	Services' ("VeriSign") Whois database is provided by VeriSign for 
	information purposes only, and to assist persons in obtaining information 
	about or related to a domain name registration record. VeriSign does not 
	guarantee its accuracy. By submitting a Whois query, you agree to abide 
	by the following terms of use: You agree that you may use this Data only 
	for lawful purposes and that under no circumstances will you use this Data 
	to: (1) allow, enable, or otherwise support the transmission of mass 
	unsolicited, commercial advertising or solicitations via e-mail, telephone, 
	or facsimile; or (2) enable high volume, automated, electronic processes 
	that apply to VeriSign (or its computer systems). The compilation, 
	repackaging, dissemination or other use of this Data is expressly 
	prohibited without the prior written consent of VeriSign. You agree not to 
	use electronic processes that are automated and high-volume to access or 
	query the Whois database except as reasonably necessary to register 
	domain names or modify existing registrations. VeriSign reserves the right 
	to restrict your access to the Whois database in its sole discretion to ensure 
	operational stability.  VeriSign may restrict or terminate your access to the 
	Whois database for failure to abide by these terms of use. VeriSign 
	reserves the right to modify these terms at any time. 

	The Registry database contains ONLY .COM, .NET, .EDU domains and
	Registrars.
	The data contained in GoDaddy.com, LLC's WhoIs database,
	while believed by the company to be reliable, is provided "as is"
	with no guarantee or warranties regarding its accuracy.  This
	information is provided for the sole purpose of assisting you
	in obtaining information about domain name registration records.
	Any use of this data for any other purpose is expressly forbidden without the prior written
	permission of GoDaddy.com, LLC.  By submitting an inquiry,
	you agree to these terms of usage and limitations of warranty.  In particular,
	you agree not to use this data to allow, enable, or otherwise make possible,
	dissemination or collection of this data, in part or in its entirety, for any
	purpose, such as the transmission of unsolicited advertising and
	and solicitations of any kind, including spam.  You further agree
	not to use this data to enable high volume, automated or robotic electronic
	processes designed to collect or compile this data for any purpose,
	including mining this data for your own personal or commercial purposes. 

	Please note: the registrant of the domain name is specified
	in the "registrant" field.  In most cases, GoDaddy.com, LLC 
	is not the registrant of domain names listed in this database.


	   Registered through: GoDaddy.com, LLC (http://www.godaddy.com)
	   Domain Name: VINODHALAHARVI.COM
	      Created on: 08-Dec-11
	      Expires on: 08-Dec-14
	      Last Updated on: 07-Oct-12

	   Registrant:
	   Vinod Halaharvi
	   10010 Skinner Lake drive
	   Jacksonville, Florida 32246
	   United States

	   Administrative Contact:
	      Halaharvi, Vinod  halavin@iit.edu
	      10010 Skinner Lake drive
	      Jacksonville, Florida 32246
	      United States
	      9042001070

	   Technical Contact:
	      Halaharvi, Vinod  halavin@iit.edu
	      10010 Skinner Lake drive
	      Jacksonville, Florida 32246
	      United States
	      9042001070

	   Domain servers in listed order:
	      NS73.DOMAINCONTROL.COM
	      NS74.DOMAINCONTROL.COM


	192.168.0.105

#### Running preset commands
	#if you have list of hostnames in the input file you can ping and do a dns lookup on them 
	# commandlist file
	www.google.com
	www.yahoo.com
	cnn.com
	hotwire.com

	python threadedcommands.py -c ping -n 10  < commandlist

#### or a name lookup 
	python threadedcommands.py -c dig -n 10  < commandlist

####Its very easy to extend commands. Use the "commands" dict in the code to add more functions. 

	Usage: threadedcommands.py [options] < commandlistfile
	-h, --help            show this help message and exit
	-H, --Help            More descriptive help message
	-n NUMTHREADS, --numthreads=NUMTHREADS
			Number of threads of execution
	-r, --rawcommands     Treat input as raw commands? Boolen value
	-d DELIMITER, --delimiter=DELIMITER
			Delimiter if any in the input stream
			input is split on this delimiter and they become
			params to the 'command'
	-c COMMAND, --command=COMMAND
			command to execute, eg. ping, dig, snmp

		options available:
			--rawcommands
				Treat the input file as set of raw commands to be 
				executed one command per line.
			--delimiter
				default is comma(,). This is used to split each line
				of input to its fields that makes sense to that 
				particular command
			--command 
				currently available subcommands ping, dig, snmp. 
				--command=ping
				--command=dig
			Sample Usages:
				cat commandsfile | python threadedcommands.py --command=ping 
				cat commandsfile | python threadedcommands.py --command=dig 
				cat commandsfile | python threadedcommands.py --command=snmp --delimiter=","
				cat commandsfile | python threadedcommands.py --rawcommands
				python threadedcommands.py -n 10 -r  < commandlist
				
		
