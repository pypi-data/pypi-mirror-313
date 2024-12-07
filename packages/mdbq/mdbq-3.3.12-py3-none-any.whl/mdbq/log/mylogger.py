import logging
from logging import Logger
from logging import handlers


class MyLogger(Logger):
    """
    从Logger类中继承，实例化一个日志器
    """
    def __init__(self, logger_name, level='INFO', is_stream_handler=True, file=None, debug_file=None,
                 max_bytes=False, back_count=10, when=None):
        """
        :param logger_name: 日志器的名字
        :param level: 日志级别  # DEBUG  INFO  WARNING  ERROR  CRITICAL
        :param is_stream_handler: 默认True输出到控制台
        :param file: 传入文件名，默认None不输出到 file
        param debug_file: 传入文件名，记录详细debug时使用，默认None不输出， 尽量不要和file同时使用，会重复写
        :param when: 按周期分割日志，默认不分割，除非指定其他值
        :param max_bytes: 按文件大小分割日志
        :param back_count: 保留日志的数量， 值从0开始
        """
        # 设置日志器名字、级别
        super().__init__(logger_name, level)

        # 定义日志格式, 使用Formatter类实例化一个日志类
        fmt_stream = "%(asctime)s %(levelname)s %(name)s: %(message)s"
        fmt_file = "%(asctime)s %(name)s: %(message)s"
        fmt_debug_file = "%(asctime)s %(levelname)s %(name)s %(funcName)s: %(message)s"
        formatter_stream = logging.Formatter(fmt_stream, datefmt="%Y-%m-%d %H:%M:%S")
        formatter_file = logging.Formatter(fmt_file, datefmt="%Y-%m-%d %H:%M:%S")
        formatter_debug_file = logging.Formatter(fmt_debug_file, datefmt="%Y-%m-%d %H:%M:%S")

        # 创建一个handler，默认输出到控制台，如果设置为False，日志将不输出到控制台
        if is_stream_handler:
            stream_handler = logging.StreamHandler()  # 设置渠道当中的日志格式
            stream_handler.setFormatter(formatter_stream)  # 将渠道与实例日志器绑定
            self.addHandler(stream_handler)

        # 创建一个handler，输出到文件file
        if file:
            file_handle = logging.FileHandler(file, mode='a', encoding='utf-8')
            file_handle.setFormatter(formatter_file)
            self.addHandler(file_handle)

        # 创建一个handler，输出到文件file，记录详细的debug信息
        if debug_file:
            debug_file_handle = logging.FileHandler(debug_file, mode='a', encoding='utf-8')
            debug_file_handle.setFormatter(formatter_debug_file)
            self.addHandler(debug_file_handle)

        # 创建一个handler，按日志文件大小分割
        if max_bytes:
            formatter_ = logging.Formatter(fmt='%(asctime)s %(name)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S")
            formatter_time = handlers.RotatingFileHandler(filename='日志_分割.txt', encoding='utf-8',
                                                          maxBytes=max_bytes, backupCount=back_count)
            formatter_time.setLevel(level)
            formatter_time.setFormatter(formatter_)
            self.addHandler(formatter_time)

        # 创建一个handler，按指定周期分割日志
        if when:
            pass


if __name__ == '__main__':
    pass
