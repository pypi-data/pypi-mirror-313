from __future__ import annotations
import random
import time
from typing import TypeVar
import urllib.parse
import re

import requests

from relationalai.errors import RAIException

# replace the values of the URL parameters that start with X-Amz- with XXX
def scrub_url(url):
    parsed = urllib.parse.urlparse(url)
    parsed_qs = urllib.parse.parse_qs(parsed.query)
    for key in parsed_qs:
        if key.startswith("X-Amz-"):
            parsed_qs[key] = ["XXX"]
    new_qs = urllib.parse.urlencode(parsed_qs, doseq=True)
    return urllib.parse.urlunparse(parsed._replace(query=new_qs))

def find_urls(string):
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    urls = re.findall(url_pattern, string)
    return urls

def scrub_urls(string, urls):
    for url in urls:
        # replace with scrubbed version
        string = string.replace(url, scrub_url(url))
    return string

E = TypeVar("E", bound=BaseException)

def scrub_exception(exception: E) -> E|RAIException:
    exception_str = str(exception)
    urls = find_urls(exception_str)
    if urls:
        return RAIException(scrub_urls(exception_str, urls))
    return exception

def escape_for_f_string(code: str) -> str:
    return (
        code
        .replace("\\", "\\\\")
        .replace("{", "{{")
        .replace("}", "}}")
        .replace("\n", "\\n")
        .replace('"', '\\"')
        .replace("'", "\\'")
    )

def escape_for_sproc(code: str) -> str:
    return code.replace("$$", "\\$\\$")

# @NOTE: `overhead_rate` should fall between 0.05 and 0.5 depending on how time sensitive / expensive the operation in question is.
def poll_with_specified_overhead(
    f,
    overhead_rate: float, # This is the percentage of the time we've already waited before we'll poll again.
    start_time: float | None = None,
    timeout: int | None = None,
    max_tries: int | None = None,
    max_delay: float = 120,
    min_delay: float = 0.1
):
    if overhead_rate < 0:
        raise ValueError("overhead_rate must be non-negative")

    if start_time is None:
        start_time = time.time()
    
    tries = 0
    max_time = time.time() + timeout if timeout else None

    while True:
        if f():
            break

        current_time = time.time()
        
        if max_tries is not None and tries >= max_tries:
            raise Exception(f'max tries {max_tries} exhausted')

        if max_time is not None and current_time >= max_time:
            raise Exception(f'timed out after {timeout} seconds')

        duration = (current_time - start_time) * overhead_rate
        duration = max(min(duration, max_delay), min_delay, 0)
        
        time.sleep(duration) 
        tries += 1

def get_with_retries(
    session: requests.Session,
    url: str,
    max_retries: int = 3,
    backoff_factor = 2,
    min_backoff_s = 2,
):
    attempt = 1
    jitter_s = random.uniform(0.5, 1.5)
    delay_s = min_backoff_s
    while attempt <= max_retries:
        res = session.get(url)
        attempt += 1
        if 500 <= res.status_code <= 504:
            delay_s *= backoff_factor
            time.sleep(delay_s + jitter_s)
            continue
        return res
    raise Exception(f"max retries exceeded fetching {url}")
