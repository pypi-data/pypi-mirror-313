import requests
from .exceptions import APIError
from .utils import build_url, validate_username


class LeetcodeWrapper:
    """A Python wrapper for the Alfa LeetCode API.

    Provides methods to interact with the Alfa LeetCode API endpoints for retrieving user profile,
    badges, solved problems, contest details, submissions, and more.

    Attributes:
        BASE_URL (str): The base URL of the Alfa LeetCode API.
        username (str): The username of the LeetCode user.
    """

    BASE_URL = "https://alfa-leetcode-api.onrender.com"

    def __init__(self, username):
        """Initializes the LeetcodeWrapper instance with the provided username.

        Args:
            username (str): The LeetCode username.

        Raises:
            ValidationError: If the username is invalid.
        """
        validate_username(username)
        self.username = username

    def _request(self, endpoint, params=None):
        """Sends a GET request to the specified API endpoint.

        Args:
            endpoint (str): The API endpoint to call.
            params (dict, optional): Query parameters for the request.

        Returns:
            dict: The JSON response from the API.

        Raises:
            APIError: If the API returns an error response.
        """
        url = build_url(self.BASE_URL, endpoint, params)
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise APIError(f"Error: {response.status_code}, {response.text}")
        return response.json()

    def get_profile(self):
        """Fetches the user's profile details.

        Returns:
            dict: The user's profile data.
        """
        return self._request(f"/{self.username}")

    def get_badges(self):
        """Fetches the badges earned by the user.

        Returns:
            dict: The user's badges data.
        """
        return self._request(f"/{self.username}/badges")

    def get_solved(self):
        """Fetches the total number of problems solved by the user.

        Returns:
            dict: The user's solved problems data.
        """
        return self._request(f"/{self.username}/solved")

    def get_contest_details(self):
        """Fetches the user's contest participation details.

        Returns:
            dict: The user's contest details.
        """
        return self._request(f"/{self.username}/contest")

    def get_contest_history(self):
        """Fetches the user's contest history.

        Returns:
            dict: The user's contest history data.
        """
        return self._request(f"/{self.username}/contest/history")

    def get_submissions(self, limit=None):
        """Fetches the user's recent submissions.

        Args:
            limit (int, optional): The number of submissions to fetch. Defaults to None.

        Returns:
            dict: The user's submissions data.
        """
        endpoint = f"/{self.username}/submission"
        if limit:
            endpoint += f"?limit={limit}"
        return self._request(endpoint)

    def get_accepted_submissions(self, limit=None):
        """Fetches the user's recent accepted submissions.

        Args:
            limit (int, optional): The number of accepted submissions to fetch. Defaults to None.

        Returns:
            dict: The user's accepted submissions data.
        """
        endpoint = f"/{self.username}/acSubmission"
        if limit:
            endpoint += f"?limit={limit}"
        return self._request(endpoint)

    def get_calendar(self):
        """Fetches the user's submission calendar.

        Returns:
            dict: The user's calendar data.
        """
        return self._request(f"/{self.username}/calendar")

    def get_language_stats(self):
        """Fetches the user's language statistics.

        Returns:
            dict: The user's language stats data.
        """
        return self._request(f"/languageStats?username={self.username}")

    def get_skill_stats(self):
        """Fetches the user's skill statistics.

        Returns:
            dict: The user's skill stats data.
        """
        return self._request(f"/skillStats/{self.username}")

    def get_user_contest_ranking(self):
        """Fetches the user's contest ranking information.

        Returns:
            dict: The user's contest ranking data.
        """
        return self._request(f"/userContestRankingInfo/{self.username}")

    def get_daily_question(self):
        """Fetches the daily LeetCode question.

        Returns:
            dict: The daily question data.
        """
        return self._request("/daily")

    def get_problem_details(self, title_slug):
        """Fetches details about a specific problem.

        Args:
            title_slug (str): The title slug of the problem.

        Returns:
            dict: The problem details data.
        """
        return self._request(f"/select?titleSlug={title_slug}")

    def get_problems(self, limit=None, tags=None, skip=None, difficulty=None):
        """Fetches a list of problems based on filters.

        Args:
            limit (int, optional): The number of problems to fetch. Defaults to None.
            tags (list, optional): A list of tags to filter problems. Defaults to None.
            skip (int, optional): The number of problems to skip. Defaults to None.
            difficulty (str, optional): The difficulty level ("EASY", "MEDIUM", "HARD"). Defaults to None.

        Returns:
            dict: The filtered problems data.
        """
        params = {}
        if limit:
            params["limit"] = limit
        if tags:
            params["tags"] = "+".join(tags)
        if skip:
            params["skip"] = skip
        if difficulty:
            params["difficulty"] = difficulty
        return self._request("/problems", params=params)


leetcode_Wrapper = LeetcodeWrapper
