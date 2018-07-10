import unittest

from pipeline.git import Git


class TestGit(unittest.TestCase):
    def test_should_return_the_highest_tag(self):
        # Arrange
        expected = "3.2.2"
        tags = [FakeTag("1.2.0"), FakeTag("0.4.1"), FakeTag("3.2.2")]
        git = Git(FakeRepo(tags))

        # Act
        tag = git.get_highest_tag()

        # Assert
        self.assertEqual(tag, expected)


class FakeRepo():
    def __init__(self, tags):
        self.__tags = tags

    @property
    def tags(self):
        return self.__tags

class FakeTag():
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name