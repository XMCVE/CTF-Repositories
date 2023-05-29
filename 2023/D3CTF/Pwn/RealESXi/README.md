This task is about a real ESXi sandbox escape. Suppose you already can execute arbitrary code in vmx, but you are still tied to the sandbox, escape from the sandbox and capture the flag (/var/run/vmware-hostd-ticket/flag).

There are two ports open for you: the ssh port and the server.py bound port. Use client.py to send your exp.
You have two known weapons: CVE-2021-22042 and CVE-2021-22043.

Local test method: install ESXi and run "python server.py" on it.

The ESXi has a long start-up time, please connect 5 minutes after the gambox start.

Many thanks to Moesang for his help in building the task environment. Server.py and client.py are partially borrowed from ESXisbx in Qiangwang Cup S5.

本题目由蚂蚁安全光年实验室命题。
This challenge is offered by Ant Group Light-Year Security Lab.

Attachment:
RealESXi.zip
HINTS:
These are two simple bugs that have nothing to do with memory corruption, diffing with the fixed version will quickly find them.
