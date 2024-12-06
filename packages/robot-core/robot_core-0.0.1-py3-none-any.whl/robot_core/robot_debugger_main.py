# -*- coding:utf8 -*-
import base64
import codecs
import json
import os
import sys
from io import StringIO
from typing import Optional, Dict

from pydantic import Field, BaseModel
from robot_base import log_util

if sys.stdout.encoding is None or sys.stdout.encoding.upper() != "UTF-8":
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
if sys.stderr.encoding is None or sys.stderr.encoding.upper() != "UTF-8":
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")


class PythonREPL(BaseModel):
    """Simulates a standalone Python REPL."""

    globals: Optional[Dict] = Field(default_factory=dict, alias="_globals")
    locals: Optional[Dict] = Field(default_factory=dict, alias="_locals")

    def run(self, command: str) -> str:
        """Run command with own globals/locals and returns anything printed."""
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        try:
            exec(command, self.globals, self.locals)
            sys.stdout = old_stdout
            output = mystdout.getvalue()
        except Exception as e:
            sys.stdout = old_stdout
            output = str(e)
        return output


def main(input_param):
    robot_raw_inputs = base64.b64decode(input_param).decode("utf-8")
    robot_inputs = json.loads(robot_raw_inputs)

    init_log(robot_inputs)
    args = robot_inputs.get("inputs", {})
    if args is None:
        args = {}

    if robot_inputs["environment_variables"] is not None:
        for env_key, env_value in robot_inputs["environment_variables"].items():
            if env_value is not None:
                os.environ[env_key] = env_value

    _insert_sys_path(robot_inputs["sys_path_list"])
    repl = PythonREPL()
    while True:
        encode_str = input(">>>")
        code = base64.b64decode(encode_str).decode("utf-8")
        result = repl.run(code)
        if result:
            print(result)


def init_log(robot_inputs):
    log_util.Logger(robot_inputs["log_path"], "INFO")


def _insert_sys_path(sys_path_list):
    for sys_path in sys_path_list:
        sys.path.insert(0, sys_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("参数错误", file=sys.stderr)
    else:
        main(sys.argv[1])
