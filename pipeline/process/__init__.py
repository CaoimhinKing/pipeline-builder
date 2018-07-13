from subprocess import check_call, CalledProcessError


class Process():
    def check_call(self, cmd):
        try:
            check_call(cmd, shell=True)
        except CalledProcessError as e:
            raise ExternalCommandError(e.stdout)

class ExternalCommandError(Exception):
    def __init__(self, message):
        super().__init__(message)