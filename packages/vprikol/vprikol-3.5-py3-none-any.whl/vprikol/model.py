import datetime
from typing import TypeVar, List, Optional, Dict, Generic, Union, Any, Literal
from pydantic import BaseModel, Field

DataT = TypeVar('DataT')

Gender = Literal['male', 'female']
Nation = Literal['russian', 'american', 'german', 'french', 'italian', 'japanese', 'latinos', 'swedish', 'danish', 'romanian']

PunishType = Literal['kick', 'warn', 'warnoff', 'jail', 'jailoff', 'mute', 'muteoff', 'rmute', 'ban', 'banip', 'unjail',
                     'unmute', 'unrmute', 'apunish', 'unapunish']


class FastAPIErrorDetail(BaseModel):
    loc: List[str]
    message: str = Field(alias='msg')
    type: str

 
class FastApiErrorResponse(BaseModel):
    detail: Union[list[FastAPIErrorDetail], str]


class APIErrorResponse(BaseModel):
    error_code: int
    detail: str


class Response(BaseModel, Generic[DataT]):
    result_data: Optional[DataT] = None
    error: Optional[Union[FastApiErrorResponse, APIErrorResponse]] = None
    success: bool = True


class MembersAPIPlayer(BaseModel):
    account_id: Optional[int]
    nickname: str
    is_online: bool
    is_leader: bool
    rank_number: int
    rank_label: Optional[str]
    ingame_id: Optional[int]
    nickname_color: Optional[int]


class MembersAPIRecord(BaseModel):
    online_players: int
    leader_nickname: Optional[str]
    modified_at: Optional[datetime.datetime]
    modified_by: Literal['system', 'admin']


class MembersFractionData(BaseModel):
    fraction_id: int
    fraction_label: str
    players: List[MembersAPIPlayer]
    total_players: int
    total_online: int
    leader_nickname: Optional[str]
    is_leader_online: bool
    online_updated_at: datetime.datetime
    members_updated_at: datetime.datetime
    online_record: MembersAPIRecord


class MembersAPIResponse(BaseModel):
    server_id: int
    server_label: str
    data: List[MembersFractionData]


class ServerStatusAPIResponse(BaseModel):
    server_id: int
    server_label: str
    server_ip: str
    server_port: int
    server_vk: Optional[str]
    server_ds: Optional[str]
    online_players: int
    max_players: int
    is_closed: bool
    main_admin_vk: Optional[str]
    deputy_main_admin_vk: Optional[str]
    updated_at: datetime.datetime


class PlayerInfo(BaseModel):
    nickname: str
    ingame_id: int
    nickname_color: int
    lvl: int
    ping: int


class PlayerInfoAPIResponse(BaseModel):
    server_id: int
    server_label: str
    updated_at: datetime.datetime
    data: List[PlayerInfo]


class RatingPlayerInfo(BaseModel):
    ranking: int
    nickname: str
    value: Optional[Any]
    additional_value: Optional[Any]
    az_coins: int
    family: Optional[str] = None


class RatingPlayerInfoCrossServer(BaseModel):
    ranking: int
    nickname: str
    value: Optional[Any]
    additional_value: Optional[Any]
    az_coins: int
    family: Optional[str] = None
    server_id: int
    server_label: str


class RatingAPIResponseCrossServer(BaseModel):
    server_id: int
    server_label: str
    updated_at: datetime.datetime
    data: Dict[str, list[Optional[RatingPlayerInfoCrossServer]]]


class RatingAPIResponse(BaseModel):
    server_id: int
    server_label: str
    updated_at: datetime.datetime
    data: Dict[str, list[Optional[RatingPlayerInfo]]]


class CheckRPUsernameInfo(BaseModel):
    value: Optional[str] = None
    is_existing: bool
    is_confirmed: bool
    nationalities_chart: Optional[str] = None


class CheckRPUsernameAPIResponse(BaseModel):
    first_name: CheckRPUsernameInfo
    last_name: CheckRPUsernameInfo
    nickname: str


class GhettoZonesData(BaseModel):
    grove: int
    ballas: int
    vagos: int
    rifa: int
    aztec: int
    nw: int


class ServerMapAPIResponse(BaseModel):
    image: str
    ghetto_zones: GhettoZonesData
    server_id: int
    server_label: str
    updated_at: datetime.datetime


