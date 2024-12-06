import os
from time import sleep
from typing import Any, Callable, Dict, Optional
import requests


def send_rest_api_request(method, endpoint, data=None):
    api_url = os.getenv("TANGENT_API_URL", "https://api.tangent.works")
    license_key = os.getenv("TANGENT_LICENSE", "")
    headers = {"Authorization": "Bearer " + license_key}

    response = requests.request(
        method, f"{api_url}{endpoint}", headers=headers, files=data
    )
    response.raise_for_status()

    return response


def print_job_status_update(status) -> None:
    print(
        f"Status update: id: {status.get('id' '')}, status: {status.get('status' '')}, progress: {status.get('progress' '')}",
        end="\r",
    )


def wait_for_job_to_finish(job_type, job_id, status_poll: bool = True):
    i = 900
    while i > 0:
        status_response = send_rest_api_request("GET", f"/{job_type}/{job_id}")
        status_response_dict = status_response.json()
        job_status = status_response_dict["status"]

        if status_poll:
            print_job_status_update(status_response_dict)

        if job_status == "Finished":
            return job_status
        if job_status == "Failed":
            try:
                error_message = status_response.json()["log"][-1]["message"]
            except:
                error_message = "Unknown error"
            raise ValueError(error_message)
        i -= 1
        sleep(2)
    raise ValueError("API response timeout reached")
