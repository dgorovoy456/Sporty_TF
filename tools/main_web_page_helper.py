from typing import Union

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException

ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)


@dataclass()
class Odd:
    button: WebElement
    label: str
    value: float


@dataclass()
class Odds:
    home: Odd
    draw: Odd
    away: Odd


@dataclass()
class Stake:
    currency: str
    total_stake: str
    potential_payout: str
    place_bet_button: WebElement


@dataclass()
class FullBetSlipData:
    teams: str
    match_winner: str
    close_button: WebElement
    odds: str
    stake: Stake


@dataclass()
class EmptyBetSlipData:
    message: str


@dataclass()
class BetSlipData:
    data: Union[FullBetSlipData, EmptyBetSlipData]


@dataclass()
class SuccessfulBetSummary:
    bet_id: str
    match: str
    stake: float
    odds: float
    potential_payout: float
    placed_at: str


@dataclass()
class SuccessModalData:
    title: str
    summary: SuccessfulBetSummary
    close_button_x: WebElement
    close_button_footer: WebElement


@dataclass()
class FailModalData:
    summary: str = None  # :TODO Add fail data when available


@dataclass()
class PlaceBetSummary:
    is_bet_successful: bool
    bet_modal_data: Union[SuccessModalData, FailModalData]


class BaseDriver:
    def __init__(self, driver):
        self.driver = driver

    def click(self, by, path):
        WebDriverWait(self.driver, 20, ignored_exceptions=ignored_exceptions).until(
            EC.visibility_of_element_located((by, path))
        ).click()

    def send_keys(self, by, path, keys):
        element = WebDriverWait(self.driver, 20, ignored_exceptions=ignored_exceptions).until(
            EC.visibility_of_element_located((by, path))
        )
        element.clear()
        element.send_keys(keys)

    def get_element(self, by, path, timeout=10) -> WebElement:
        element = WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, path)))
        return element


class MatchCard:
    def __init__(self, base_driver: BaseDriver, match: WebElement):
        self.match = match
        self.base_driver = base_driver

    def is_upcoming(self):
        if self.match.find_element(By.CSS_SELECTOR, value=".matchMeta .badge").text == "UPCOMING":
            return True
        return False

    def get_odds(self) -> Odds:
        odd_list = []
        for button in self.match.find_elements(By.CSS_SELECTOR, ".oddsGrid .oddsButton"):
            odd_list.append(
                Odd(
                    button=button,
                    label=button.find_element(By.CLASS_NAME, value="oddsButtonLabel").text,
                    value=float(button.find_element(By.CLASS_NAME, value="oddsButtonValue").text),
                )
            )
        if len(odd_list) != 3:
            raise Exception(f"Expected only 3 buttons, but was {len(odd_list)}")
        return Odds(home=odd_list[0], draw=odd_list[1], away=odd_list[2])


class BetSlip:
    def __init__(self, base_driver: BaseDriver):
        self.base_driver = base_driver

    def is_bet_sleep_empty(self):
        try:
            bet_slip_empty = self.base_driver.get_element(By.CLASS_NAME, "betSlipBodyEmpty", timeout=1)
            if bet_slip_empty.text == "Select odds to place a bet":
                return True
        except TimeoutException:
            return False
        return False

    def get_bet_slip_data(self):
        if not self.is_bet_sleep_empty():
            return BetSlipData(
                data=FullBetSlipData(
                    teams=self.base_driver.get_element(By.CLASS_NAME, "betSelectionTeams").text,
                    match_winner=self.base_driver.get_element(By.CLASS_NAME, "betSelectionMarket").text,
                    close_button=self.base_driver.get_element(By.CSS_SELECTOR, ".betSelectionTop button"),
                    odds=self.base_driver.get_element(By.CLASS_NAME, "betSelectionOdds").text,
                    stake=Stake(
                        currency=self.base_driver.get_element(By.CLASS_NAME, "stakeCurrency").text,
                        total_stake=self.base_driver.get_element(By.CLASS_NAME, "stakeInput").get_attribute("value"),
                        potential_payout=self.base_driver.get_element(By.ID, "bet-slip-potential-payout").text,
                        place_bet_button=self.base_driver.get_element(By.ID, "bet-slip-place-bet"),
                    ),
                )
            )
        return BetSlipData(
            data=EmptyBetSlipData(message=self.base_driver.get_element(By.CLASS_NAME, "betSlipBodyEmpty").text)
        )

    def update_stake_value(self, value):
        self.base_driver.send_keys(By.CLASS_NAME, "stakeInput", value)

    def place_bet(self):
        self.base_driver.click(By.ID, "bet-slip-place-bet")


