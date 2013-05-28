#!/usr/bin/python
#####################################################################
# Python script provided by Vinod Halaharvi
# RTP Network services
# Email: vinod.halaharvi@gmail.com, vinod.halaharvi@rtpnet.net
# Usage: cat listfile | python threadscommands.py --command=dig 
#####################################################################
import Queue, os, threading,  time,  shlex, subprocess,  sys 
exitFlag = 0

class CommandThread (threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q
    def run(self):
        processdata(self.name, self.q)

def snmp(line):
	(device, community , oid) = line.split(delimiter)
	"""docstring for snmp"""
	#snmpwalk -Os -c public -v 1 localhost system
	return "snmpwalk -Os  -c %s -v 1 %s %s" % ( community, device, oid) 


def ping(line):
	"""docstring for ping"""
	return "ping -c 2 " + line	

def dig(line):
        """docstring for getcommand"""
        return "dig " + line 


commands = {
		'dig': dig, 
		'ping': ping, 
		'snmp': snmp, 
	}

def run(line):
        """docstring for run"""
        line = line.strip()
	if not rawcommands:
		commandf = commands.get(command, '')
		if not commandf:
			return 
		else:
			cmdline = commandf(line)
			print cmdline
	else:
		cmdline = line
		print cmdline
        p = subprocess.Popen(shlex.split(cmdline),
                                 stdout = subprocess.PIPE,
                                 stderr = subprocess.PIPE,
                                 env = os.environ
                        )
        stdout, stderr = p.communicate()
	if stderr:
		print stderr
	print stdout
        p.stderr.close()
        p.stdout.close()
        status = p.returncode

# function that actually does something
def processdata(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            line = q.get()
            queueLock.release()
            args = shlex.split(line)
	    run(line)
        else:
            queueLock.release()

# globals
#Using 100 threads
#Increase this list if you want to open more threads

if __name__ == '__main__':
	import optparse
	parser = optparse.OptionParser(usage="usage: %prog [options] < commandlistfile")
	parser.add_option(
		"-H", "--Help",
		action="store_true", dest="Help", default=False, 
		help="More descriptive help message",
	)
	parser.add_option("-n", "--numthreads",
			dest="numthreads", default=10, type="int",
			help="Number of threads of execution", 
	)
	parser.add_option("-r", "--rawcommands",
			action="store_true", dest="rawcommands", default=False,
			help="Treat input as raw commands? Boolen value", 
	)
	parser.add_option("-d", "--delimiter",
			dest="delimiter", default=",",
			help="""Delimiter if any in the input stream
			input is split on this delimiter and they become 
			params to the 'command'""", 
	)
	parser.add_option("-c", "--command",
			dest="command", default="ping",
			help="command to execute, eg. ping, dig, snmp", 
	)
	(options, args) = parser.parse_args(sys.argv)
	if options.rawcommands and options.command != "ping":
		print "You cannot give both rawcommands and command option .."
		sys.exit(0)

	if options.Help:
		print """
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
				
		"""
		sys.exit(0)
	delimiter = options.delimiter
	rawcommands =  options.rawcommands
	numthreads = options.numthreads
	command = options.command

	threadList = ["Thread" + str(suffix) for suffix in range(numthreads)]
	queueLock = threading.Lock()
	workQueue = Queue.Queue()
	#input comes from stdin
	file = sys.stdin
	#file = open("list", "r")
	threads = []
	threadID = 1

	# Fill the queue
	queueLock.acquire()
	for line in file.readlines():
	    workQueue.put(line)
	queueLock.release()

	# Create new threads
	for tName in threadList:
	    thread = CommandThread(threadID, tName, workQueue)
	    thread.start()
	    threads.append(thread)
	    threadID += 1

	# Wait for queue to empty
	while not workQueue.empty():
	    pass

	# Notify threads it's time to exit
	exitFlag = 1

	# Wait for all threads to complete
	for t in threads:
	    t.join()
