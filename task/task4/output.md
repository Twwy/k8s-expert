从调试输出中可以看到，Helm 安装失败的原因是 Kubernetes 集群不可达。具体错误信息是：

```
Error: INSTALLATION FAILED: Kubernetes cluster unreachable: Get "http://localhost:8080/version": dial tcp [::1]:8080: connect: connection refused
```

这表明 Helm 试图连接到本地的 Kubernetes API 服务器（默认地址为 `http://localhost:8080`），但连接被拒绝了。这通常意味着 Kubernetes 集群没有运行，或者 API 服务器的地址和端口配置不正确。

要解决这个问题，请确保以下几点：
1. **Kubernetes 集群正在运行**：如果您使用的是 Minikube 或其他本地 Kubernetes 集群，请确保它已经启动。
2. **Kubernetes 配置文件 (`kubeconfig`) 正确设置**：请确保您的 `kubeconfig` 文件指向正确的集群，并且您有权限访问该集群。
3. **环境变量 `KUBECONFIG` 正确设置**：如果您的 `kubeconfig` 文件不在默认位置（通常是 `~/.kube/config`），请确保设置了 `KUBECONFIG` 环境变量。

您可以尝试以下步骤来检查和解决问题：

1. **检查 Kubernetes 集群状态**：
   ```sh
   kubectl cluster-info
   ```

2. **验证 `kubeconfig` 文件**：
   ```sh
   kubectl config view
   ```

如果您还没有安装 `kubectl`，可以使用以下命令安装：
```sh
apk add kubectl
```

请您先检查并确保 Kubernetes 集群正在运行并且配置正确。如果需要进一步的帮助，请告诉我。