class ModalData:
    def __init__(self, base_driver: BaseDriver):
        self.base_driver = base_driver

    @staticmethod
    def cast_value_to_float(currency: str, value: str):
        return float(value.replace(currency, ""))

    def get_data(self, currency) -> PlaceBetSummary:
        modal_title = self.base_driver.get_element(By.CLASS_NAME, "modalTitle").text
        if modal_title == "Bet Placed Successfully!":
            return PlaceBetSummary(
                is_bet_successful=True,
                bet_modal_data=SuccessModalData(
                    title=self.base_driver.get_element(By.CLASS_NAME, "modalTitle").text,
                    close_button_x=self.base_driver.get_element(By.ID, "modal-success-close-x"),
                    close_button_footer=self.base_driver.get_element(By.ID, "modal-success-close"),
                    summary=SuccessfulBetSummary(
                        bet_id=self.base_driver.get_element(By.ID, "modal-success-bet-id").text,
                        match=self.base_driver.get_element(By.ID, "modal-success-match").text,
                        stake=self.cast_value_to_float(
                            currency=currency, value=self.base_driver.get_element(By.ID, "modal-success-stake").text
                        ),
                        odds=self.cast_value_to_float(
                            currency=currency, value=self.base_driver.get_element(By.ID, "modal-success-odds").text
                        ),
                        potential_payout=self.cast_value_to_float(
                            currency=currency, value=self.base_driver.get_element(By.ID, "modal-success-payout").text
                        ),
                        placed_at=self.base_driver.get_element(By.ID, "modal-success-placed-at").text,
                    ),
                ),
            )
        return PlaceBetSummary(is_bet_successful=False, bet_modal_data=FailModalData())


class MainSportyPage(BaseDriver):
    def __init__(self, driver):
        super().__init__(driver)

    def get_list_matches(self) -> list[MatchCard]:
        matches = []
        match_list = self.get_element(By.CLASS_NAME, path="matchList")
        for match in match_list.find_elements(By.CLASS_NAME, value="matchCard"):
            matches.append(MatchCard(base_driver=self, match=match))
        return matches

    def get_match(self, is_upcoming: bool):
        """Returns first incoming match found on the page"""
        for match in self.get_list_matches():
            if match.is_upcoming():
                return match
        raise Exception("No upcoming match found")

    def get_bet_slip(self):
        return BetSlip(base_driver=self)

    def get_modal(self):
        return ModalData(base_driver=self)

    def make_bet(self, odd: str, stake: float = 1.0, is_upcoming: bool = True):
        match = self.get_match(is_upcoming=is_upcoming)
        match_data = match.get_odds()
        if odd == "home":
            match_data.home.button.click()
        elif odd == "draw":
            match_data.draw.button.click()
        elif odd == "away":
            match_data.away.button.click()
        else:
            raise Exception(f"Invalid odd value: {odd}")

        bet_slip = self.get_bet_slip()
        bet_slip_data = bet_slip.get_bet_slip_data()
        bet_slip.update_stake_value(stake)
        bet_slip.place_bet()
        bet_place_data = self.get_modal().get_data(bet_slip_data.data.stake.currency)

        return bet_place_data
