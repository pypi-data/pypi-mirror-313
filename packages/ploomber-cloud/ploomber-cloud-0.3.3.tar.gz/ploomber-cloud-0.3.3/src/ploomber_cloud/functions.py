import base64
import time
from functools import partial, wraps
from os import environ
import sys

import requests
import cloudpickle


from ploomber_cloud import client

PYTHON_VERSION = (
    f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
)

API_ROOT = (
    "http://localhost:80"
    if environ.get("PLOOMBER_DEBUG")
    else "https://serverless.ploomber.io"
)


class TimeoutError(Exception):
    pass


class JobError(Exception):
    pass


class JobPendingError(Exception):
    pass


def call_with_timeout(func, timeout, job_id, delay=0.5):
    start_time = time.time()

    while True:
        try:
            return func()
        except JobPendingError as e:
            if time.time() - start_time > timeout:
                raise TimeoutError(
                    f"Tiemout for job with ID: {job_id!r}, you "
                    "can check the status manually"
                ) from e

            time.sleep(delay)


class PloomberFunctionsClient(client.PloomberBaseClient):
    def call_remotely(self, func, requirements, args, kwargs):
        data = {"requirements": requirements, "python_version": PYTHON_VERSION}

        response = requests.post(
            f"{API_ROOT}/functions/serverless",
            headers=self._get_headers(),
            data=data,
            files=[
                (
                    "files",
                    (
                        "function",
                        cloudpickle.dumps(func),
                        "application/octet-stream",
                    ),
                ),
                (
                    "files",
                    (
                        "args",
                        cloudpickle.dumps(args),
                        "application/octet-stream",
                    ),
                ),
                (
                    "files",
                    (
                        "kwargs",
                        cloudpickle.dumps(kwargs),
                        "application/octet-stream",
                    ),
                ),
            ],
        )

        response.raise_for_status()

        return response.json()["job_id"]

    def _generic_pdf_endpoint(self, path_to_pdf, endpoint):
        with open(path_to_pdf, "rb") as file:
            response = requests.post(
                f"{API_ROOT}/{endpoint}",
                headers=self._get_headers(),
                files={"file": ("file.pdf", file, "application/pdf")},
            )

        response.raise_for_status()

        return response

    def pdf_to_text(self, path_to_pdf):
        return self._generic_pdf_endpoint(path_to_pdf, "functions/pdf-to-text")

    def scanned_pdf_to_text(self, path_to_pdf):
        return self._generic_pdf_endpoint(path_to_pdf, "functions/scanned-pdf-to-text")

    def image_to_text(self, path_to_image, question):
        question = requests.utils.quote(question)

        with open(path_to_image, "rb") as file:
            response = requests.post(
                f"{API_ROOT}/functions/image-to-text?question={question}",
                headers=self._get_headers(),
                files={"file": ("image", file, "image/*")},
            )

        response.raise_for_status()

        return response

    def get_job_status(self, job_id):
        response = requests.get(
            f"{API_ROOT}/status/{job_id}",
            headers=self._get_headers(),
        )
        response.raise_for_status()
        return response.json()

    def get_result(self, job_id, unserialize=True):
        response_ = self.get_job_status(job_id)

        if response_["status"] == "SUBMITTED":
            raise JobPendingError("Job is still running")
        elif response_["status"] == "FAILED":
            traceback = response_["traceback"]
            raise JobError(f"Job failed: {traceback}")
        elif response_["status"] == "SUCCEEDED":
            URL = (
                f"{API_ROOT}/result/{job_id}"
                if unserialize
                else f"{API_ROOT}/result/{job_id}/raw"
            )
            response = requests.get(URL, headers=self._get_headers())
            response.raise_for_status()
            return response.json()
        else:
            raise JobError(f"Unexpected status: {response_['status']}")


client = PloomberFunctionsClient()


def get_job_status(job_id):
    return client.get_job_status(job_id)


def poll_until_done(job_id, timeout=300, delay=1, unserialize=True):
    get_result = partial(client.get_result, job_id, unserialize)
    return call_with_timeout(get_result, timeout, job_id, delay=delay)


def _pdf_function_factory(function):
    def _pdf_function(path_to_pdf, timeout=300, block=True):
        response = function(path_to_pdf)

        if block:
            return poll_until_done(
                response.json()["job_id"],
                timeout,
                unserialize=True,
            )["output"]
        else:
            return response.json()["job_id"]

    return _pdf_function


pdf_to_text = _pdf_function_factory(client.pdf_to_text)
pdf_scanned_to_text = _pdf_function_factory(client.scanned_pdf_to_text)


def image_to_text(path_to_image, question, timeout=20, block=True):
    """Ask a question to an image"""
    response = client.image_to_text(path_to_image, question)

    if block:
        return poll_until_done(
            response.json()["job_id"],
            timeout,
            unserialize=True,
        )["output"]
    else:
        return response.json()["job_id"]


def get_result(job_id):
    """Get the result of a job"""
    return client.get_result(job_id)["output"]


def get_result_from_remote_function(job_id):
    """Get the result of a job"""
    result = client.get_result(job_id, unserialize=False)["output"]
    return cloudpickle.loads(base64.b64decode(result))


def _background(func, requirements, *args, **kwargs):
    return client.call_remotely(func, requirements, args, kwargs)


def serverless(
    *,
    requirements,
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            job_id = client.call_remotely(func, requirements, args, kwargs)
            result = poll_until_done(job_id, unserialize=False)["output"]
            return cloudpickle.loads(base64.b64decode(result))

        wrapper.background = partial(_background, func, requirements)

        return wrapper

    return decorator
