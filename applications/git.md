# Rebase

Must rebase before commit

## Configuring Your Remotes

rebase check your remote status，now your origin is forked from target：
```console
$ git remote -v
origin  git@github.com:YOUR_GITHUB_USERNAME/terraform-provider-alicloud.git (fetch)
origin  git@github.com:YOUR_GITHUB_USERNAME/terraform-provider-alicloud.git (push)
```

add target repo into remote， name it "alicloud"
```console
$ git remote add alicloud https://github.com/alibaba/terraform-provider-alicloud.git

$ git remote -v
origin  git@github.com:YOUR_GITHUB_USERNAME/terraform-provider-alicloud.git (fetch)
origin  git@github.com:YOUR_GITHUB_USERNAME/terraform-provider-alicloud.git (push)
alicloud  https://github.com/terraform-providers/terraform-provider-alicloud.git (fetch)
alicloud  https://github.com/terraform-providers/terraform-provider-alicloud.git (push)
```
check remote again
```
$ git status
On branch YOUR_BRANCH
Your branch is up-to-date with 'origin/YOUR_BRANCH'.
nothing to commit, working tree clean
```

## Rebasing Your Branch

rebase when you added remote and finish commit:
```console
$ git pull --rebase alicloud master
```

if got conflics, fix conflic go on rebase, then check again:
```console
$ git status
On branch YOUR_BRANCH
Your branch and 'origin/YOUR_BRANCH' have diverged,
and have 4 and 1 different commits each, respectively.
  (use "git pull" to merge the remote branch into yours)
nothing to commit, working tree clean
```

## Uploading Your Code

push after rebase, you can add -f or --force to force push.
```console
$ git push origin <your branch>
```


## Submitting Your Pull Request

add some comment in you PR

## Updating Your Pull Request

if you need fix your code after review, firest redraw you last commit：

```console
$ git reset HEAD^1
Unstaged changes after reset:
******
```

then stash, and use rebase to pull the latest code to avoid conflics:

```console
$ git stash
Saved working directory and index state WIP on YOUR_BRANH: *******
HEAD is now at *******

# rebase to pull latest code
$ git pull --rebase alicloud master
```

after rebase，pump out stash code：

```console
$ git stash pop
On branch YOUR_BRANCH
Changes not staged for commit:
*****
```
then fix your code deponds on review. commmit rebase and push again.
