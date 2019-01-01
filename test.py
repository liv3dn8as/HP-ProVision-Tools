from __future__ import print_function
from __future__ import unicode_literals
import re
import time
import socket
from netmiko.cisco_base_connection import CiscoSSHConnection
from netmiko import log
import paramiko
import time

#cleanup output jibberish
def cleanup(self):
	"""Gracefully exit the SSH session."""
	self.exit_config_mode()
	self.write_channel("logout" + self.RETURN)
	count = 0
	while count <= 5:
		time.sleep(0.5)
		output = self.read_channel()
		if "Do you want to log out" in output:
			self._session_log_fin = True
			self.write_channel("y" + self.RETURN)
		# Don't automatically save the config (user's responsibility)
		elif "Do you want to save the current" in output:
			self._session_log_fin = True
			self.write_channel("n" + self.RETURN)

		try:
			self.write_channel(self.RETURN)
		except socket.error:
			break
		count += 1

def disable_paging(remote_conn):
    '''Disable paging on a HP router'''

    remote_conn.send("terminal length 1000\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output
	
if __name__ == '__main__':

# VARIABLES THAT NEED CHANGED
	ip = '10.1.1.1'
	uname = 'admin'
	pw = 'he770@d187.org'

remote_conn_pre=paramiko.SSHClient()
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())

remote_conn_pre.connect(ip, username=uname, password=pw, look_for_keys=False, allow_agent=False)
print ("SSH Connection established to %s" % ip)

# Use invoke_shell to establish an 'interactive session'
remote_conn=remote_conn_pre.invoke_shell()

#strip initial prompt
output=remote_conn.recv(1000)
print(output)

#turn off paging
disable_paging(remote_conn)

remote_conn.send("\n")
remote_conn.send("show run")

time.sleep(3)

output=remote_conn.recv(65535)
print(output)