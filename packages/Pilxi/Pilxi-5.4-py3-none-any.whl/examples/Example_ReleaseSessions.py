from __future__ import print_function
from pilxi import *

IPaddr = "192.168.0.240"

com = pi_comm(0, str.encode(IPaddr), 1024, 1000)

err, sessions, numSessions = com.GetForeignSessions()

for session in sessions:
    com.ReleaseForeignSession(session)

com.Disconnect()
