在 `server-configmap.yaml` 文件的第36行，我们找到了与错误信息相关的配置项 `APPMANAGER_JWT_SECRET_KEY`。这里使用了Helm模板函数 `required` 来确保 `.Values.server.jwtSecretKey` 的值是必须提供的。当这个值没有被提供时，Helm 会抛出一个错误，提示 `appmanager.server.jwtSecretKey is required`。

要解决这个问题，您需要在安装该 Helm Chart 时提供 `server.jwtSecretKey` 的值。这可以通过在 `values.yaml` 文件中设置该值或者在执行 Helm 安装命令时通过 `--set` 参数来指定它。例如：

- **方法一**：修改 `sreworks/charts/appmanager/values.yaml` 文件，在其中添加或更新如下内容：
  ```yaml
  server:
    jwtSecretKey: "your-unique-secret-key"
  ```
- **方法二**：在执行 Helm 安装命令时直接指定 `server.jwtSecretKey` 的值（替换 `<your-unique-secret-key>` 为实际密钥）：
  ```bash
  helm install [RELEASE_NAME] sreworks-0.1.1.tgz --set server.jwtSecretKey=<your-unique-secret-key>
  ```

请根据您的实际情况选择一种方式来设置 `jwtSecretKey` 值，并重新尝试安装。如果您需要进一步的帮助，请告诉我。