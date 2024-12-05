import random
from typing import Literal
import requests
from tldextract import extract
from functools import lru_cache


def extract_domain(url: str) -> str:
    """
    Extract the domain from a url. We dedicate a function here to make sure we do it the same way everywhere.

    ex: https://www.inoopa.com/contact -> inoopa.com
    """
    # if http is not present, we can't parse the domain
    if "https://" in url and "http://" not in url:
        url = "http://" + url
    return extract(url).registered_domain


@lru_cache()
def get_all_latest_user_agents() -> list[str]:
    """
    Daily updated list of user agents

    :return: A list of user agents.
    """
    url = "https://jnrbsn.github.io/user-agents/user-agents.json"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def get_random_user_agent() -> str:
    """Get a random user agent. the user agents list is cached."""
    return random.choice(get_all_latest_user_agents())


def get_latest_user_agent(
    operating_system: Literal["macintosh", "windows", "x11"] = "macintosh",
    browser: Literal["version", "chrome", "firefox"] = "version",
) -> str:
    """
    General function to fetch the latest user agent for a given operating system and browser.

    :param operating_system: The operating system to search for. Default is macintosh, X11 is Linux.
    :param browser: The browser to search for. Version is the latest Safari.
    :return: The latest user agent for the given operating system and browser.
    """
    user_agents = get_all_latest_user_agents()
    for user_agent in user_agents:
        user_agent_lower = user_agent.lower()
        if operating_system.lower() in user_agent_lower and browser.lower() in user_agent_lower:
            return user_agent
    raise ValueError(f"No user-agent found for OS: {operating_system} and browser: {browser}")
