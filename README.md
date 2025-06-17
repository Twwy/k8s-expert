```
[
    {
        "title": "检查安装包完整性",
        "description": "确认从给定URL下载的sreworks-0.1.1.tgz文件是否完整无损坏。",
        "executor": "browser",
        "id": "task1",
        "result": "已经从指定URL下载sreworks-0.1.1.tgz文件并计算其SHA256校验和。这是计算得到的SHA256值：{stdout}。请提供官方的SHA256值以验证文件的完整性。",
        "finish": true
    },
    {
        "title": "解压tgz文件",
        "description": "将sreworks-0.1.1.tgz文件解压到指定目录，以便查看和修改内部文件。",
        "executor": "explorer",
        "id": "task2"
    },
    {
        "title": "定位错误配置文件",
        "description": "找到并打开sreworks/charts/appmanager/templates/server-configmap.yaml文件，准备进行编辑。",
        "executor": "explorer",
        "id": "task3"
    },
    {
        "title": "修改配置文件",
        "description": "在server-configmap.yaml文件中定位到第36行附近，根据错误提示添加或更新appmanager.server.jwtSecretKey的值。",
        "executor": "explorer",
        "id": "task4"
    },
    {
        "title": "重新打包tgz",
        "description": "对修改后的文件重新打包为tgz格式，确保所有更改被正确包含。",
        "executor": "explorer",
        "id": "task5"
    },
    {
        "title": "重新尝试安装",
        "description": "使用更新后的tgz包重新执行安装命令，并检查是否解决了之前遇到的问题。",
        "executor": "explorer",
        "id": "task6"
    }
]
```
