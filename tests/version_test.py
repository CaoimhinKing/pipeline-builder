import unittest

from pipeline.version import InvalidVersionError, Versioner


class TestVersioner(unittest.TestCase):
    def test_should_bump_patch(self):
        # Arrange
        curent = "1.2.x-SNAPSHOT"
        previous = "1.2.2"
        expected = "1.2.3"
        versioner = Versioner()

        # Act
        version = versioner.compute_next_version(curent, previous)

        # Assert
        self.assertEqual(version, expected)

    def test_should_throw_error_if_previous_major_minor_pair_greater_than_current(self):
        # Arrange
        current = "1.2.x-SNAPSHOT"
        previous = "1.3.3"
        versioner = Versioner()

        # Act
        with self.assertRaises(InvalidVersionError) as ctx:
            versioner.compute_next_version(current, previous)

        # Assert
        self.assertEqual(
            "Computed version (1.2.4) is less than or equal to previous version (1.3.3)", str(ctx.exception))
