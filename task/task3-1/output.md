安装过程中遇到了一个新的错误，提示 Kubernetes 集群无法访问。具体来说，Helm 尝试通过 `http://localhost:8080/version` 访问集群的 API 服务器，但连接被拒绝了。这通常意味着当前环境没有配置好与 Kubernetes 集群的连接，或者集群没有运行在本地。

为了进一步诊断这个问题，我们需要检查以下几个方面：

1. **Kubernetes 配置**：确保 `kubectl` 和 Helm 使用的是正确的 kubeconfig 文件。
2. **Kubernetes 集群状态**：确认 Kubernetes 集群正在运行，并且可以从当前机器访问。
3. **网络设置**：检查是否有防火墙或其他网络配置阻止了与集群的通信。

请检查您是否已经设置了 `KUBECONFIG` 环境变量或使用了 `--kubeconfig` 参数来指定正确的 kubeconfig 文件。如果集群是在本地运行的（例如 Minikube 或 Kind），请确保它们已经启动并正在运行。

如果您可以提供更多信息，比如您的 Kubernetes 环境如何设置的，我将能够更好地帮助您解决这个问题。如果没有更多上下文，我们可能需要验证和配置这些设置。