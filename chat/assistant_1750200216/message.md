根据你提供的信息，你在尝试安装 `sreworks-0.1.1.tgz` 时遇到了一个错误。具体错误信息是：

```
Error: execution error at (sreworks/charts/appmanager/templates/server-configmap.yaml:36:32): appmanager.server.jwtSecretKey is required Use --debug flag to render out invalid YAML
```

这个错误提示表明在 `server-configmap.yaml` 文件的第 36 行第 32 列处，缺少了一个必需的配置项 `appmanager.server.jwtSecretKey`。

### 解决方案

1. **检查 Helm Chart 的值文件**：
   确保你的 Helm Chart 值文件（通常是 `values.yaml`）中包含了 `appmanager.server.jwtSecretKey` 的配置。如果没有，你需要添加这个配置项。

   ```yaml
   appmanager:
     server:
       jwtSecretKey: "your-secret-key-here"
   ```

2. **使用 `--set` 参数传递值**：
   如果你不想修改 `values.yaml` 文件，可以在安装时通过 `--set` 参数传递这个值。

   ```sh
   helm install sreworks https://abm-mind-server.oss-cn-zhangjiakou.aliyuncs.com/sreworks-0.1.1.tgz --set appmanager.server.jwtSecretKey="your-secret-key-here"
   ```

3. **调试模式**：
   如果你仍然遇到问题，可以使用 `--debug` 标志来查看更详细的错误信息，这可能会帮助你更好地理解问题所在。

   ```sh
   helm install sreworks https://abm-mind-server.oss-cn-zhangjiakou.aliyuncs.com/sreworks-0.1.1.tgz --debug
   ```

### 总结

本次任务的主要问题是由于缺少 `appmanager.server.jwtSecretKey` 配置项导致的安装失败。你可以通过在 `values.yaml` 中添加该配置项或在安装时使用 `--set` 参数来解决这个问题。如果需要进一步调试，可以使用 `--debug` 标志来获取更多详细信息。