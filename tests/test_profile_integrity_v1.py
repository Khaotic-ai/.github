#!/usr/bin/env python3
"""Public organization profile integrity checks (no private repo operations)."""
from pathlib import Path
import re
import unittest
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "profile/README.md"
BANNER = ROOT / "assets/khaotic-org-signal.svg"

class PublicOrganizationProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.md = README.read_text(encoding="utf-8")
        cls.svg = BANNER.read_text(encoding="utf-8")

    def test_profile_and_banner_are_present(self):
        self.assertTrue(README.is_file())
        self.assertTrue(BANNER.is_file())

    def test_svg_is_static_public_and_accessible(self):
        doc = ElementTree.fromstring(self.svg)
        self.assertEqual(doc.get("viewBox"), "0 0 1280 410")
        self.assertIn("Khaotic.AI", self.svg)
        self.assertIn("Build the Possibility", self.svg)
        self.assertNotIn("<script", self.svg.lower())
        without_xml_namespace = self.svg.replace("http://www.w3.org/2000/svg", "")
        self.assertNotIn("http://", without_xml_namespace.lower())
        self.assertNotIn("https://", self.svg.lower())

    def test_banner_relative_path_resolves(self):
        self.assertIn("../assets/khaotic-org-signal.svg", self.md)
        self.assertTrue((README.parent / "../assets/khaotic-org-signal.svg").exists())
        self.assertIn('width="100%"', self.md)

    def test_main_public_destinations(self):
        for u in (
            "https://k-haotic.github.io/K-haotic/organization/",
            "https://k-haotic.github.io/K-haotic/ai-systems-circuit/",
            "https://k-haotic.github.io/K-haotic/ai-systems-circuit/learn/",
            "https://k-haotic.github.io/K-haotic/",
        ):
            with self.subTest(url=u):
                self.assertIn(u, self.md)

    def test_original_ai_literacy_title(self):
        self.assertIn("AI for Dummies (Tutor) — AI Literacy Training", self.md)

    def test_private_research_and_membership_boundaries(self):
        self.assertIn("not an active follower-based entitlement", self.md)
        self.assertIn("These are not exposed or automatically granted", self.md)
        self.assertIn("Private:", self.md)

    def test_no_sensitive_source_or_exposed_credentials(self):
        combined=(self.md+"\n"+self.svg).lower()
        for token in (
            "client_secret", "oauth_refresh", "access_token",
            "github_pat_", "api_key=", "sk-", "gpu_init", "native/levi-",
            "khaotic-owner", "127.0.0.1:", "ssh-rsa"
        ):
            with self.subTest(token=token):
                self.assertNotIn(token, combined)

    def test_profile_contains_only_public_links(self):
        urls = re.findall(r"https?://[^)\s\"<>]+", self.md)
        self.assertGreaterEqual(len(urls), 8)
        allowed = (
            "https://k-haotic.github.io/K-haotic/",
            "https://github.com/K-haotic",
            "https://khaotic.ai/",
        )
        for u in urls:
            with self.subTest(url=u):
                self.assertTrue(u.startswith(allowed), u)
        self.assertNotIn("PRIVATE_REPOSITORY", self.md)

if __name__ == "__main__":
    unittest.main(verbosity=2)
