# transformers

transformers allow you change a bit field value in a resource, for example image name, tag, deployment replicas and so on.

Build in transformers:
* **namespace** add a namespace in each resource
* **images** modify the name, tags and/or digest for images
* **commonLabels**/**commonAnnotations** add labels and annotations
* **namePrefix**/**nameSuffix**
* **replicas**
* **vars**
* **valueAdd**
* **nameReferences**

examples
```yaml

namespace: test
namePrefix: pre-
nameSuffix: -suf

images:
- name: container-name
  newName: my-registry/my-image
  newTag: v1
  digest: sha256:24a0c4b4a4c0eb97a1aabb8e29f18e917d05abfe1b7a7c07857230879ce7d3d3
  
replicas:
- name: deployment-name
  count: 5
```
