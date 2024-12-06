"""
Traverse every script file in the dataset.
You can specify the method how program read, process and filter the scripts.
"""
import os
from typing import Any, List, Optional, Dict
import concurrent.futures

from ..utils import FileManager


class TraverseDatasetItems:

    @staticmethod
    def item_reader(file_abs_path: str) -> Any:
        """
        读取数据集元素的方法。
        默认通过文本的方式读取数据集文件。如需重写，请不要改动参数。
        :param file_abs_path: 文件的绝对路径
        :return: raw data from file.
        """
        with FileManager(file_abs_path, 'r') as f:
            return f.read()

    @staticmethod
    def item_processor(**kwargs) -> Optional[Any]:
        """
        根据元素的绝对路径和 item_reader 获取的原始数据，处理数据返回 processed_item_data。
        默认打印 file_abs_path 和 raw_item_data，并直接返回 raw_item_data。如需重写，请不要改动参数。
        <param traverse_dir> 遍历数据集的目录的绝对路径
        <param file_abs_path> 数据集元素文件的绝对路径
        <param raw_item_data> item_reader 获取的原始数据
        <param external_raw_data> 向 item_process 中传入的额外的数据
        <returns> processed_item_data 处理过的元素数据 or None
        """
        print(
            f"processing:\ntraverse_dir: {kwargs['traverse_dir']}, \nfile_path: {kwargs['file_abs_path']},\nraw_data:\n{kwargs['raw_item_data']}",
            end='\n\n')
        return kwargs['raw_item_data']

    @staticmethod
    def item_filter(**kwargs) -> bool:
        """
        根据元素的绝对路径、item_reader 获取的原始数据 和 已经收集元素数据的数量，判断是否保留数据。
        默认直接返回 True，保留所有数据。如需重写，请不要改动参数。
        <param traverse_dir> 遍历数据集的目录的绝对路径
        <param file_abs_path> 数据集元素文件的绝对路径
        <param processed_item_data> item_processor 处理过的元素数据
        <returns> True，保留数据；False，反之。
        """
        return True

    @classmethod
    def __item_processing(cls, file_abs_path, traverse_dir, external_raw_data):
        """
        对单个数据集 item 执行的操作
        :param file_abs_path: 需要处理的数据集 item 文件的绝对路径
        :param traverse_dir: 遍历的目录
        :param external_raw_data: 向 item_process 中传入的额外的数据
        :return: 如果 item_filter 为 True，则返回 result of item_processor；否则返回 None。
        """
        raw_item_data = cls.item_reader(file_abs_path)

        processed_item_data = cls.item_processor(traverse_dir=traverse_dir,
                                                 file_abs_path=file_abs_path,
                                                 raw_item_data=raw_item_data,
                                                 external_raw_data=external_raw_data)

        if cls.item_filter(traverse_dir=traverse_dir, file_abs_path=file_abs_path,
                           processed_item_data=processed_item_data):
            return processed_item_data

    @classmethod
    def __batch_processing(cls, list_of_paths: List[str], traverse_dir: str,
                           external_raw_data: Optional[Dict[str, Any]]) -> list:
        """
        交由线程执行的批处理函数
        :param list_of_paths: 需要批处理的数据集 item 文件绝对路径列表
        :param traverse_dir: 遍历的目录
        :param external_raw_data: 向 item_process 中传入的额外的数据
        :return: 经过 item_reader, item_process 和 item_filter 后剩下的处理数据列表
        """
        batch_result = []
        for file_abs_path in list_of_paths:
            data = cls.__item_processing(file_abs_path, traverse_dir, external_raw_data)
            if data is not None:
                batch_result.append(data)
        return batch_result

    @classmethod
    def traverse_dataset(cls, traverse_dir: str, item_file_type: str, max_num=-1,
                         external_raw_data: Dict[str, Any] = None,
                         multi_process: bool = False, batch_size: int = 100, num_workers: int = os.cpu_count()) \
            -> List[tuple]:
        """
        遍历给定数据集目录下的元素，并对其进行处理，最终返回处理的结果。如果需要自定义数据集元素的读取、处理和过滤函数，请重写对应方法。
        :param traverse_dir: 遍历数据集的目录的绝对路径
        :param item_file_type: 数据集中元素的文件类型. E.g. 'jpg', 'jpeg', 'png', ...
        :param max_num: 遍历的最大数目. default -1, means traverse all items.
        :param external_raw_data: 向 item_process 中传入的额外的数据
        :param multi_process: 是否进行多线程处理(default: False)
        :param batch_size: 每批处理的 item 数目(default: 100)
        :param num_workers: 线程池大小(default: os.cpu_count())
        :returns: list of the tuple(item_absolute_path, return result of item_processor)
        """
        if not os.path.exists(traverse_dir):
            raise FileNotFoundError(f'Dataset not found at {traverse_dir}.')

        result = []
        count = 0
        if multi_process:  # 多线程破处理
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_workers)
            futures = []
            # 遍历数据集 item，进行多线程批处理
            temp_batch = []  # 临时存放当前批次要处理的数据
            for root, dirs, files in os.walk(traverse_dir):
                for file in files:  # file: file full name
                    # 将符合数据集文件类型的 item 并且没有达到遍历上限时，添加到当前 batch
                    file_type = os.path.splitext(file)[1]
                    if file_type == '' or file_type[1:] != item_file_type:
                        continue
                    count += 1
                    if 0 < max_num < count:
                        break
                    temp_batch.append(os.path.join(root, file))  # append the abstract path of file
                    # 若到达 batch_size，则对其进行批处理
                    if len(temp_batch) == batch_size:
                        futures.append(executor.submit(lambda p: cls.__batch_processing(*p),
                                                       [temp_batch, traverse_dir, external_raw_data]))
                        temp_batch = []  # 重置
            if len(temp_batch) > 0:  # 如果最后批次没有达到 batch_size，但还剩余，则也进行批处理
                futures.append(executor.submit(lambda p: cls.__batch_processing(*p),
                                               [temp_batch, traverse_dir, external_raw_data]))
            # 等待结果并进行合并
            for future in concurrent.futures.as_completed(futures):
                result.extend(future.result())
            executor.shutdown(wait=True)
        else:  # 单线程处理
            for root, dirs, files in os.walk(traverse_dir):
                for file in files:
                    file_type = os.path.splitext(file)[1]
                    if file_type == '' or file_type[1:] != item_file_type:
                        continue
                    count += 1
                    if 0 < max_num < count:
                        break
                    file_abs_path = os.path.join(root, file)
                    data = cls.__item_processing(file_abs_path, traverse_dir, external_raw_data)
                    if data is not None:
                        result.append(data)
        return result
