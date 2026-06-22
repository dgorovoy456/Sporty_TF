import datetime
from dataclasses import dataclass
from typing import Union
import requests

app_url = "https://qae-assignment-tau.vercel.app/"
api_matches_get = app_url + "api/matches"
api_balance_get = app_url + "api/balance"
api_rest_balance_post = app_url + "api/rest-balance"
api_place_bet_get = app_url + "api/place-bet"


@dataclass()
class Odds:
    home: float
    draw: float
    away: float


@dataclass()
class Match:
    id: str
    competition: str
    kickoffDate: datetime.date
    homeTeam: str
    awayTeam: str
    odds: Odds

    def __post_init__(self):
        if isinstance(self.kickoffDate, str):
            self.kickoffDate = datetime.date.fromisoformat(self.kickoffDate)


@dataclass()
class MatchError:
    error: str


@dataclass()
class MatchesResponse:
    response_code: int
    data: Union[list[Match], MatchError]


class APIHelper:

    def __init__(self, x_user_id: str):
        self.x_user_id = x_user_id
        self.session = requests.Session()
        self.session.headers.update({"x-user-id": self.x_user_id, "Accept": "application/json"})

    def update_user_id(self, user_id: str):
        self.session.headers.update({"x-user-id": user_id})

    def get_matches(self):
        matches = []
        api_data = self.session.get(api_matches_get)
        if api_data.status_code == 200:
            for match in api_data.json():
                matches.append(Match(**match))
            return MatchesResponse(response_code=api_data.status_code, data=matches)
        return MatchesResponse(response_code=api_data.status_code, data=MatchError(error=api_data.json()["error"]))
