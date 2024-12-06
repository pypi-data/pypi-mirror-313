from __future__ import absolute_import


class Timezones(object):
    # Timezones base API uri
    base_api_url = "api/timezones"

    def __init__(self, api_client):
        self.api_client = api_client

    def list(self):
        """
        Lists all timezones

        Returns a list of all timezones.
        Ref: https://developers.mailerlite.com/docs/timezones.html#response

        :return: JSON array
        :rtype: dict
        """

        return self.api_client.request("GET", self.base_api_url).json()
