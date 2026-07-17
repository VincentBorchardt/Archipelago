import asyncio


def launch_civ_4_client(*args):
    from .civ_4_client import main
    asyncio.run(main(args))