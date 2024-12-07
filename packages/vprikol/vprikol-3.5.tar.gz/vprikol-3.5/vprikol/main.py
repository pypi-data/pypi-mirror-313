import datetime
from io import BytesIO
from typing import List, Literal, Optional, Union

from aiohttp import FormData
from pydantic import parse_obj_as

from .api import get_json, get_bytes
from .model import (MembersAPIResponse, PlayerInfoAPIResponse,
                    ServerStatusAPIResponse, RatingAPIResponse, CheckRPUsernameAPIResponse,
                    GenerateRPUsernameAPIResponse, PlayerSessionsAPIResponse, PlayerEstateAPIResponse,
                    PlayersAPIResponse, Gender, Nation, ServerMapAPIResponse, TokenStatCountsAPIResponse,
                    TokenStatRequestsAPIResponse, FindPlayerInfoNotFound, FindPlayerInfoAPIResponse,
                    RatingAPIResponseCrossServer, DeputiesAPIResponse, LeadersAPIResponse, PunishesAPIResponse,
                    PunishType, InterviewsAPIResponse, AiSSAPIResponse)


class VprikolAPI:
    def __init__(self, token: str, base_url: str = 'https://api.szx.su/'):
        if not token.startswith('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.'):
            raise Exception('Вы указали некорректный авторизационный токен.')
        self.headers = {'Authorization': f'Bearer {token}'}
        self.base_url = base_url

    async def get_members(self, server_id: int,
                          fraction_ids: Optional[Union[int, List[int]]] = None) -> MembersAPIResponse:
        params = {'server_id': server_id}
        if fraction_ids:
            params['fraction_ids'] = fraction_ids
        result = await get_json(url=f'{self.base_url}members', headers=self.headers, params=params)

        if not result.success:
            raise Exception(result.error)

        return MembersAPIResponse(**result.result_data)

    async def get_player_information(self, server_id: int, nickname: Optional[str] = None) -> Union[PlayerInfoAPIResponse]:
        params = {'server_id': server_id}
        if nickname:
            params['nickname'] = nickname
        result = await get_json(url=f'{self.base_url}players', headers=self.headers, params=params)

        if not result.success:
            raise Exception(result.error)

        return PlayerInfoAPIResponse(**result.result_data)

    async def get_server_status(self, server_id: Optional[int] = None) -> List[ServerStatusAPIResponse]:
        params = {'server_id': server_id} if server_id else None
        result = await get_json(url=f'{self.base_url}status', headers=self.headers, params=params)

        if not result.success:
            raise Exception(result.error)

        return parse_obj_as(List[ServerStatusAPIResponse], result.result_data)

    async def get_rating(self, server_id: int, rating_type: Literal["advocates", "combine_operators", "bus_drivers",
                                                                    "tractor_drivers", "catchers", "collectors",
                                                                    "corn_pilots", "crypto_asc", "crypto_btc",
                                                                    "electric_train_drivers", "lvl_families",
                                                                    "lvl_players", "mechanics", "richest", "outbids",
                                                                    "pilots", "sellers", "taxi_drivers", "tram_drivers",
                                                                    "truckers", "cladmens", "admins"] = None) -> RatingAPIResponse | RatingAPIResponseCrossServer:
        params = {'rating_type': rating_type, 'server_id': server_id} if rating_type else {'server_id': server_id}
        result = await get_json(url=f'{self.base_url}rating', headers=self.headers, params=params)

        if not result.success:
            raise Exception(result.error)
        if server_id:
            return RatingAPIResponse(**result.result_data)
        return RatingAPIResponseCrossServer(**result.result_data)

    async def check_rp_nickname(self, first_name: Optional[str] = None,
                                last_name: Optional[str] = None) -> CheckRPUsernameAPIResponse:
        params = {}
        if first_name:
            params['first_name'] = first_name
        if last_name:
            params['last_name'] = last_name
        result = await get_json(url=f'{self.base_url}checkrp', headers=self.headers, params=params)

        if not result.success:
            raise Exception(result.error)

        return CheckRPUsernameAPIResponse(**result.result_data)

    async def generate_rp_nickname(self, gender: Gender = 'male', nation: Nation = 'american',
                                   count: int = 1) -> GenerateRPUsernameAPIResponse:
        result = await get_json(url=f'{self.base_url}rpnick', headers=self.headers,
                                params={'gender': gender, 'nation': nation, 'count': count})

        if not result.success:
            raise Exception(result.error)

        return GenerateRPUsernameAPIResponse(**result.result_data)

    async def get_player_sessions(self, server_id: int, nickname: str, count: int = 1000, offset: int = 0,
                                  start_datetime: Optional[datetime.datetime] = None,
                                  end_datetime: Optional[datetime.datetime] = None) -> PlayerSessionsAPIResponse:
        params = {'nickname': nickname, 'count': count, 'offset': offset, 'server_id': server_id}
        if start_datetime:
            params['start_datetime'] = start_datetime.isoformat() + '+03:00'
        if end_datetime:
            params['end_datetime'] = end_datetime.isoformat() + '+03:00'
        result = await get_json(url=f'{self.base_url}sessions', headers=self.headers, params=params)

        if not result.success:
            raise Exception(result.error)

        return PlayerSessionsAPIResponse(**result.result_data)

    async def get_server_map(self, server_id: int, only_ghetto: bool = False) -> ServerMapAPIResponse:
        result = await get_json(url=f'{self.base_url}map', headers=self.headers,
                                params={'server_id': server_id, 'only_ghetto': int(only_ghetto)})

        if not result.success:
            raise Exception(result.error)

        return ServerMapAPIResponse(**result.result_data)

    async def get_estate(self, server_id: int, nickname: Optional[str] = None) -> PlayerEstateAPIResponse:
        params = {'server_id': server_id}
        if nickname:
            params['nickname'] = nickname
        result = await get_json(url=f'{self.base_url}estate', headers=self.headers, params=params)

        if not result.success:
            raise Exception(result.error)

        return PlayerEstateAPIResponse(**result.result_data)

    async def get_players(self, server_id: int, nicknames: Optional[List[Union[str, int]]] = None) -> PlayersAPIResponse:
        params = {'server_id': server_id}
        if nicknames:
            params['nicknames'] = nicknames
        result = await get_json(url=f'{self.base_url}players', headers=self.headers, params=params)

        if not result.success:
            raise Exception(result.error)

        return PlayersAPIResponse(**result.result_data)

    async def generate_ss(self, commands: list, screen: Union[bytes, BytesIO], font: str = '/fonts/arialbd.ttf',
                          text_top: bool = True, text_size: float = 0.95, commands_colors=None) -> bytes:

        if not commands_colors:
            commands_colors = {}
        if isinstance(screen, bytes):
            screen = BytesIO(screen)

        data = FormData()
        data.add_field('screen', screen, filename='screen.png', content_type='application/octet-stream')

        result = await get_bytes(url=f'{self.base_url}generate_ss', headers=self.headers,
                                 params={'commands': commands, 'font': font, 'text_top': int(text_top),
                                         'commands_colors': str(commands_colors), 'text_size': text_size},
                                 post_data=data)

        if not result.success:
            raise Exception(result.error)

        return result.result_data

    async def generate_aiss(self, theme: str) -> AiSSAPIResponse:
        result = await get_json(url=f'{self.base_url}aiss', headers=self.headers, params={'theme': theme})

        if not result.success:
            raise Exception(result.error)

        return AiSSAPIResponse(**result.result_data)

    async def get_token_stat(self, methods: Optional[List[Union[str, int]]] = None,
                             start_datetime: Optional[datetime.datetime] = None,
                             end_datetime: Optional[datetime.datetime] = None,
                             response_type: Literal['counts', 'requests'] = 'counts',
                             requests_limit: int = 1000, requests_offset: int = 0) -> TokenStatCountsAPIResponse | TokenStatRequestsAPIResponse:
        params = {'response_type': response_type, 'requests_limit': requests_limit, 'requests_offset': requests_offset}
        if start_datetime:
            params['start_datetime'] = start_datetime.isoformat() + '+03:00'
        if end_datetime:
            params['end_datetime'] = end_datetime.isoformat() + '+03:00'
        if methods:
            params['methods'] = methods
        result = await get_json(url=f'{self.base_url}stat', headers=self.headers, params=params)

        if not result.success:
            raise Exception(result.error)

        if response_type == 'counts':
            return TokenStatCountsAPIResponse(**result.result_data)
        elif response_type == 'requests':
            return TokenStatRequestsAPIResponse(**result.result_data)

    async def find_player(self, server_id: int, nickname: str, recaptcha_token: Optional[str] = None) -> Union[FindPlayerInfoAPIResponse, FindPlayerInfoNotFound]:

        params = {'server_id': server_id, 'nickname': nickname}
        if recaptcha_token:
            params['recaptcha_token'] = recaptcha_token

        result = await get_json(url=f'{self.base_url}find', headers=self.headers, params=params)

        if not result.success:
            raise Exception(result.error)

        if result.error and result.error.error_code == 422:
            return FindPlayerInfoNotFound(**result.error.dict())

        if result.error and result.error.error_code in [500, 502, 503]:
            raise Exception(result.error.detail)

        return FindPlayerInfoAPIResponse(**result.result_data)

    async def get_deputies(self, server_id: int) -> DeputiesAPIResponse:
        result = await get_json(url=f'{self.base_url}deputies', headers=self.headers, params={'server_id': server_id})

        if not result.success:
            raise Exception(result.error)

        return DeputiesAPIResponse(**result.result_data)

    async def get_leaders(self, server_id: int) -> LeadersAPIResponse:
        result = await get_json(url=f'{self.base_url}leaders', headers=self.headers, params={'server_id': server_id})

        if not result.success:
            raise Exception(result.error)

        return LeadersAPIResponse(**result.result_data)

    async def get_punishes(self, server_id: int,
                           player_nickname: Optional[str] = None, admin_nickname: Optional[str] = None,
                           start_datetime: Optional[datetime.datetime] = None,
                           end_datetime: Optional[datetime.datetime] = None,
                           punish_type: Optional[PunishType] = None,
                           count: int = 1000, offset: int = 0) -> PunishesAPIResponse:
        params = {'server_id': server_id, 'count': count, 'offset': offset}
        if start_datetime:
            params['start_datetime'] = start_datetime.isoformat() + '+03:00'
        if end_datetime:
            params['end_datetime'] = end_datetime.isoformat() + '+03:00'
        if player_nickname:
            params['player_nickname'] = player_nickname
        if admin_nickname:
            params['admin_nickname'] = admin_nickname
        if punish_type:
            params['punish_type'] = punish_type
        result = await get_json(url=f'{self.base_url}punishes', headers=self.headers, params=params)

        if not result.success:
            raise Exception(result.error)

        return PunishesAPIResponse(**result.result_data)

    async def get_active_interviews(self, server_id: int) -> InterviewsAPIResponse:
        result = await get_json(url=f'{self.base_url}interviews', headers=self.headers, params={'server_id': server_id})

        if not result.success:
            raise Exception(result.error)

        return InterviewsAPIResponse(**result.result_data)
