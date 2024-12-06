import requests
from requests.exceptions import RequestException
from typing import Optional, Dict, Any
import json


class Halluminate:
    def __init__(
        self, api_token, base_url="https://api.halluminate.ai"
    ):  # set base_url to localhost when testing, otherwhise set to production url
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token {api_token}",
        }

    def send_request(self, method, endpoint, data=None):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(
                method, url, headers=self.headers, json=data, timeout=30
            )
            response.raise_for_status()
            return response.json()
        except json.JSONDecodeError:
            return {"status_code": response.status_code, "text": response.text}
        except RequestException as e:
            return {"error": str(e)}

    def evaluate_criteria(self, **kwargs):
        endpoint_url = f"criteria/evaluate/"
        data = {}
        data.update(kwargs)
        return self.send_request("POST", endpoint_url, data=data)

    def evaluate_basic(
        self,
        criteria_uuid,
        model_output,
        prompt=None,
        context=None,
        hyperparameters=None,
    ):
        return self.evaluate_criteria(
            criteria_uuid=criteria_uuid,
            model_output=model_output,
            evaluation_method="evaluate_basic",
            prompt=prompt,
            context=context,
            hyperparameters=hyperparameters,
        )

    def evaluate_with_bot_court(
        self,
        criteria_uuid,
        model_output,
        prompt=None,
        context=None,
        hyperparameters=None,
    ):
        return self.evaluate_criteria(
            criteria_uuid=criteria_uuid,
            model_output=model_output,
            evaluation_method="evaluate_with_bot_court",
            prompt=prompt,
            context=context,
            hyperparameters=hyperparameters,
        )

    def evaluate_with_mixture_of_judges(
        self,
        criteria_uuid,
        model_output,
        prompt=None,
        context=None,
        hyperparameters=None,
    ):
        return self.evaluate_criteria(
            criteria_uuid=criteria_uuid,
            model_output=model_output,
            evaluation_method="evaluate_with_mixture_of_judges",
            prompt=prompt,
            context=context,
            hyperparameters=hyperparameters,
        )

    def evaluate_with_reflection(
        self,
        criteria_uuid,
        model_output,
        prompt=None,
        context=None,
        hyperparameters=None,
    ):
        return self.evaluate_criteria(
            criteria_uuid=criteria_uuid,
            model_output=model_output,
            evaluation_method="evaluate_with_reflection",
            prompt=prompt,
            context=context,
            hyperparameters=hyperparameters,
        )
