#!/usr/bin/env python3

import os
import sys
import yaml
import json
from openai import OpenAI
import subprocess
import argparse
# from agitops.util import run_command
# from agitops.tool import ToolHandler

class ToolBash():
    def __init__(self, cwd=None):
        self.cwd = cwd
        self.schema = {
            "type": "function",
            "function": {
                "name": "bash",
                "description": "执行bash脚本",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "要执行的bash命令，可使用工具有w3m"
                        }
                    },
                    "required": ["command"]
                }
            }
        }

    def run(self, arguments):
        print(f"run command: {arguments['command']}")
        process = subprocess.Popen(arguments["command"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, cwd=self.cwd)
        stdout, stderr = process.communicate()
        return f"ret:{process.returncode}\nstdout:\n{stdout}\nstderr:\n{stderr}\n"

class ExecutorAgent():
    sys_prompt = "你是一个任务专家"
    reflect_prompt = """
<requirement>中是用户提出需求，<result>是已经完成的任务结果。如果任务已满足需求，请返回『满足』，否则的话，请为了满足这个需求可能要解决哪些问题，如果有多个问题请选择最重要的一个问题提出来，这个问题不要重复用户的问题，使用JSON格式返回。
返回JSON必须包含字段:
- question 问题
- answer_deliverable 答案交付物清单，使用数组
"""
    resolve_prompt = """
<requirement>中是用户提出需求。<task>是你本次需要完成解决的问题，最终请按照 answer_deliverable 的要求交付结果。
"""

    def __init__(self, conf_path):
        # /gitops.yaml
        # llm_model: qwen-max
        # llm_api_url: http://
        # llm_api_key: *****
        # workspace_path: *
        # task_path: *

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

        conf_keys = ["llm_model", "llm_api_url", "llm_api_key", "workspace_path", "task_path"]
        for conf_key in conf_keys:
            if conf_key not in self.conf:
                print(f"not found {conf_key} in {conf_path}")
                sys.exit(1)

        self.workspace_path = self.conf["workspace_path"]
        self.task_path = self.conf["task_path"]
        with open(os.path.join(self.workspace_path, "input.md"), 'r') as f:
            self.requirement = f.read()

        self.tools = {
            "bash": ToolBash(cwd=self.workspace_path)
        }

        self.llm_client = OpenAI(
            api_key=self.conf["llm_api_key"],
            base_url=self.conf["llm_api_url"],
        )

    def append_stack_task(self, questions):

        stackData = self.read_stack_task()

        stackData["loopCnt"] += 1
        stackLoop = {
            "loop": stackData["loopCnt"],
            "tasks": []
        }

        tasks = []
        for question in questions:

            taskName = f"task{stackData['taskCnt']}"
            task_path = os.path.join(self.task_path, taskName)
            os.makedirs(task_path, exist_ok=True)
            with open(os.path.join(task_path, "input.json"), 'w') as f:
                f.write(json.dumps(question, indent=4, ensure_ascii=False))

            stackData["taskCnt"] += 1

            tasks.append(taskName)
            stackLoop["tasks"].append({
                "question": question,
                "task": taskName,
            })

        stackData["stack"].append(stackLoop)

        with open(os.path.join(self.task_path, "stack.json"), 'w') as f:
            f.write(json.dumps(stackData, indent=4, ensure_ascii=False))

        with open(os.path.join(self.task_path, "todo-task"), 'w') as f:
            f.write("\n".join(tasks)+"\n")
    
    def read_stack_task(self):

        stackData = {
            "loopCnt": 0,
            "taskCnt": 0,
            "stack": []
        }

        if os.path.isfile(self.task_path):
            os.remove(self.task_path)
            os.makedirs(self.task_path, exist_ok=True)

            with open(os.path.join(self.task_path, "stack.json"), 'w') as f:
                f.write(json.dumps(stackData, indent=4, ensure_ascii=False))
        else:
            with open(os.path.join(self.task_path, "stack.json"), 'r') as f:
                stackData = json.loads(f.read())

        return stackData


    def reflect(self, number=3):
        stackData = self.read_stack_task()

        messages = [{"role": "system", "content": self.sys_prompt}]

        taskResult = ""
        if len(stackData["stack"]) > 0:
            lastStack = stackData["stack"][-1]
            for task in lastStack["tasks"]:
                if not os.path.isfile(os.path.join(self.task_path, task["task"], "output.md")):
                    print(f"当前有未完成的任务: {task['task']}")
                    return 
                with open(os.path.join(self.task_path, task["task"], "output.md"), 'r') as f:
                    task["result"] = f.read()
            
            with open(os.path.join(self.task_path, "stack.json"), 'w') as f:
                f.write(json.dumps(stackData, indent=4, ensure_ascii=False))
            taskResult = f"<result>{json.dumps(stackData, ensure_ascii=False)}</result>"
        
        questions = []
        for i in range(number):
            if i == 0:
                messages.append({"role": "user", "content": f"<requirement>{self.requirement}</requirement>{taskResult}{self.reflect_prompt}"})
            else:
                for question in questions:
                    messages.append({"role": "assistant", "content": json.dumps(question, ensure_ascii=False)})
                messages.append({"role": "user", "content": f"除了这个问题，还有其他什么问题吗？不要和前面已有的问题完全重复。请继续使用包含 question,answer_deliverable 的JSON返回"})

            completion = self.llm_client.chat.completions.create(
                model=self.conf["llm_model"],
                messages=messages,
                temperature=1.5
            ).to_dict()

            print(json.dumps(messages, indent=4, ensure_ascii=False))
            print(json.dumps(completion, indent=4, ensure_ascii=False))
            for raw in completion["choices"][0]["message"]["content"].replace("\n\n", "```").split("```"):
                if raw.startswith("json"):
                    raw = raw[4:].strip()
                raw = raw.strip()
                if raw.startswith("{") and raw.endswith("}"):
                    questions.append(json.loads(raw))
            
            if len(questions) >= number:
                break

        self.append_stack_task(questions)
        return questions

    def resolve(self, taskName, max_steps=30):

        with open(os.path.join(self.task_path, taskName, "input.json"), 'r') as f:
            task = json.loads(f.read())

        messages = [
            {"role": "system", "content": self.sys_prompt},
            {"role": "user", "content": f"<requirement>{self.requirement}</requirement><task>{task}</task>{self.resolve_prompt}"}
        ]

        finalAnswer = None

        for i in range(max_steps):
            tools = [t.schema for t in self.tools.values()]
            completion = self.llm_client.chat.completions.create(
                model=self.conf["llm_model"],
                messages=messages,
                tools=tools
            ).to_dict()

            print(json.dumps(completion, indent=4, ensure_ascii=False))

            if completion.get("choices") is not None:
                messageData = completion["choices"][0].get("message")

            if messageData is None:
                raise Exception("no message")

            callThought = messageData.get("content")
            if callThought in [None, ""]:
                callThought = "call tool"

            if messageData.get("tool_calls") is not None:
                messages.append(messageData)
                for tool_call in messageData["tool_calls"]:
                    print(f"call thought: {callThought}")
                    print(f"exec tool {tool_call}")
                    tool_name = tool_call.get("function", {}).get("name")
                    arguments = json.loads(tool_call.get("function", {}).get("arguments", "{}"))
                    tool_result = self.tools[tool_name].run(arguments=arguments)
                    message = {
                        "role": "tool",
                        "tool_call_id": tool_call["id"],
                        "content": tool_result
                    }
                    print(f"exec tool result {message}")
                    messages.append(message)
            else:
                finalAnswer = callThought
                break
        
        with open(os.path.join(self.task_path, taskName, "output.md"), 'w') as f:
            f.write(finalAnswer)

        return finalAnswer



if __name__ == "__main__":

    agent = ExecutorAgent("/etc/gitops.yaml")

    parser = argparse.ArgumentParser(description="智能体")
    subparsers = parser.add_subparsers(dest="command")

    agent_parser = subparsers.add_parser("reflect", help="反思")
    agent_parser = subparsers.add_parser("resolve", help="解决")
    agent_parser.add_argument("--task", help="待解决任务名", required=True)

    args = parser.parse_args()

    if args.command == "reflect":
        agent.reflect()
    elif args.command == "resolve":
        agent.resolve(args.task)
    else:
        print("unknown command")
        sys.exit(1)
