from tools.main_web_page_helper import MainSportyPage


class TestPlaceBet:

    def test_that_bet_for_incoming_match_can_be_placed(self, web_driver):
        main_page = MainSportyPage(web_driver)
        bet_result = main_page.make_bet(odd="home")
        assert bet_result.is_bet_successful, f"Expected bet is successful but got: {bet_result}"

    def test_that_bet_for_past_match_cannot_be_placed(self, web_driver):
        main_page = MainSportyPage(web_driver)
        bet_result = main_page.make_bet(odd="draw")
        assert not bet_result.is_bet_successful, f"Expected bet is not successful but got: {bet_result}"

    def test_that_potential_bet_payout_is_correct(self, web_driver):
        main_page = MainSportyPage(web_driver)
        bet_result = main_page.make_bet(odd="away")
        actual_payout = bet_result.bet_modal_data.summary.potential_payout
        expected_payout = bet_result.bet_modal_data.summary.stake * bet_result.bet_modal_data.summary.odds
        assert expected_payout == actual_payout, f"Expected {expected_payout} but got {actual_payout}"
