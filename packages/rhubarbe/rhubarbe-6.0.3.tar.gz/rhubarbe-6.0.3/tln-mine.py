#!/usr/bin/env python3

import time

import asyncio
import telnetlib3
import logging

# if an individual command outputs more than that
# then we are in trouble
MAX_BUF = 16 * 1024

async def _shell(reader, writer, commands):

    recv = await reader.read(MAX_BUF)
    print(f'--init--(({recv}))', end='', flush=True)

    commands.append('echo _TELNET_STATUS=$?')
    commands.append('exit')

    for command in commands:
        print(f'[[{command}]]')
        writer.write(command + '\n')

    while True:
        if reader.at_eof():
            break
        recv = await reader.read(MAX_BUF)
        print(f"(({recv}))", end="", flush=True)

async def shell(reader, writer):
    commands = [
        'hostname',
        'cat /etc/fedora-release',
        'cat /etc/lsb-release',
        'frisbee -i 192.168.3.4 -m 234.5.6.1 -p 10001 /dev/sda',
    ]

    await _shell(reader, writer, commands)

async def complete(hostname, timeout, connect_minwait, connect_maxwait):
    print(f"timeout={timeout} min={connect_minwait}, max={connect_maxwait}")
    coro = telnetlib3.open_connection(
        hostname, 23, shell=None,
        connect_minwait=connect_minwait,
        connect_maxwait=connect_maxwait)
    start = time.time()
    try:
        result = reader, writer = await asyncio.wait_for(coro, timeout=timeout)
        middle = time.time()
        print(f"connection duration={middle-start}")
        await shell(reader, writer)
    except (asyncio.TimeoutError, OSError) as exc:
        # logging.error(f"OOPS {type(exc)} : {exc}")
        logging.error(f"OOPS: {type(exc)} {exc} ")
        result = None, None
    end = time.time()
    print(f"total duration={end-start}")
    return result


print(telnetlib3.__get_version())

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-t", "--timeout", dest='timeout', default=5.0, type=float)
parser.add_argument("-a", "--max", dest='connect_maxwait', default=3.0, type=float)
parser.add_argument("-i", "--min", dest='connect_minwait', default=1.0, type=float)
parser.add_argument("hostname")

args = parser.parse_args()

hostname = args.hostname

loop = asyncio.new_event_loop()
ok = loop.run_until_complete(
    complete(args.hostname, args.timeout,
             args.connect_minwait, args.connect_maxwait))
print(ok)
