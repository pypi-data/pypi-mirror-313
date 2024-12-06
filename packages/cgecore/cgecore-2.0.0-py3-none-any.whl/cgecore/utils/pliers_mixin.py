#!/usr/bin/env python3

import subprocess
from git import Repo
from git.exc import InvalidGitRepositoryError


class PliersMixin():

    DB_VERSION_FILE = "VERSION"

    @staticmethod
    def get_version_commit(gitdir):
        """
            Input: Path to git directory
            Return: (version, commmit_hash)

            commmit_hash: The 40 character hash describing the exact commit of
            the git directory.
            version: The tag of the current commit. If no tag exists the first
            7 characters of the commit hash will be returned instead.

            If the given directory is not a git directory the returned values
            will be 'unknown'.
        """
        try:
            repo = Repo(gitdir)
        except InvalidGitRepositoryError:
            return ("unknown", "unknown")

        com2tag = {}
        for tag in repo.tags:
            com2tag[tag.commit.hexsha] = str(tag)

        version = com2tag.get(repo.commit().hexsha, repo.commit().hexsha[:7])

        return (version, repo.commit().hexsha)

    @staticmethod
    def get_version_pymodule(name):
        """
            Input: python module name
            Return: (version)

            version: The version of the module.

            If the given directory is not a python module it will return
            'unknown'
        """
        try:
            from importlib.metadata import version
            version = version(str(name))
        except ModuleNotFoundError:
            try:
                from pkg_resources import get_distribution
                from pkg_resources import DistributionNotFound
                version = get_distribution(str(name)).version
            except DistributionNotFound or AttributeError:
                try:
                    from importlib import import_module
                    mymodule = import_module(str(name))
                    version = mymodule.__version__
                except ModuleNotFoundError or NameError:
                    version = "unknown"
        return version

    @staticmethod
    def get_version_database(db_path):
        try:
            with open(f"{db_path}/{PliersMixin.DB_VERSION_FILE}") as fh:
                version = fh.readline().strip()
        except FileNotFoundError:
            version = "unknown"
        return version

    @staticmethod
    def get_git_tag(folders_path):
        try:
            git_tag = str(
                subprocess.check_output(
                    ['git', 'describe', '--tags', '--abbrev=0'],
                    stderr=subprocess.STDOUT, cwd=folders_path,
                )).strip('\'b\\n')
        except subprocess.CalledProcessError as exc_info:
            match = re.search(
                'fatal: no tag exactly matches \'(?P<commit>[a-z0-9]+)\'', str(exc_info.output))
            if match:
                raise Exception(
                    'Bailing: there is no git tag for the current commit, {commit}'.format(
                    commit=match.group('commit')))
            raise Exception(str(exc_info.output))
        return git_tag
