已经按照任务要求完成了以下操作：

1. 在 `sreworks/charts/appmanager/values.yaml` 文件中添加了 `jwtSecretKey` 参数，并设置了一个临时值 `myTempJwtSecretKey1234567890`。
2. 更新了 `sreworks/charts/appmanager/templates/server-configmap.yaml` 文件，在其中添加了 `appmanager.server.jwtSecretKey` 字段，并使用了上述设置的值。

现在您可以尝试重新运行安装命令来检查问题是否已经解决。如果还有其他问题或需要进一步的帮助，请告诉我。下面是更新后的相关文件内容摘要，以供确认：

- `sreworks/charts/appmanager/values.yaml` 中 `jwtSecretKey` 的值：
  ```yaml
  jwtSecretKey: myTempJwtSecretKey1234567890
  ```

- `sreworks/charts/appmanager/templates/server-configmap.yaml` 中新添加的内容：
  ```yaml
  appmanager.server.jwtSecretKey: myTempJwtSecretKey1234567890
  ```

请继续执行您的安装步骤，或者如果您希望我帮助您完成接下来的操作，请告知。