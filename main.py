import asyncio
import logging
import threading

from bot import Bot

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    _loop = asyncio.get_event_loop()
    threading.Thread(target=Bot(_loop, rand_sleep=False).start_test).start()
    _loop.run_forever()
