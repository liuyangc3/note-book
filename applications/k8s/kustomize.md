# transformer

transformer allow you change a bit field value in a resource, for example image name, tag, deployment replicas and so on.

Build in transformers:
* **namespace** add a namespace in each resource
* **images** modify the name, tags and/or digest for images
* **commonLabels**/**commonAnnotations** add labels and annotations
* **namePrefix**/**nameSuffix**
* **replicas**
* **vars**
* **valueAdd**

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

## transformer configuration

default transformer has a `FieldSpec` configuatoin
```yaml
group: group # resource gvk 
version: version # resource gvk
kind: kind # resource gvk
path: path/to/the/field # resource spec path that a transformer affect on
create: false # if spec fied not exist create it
```
examples
```yaml
# config.yaml
commonLabels:
- path: metadata/labels
  create: true

- path: spec/selector
  create: true
  version: v1
  kind: Service
  
# kustomization.yaml
resources:
  - ../base

configurations:
  - config.yaml
```
`nameReference`

nameReference is an Kustomize object that holds configurations that point Kustomize to resource references when there are custom resources in play.

`varReference`
