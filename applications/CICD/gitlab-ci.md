

# share changes between stage
```yaml
before:
  stage: before
  script:
    # do somechanges in repo files
    - echo "hello" > test

after:
  stage: after
  script:
    # by default content of test will not change
    - cat test
```

use cache
```yaml
cache:
  untracked: true # used when changed files are not in repo
  paths:
    - test

before:
  stage: before
  script:
    - echo "hello" > test

after:
  stage: after
  script:
    # output will be hello
    - cat test
```
