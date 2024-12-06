from typing import Optional, Any

from tq_datasets.dataset_op_interface import TraverseDatasetItems
from tq_utils import my_json, time_util


def test_default_method():
    print()
    t = TraverseDatasetItems()
    t.traverse_dataset(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng\al-monitor',
                       'json')


class TraverseDOWLItems(TraverseDatasetItems):
    @staticmethod
    def item_reader(file_abs_path: str) -> str:
        print('oaushoiasdoiajsodiasoidowifoqn')
        return my_json.load_json_safe(file_abs_path)

    @staticmethod
    def item_processor(**kwargs) -> Optional[Any]:
        print('asdasda')
        return kwargs['raw_item_data']


def test_override_methods():
    print()
    t = TraverseDOWLItems()
    with time_util.Timer('aa'):
        r = t.traverse_dataset(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng',
                               'json', external_raw_data={'s': 1})
        print(len(r))
    """
    3174
    Elapsed time: 2.8971 seconds
    """


def test_override_methods_multithread():
    print()
    t = TraverseDOWLItems()
    with time_util.Timer('aa'):
        r = t.traverse_dataset(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng',
                               'json', external_raw_data={'s': 1}, multi_process=True)
        print(len(r))
    """
    3174
    Elapsed time: 0.9121 seconds
    """


def test_override_methods_with_max_num():
    print()
    t = TraverseDOWLItems()
    with time_util.Timer('aa'):
        r = t.traverse_dataset(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng',
                               'json', max_num=30, external_raw_data={'s': 1})
        print(len(r))
    """
    30
    Elapsed time: 0.0765 seconds
    """


def test_override_methods_multithread_with_max_num():
    print()
    t = TraverseDOWLItems()
    with time_util.Timer('aa'):
        r = t.traverse_dataset(r'E:\Workspace\Pycharm\Datasets\data\Dataset-DOWL2\DOWL2\eng',
                               'json', max_num=30, external_raw_data={'s': 1}, multi_process=True)
        print(len(r))
    """  数量比较少，反而开销打了，没有单线程来的划算
    30
    Elapsed time: 0.0800 seconds
    """
