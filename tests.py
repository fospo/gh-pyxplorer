import unittest
from unittest.mock import Mock
from common import group_by_name, check_licenses, check_other_license_names


class TestGroupByName(unittest.TestCase):
    def test_group_by_name(self):
        results = [
            {"name": "test-repo1", "private": True},
            {"name": "test-repo2", "private": True},
            {"name": "test-repo3", "private": False},
            {"name": "another-repo", "private": False},
        ]

        expected_output = {
            "test": {
                "count": 3,
                "private-repos": [
                    "test-repo1",
                    "test-repo2",
                ],
                "public-repos": [
                    "test-repo3",
                ],
            },
            "another": {
                "count": 1,
                "private-repos": [],
                "public-repos": [
                    "another-repo",
                ],
            },
        }

        self.assertEqual(group_by_name(results), expected_output)


class TestCommonFunctions(unittest.TestCase):
    def test_check_licenses(self):
        # Mock an OK repository object
        repository = Mock()
        repository.get_license.return_value.license.name = "MIT License"

        self.assertEqual(check_licenses(repository), "MIT License")

    def test_check_other_license_names(self):
        repository = Mock()
        repository.get_contents.return_value = [
            Mock(path="license.txt"),
            Mock(path="README.md"),
        ]

        self.assertEqual(check_other_license_names(repository), "license.txt")

    def test_check_licenses_no_license(self):
        # Mock a repository object with no license
        repository = Mock()
        repository.get_license.return_value = None
        repository.get_contents.return_value = []

        self.assertEqual(check_licenses(repository), None)

    def test_check_other_license_names_no_license_file(self):
        # Mock a repository object with no license file
        repository = Mock()
        repository.get_contents.return_value = [
            Mock(path="README.md"),
        ]

        self.assertEqual(check_other_license_names(repository), None)

    def test_check_other_license_names_multiple_license_files(self):
        # Mock a repository object with multiple license files
        repository = Mock()
        repository.get_contents.return_value = [
            Mock(path="LICENSE"),
            Mock(path="license.txt"),
        ]

        self.assertEqual(check_other_license_names(repository), "LICENSE")


if __name__ == "__main__":
    unittest.main()
