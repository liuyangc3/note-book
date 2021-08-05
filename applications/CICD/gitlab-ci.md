# script


## yaml format basic

Block Style Indicator:
- literal style,  indicated by a pipe (`|`)
- folded style, indicated by a right angle bracket (`>`)


```yaml
example: >
··Several lines of text,\n
··with some "quotes" of various 'types',\n
··and also a blank line:\n
··\n
··plus another line at the end.\n
··\n


# Result
Several lines of text, with some "quotes" of various 'types', and also a blank line:\n
plus another line at the end.\n
```

```yaml
example: |
··Several lines of text,\n
··with some "quotes" of various 'types',\n
··and also a blank line:\n
··\n
··plus another line at the end.\n
··\n

# Result
Several lines of text,\n
with some "quotes" of various 'types',\n
and also a blank line:\n
\n
plus another line at the end.\n
```

`-`  after block Style Indicator means `No newline at end` (strip)

- `>-`
- `|-`

example
```yaml
job:
  script:
    - |
      cat << EOF > /kaniko/.docker/config.json
      {  
        "credsStore": "ecr-login"
      }
      EOF
    - >
      /kaniko/executor
        --context $CI_PROJECT_DIR
        --dockerfile Dockerfile
        --destination "701613234364.dkr.ecr.ap-east-1.amazonaws.com/hello-world:$APP_VERSION"
    - >-
      curl -s -H "PRIVATE-TOKEN: ${API_TOKEN}" ${MERGE_REQUEST_API}/changes |
      jq -r '.changes[].new_path' | sh .gitlab/workspace.sh > workspace.env
```


# cache and artifacts
## share changes between stage
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
