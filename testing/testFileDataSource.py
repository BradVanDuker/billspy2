from os import path, remove
import unittest

from Models.fileDataSource import FileDataSource
from Models.configData import ConfigData


class TestFileDataSource(unittest.TestCase):
    def test_write_file(self):
        fds = FileDataSource()
        text = 'This is sample text'
        filename = 'foobar.txt'
        for is_meta, subdir in [(True, 'meta'), (False, 'raw')]:
            fds.write_file(filename, text, is_metadata=is_meta)

            # check the file exists in the correct folder
            configs = ConfigData.get_config_dict()
            directory = configs['corpus_directory']
            filepath = path.join(directory, subdir, 'foobar.txt')
            assert path.exists(filepath)

            # erase the file
            remove(filepath)

    def test_read_file(self):
        fds = FileDataSource()
        doc_name = 'BILL-0000'
        text = 'This is sample text'
        fds.write_file(doc_name, text)

        assert fds.read_file(doc_name) == text

        # erase the file
        configs = ConfigData.get_config_dict()
        directory = configs['corpus_directory']
        filepath = path.join(directory, 'raw', doc_name)
        remove(filepath)


if __name__ == '__main__':
    unittest.main()