from functools import reduce
from subprocess import check_call
from pipeline.process import ExternalCommandError


class Gradle():
    def __init__(self, process):
        self.__process = process
        self.__cmd = "./gradlew"
        self.__args = set()

    def build(self):
        self.__args.add("build")
        return self

    def clean(self):
        self.__args.add("clean")
        return self

    def console(self, typ):
        self.__args.add("--console {}".format(typ))
        return self

    def execute(self, directory=None):
        if directory is not None:
            cmd = "cd {} && {}".format(directory, str(self))
        else:
            cmd = "{}".format(str(self))
        try:
            self.__process.check_call(cmd)        
        finally:
            self.__args = set()

    def __str__(self):
        return "{} {}".format(self.__cmd, reduce(lambda acc, val: "{} {}".format(acc, val), self.__args))
