import os

from tq_datasets import OrganizeDataset
from tq_datasets.utils import tq_json
from test import TEST_DATA_DIR


def test_organize_dataset():  # pass
    organized_dataset = OrganizeDataset.organize_dataset(
        r'E:\Workspace\Pycharm\ocr-test\ocr-test-data\Dataset-DOWL2\DOWL2',
        ['png', 'json'])
    output_file = os.path.join(TEST_DATA_DIR, 'organized_dataset.json')
    tq_json.dump_json_safe(output_file, organized_dataset)
