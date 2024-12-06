import threading
import time
import atexit

RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"

class bLogger:
    def __init__(self, file=None, ifTime=False):
        '''
        :param file: 日志保存路径
        :param ifTime: 是否输出时间
        '''
        self.file = file
        self.ifTime = ifTime
        self.f = None
        if self.file:
            self.f = open(self.file, "a", encoding="utf-8")

    def setFile(self, file, ifTime=False):
        if self.f:
            self.f.close()
        self.file = file
        self.ifTime = ifTime
        self.f = open(self.file, "a", encoding="utf-8")

    def clearFile(self):
        assert self.f is not None, "请先调用setFile方法"
        self.f.close()
        self.f = open(self.file, 'w', encoding="utf-8")

    def closeFile(self):
        if self.f:
            self.f.close()
            self.f = None

    def toCmd(self, string):
        print(BLUE + string + RESET)

    def toFile(self, string):
        assert self.f is not None, "请先调用setFile方法"
        if self.ifTime:
            t = time.strftime("%Y-%m-%d %H:%M:%S ##### ", time.localtime())
            self.f.write(t)
        self.f.write(string)
        self.f.write("\n")
        self.f.flush()

    def toBoth(self, string):
        self.toFile(string)
        self.toCmd(string)

class bGlobalLogger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    # 初始化
                    cls._instance.file = None
                    cls._instance.f = None
                    cls._instance.ifTime = False
                    atexit.register(cls._instance.closeFile)  # 注册关闭方法
        return cls._instance

    @classmethod
    def setFile(cls, file, ifTime=False):
        cls()
        cls._instance.ifTime = ifTime
        cls._instance.file = file
        cls._instance.f = open(cls._instance.file, "a", encoding="utf-8")

    @classmethod
    def clearFile(cls):
        cls()
        assert cls._instance.f is not None, "请先调用setFile方法"
        cls._instance.f.close()
        cls._instance.f = open(cls._instance.file, 'w', encoding="utf-8")

    @classmethod
    def closeFile(cls):
        if cls._instance.f:
            cls._instance.f.close()
            cls._instance.f = None

    @classmethod
    def toCmd(cls, string):
        cls()
        print(string)

    @classmethod
    def toFile(cls, string):
        cls()
        assert cls._instance.f is not None, "请先调用setFile方法"
        if  cls._instance.ifTime:
            t = time.strftime("%Y-%m-%d %H:%M:%S ##### ", time.localtime())
            cls._instance.f.write(t)
        cls._instance.f.write(string)
        cls._instance.f.write("\n")
        cls._instance.f.flush()

    @classmethod
    def toBoth(cls, string):
        cls()
        cls.toFile(string)
        cls.toCmd(string)
