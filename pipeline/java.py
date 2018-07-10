from abc import ABC, abstractmethod
from git import Repo, GitCommandError
from subprocess import check_call
from distutils.version import StrictVersion
from configparser import ConfigParser
from io import StringIO
from functools import reduce
from pipeline.interface import AbstractExecutor, AbstractLibrarySteps, stage_decorator

import os


class JavaLibraryExecutor(AbstractExecutor):
    def __init__(self, metadata):
        self.__repo_path = "{}/the-repo".format(os.getcwd())
        check_call("git clone {} {}".format(
            metadata.repo_url, self.__repo_path), shell=True)
        super().__init__(self.__repo_path)
        self.__metadata = metadata

    def execute(self):
        self.repo.git.checkout(self.__metadata.branch)
        steps = JavaLibrarySteps(self.__repo_path, self.__metadata)
        steps.build()
        steps.version()
        if self.__metadata.branch == "master":
            steps.publish()


class JavaLibrarySteps(AbstractLibrarySteps):
    def __init__(self, repo_path, metadata):
        self.repo_path = "{}/the-repo".format(os.getcwd())
        super().__init__(self.repo_path)
        self.__next_version = self.__compute_next_version()

    @stage_decorator
    def build(self):
        check_call(
            "(cd {} && ./gradlew clean build --console plain --info --refresh-dependencies)".format(self.repo_path), shell=True)

    @stage_decorator
    def version(self):
        print("Creating tag for version {}".format(self.__next_version))
        self.__create_and_push_tags(self.__next_version)

    @stage_decorator
    def publish(self):
        check_call(
            "(cd {} && ./gradlew artifactoryPublish --info --console plain)".format(self.repo_path), shell=True)

    def __compute_next_version(self):
        current_version = self.__read_properties().current_version
        latest_tag = self.__get_latest_tag()

        latest_patch = latest_tag.split(".")[-1]
        latest_tag_no_patch = remove_patch(latest_tag)
        current_version_no_patch = remove_patch(current_version)

        next_patch = 0 if StrictVersion(current_version_no_patch) > StrictVersion(
            latest_tag_no_patch) else int(latest_patch) + 1

        next_version = "{}.{}".format(current_version_no_patch, next_patch)

        if StrictVersion(next_version) <= StrictVersion(latest_tag):
            raise ValueError(
                "ERROR: Version computed ({}) is less than or equal to the previous version ({})!".format(next_version, latest_tag))

        print("Computed next version {}.".format(next_version))
        return next_version

    def __create_and_push_tags(self, version):
        self.repo.create_tag(version)
        response = self.repo.remote().push(version)

        for info in response:
            print(info.summary)

    def __get_latest_tag(self):
        tags = list(map(lambda tag: tag.name, self.repo.tags))
        tags.sort(key=StrictVersion, reverse=True)
        return tags[0]

    def __read_properties(self):
        properties_path = "{}/gradle.properties".format(self.repo_path)
        return GradleProperties(properties_path)


class GradleProperties():
    def __init__(self, properties_path):
        self.__properties = self.__read_config_file(properties_path)

    @property
    def current_version(self):
        return self.__properties["currentVersion"]

    def __read_config_file(self, file_path):
        """
        Hack to allow configparser read a properties file with no sections.
        Injects a [root] section into thr properties to achieve this.
        """
        conf_file = '[root]\n' + open(file_path, 'r').read()
        conf_file_fp = StringIO(conf_file)
        config = ConfigParser()
        config.readfp(conf_file_fp)
        return config['root']


def remove_patch(version):
    return version_list_to_string(version.split(".")[:-1])


def version_list_to_string(version):
    return reduce(lambda acc, val:  "{}.{}".format(acc, str(val)), version)