class AuctionInfo(BaseModel):
    active: bool
    minimal_bet: int
    time_end: Optional[datetime.datetime]
    start_price: int


class Coordinates(BaseModel):
    x: float
    y: float


class EstateItemInfo(BaseModel):
    id: int
    name: Optional[str]
    auction: AuctionInfo
    coordinates: Coordinates


class EstatePlayer(BaseModel):
    houses: List[EstateItemInfo]
    businesses: List[EstateItemInfo]


class PlayerEstateAPIResponse(BaseModel):
    server_id: int
    server_label: str
    updated_at: datetime.datetime
    data: Dict[str, EstatePlayer]


class RPNickname(BaseModel):
    first_name: str
    last_name: str
    nickname: str


class GenerateRPUsernameAPIResponse(BaseModel):
    gender: Gender
    nation: Nation
    data: list[RPNickname]


class PlayerSessionInfo(BaseModel):
    login_at: datetime.datetime
    logout_at: datetime.datetime


class PlayerSessionsAPIResponse(BaseModel):
    server_id: int
    server_label: str
    nickname: str
    data: List[PlayerSessionInfo]


class PlayerGameInfo(BaseModel):
    nickname: str
    ingame_id: int
    nickname_color: int
    lvl: int
    ping: int


class PlayersAPIResponse(BaseModel):
    server_id: int
    server_label: str
    updated_at: datetime.datetime
    data: List[PlayerGameInfo]


class TokenStatCountsAPIResponse(BaseModel):
    find: Optional[int] = None
    members: Optional[int] = None
    status: Optional[int] = None
    rating: Optional[int] = None
    rpnick: Optional[int] = None
    checkrp: Optional[int] = None
    players: Optional[int] = None
    estate: Optional[int] = None
    map: Optional[int] = None
    sessions: Optional[int] = None
    generate_ss: Optional[int] = None


class TokenStatRequest(BaseModel):
    request_id: int = Field(alias='id')
    method: str
    params: dict[str, Any]
    ip_address: str
    requested_at: datetime.datetime


class TokenStatRequestsAPIResponse(BaseModel):
    data: List[TokenStatRequest]


class FindPlayerInfoAPIResponse(BaseModel):
    server_id: int
    server_label: str
    nickname: str
    health: int
    hunger: int
    max_hunger: int
    lvl: int
    gender: Gender
    played_hours: int
    law_count: int
    wanted_lvl: int
    marriage: Optional[str]
    job_label: str
    drug_addict_lvl: int
    phone_number: Optional[int]
    warns_count: int
    vip_lvl: int
    vip_label: str
    vip_expiration_date: Optional[datetime.datetime]
    have_addition_vip: bool
    addition_vip_expiration_date: Optional[datetime.datetime]
    current_xp: int
    max_xp: int
    az_coins: int
    total_money: int
    bank_balance: int
    have_bank_card: bool
    charity_money: int
    phone_balance: int
    cash: int
    deposit: int
    individual_accounts: Dict[str, Optional[int]]


class FindPlayerInfoNotFound(APIErrorResponse):
    pass


class DeputyInfo(BaseModel):
    fraction_id: int
    fraction_label: str
    nickname: str
    ingame_id: int
    phone_number: Optional[int]
    afk: int


class DeputiesAPIResponse(BaseModel):
    server_id: int
    server_label: str
    updated_at: datetime.datetime
    data: List[DeputyInfo]


class LeaderInfo(BaseModel):
    fraction_id: int
    fraction_label: str
    nickname: str
    ingame_id: int
    phone_number: Optional[int]
    afk: int


class LeadersAPIResponse(BaseModel):
    server_id: int
    server_label: str
    updated_at: datetime.datetime
    data: List[LeaderInfo]


class PunishInfo(BaseModel):
    punish_type: PunishType
    player_nickname: str
    admin_nickname: str
    reason: str
    full_string: str
    active: bool
    created_at: datetime.datetime
    expires_at: Optional[datetime.datetime]


class PunishesAPIResponse(BaseModel):
    server_id: int
    server_label: str
    data: List[PunishInfo]


class InterviewInfo(BaseModel):
    fraction_id: int
    fraction_label: str
    start_datetime: datetime.datetime
    place: str


class InterviewsAPIResponse(BaseModel):
    server_id: int
    server_label: str
    updated_at: datetime.datetime
    data: List[InterviewInfo]


class AiSSAPIResponse(BaseModel):
    answer: List[str]
