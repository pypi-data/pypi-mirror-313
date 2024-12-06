# coding=utf-8

"""
@fileName       :   __init__.py
@data           :   2024/2/2
@author         :   jiangmenggui@hosonsoft.com
"""
from .log_manager import LogManager
from .attribute_dict.model import AttributeDict, IgnoreCaseAttributeDict
# from .attribute_dict.pydantic_model import NullableBaseModel

Model = AttributeDict
logger = LogManager('my-tools', console_level='DEBUG').get_logger()

if __name__ == '__main__':
    logger.debug('debug')
    pass
