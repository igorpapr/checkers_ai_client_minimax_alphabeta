import asyncio
import logging
import time
import random

import aiohttp
from checkers import game

import solver


class Bot:
    def __init__(self, loop):
        self._api_url = 'http://localhost:8081'
        self._team_name = 'Дмитрий Негрдон'
        self._session = aiohttp.ClientSession()
        self._player = {}
        self._game = game.Game()
        self._loop = loop
        self._last_move = None

    async def _prepare_player(self):
        async with self._session.post(
                f'{self._api_url}/game',
                params={'team_name': self._team_name}
        ) as resp:
            res = (await resp.json())['data']
            self._player = {
                'color': res['color'],
                'token': res['token']
            }

    async def _make_move(self, move):
        json = {'move': move}
        headers = {'Authorization': f'Token {self._player["token"]}'}
        async with self._session.post(
                f'{self._api_url}/move',
                json=json,
                headers=headers
        ) as resp:
            logging.debug(await resp.text())
            resp = (await resp.json())['data']
            logging.info(f'Player {self._team_name} made move {move}, response: {resp}')

    async def _get_game(self):
        async with self._session.get(f'{self._api_url}/game') as resp:
            return (await resp.json())['data']

    async def _play_game(self):
        current_game_progress = await self._get_game()
        is_finished = current_game_progress['is_finished']
        is_started = current_game_progress['is_started']

        while is_started and not is_finished:
            # waiting until our turn
            if current_game_progress['whose_turn'] != self._player['color']:
                current_game_progress = await self._get_game()
                is_finished = current_game_progress['is_finished']
                is_started = current_game_progress['is_started']
                await asyncio.sleep(0.1)
                continue

            # storing last moves of the opponent
            last_move = current_game_progress['last_move']
            logging.debug(last_move)
            if last_move and last_move['player'] != self._player['color']:
                for move in last_move['last_moves']:
                    logging.debug(f'apply last move {move}')
                    self._game.move(move)

            moves = self._game.get_possible_moves()
            if not moves:
                break
            move = random.choice(moves)
            await asyncio.sleep(0.5)
            self._game.move(move)

            await self._make_move(move)

            current_game_progress = await self._get_game()
            is_finished = current_game_progress['is_finished']
            is_started = current_game_progress['is_started']

    def start_test(self):
        asyncio.run_coroutine_threadsafe(self.start(), self._loop)

    async def start(self):
        try:
            logging.info('API Tester initialized, test will start in 2 secs')

            await asyncio.ensure_future(self._prepare_player())

            logging.info('Game started, players initialized')

            await asyncio.sleep(0.5)

            logging.info(f'Player: {self._player}')

            await asyncio.sleep(0.5)

            await self._play_game()

            logging.info('Game finished')
            last_game_progress = await self._get_game()
            logging.info(str(last_game_progress))

            await self._session.close()
        except Exception as e:
            logging.error(e, exc_info=True)