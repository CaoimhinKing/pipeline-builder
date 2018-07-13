import unittest
from subprocess import CalledProcessError
from pipeline.gradle import Gradle
from pipeline.process import Process, ExternalCommandError


class TestGradle(unittest.TestCase):
    def test_should_raise_error_if_gradle_call_fails(self):
        # Arrange
        process = FailingFakeProcess()
        gradle = Gradle(process)

        # Act
        with self.assertRaises(ExternalCommandError) as ctx:
            gradle.clean().build().console("nah").execute("")

        # Assert
        self.assertEqual(
            "failed", str(ctx.exception))

    def test_should_not_raise_error_if_gradle_call_succeeds(self):
        # Arrange
        process = SucceedingFakeProcess()
        gradle = Gradle(process)

        # Act
        gradle.clean().build().console("nah").execute("")        


class FailingFakeProcess():
    def check_call(self, cmd):
        raise ExternalCommandError("failed")

class SucceedingFakeProcess():
    def check_call(self, cmd):
        pass