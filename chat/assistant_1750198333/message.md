从你的描述来看，你在尝试安装 `sreworks-0.1.1.tgz` 时遇到了一个错误。具体错误信息是：

```
Error: execution error at (sreworks/charts/appmanager/templates/server-configmap.yaml:36:32): appmanager.server.jwtSecretKey is required
Use --debug flag to render out invalid YAML
```

这个错误提示你缺少了一个必需的配置项 `appmanager.server.jwtSecretKey`。这个密钥通常用于生成和验证 JSON Web Tokens (JWT)，以确保应用的安全性。

### 解决方案

1. **提供 `jwtSecretKey`**:
   你需要在安装过程中提供 `appmanager.server.jwtSecretKey` 的值。你可以通过 Helm 的 `--set` 参数来传递这个值。例如：
   ```sh
   helm install sreworks ./sreworks-0.1.1.tgz --set appmanager.server.jwtSecretKey=your-secure-secret-key
   ```

2. **使用 `values.yaml` 文件**:
   如果你更喜欢使用 `values.yaml` 文件来管理配置，可以在文件中添加或修改以下内容：
   ```yaml
   appmanager:
     server:
       jwtSecretKey: your-secure-secret-key
   ```
   然后使用该文件进行安装：
   ```sh
   helm install sreworks ./sreworks-0.1.1.tgz -f values.yaml
   ```

3. **调试 YAML 文件**:
   如果你想查看具体的 YAML 渲染结果，可以使用 `--debug` 标志来帮助你调试：
   ```sh
   helm install sreworks ./sreworks-0.1.1.tgz --debug
   ```

### 总结

本次任务的主要问题是缺少 `appmanager.server.jwtSecretKey` 配置项。解决方案是通过 Helm 的 `--set` 参数或 `values.yaml` 文件来提供这个值。这样可以解决安装过程中遇到的错误，并顺利完成安装。