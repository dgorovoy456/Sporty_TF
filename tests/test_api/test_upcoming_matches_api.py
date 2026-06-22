import datetime

today_date = datetime.date.today()

class TestUpcomingMatchesAPI:
    def test_that_list_of_upcoming_matches_are_returned(self, api_helper):
        matches = api_helper.get_matches()
        assert len(matches.list_matches) > 0

    def test_that_only_upcoming_matches_are_returned(self, api_helper):
        #TODO: Clarify the scenario where the match fits the current date but already passed.
        #TODO: Unless clarified, threat the current day match as passed to avoid false positive result.
        matches = api_helper.get_matches()
        for match in matches.list_matches:
            assert match.kickoffDate > today_date, (
                f"The {today_date} is greater then {match.kickoffDate}, so the match {match} cannot be upcoming"
            )
    def test_that_no_matches_are_returned_for_invalid_user(self, api_helper):
        api_helper.update_user_id(user_id="unexisting-user")
        matches = api_helper.get_matches()
        assert matches.response_code == 401
        assert len(matches.list_matches) == 1, "Expected exact one error in the list"
        assert matches.list_matches[0].error == "invalid_user_id", "Unexpected error cause observed in the list"