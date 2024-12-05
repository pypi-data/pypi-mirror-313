import asyncio
import aioping

import sys
target = sys.argv[1]

async def do_ping1(host):
    print(f"{host=}")
    try:
        delay = await aioping.ping(host, timeout=1) * 1000
        print("Ping response in %s ms" % delay)

    except TimeoutError:
        print("Timed out")


async def do_ping2(host):
    command = ["ping", "-c", "1", "-t", "1", host]
    ping_timeout = 0.5
    subprocess = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL)
    # failure occurs through timeout
    returncode = await asyncio.wait_for(
        subprocess.wait(), timeout=ping_timeout)
    print(f"{returncode=}")

print("with aioping")
asyncio.run(do_ping1(target))
print("with ping & subprocess")
asyncio.run(do_ping2(target))
