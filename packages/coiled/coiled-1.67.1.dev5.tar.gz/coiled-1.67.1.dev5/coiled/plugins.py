import logging
import os

from distributed.diagnostics.plugin import SchedulerPlugin, WorkerPlugin


class DaskSchedulerWriteFiles(SchedulerPlugin):
    name = "scheduler-write-files"

    def __init__(self, files, symlink_dirs=None):
        self._files_to_write = {**(files or {})}
        self._symlink_dirs = {**(symlink_dirs or {})}

    def start(self, *args, **kwargs):
        logger = logging.getLogger("distributed.scheduler")
        files = self._files_to_write
        for path, content in files.items():
            abs_path = os.path.expanduser(path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w") as f:
                f.write(content)
                logger.info(f"{self.name} wrote to {abs_path}")

        for source_dir, target_dir in self._symlink_dirs.items():
            target_dir = os.path.abspath(os.path.expanduser(target_dir))
            if not os.path.exists(target_dir):
                try:
                    os.symlink(source_dir, target_dir)
                except Exception:
                    logger.exception(f"Error creating symlink from {source_dir} to {target_dir}")


class DaskWorkerWriteFiles(WorkerPlugin):
    name = "worker-write-files"

    def __init__(self, files, symlink_dirs=None):
        self._files_to_write = {**(files or {})}
        self._symlink_dirs = {**(symlink_dirs or {})}

    def setup(self, *args, **kwargs):
        logger = logging.getLogger("distributed.worker")
        files = self._files_to_write
        for path, content in files.items():
            abs_path = os.path.expanduser(path)
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            with open(abs_path, "w") as f:
                f.write(content)
                logger.info(f"{self.name} wrote to {abs_path}")

        for source_dir, target_dir in self._symlink_dirs.items():
            target_dir = os.path.abspath(os.path.expanduser(target_dir))
            if not os.path.exists(target_dir):
                try:
                    os.symlink(source_dir, target_dir)
                except Exception:
                    logger.exception(f"Error creating symlink from {source_dir} to {target_dir}")
