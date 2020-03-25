https://kubernetes.io/docs/setup/learning-environment/minikube/
```bash
brew install hyperkit
brew install minikube
minikube start --vm-driver=hyperkit --kubernetes-version v1.17.0

# work with the local Docker daemon on your Mac/Linux host
minikube docker-env
```

