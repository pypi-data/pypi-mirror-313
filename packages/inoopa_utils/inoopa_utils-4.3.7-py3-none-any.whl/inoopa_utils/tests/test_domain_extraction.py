import unittest
from helpers import extract_domain


class TestDomainExtraction(unittest.TestCase):
    """Ensure the extraction of domain works as expected."""

    def test_extract_domain_endpoint(self):
        url = "https://www.inoopa.com/contact"
        domain = extract_domain(url)
        self.assertEqual(domain, "inoopa.com")

    def test_extract_domain_endpoint_with_params(self):
        url = "https://www.inoopa.com/contact/index.php?param=value"
        domain = extract_domain(url)
        self.assertEqual(domain, "inoopa.com")

    def test_extract_domain_endpoint_with_subdomain(self):
        url = "https://www.inoopa.com/contact"
        domain = extract_domain(url)
        self.assertEqual(domain, "inoopa.com")

        url = "https://test.www.inoopa.com/contact"
        domain = extract_domain(url)
        self.assertEqual(domain, "inoopa.com")

    def test_extract_domain_with_double_extension(self):
        url = "https://www.inoopa.co.uk/contact.html"
        domain = extract_domain(url)
        self.assertEqual(domain, "inoopa.co.uk")


if __name__ == "__main__":
    unittest.main()
