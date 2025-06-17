看起来`~/.kube/config`文件不存在，这意味着当前环境中没有配置Kubernetes集群的访问信息。这可能是导致Helm无法连接到Kubernetes集群的原因。

为了继续解决这个问题，您需要确保您的Kubernetes集群已经启动，并且`kubeconfig`文件已正确配置。以下是一些常见的步骤来设置和配置Kubernetes集群：

### 1. 启动本地Kubernetes集群
如果您使用的是Minikube或Kind等本地Kubernetes集群工具，请确保它们已经启动。例如：
- **Minikube**:
  ```bash
  minikube start
  ```
- **Kind**:
  ```bash
  kind create cluster
  ```

### 2. 配置`kubeconfig`文件
一旦集群启动，您可以使用以下命令来获取`kubeconfig`文件：
- **Minikube**:
  ```bash
  minikube config view
  ```
- **Kind**:
  ```bash
  kind get kubeconfig > ~/.kube/config
  ```

### 3. 设置`KUBECONFIG`环境变量
如果您的`kubeconfig`文件位于非默认位置，请设置`KUBECONFIG`环境变量：
```bash
export KUBECONFIG=/path/to/your/kubeconfig
```

### 4. 检查Kubernetes集群状态
再次检查Kubernetes集群的状态：
```bash
kubectl cluster-info
```

请根据您的实际情况选择合适的步骤来启动和配置Kubernetes集群。如果您已经在其他地方启动了Kubernetes集群并有相应的`kubeconfig`文件，请告诉我该文件的路径，我将帮助您进行进一步的配置。

如果您有任何其他问题或需要进一步的帮助，请随时告诉我！