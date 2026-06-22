import datetime

today_date = datetime.date.today()


class TestUpcomingMatchesAPI:
    def test_that_list_of_matches_is_returned_for_the_valid_user(self, api_helper):
        matches = api_helper.get_matches()
        assert matches.response_code == 200, f"Unexpected error cause is observed: {matches.data}"
        assert len(matches.data) > 0, "No matches returned"

    def test_that_only_upcoming_matches_are_returned(self, api_helper):
        # TODO: Clarify the scenario where the match fits the current date but already passed.
        # TODO: Unless clarified, threat the current day match as passed to avoid false positive result.
        matches = api_helper.get_matches()
        for match in matches.data:
            assert (
                match.kickoffDate > today_date
            ), f"The {today_date} is greater then {match.kickoffDate}, so the match {match} cannot be upcoming"

    def test_that_no_matches_are_returned_for_invalid_user(self, api_helper):
        api_helper.update_user_id(user_id="unexisting-user")
        matches = api_helper.get_matches()
        assert matches.response_code == 401
        assert matches.data.error == "invalid_user_id", "Unexpected error cause observed in the list"
