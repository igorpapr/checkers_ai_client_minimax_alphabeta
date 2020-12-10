import asyncio
import logging
import threading

from test_bot import Bot

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    _loop = asyncio.get_event_loop()
    thread = threading.Thread(target=Bot(_loop).start_test)
    thread.start()
    _loop.run_forever()
