import unittest
from common import group_by_name  # Replace with your actual module name


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


if __name__ == "__main__":
    unittest.main()