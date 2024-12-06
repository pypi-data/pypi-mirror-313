from __future__ import absolute_import


class Batches(object):
    base_api_url = "api/batch"

    def __init__(self, api_client):
        self.api_client = api_client

    def request(self, requests=[]):
        """
        Send a batch request

        Provides an ability to make multiple request to our api in a single call.
        Ref: https://developers.mailerlite.com/docs/batching.html#request-body

        :param requests: dict Array of objects containing required method and path properties and optional body
        :raises: :class: `TypeError` : `requests` type is not valid
        :return: JSON array
        :rtype: dict
        """

        if type(requests) is not list:
            raise TypeError(
                f"`requests` type is not valid. Expected `dict`, got {type(requests)}."
            )

        body_params = {"requests": requests}

        return self.api_client.request(
            "POST", self.base_api_url, body=body_params
        ).json()
