#!/usr/bin/env python3
MAX_BUF = 4096

import asyncio, telnetlib3

print(telnetlib3.__file__)

print(telnetlib3.__get_version())

async def shell(reader, writer):

    recv = await reader.read(MAX_BUF)
    print(f'--init--(({recv}))', end='', flush=True)

    commands = []
    commands.append("echo 1")
    commands.append("echo 2; echo 3")
    commands.append("echo 4; echo 5; echo 6;")
    commands.append("""[ -d /mnt ] || mkdir /mnt; mount /dev/sda1 /mnt && { echo "2019-05-29@14:44 - node fit37  - image f-strings - by root" >> /mnt/etc/rhubarbe-image ; umount /mnt; } ; imagezip -o -z1 /dev/sda - | nc 192.168.3.100 10001; echo STATUS=$?""")
    commands.append('exit')

    for command in commands:
        print(f'[[{command}]]')
        writer.write(command + '\n')
        recv = await reader.read(MAX_BUF)
        if reader.at_eof():
            # End of File
            break
        print(f"(({recv}))", end="", flush=True)
    while not reader.at_eof():
        recv = await reader.read(MAX_BUF)
        print(f"::{recv}::", end="", flush=True)

loop = asyncio.new_event_loop()
coro = telnetlib3.open_connection('fit04', 23, shell=shell)
reader, writer = loop.run_until_complete(coro)
loop.run_until_complete(writer.protocol.waiter_closed)
