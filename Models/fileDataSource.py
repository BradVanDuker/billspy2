import os.path
from os import path, makedirs, listdir

from Models.configData import ConfigData


class FileDataSource:
    corpus_location = ConfigData.get_config_dict()['corpus_directory']
    raw_text_dir_name = 'raw'
    meta_text_dir_name = 'meta'

    @classmethod
    def _get_dir(cls, is_metadata):
        if is_metadata:
            subdir = cls.meta_text_dir_name
        else:
            subdir = cls.raw_text_dir_name
        return path.join(cls.corpus_location, subdir)

    @classmethod
    def store(cls, bill_id, text,  is_metadata=False):
        # check if the file exists and if it doesn't, go ahead and write the file
        p = cls._get_file_name(bill_id, is_metadata=is_metadata)
        with open(p, mode='w+') as f:
            f.write(text)

    @classmethod
    def get(cls, bill_id, is_metadata=False):
        filename = cls._get_file_name(bill_id, is_metadata)
        with open(filename, mode='r') as f:
            data = f.read()
        return data

    @classmethod
    def does_bill_exist(cls, bill_id, is_metadata=False):
        filename = cls._get_file_name(bill_id, is_metadata=is_metadata)
        return path.exists(filename)

    @classmethod
    def _get_file_name(cls, bill_id, is_metadata=False):
        return path.join(cls._get_dir(is_metadata), bill_id)

    @classmethod
    def get_bill_ids(cls, is_metadata=False):
        subdir = cls._get_dir(is_metadata)
        return [f for f in listdir(subdir) if path.isfile(subdir, f)]

