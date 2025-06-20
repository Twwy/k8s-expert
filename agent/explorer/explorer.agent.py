#!/usr/bin/env python3

import os
import sys
import tempfile
import yaml
import json
from openai import OpenAI
from agitops.util import run_command
from agitops.tool import ToolHandler

class ExecutorAgent():
    sys_prompt = "你是一个任务专家"
    ask_prompt = """
<requirement>中是用户提出需求，你为了完成这个需求，你会提出什么问题。请使用JSON格式返回。
返回JSON必须包含字段:
- question 问题
- answer_deliverable 答案交付物，使用自然语言描述，比如包含什么的一个文件等
- thought 思考过程
"""

    def __init__(self, conf_path):
        # /gitops.yaml
        # llm_model: qwen-max
        # llm_api_url: http://
        # llm_api_key: *****
        # work_root_path: *
        # task_name: *

        if os.path.exists(conf_path):
            h = open(conf_path, "r")
            conf_yaml = h.read()
            h.close()
            print(f"[{conf_path}]")
            print(conf_yaml)
            self.conf = yaml.safe_load(conf_yaml)
        else:
            print(f"not found {conf_path}")
            sys.exit(1)

        conf_keys = ["llm_model", "llm_api_url", "llm_api_key"]
        for conf_key in conf_keys:
            if conf_key not in self.conf:
                print(f"not found {conf_key} in {conf_path}")
                sys.exit(1)

        # self.workspace_path = os.path.join(self.conf["work_root_path"], "workspace")

        # if os.path.isfile(self.workspace_path):
        #     os.remove(self.workspace_path)
        #     os.makedirs(self.workspace_path, exist_ok=True)
        #     # 存放一个文件，避免第一轮没有文件
        #     with open(os.path.join(self.workspace_path, ".gitignore"), 'w') as f:
        #         pass 

        # self.toolHandler = ToolHandler({"bash": "bash.py"})

        self.llm_client = OpenAI(
            api_key=self.conf["llm_api_key"],
            base_url=self.conf["llm_api_url"],
        )

    def ask(self, question):
        messages = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": f"<requirement>{question}</requirement>{self.ask_prompt}"}]

        completion = self.llm_client.chat.completions.create(
            model=self.conf["llm_model"],
            messages=messages
        ).to_dict()

        print(json.dumps(completion, indent=4, ensure_ascii=False))


    def reslove(self, question):
        pass


if __name__ == "__main__":

    agent = ExecutorAgent("/etc/gitops.yaml")

    agent.ask("帮我看一下今天aliyun有什么新闻")

    # next_loop = True
    # count = 0
    # while next_loop:
    #     if count > 30:
    #         print("max loop 30")
    #         sys.exit(1)
    #     count += 1
    #     print(f"\nthought loop: {count}", flush=True)
    #     next_loop = agent.run()