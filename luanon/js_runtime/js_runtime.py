"""
    Tác giả: GnU
    Ngày tạo: 11/14/2023
    ©2023 LuaNonTeam
"""

import os
import json
import queue
import base64
import signal
import string
import threading
import traceback
import subprocess

from .exception import PyError, NodeJsError


class JSRuntime:

    def __init__(self, filename: str = "") -> None:
        # Replace để đảm bảo cái này không bị lỗi prefix \ và /
        filename = filename or os.path.abspath(__file__.replace("js_runtime.py", "js_runtime.js"))
        self._node = subprocess.Popen(
            ["node", filename],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="UTF-8",
            text=True
        )
        self._lock_event = threading.Lock()
        self._stop_event = threading.Event()
        self._queue = queue.Queue()

    def __enter__(self) -> "JSRuntime":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        if self._node and self._node.poll() is None:
            os.kill(self._node.pid, signal.SIGINT)
            self._node.wait()
        if self._lock_event.locked():
            self._lock_event.release()
        self._stop_event.set()
        self._queue.put(None)

    @staticmethod
    def _create_function_call(function_name: str, *args: any) -> str:
        if not function_name.strip():
            return ""

        js_args = []

        for arg in args:
            match arg:
                case bool():
                    js_args.append(str(arg).lower())
                case int():
                    js_args.append(str(arg))
                case _:
                    js_args.append(f"`{arg}`")

        return f"{function_name}({', '.join(js_args)})"

    def eval(self, command: str, timeout: int = 30) -> tuple[any, any, any]:
        with self._lock_event:
            # Encode command để khỏi xử lý \n hay ' hay " gì đó
            data = json.dumps({"command": command})
            data = base64.b64encode(data.encode()).decode()
            self._node.stdin.write(f"{data}\n")
            self._node.stdin.flush()

            while not self._queue.empty():
                try:
                    self._queue.get_nowait()
                except queue.Empty:
                    continue

            def get_result() -> None:
                while not self._stop_event.is_set():
                    try:

                        _result = ""
                        _read_flag = False
                        _reading_flag = False
                        while True:
                            r = self._node.stdout.read(1).strip()
                            if not _read_flag:
                                if r == "-":
                                    _read_flag = True
                            else:
                                if r in [
                                    *list(string.ascii_lowercase),
                                    *list(string.ascii_uppercase),
                                    *list(string.digits),
                                    "+",
                                    "/",
                                    "="
                                ]:
                                    _result += r
                                    _reading_flag = True
                                else:
                                    if _reading_flag and r == "-":
                                        break
                        output = base64.b64decode(_result.encode()).decode()
                        output = json.loads(output)
                        if output:
                            self._queue.put(tuple(output.values()))
                        else:
                            self._queue.put(("", "PyError: Kết quả trả về là rỗng"))
                    except json.decoder.JSONDecodeError:
                        self._queue.put(("", f"PyError: {traceback.format_exc()}"))
                    return

            dont_call_this_again = threading.Thread(target=get_result, daemon=True)
            dont_call_this_again.start()

            try:
                result = self._queue.get(timeout=timeout)
            except queue.Empty:
                result = "", "PyError: Hết thời gian chạy lệnh"
            if result[1]:
                error = result[1]
                if "PyError" in error:
                    raise PyError(error.split(":", 1)[-1].strip())
                if "NodeError" in error:
                    raise NodeJsError(error.split(":", 1)[-1].strip())
            # Cái dòng chết tiệt này tốn 3 ngày để fix
            # Vì lý do chết tiệt gì đó mà hàm set() lại không hoạt động
            self._stop_event.clear()
            return result

    def call(self, function_name: str, *args: any, timeout: int = 30) -> tuple[any, any, any]:
        return self.eval(self._create_function_call(function_name, *args), timeout)
