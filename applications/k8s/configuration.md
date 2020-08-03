declarative-application-management

https://github.com/kubernetes/community/blob/master/contributors/design-proposals/architecture/declarative-application-management.md

Parameterization solutions are easy to implement and to use at small scale, but parameterized templates tend to become complex and difficult to maintain. Syntax-oblivious macro substitution (e.g., sed, jinja, envsubst) can be fragile, and parameter substitution sites generally have to be identified manually, which is tedious and error-prone, especially for the most common use cases, such as resource name prefixing.

can not easily find out which part of YAML should be changed later, so **everything gets parameterized**.


Reconcile 

https://myslide.cn/slides/9331

https://coreos.com/kubernetes/docs/latest/replication-controller.html#the-reconciliation-loop-in-detail


tools:
- helm
- kustomize
- jsonnet/ksonnet-lib

https://gravitational.com/blog/kubernetes-kustomize-kep-kerfuffle/

https://blog.argoproj.io/the-state-of-kubernetes-configuration-management-d8b06c1205
