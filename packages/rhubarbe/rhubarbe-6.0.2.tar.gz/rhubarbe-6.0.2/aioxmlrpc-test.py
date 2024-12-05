#!/usr/bin/env python3

# issuing GetNodes() on our plcapi instance

url = "https://r2labapi.inria.fr:443/PLCAPI/"
auth = { 'AuthMethod' : 'password',
         'Username'   : 'root@r2lab.inria.fr',
         'AuthString' : 'onecalvin' }

import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.check_hostname = False


########## synchroneous version

def sync_nodes():

    import xmlrpc.client

    proxy = xmlrpc.client.ServerProxy(url, allow_none=True, context=context)

    nodes = proxy.GetNodes(auth, {}, ['hostname'] )

    print("synchro nodes[0] -> {}".format(nodes[0]))


########## async

import asyncio


async def co_async_nodes():

    import aioxmlrpc.client

    try:
        proxy = aioxmlrpc.client.ServerProxy(url, allow_none=True, context=context)
    except:
        import traceback
        traceback.print_exc()
        exit(1)
    nodes = await proxy.GetNodes(auth, {}, ['hostname'] )
    print("asynchro nodes[0] -> {}".format(nodes[0]))


def async_nodes():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(co_async_nodes())


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-s", "--sync", default=False, action='store_true')
    args = parser.parse_args()
    synchro_mode = args.sync

    if synchro_mode:
        sync_nodes()
    else:
        async_nodes()

main()
