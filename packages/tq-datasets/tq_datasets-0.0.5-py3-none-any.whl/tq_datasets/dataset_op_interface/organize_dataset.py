import os
from typing import Any, List, Optional, Dict


class OrganizeDataset:
    """
    用于获得根据分类结构化的数据集
    """

    @staticmethod
    def item_processor(**kwargs) -> Optional[Any]:
        """
        根据元素的绝对路径，数据集目录和传入的额外数据，返回数据项所属的分类列表.
        默认根据相对于数据集目录的数据项相对路径的目录列表作为分类列表。如需重写，请不要改动参数。
        <param traverse_dir> 遍历数据集的目录的绝对路径
        <param file_abs_path> 数据集元素文件的绝对路径
        <param external_raw_data> 向 item_process 中传入的额外的数据
        <returns> 数据项所属的分类列表(e.g. ['lang', 'source', 'resolution']) or None(若为 None, 该数据项会被过滤)
        """
        traverse_dir: str = kwargs['traverse_dir']  # e.g. E:\..
        file_abs_path: str = kwargs['file_abs_path']  # e.g. E:\..\zh\al-monitor\2k\1.png
        dir_abs_path = os.path.dirname(file_abs_path)  # e.g. E:\..\zh\al-monitor\2k
        dir_relative_path = dir_abs_path[len(traverse_dir) + 1:]  # e.g. zh\al-monitor\2k
        return dir_relative_path.split(os.sep)  # e.g. ['zh', 'al-monitor', '2k']

    @classmethod
    def organize_dataset(cls, traverse_dir: str, item_extensions: List[str],
                         external_raw_data: Dict[str, Any] = None, ) \
            -> dict:
        """
        获得根据分类结构化的数据集。如果需要自定义数据集元素的处理函数 item_processor，请重写该方法，详细见其 docstring。
        :param traverse_dir: 遍历数据集的目录的绝对路径
        :param item_extensions: 数据集中元素的文件后缀名列表. E.g. ['jpg', 'jpeg', 'png', ...]
        :param external_raw_data: 向 item_process 中传入的额外的数据
        :returns: 使用字典，进行一层层分类，即嵌套字典；最后分类的值为对应所属数据项的列表(列表项为数据项的绝对路径).
        """
        if not os.path.exists(traverse_dir):
            raise FileNotFoundError(f'Dataset not found at {traverse_dir}.')

        result = {}
        for root, dirs, files in os.walk(traverse_dir):
            for file in files:
                file_type = os.path.splitext(file)[1]
                if file_type == '' or file_type[1:] not in item_extensions:
                    continue
                file_abs_path = os.path.join(root, file)
                classes = cls.item_processor(traverse_dir=traverse_dir, file_abs_path=file_abs_path,
                                             external_raw_data=external_raw_data)
                if classes is None:
                    continue
                temp = result
                for c in classes[:-1]:
                    temp = temp.setdefault(c, dict())
                temp.setdefault(classes[-1], []).append(file_abs_path)
        return result
