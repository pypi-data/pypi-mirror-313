"""
This module is highly inspired by Mail Scout: https://github.com/batuhanaky/mailscout
Do a regular check on their repository and implement the good ideas here.
"""

import re
import time
import smtplib
import dns.name
import itertools
import unicodedata
import dns.resolver
from functools import partial
from rich.pretty import pprint
from unidecode import unidecode
from concurrent.futures import ThreadPoolExecutor, as_completed


def find_generic_emails_bulk(
    domains: list[str], custom_prefixes: list[str] | None = None
) -> dict[str, list[str]] | None:
    """
    Find valid generic email addresses in bulk for multiple domains.

    :param domains: List of domains to search for generic emails.
    :param custom_prefixes: List of custom prefixes to search for. If not provided, common prefixes will be used.
    :return: A dictionary containing: {domain: [generic_emails]}
    """
    results = {}
    with ThreadPoolExecutor() as executor:
        # We make futures a dict to keep track of the domain associated with each future (list of emails).
        futures = {}
        for domain in domains:
            future = executor.submit(partial(find_generic_emails, domain, custom_prefixes))
            futures[future] = domain
        for future in as_completed(futures):
            domain = futures[future]
            generic_emails = future.result()
            results[domain] = generic_emails
    return results or None


def find_personal_emails_bulk(
    domain: str, names: list[str], check_catchall: bool = True, normalize: bool = True
) -> dict[str, list[str]] | None:
    """
    Find valid personal email addresses in bulk for multiple domains.

    :param domain: Domain to search for personal emails.
    :param names: List of names to search for.
    :param check_catchall: Check if the domain is a catch-all domain.
    :param normalize: Normalize the names to email-friendly format.
    :return: A dictionary containing: {name: [personal_emails]}
    """
    if _check_email_is_catchall(domain):
        return None

    results = {}
    with ThreadPoolExecutor() as executor:
        # We make futures a dict to keep track of the name associated with each future (list of emails).
        futures = {}
        for name in names:
            future = executor.submit(partial(find_personal_emails, domain, name, check_catchall, normalize))
            futures[future] = name

        for future in as_completed(futures):
            name = futures[future]
            personal_emails = future.result()
            results[name] = personal_emails
    return results or None


def find_generic_emails(domain: str, custom_prefixes: list[str] | None = None) -> list[str] | None:
    """
    Generate a list of generic email addresses for a given domain.

    :param domain: Domain to search for generic emails.
    :param custom_prefixes: List of custom prefixes to search for. If not provided, common prefixes will be used.
    :return: A list of generic email addresses. If the domain is a catch-all domain, returns None.
    """
    if _check_email_is_catchall(domain):
        return None
    generic_emails = _generate_generic_emails(domain, custom_prefixes)
    for email in generic_emails:
        # return the first delivrable email. This is to avoid getting flagged/banned by the SMTP server.
        if check_email_is_deliverable(email):
            return [email]
    return None


def find_personal_emails(
    domain: str, name: str, check_catchall: bool = True, normalize: bool = True
) -> list[str] | None:
    """
    Generate a list of personal email addresses for a given domain.

    :param domain: Domain to search for personal emails.
    :param name: Name to search for.
    :param check_catchall: Check if the domain is a catch-all domain.
    :param normalize: Normalize the name to email-friendly format.
    :return: A list of personal email addresses. If the domain is a catch-all domain, returns None.
    """
    if check_catchall and _check_email_is_catchall(domain):
        print("catchall")
        return None

    email_variants = _generate_email_variants(name.split(" "), domain, normalize=normalize)
    print("--- Variants ---")
    pprint(email_variants)
    for email in email_variants:
        if check_email_is_deliverable(email):
            # return the first delivrable email. This is to avoid getting flagged/banned by the SMTP server.
            return [email]
    return None


