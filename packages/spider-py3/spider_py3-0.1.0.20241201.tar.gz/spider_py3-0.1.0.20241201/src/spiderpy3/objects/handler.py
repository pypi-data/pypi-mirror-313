from abc import abstractmethod
from typing import Any

from spiderpy3.objects.object import Object


class Handler(Object):

    @abstractmethod
    def action(self, *args, **kwargs) -> Any:
        pass

    def run_ok_method(self, result: Any) -> Any:
        pass

    def run_error_method(self, e: Exception) -> bool:
        """
        未处理该异常时，需要抛出该异常，那么后续就会打印该异常的堆栈信息；
        已处理该异常时，当返回 True，后续就不会有该异常的日志，当返回 False，后续就会有该异常的日志。

        :param e:
        :return:
        """
        raise e

    def run(self, *args, **kwargs) -> Any:
        try:
            result = self.action(*args, **kwargs)
        except Exception as e:
            try:
                ret = self.run_error_method(e)
            except Exception as e:
                self.logger.exception(e)
            else:
                if ret is False:
                    self.logger.error(e)
        else:
            self.run_ok_method(result)
            return result

    def loop_run(self, *args, **kwargs) -> None:
        run_times = 0
        while True:
            run_times += 1
            self.logger.debug(f"循环运行第{run_times}次开始")
            self.run(*args, **kwargs)
            self.logger.debug(f"循环运行第{run_times}次结束")
