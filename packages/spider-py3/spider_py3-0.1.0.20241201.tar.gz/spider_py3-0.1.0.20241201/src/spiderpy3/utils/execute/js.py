import execjs
import py_mini_racer
from typing import Optional, Tuple, Any


def execute_js_code_by_execjs(
        js_code: Optional[str] = None,
        js_file_path: Optional[str] = None,
        func_name: Optional[str] = None,
        func_args: Optional[Tuple[Any, ...]] = None) -> Any:
    if js_code is None and js_file_path is None:
        raise ValueError(f"js_code：{js_code}，js_file_path：{js_file_path} 不能同时为 None ！")
    if js_file_path is not None:
        with open(js_file_path, "r", encoding="utf-8") as f:
            js_code = f.read()
    ctx = execjs.compile(js_code)
    if func_name is None:
        result = ctx.eval(js_code)
    else:
        if func_args is None:
            func_args = tuple()
        result = ctx.call(func_name, *func_args)
    return result


def execute_js_code_by_py_mini_racer(
        js_code: Optional[str] = None,
        js_file_path: Optional[str] = None,
        func_name: Optional[str] = None,
        func_args: Optional[Tuple[Any, ...]] = None) -> Any:
    if js_code is None and js_file_path is None:
        raise ValueError(f"js_code：{js_code}，js_file_path：{js_file_path} 不能同时为 None ！")
    if js_file_path is not None:
        with open(js_file_path, "r", encoding="utf-8") as f:
            js_code = f.read()
    ctx = py_mini_racer.MiniRacer()
    if func_name is None:
        result = ctx.eval(js_code)
    else:
        ctx.eval(js_code)
        if func_args is None:
            func_args = tuple()
        result = ctx.call(func_name, *func_args)
    return result
