#!/usr/bin/python3 -u

__builtins__.KeyboardInterrupt = __builtins__.SystemExit
import hashlib
import asyncio
import asynccmd
del asynccmd.Cmd.do_test

from secrets import FLAG, KEY, CREDS

H = lambda b: hashlib.sha256(b).digest()
EH = lambda *x: print(x[1]['exception'])


def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


class Validator:
    def __init__(self, buf):
        self.buf = buf
        self.counter = 0

    async def __invert__(self):
        self.counter += 1
        assert self.counter < 10000, "Invalid login"
        xx = xor(H(self.buf[-32:]), self.buf[:32])
        self.buf = xx + xor(H(xx), self.buf[-32:])

    def __radd__(self, *args):
        eval(self.buf[:-32])

    def __bool__(self, *args, **kwargs):
        return H(self.buf[:32]+KEY) == self.buf[-32:]


class Cli(asynccmd.Cmd):
    intro = f'Guest credentials: guest / {CREDS}'
    prompt = '>>> '
    score = 0

    def __init__(self, loop):
        self.cmdloop(loop)
        self.loop.set_exception_handler(EH)

    def do_login(self, arg):
        try:
            user, password = arg.split()
            self.loop.create_task(self.login(user, password))
        except ValueError:
            raise RuntimeError('Usage: login [username] [password]')

    async def login(self, user, password):
        if await self.validate(bytes.fromhex(password)):
            print("Logged in as {user}.")

    async def  validate(self, aval):
        bval = Validator(aval)
        while not bval:
            await (~bval)
        self.score += bval

    def do_play_game_and_get_points(self, arg):
        raise NotImplementedError('TODO later, maybe.')

    def do_flag(self, arg):
        try:
            assert self.score > 1337
            print(FLAG)
        except Exception:
            print("Not yet.")


async def main():
    Cli(asyncio.get_event_loop())
    await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
