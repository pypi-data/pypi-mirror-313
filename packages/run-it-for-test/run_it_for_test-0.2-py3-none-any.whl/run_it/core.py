from functools import wraps
from typing import Callable, TypeVar, Any, cast
from typing_extensions import ParamSpec
import inspect
import sys

# 定义类型变量
P = ParamSpec("P")  # 用于捕获和保持函数参数的类型信息
R = TypeVar("R")  # 用于捕获和保持函数返回值的类型信息


def run_it(func: Callable[P, R]) -> Callable[P, R]:
    """运行示例装饰器
    标记函数为可执行的示例函数。
    在主程序中会自动执行被标记的函数。

    用法:
        @run_it
        def example() -> None:
            print("This is an example")

        if __name__ == "__main__":
            # 会自动执行所有被 @run_it 标记的函数
            run_examples()
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        return func(*args, **kwargs)

    # 标记这个函数为示例函数
    wrapper._is_example = True  # type: ignore
    return cast(Callable[P, R], wrapper)


def run_examples() -> None:
    """执行当前模块中所有被 @run_it 标记的函数"""
    frame = inspect.currentframe()
    if frame is None:
        return

    caller_frame = frame.f_back
    if caller_frame is None:
        return

    module_name = caller_frame.f_globals.get("__name__")
    if module_name not in sys.modules:
        return

    module = sys.modules[module_name]
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and getattr(obj, "_is_example", False):
            print(f"\n=== Running {name} ===")
            try:
                obj()
            except Exception as e:
                print(f"Error running {name}: {e}")


def is_example(func: Callable) -> bool:
    """检查函数是否被标记为示例"""
    return getattr(func, "_is_example", False)
