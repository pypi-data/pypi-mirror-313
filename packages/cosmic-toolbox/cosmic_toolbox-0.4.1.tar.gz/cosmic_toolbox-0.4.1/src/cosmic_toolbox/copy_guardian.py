# Copyright (C) 2017 ETH Zurich, Cosmology Research Group

"""
Created on Aug 23, 2017
@author: Joerg Herbel
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
import distutils.dir_util
import os
import random
import shlex
import shutil
import subprocess
import time

from cosmic_toolbox import file_utils, logger

LOGGER = logger.get_logger(__file__)


SEMAPHORE_DIRECTORY = os.path.expanduser("~/copy_guardian_semaphores")


if not os.path.isdir(SEMAPHORE_DIRECTORY):
    try:
        os.mkdir(SEMAPHORE_DIRECTORY)
    except OSError:
        LOGGER.warning(
            "Semaphore directory does not exist, but it could not " "be created either!"
        )


class CopyGuardian(object):
    def __init__(
        self,
        n_max_connect,
        n_max_attempts_remote,
        time_between_attempts,
        use_copyfile=False,
    ):
        self.n_max_connect = n_max_connect
        self.n_max_attempts_remote = n_max_attempts_remote
        self.time_between_attempts = time_between_attempts
        self.use_copyfile = use_copyfile

    def __call__(self, sources, destination):
        # Ensure correct type
        if str(sources) == sources:
            sources = [sources]

        if str(destination) != destination:
            raise ValueError(
                "Destination {} not supported. Multiple destinations for "
                "multiple sources not implemented.".format(destination)
            )

        # Ensure that rsync and local copy behave equally
        for i, source in enumerate(sources):
            if os.path.isdir(source) and not source.endswith("/"):
                sources[i] += "/"

        if destination.endswith("/"):
            destination = destination[:-1]

        # Check if destination is remote
        if file_utils.is_remote(destination):
            # Check for remote sources
            for source in sources:
                if file_utils.is_remote(source):
                    raise IOError(
                        "Cannot copy remote source {} to remote "
                        "destination {}".format(source, destination)
                    )

            self._copy_remote(sources, destination)

        else:
            # Split into local and remote sources
            sources_remote = []

            for source in sources:
                # Remote source
                if file_utils.is_remote(source):
                    sources_remote.append(source)

                # Local source
                else:
                    self._copy_local(source, destination)

            # Now handle remaining (remote) tasks
            if len(sources_remote) > 0:
                self._copy_remote(sources_remote, destination)

    def _copy_local(self, source, destination):
        LOGGER.info("Copying locally: {} -> {}".format(source, destination))

        if os.path.isdir(source):
            distutils.dir_util.copy_tree(source, destination)

        elif os.path.isdir(destination) or not self.use_copyfile:
            shutil.copy(source, destination)

        else:
            shutil.copyfile(source, destination)

    def _copy_remote(self, sources, destination):
        n_attempts = 0

        sources_split = self._split_sources_by_host(sources)
        print(sources_split)

        while n_attempts < self.n_max_attempts_remote:
            self._wait_for_allowance()
            path_semaphore = self._create_semaphore()

            copied = True

            for srcs in sources_split:
                for src in srcs:
                    copied &= self._call_rsync([src], destination)
                # copied &= self._call_rsync(srcs, destination)

            os.remove(path_semaphore)

            if copied:
                break

            else:
                n_attempts += 1
                time.sleep(self.time_between_attempts)
                if n_attempts * self.time_between_attempts > (5 * 60):
                    LOGGER.warning(
                        "waiting for free semaphore for long time, "
                        "n_attempts={}, time={}s".format(
                            n_attempts, n_attempts * self.time_between_attempts
                        )
                    )

        else:
            raise IOError(
                "Failed to rsync {} -> {} ".format(", ".join(sources), destination)
            )

    def _wait_for_allowance(self):
        while True:
            time.sleep(1 + random.random())

            file_list = os.listdir(SEMAPHORE_DIRECTORY)
            file_list = list(
                filter(lambda filename: not filename.startswith("."), file_list)
            )

            if len(file_list) < self.n_max_connect:
                return

    def _create_semaphore(self):
        filename = "{}_{}".format(os.getpid(), datetime.datetime.now()).replace(" ", "")
        filepath = os.path.join(SEMAPHORE_DIRECTORY, filename)
        open(filepath, "w").close()
        return filepath

    def _call_rsync(self, sources, destination):
        LOGGER.info("Rsyncing: {} -> {}".format(", ".join(sources), destination))

        cmd = "rsync -av {} {}".format(" ".join(sources), destination)
        print(cmd)

        try:
            subprocess.check_call(shlex.split(cmd))
            return True

        except subprocess.CalledProcessError:
            return False

    def _split_sources_by_host(self, sources):
        host_dict = {}

        for s in sources:
            host = s.split(":/")[0]

            if host in host_dict:
                host_dict[host].append(s)

            else:
                host_dict[host] = [s]

        return host_dict.values()
