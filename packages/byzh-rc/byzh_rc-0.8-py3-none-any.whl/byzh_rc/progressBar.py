import sys
import time

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

class bProgressBar:
    def __init__(self, total, prefix='Processing', suffix='', length=20, fill='█'):
        '''
        类似tqdm的进度条
        :param total: 总数
        :param prefix: 前缀
        :param suffix: 后缀
        :param length: 进度条长度(字符)
        :param fill: 填充字符
        '''
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.start_time = 0
        self.current = 0

    def _format_time(self, seconds):
        """将秒数转换为 mm:ss 格式"""
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f'{minutes:02}:{seconds:02}'

    def update(self, n, color=BLUE, prefix=None, suffix=None):
        if self.current == 0:
            self.start_time = time.time()
        if prefix is not None:
            self.prefix = prefix
        if suffix is not None:
            self.suffix = suffix

        self.current += n
        filled_length = int(self.length * self.current // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        elapsed_time = time.time() - self.start_time
        estimated_time = elapsed_time / self.current * (self.total - self.current) if self.current > 0 else 0
        speed = self.current / elapsed_time if elapsed_time > 0 else 0  # 每秒处理的项数

        elapsed_str = self._format_time(elapsed_time)
        estimated_str = self._format_time(estimated_time)

        sys.stdout.write(f'\r{color}{self.prefix} |{bar}| {self.current}/{self.total} -> {elapsed_str}<{estimated_str} -> {speed:.1f} it/s | {self.suffix}{RESET}')
        sys.stdout.flush()

        if self.current == self.total:
            sys.stdout.write('\n')
            sys.stdout.flush()

