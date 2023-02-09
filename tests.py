import unittest
from unittest.mock import patch
from common import explore_licenses, group_by_project
from github import Github


# write test for group_by_project function
class TestGroupByProject(unittest.TestCase):
    def test_none(self):
        lines = None
        expected = {}
        self.assertEqual(group_by_project(lines), expected)

    def test_empty_list(self):
        lines = []
        expected = {}
        self.assertEqual(group_by_project(lines), expected)

    def test_group_by_project(self):
        lines = [
            "0, prova/prova1-etc",
            "1, prova/prova1-bbb",
            "2, prova/prova3-etc",
        ]
        expected = {
            "prova1": ["prova1-etc", "prova1-bbb"],
            "prova3": ["prova3-etc"],
        }
        self.assertEqual(group_by_project(lines), expected)

    def test_group_by_project_with_empty_line(self):
        lines = [
            "0, prova/prova1-etc",
            "1, prova/prova1-bbb",
            "2, prova/prova3-etc",
            "",
        ]
        expected = {
            "prova1": ["prova1-etc", "prova1-bbb"],
            "prova3": ["prova3-etc"],
        }
        self.assertEqual(group_by_project(lines), expected)

    def test_group_by_project_with_empty_line_and_spaces(self):
        lines = [
            "0, prova/prova1-etc",
            "1, prova/prova1-bbb",
            "2, prova/prova3-etc",
            "",
            "",
        ]
        expected = {
            "prova1": ["prova1-etc", "prova1-bbb"],
            "prova3": ["prova3-etc"],
        }
        self.assertEqual(group_by_project(lines), expected)


# test for common.py
class TestCommon(unittest.TestCase):
    def test_explore_licenses(self):
        repo = Github().get_repo("pagopa/pagopa-api")
        expected = "pagopa-api,MIT License"
        self.assertEqual(explore_licenses(repo), expected)

    @patch("github.Repository.Repository.get_license")
    def test_explore_licenses_mocked(self, mock_get_license):
        repo = Github().get_repo("pagopa/pagopa-api")
        mock_get_license.return_value.license.name = "MIT License"
        expected = "pagopa-api,MIT License"
        self.assertEqual(explore_licenses(repo), expected)


if __name__ == "__main__":
    unittest.main()
