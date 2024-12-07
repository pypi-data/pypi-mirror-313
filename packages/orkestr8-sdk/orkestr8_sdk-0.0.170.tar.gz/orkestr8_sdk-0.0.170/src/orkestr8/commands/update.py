import importlib
import logging
import os
import shutil
import sys
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import List
from uuid import uuid4

from orkestr8.clients.data_lake_client import ClientType, DataLakeClient

from ..installer import install
from .base import Command

logger = logging.getLogger()


@dataclass
class UpdateArgs:
    remote_file_path: str
    dest_file_path: str
    default_yes: bool = False
    sync_image_data: bool = True
    generate_new_train_test: bool = False


class UpdateCommand(Command[UpdateArgs]):
    @staticmethod
    def __rename_dir(old, new_=None):
        new_name = new_
        if new_ is None:
            new_name = str(uuid4())
        try:
            os.rename(old, new_name)
            return new_name
        except Exception as e:
            raise Exception(f"Renaming file failed. {str(e)}")

    @staticmethod
    def parse(args) -> UpdateArgs:
        # first try update specific, but these attr may not exist
        # if `update` wasnt called
        try:
            return UpdateArgs(
                args.update.remote_file_path,
                args.update.dest_file_path,
                args.default_yes,
            )
        except:
            return UpdateArgs(
                args.remote_file_path, args.dest_file_path, args.default_yes
            )

    def run(self):
        """Pulls down updated testing library and training data from repo"""
        # TODO: Due to imports, cannot be 'true' global env var
        # need to make a settings file
        AWS_BUCKET_NAME = os.environ["AWS_BUCKET_NAME"]
        args = self.args
        remote_path, dest_path = args.remote_file_path, args.dest_file_path

        cl = DataLakeClient(ClientType.S3, AWS_BUCKET_NAME)
        if not args.default_yes:
            confirm = input(
                "Update is a desctructive operation. The path will be completely overwritten ['Enter y to continue']. "
            )
            if confirm != "y":
                print("Exiting..")
                return
        path_exists = Path(dest_path).exists()
        new_name = None
        if path_exists:
            logger.info("Path exists. Deleting old path")
            new_name = self.__rename_dir(dest_path)

        try:
            cl.get_object(remote_path, Path(remote_path).name)
        except Exception as e:
            if new_name is not None:
                self.__rename_dir(new_name, dest_path)
            print(f"Failed to perform update operation. {type(e).__name__}:{str(e)}")
            sys.exit(1)
        else:
            if new_name is not None:
                logger.info("Removing backup file")
                shutil.rmtree(new_name, ignore_errors=True)
            logger.info("Successfully updated")
        install()
        updated = self.sync_image_data()
        if updated or self.args.generate_new_train_test:
            m = importlib.import_module("utils")
            m.split_dump_dataset()
        self.build_classes()

    @staticmethod
    def build_classes():
        classes = []
        for name in os.listdir(str(Path.home() / "data/images")):
            if "." in name:
                continue
            classes.append(name)
        classes_file = str(Path.home() / "data/images/classes.txt")
        with open(classes_file, "w") as f:
            for c in classes:
                f.write(c + "\n")

    def sync_image_data(self) -> bool:
        """Pulls down all image data from repo. Maintains 'Key' directory
         structure ie. foo/bar/.txt will exist in ~/foo/bar.txt. Updates the
        state file containing all downloaded files if it exists, else creates it.
        :returns: Return True if image_data was synced"""

        logger.info("Starting image sync process")
        AWS_BUCKET_NAME = os.environ["AWS_BUCKET_NAME"]
        cl = DataLakeClient(ClientType.S3, AWS_BUCKET_NAME)

        source_of_truth = "training_data_on_server.txt"
        complete_path = f"data/images/{source_of_truth}"

        files_on_server = []
        with cl.get_object_as_file(complete_path) as file:
            if file:
                files_on_server = [l.strip() for l in file.readlines()]

        files_to_add: List[bytes] = []
        for batch_records in cl.list_objects(prefix="data/images"):
            for record in batch_records:
                file_name = record["Key"].encode()

                if file_name not in files_on_server and is_image_file(file_name):
                    files_to_add.append(file_name)

        # Add files
        for file_name in files_to_add:
            file_name_str = file_name.decode()
            parent_dirs = Path.home() / Path(*(file_name_str.split("/")[:-1]))
            os.makedirs(str(parent_dirs), exist_ok=True)
            new_location = Path.home() / file_name_str
            cl.get_object(file_name_str, str(new_location))

        logger.info("Images in repo have been sync'd to server")
        # Update sync file in remote repo
        if files_to_add:
            with BytesIO() as s:
                for l in files_to_add + files_on_server:
                    s.write(l + b"\n")
                s.seek(0)
                logger.info("Pushing up new state data")
                cl.put_object(complete_path, s)
        else:
            logger.info("Server is sync'd with repo. No new images to add at this time")

        logger.info("Image data sync complete")
        return bool(files_to_add)


# TODO: It MAY just be better to agree on 1 file type
def is_image_file(file_name: bytes) -> bool:
    """Checks to see if the file type is the accepted"""
    image_types = [b".jpg", b".jpeg"]
    return any(file_name.endswith(it) for it in image_types)
