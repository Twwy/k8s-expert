`server-configmap.yaml` 文件中确实需要 `appmanager.server.jwtSecretKey` 的值。具体来说，该配置项在此文件的第36行被标记为必需（required）。

错误信息指出：`appmanager.server.jwtSecretKey is required`，这意味着在安装过程中必须提供这个值。要解决这个问题，您需要在您的 Helm 安装命令中通过 `--set` 参数设置 `server.jwtSecretKey` 的值，或者在您的自定义 `values.yaml` 文件中指定它。

如果您还没有设置，请使用以下方式之一来设置：

1. **通过 `--set` 参数**：
   ```bash
   helm install sreworks-0.1.1.tgz --set server.jwtSecretKey=your-secret-key
   ```

2. **通过自定义 `values.yaml` 文件**：
   创建或编辑一个名为 `my-values.yaml` 的文件，并添加如下内容：
   ```yaml
   server:
     jwtSecretKey: your-secret-key
   ```
   然后使用这个文件进行安装：
   ```bash
   helm install sreworks-0.1.1.tgz -f my-values.yaml
   ```

请将 `your-secret-key` 替换为您实际的安全密钥。这样应该可以解决安装过程中遇到的问题。