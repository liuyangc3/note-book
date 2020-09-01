declarative-application-management

https://github.com/kubernetes/community/blob/master/contributors/design-proposals/architecture/declarative-application-management.md

Parameterization solutions are easy to implement and to use at small scale, but parameterized templates tend to become complex and difficult to maintain. Syntax-oblivious macro substitution (e.g., sed, jinja, envsubst) can be fragile, and parameter substitution sites generally have to be identified manually, which is tedious and error-prone, especially for the most common use cases, such as resource name prefixing.

can not easily find out which part of YAML should be changed later, so **everything gets parameterized**.


Reconcile 

https://myslide.cn/slides/9331

https://coreos.com/kubernetes/docs/latest/replication-controller.html#the-reconciliation-loop-in-detail



Configuration reconciliation ([aka kubectl apply](https://github.com/kubernetes/kubernetes/issues/1702))

> Once user have generated a set of API objects, it should be possible to perform a number of management operations on them, such as creation, update, or even deletion. Creation and update are performed via a reconciliation process.

https://kubectl.docs.kubernetes.io/pages/kubectl_book/resources_and_controllers.html

> Controllers do not Reconcile events, rather they Reconcile the expected cluster state to the observed cluster state at the time Reconcile is run.

> Because Controllers don't respond to individual Events, but instead Reconcile the state of the system at the time that Reconcile is run, changes from several different events may be observed and Reconciled together. This is referred to as a Level Based system, whereas a system that responds to each event individually would be referred to as an Edge Based system.


tools:
- helm
- kustomize
- jsonnet/ksonnet-lib

https://gravitational.com/blog/kubernetes-kustomize-kep-kerfuffle/

https://blog.argoproj.io/the-state-of-kubernetes-configuration-management-d8b06c1205

https://blog.stack-labs.com/code/kustomize-101/

override vs templating
1. only can override parameterized config, and which part should be parameterized? need learn helm chart vars first begain to write yaml.
2. DSL in go is complicated for hunman reading and writing. 

1. You can override any part in kustomize
2. configMap hash-suffix if deployment not changed
3. good for gitops
