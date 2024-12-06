from abc import ABC, abstractmethod
from ..domain.data_dto import DataEntity


# 定义抽象基类
class Execute(ABC):
    @abstractmethod
    def execute_custom(self, dataDto: DataEntity):
        pass
