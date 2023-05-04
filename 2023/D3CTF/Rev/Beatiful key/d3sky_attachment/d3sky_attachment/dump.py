import subprocess 
import string
import itertools
from string import printable
print(printable)
pp = "0123456789abcdefABCDEF"
li = itertools.permutations(pp, 4)
for i in li:
    cin = ''.join(i)
    command = "vm.exe "
    p = subprocess.Popen([command,cin+"b"*32], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #p.stdin.write(b"1")
    out=p.stdout.read().decode()
    if("192"  not in out):
        print(out)
    p.stdout.close()
    p.kill()