def check_email_is_deliverable(email: str, smtp_port: int = 25, smtp_timeout: int = 2) -> bool:
    """Check if an email is deliverable using SMTP."""
    domain = email.split("@")[1]
    try:
        # 1. Check if the DOMAIN has valid MX records. (the domain is configured to receive emails)
        records = dns.resolver.resolve(domain, "MX")
        if not records:
            return False
        mx_record = str(records[0].exchange)  # type: ignore
        # Check if the email is deliverable using SMTP (email protocol).
        with smtplib.SMTP(mx_record, smtp_port, timeout=smtp_timeout) as server:
            server.set_debuglevel(0)
            server.ehlo("example.com")
            server.mail("test@example.com")
            code, _ = server.rcpt(email)
        # If the code is 250, the email is deliverable.
        return code == 250
    # A bunch of "normal" exceptions that can happen if the domain doesn't have valid MX records.
    except (
        dns.resolver.NoAnswer,
        dns.resolver.NXDOMAIN,
        dns.resolver.NoNameservers,
        dns.resolver.Timeout,
        dns.name.LabelTooLong,
    ):
        pass
    # A lot of stuff can be wrong with DNS, This needs to be tracked but shouldn't stop the process.
    except Exception as e:
        print(f"Error checking {email}: {e}")
    return False


def _check_email_is_catchall(email_domain: str) -> bool:
    """Check if a domain is a catch-all for email addresses."""
    random_email = f"dbv23qzk5sp2wgyowndksjp@{email_domain}"
    return check_email_is_deliverable(random_email, smtp_timeout=2)


def _normalize_name(name: str) -> str:
    """Convert a non-email compliant name to a normalized email-friendly format."""
    name = unidecode(name.lower())
    normalized = unicodedata.normalize("NFKD", name)
    ascii_encoded = normalized.encode("ascii", "ignore").decode("ascii")
    email_compliant = re.sub(r"[^a-z0-9]", "", ascii_encoded)
    return email_compliant


def _generate_generic_emails(domain: str, custom_prefixes: list[str] | None = None) -> list[str]:
    """Generate a list of email addresses with common or custom prefixes for a given domain."""
    common_prefixes = [
        "info",
        "contact",
        "support",
        "hello",
        "hi",
        "service",
        "team",
        "press",
        "help",
        "staff",
        "careers",
        "jobs",
        "customer",
        "office",
        "sales",
        "marketing",
        "hr",
        "accounts",
        "billing",
        "finance",
        "operations",
        "it",
        "admin",
        "design",
        "engineering",
        "feedback",
        "dev",
        "developer",
        "tech",
    ]
    prefixes = custom_prefixes if custom_prefixes else common_prefixes
    return [f"{prefix}@{domain}" for prefix in prefixes]


def _generate_email_variants(splitted_name: list[str], domain: str, normalize: bool = True) -> list[str]:
    """
    Generate a set of email address variants based on a list of names for a given domain.
    Return a list of email addresses sorted by length to try first variants with firstname/lastname.
    """
    variants: set[str] = set()

    if normalize:
        names = [_normalize_name(name) for name in splitted_name]

    for i in range(1, len(names) + 1):
        for name_combination in itertools.permutations(names, i):
            variants.add("".join(name_combination).lower())
            variants.add(".".join(name_combination).lower())
            variants.add("_".join(name_combination).lower())
            variants.add("-".join(name_combination).lower())

    for name_part in splitted_name:
        variants.add(name_part.lower())
        variants.add(name_part[0].lower())

    # Sort the variants by length to try first variants with firstname/lastname
    return sorted([f"{variant}@{domain}" for variant in variants], key=len, reverse=True)


# Your router's port 25 should be open to use this module. If it's not, you will think that the email is not deliverable.
# This makes the module crashes at import time if the port is not open.
assert check_email_is_deliverable(
    "contact@inoopa.com", smtp_timeout=2
), "contact@inoopa.com not deliverable, open your router's port 25"


if __name__ == "__main__":
    # --- Example usage ---
    inoopa_generic_emails = find_generic_emails("inoopa.com")
    print("Inoopa Generic emails:", inoopa_generic_emails)
    # maxim_personal_emails = find_personal_emails("inoopa.com", "Maxim Berge")
    # print("Maxim personal emails:", maxim_personal_emails)
