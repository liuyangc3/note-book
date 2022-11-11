# Deep Dive into Docker Internals - Union Filesystem

https://martinheinz.dev/blog/44


Working with Docker CLI is very straightforward - you just build, run, inspect, pull and push containers and images, but have you ever wondered how do the internals behind this Docker interface actually work? Behind this simple interface hides a lot of cool technologies and in this article we will explore one of them - the union filesystem - the underlying filesystem behind all the container and image layers...

## #What is Union Filesystem?
Union mount is a type of a filesystem that can create an illusion of merging contents of several directories into one without modifying its original (physical) sources. This can be useful as we might have related sets of files stored in different locations or media, and yet we want to show them in single, merged view. Example of this would be bunch of users' /home directories from remote NFS servers all unioned into single directory or merging split ISO image into single complete one.

Union mount or union filesystem is; however, not the filesystem type, but rather a concept with many implementations. Some of them faster, some simpler, with different goals or with various levels of maturity. So, before we start digging into specifics, let's go through quick overview of some of the more popular implementations available out there:

* UnionFS - Let's start off with the original union filesystem. UnionFS doesn't seem to be actively developed anymore, with its [latest commit](http://git.fsl.cs.sunysb.edu/?p=unionfs-2.6.39.y.git;a=summary) is from August 2014. You can read up a bit more about it on its website at https://unionfs.filesystems.org/.
* aufs - A re-implemenation of original UnionFS that added many new features, but was rejected for merging into mainline Linux kernel. Aufs was default driver for Docker on Ubuntu/Debian but was replaced by OverlayFS (for Linux kernel >4.0). It has some advantages in comparison to other union filesystems which are described in Docker docs page.
* OverlayFS - Next up, OverlayFS which is included in Linux Kernel since 3.18 (26 October 2014). This is the filesystem used by default overlay2 Docker driver (you can verify that with `docker system info | grep Storage`). It generally has better performance then aufs and has some nice features such as page cache sharing.
* ZFS - ZFS is union filesystem created by Sun Microsystems (now Oracle). It has some interesting features like hierarchical checksumming, native handling of snapshots and backup/replication or native data compression and deduplication. However, being maintained by Oracle, it has non-OSS friendly license (CDDL) and therefore cannot be shipped as part of Linux kernel. You could however use the ZFS on Linux (ZoL) project, which is described in Docker docs as healthy and maturing ..., but not ready for production. If you want to try it out, then you can find it here.
* Btrfs - Another option is Btrfs which is joint project of multiple companies - including SUSE, WD or Facebook - published under GPL license and is a part of Linux kernel. Btrfs is a default filesystem of Fedora 33. It also has some useful features such as block-level operations, defragmentation, writeable snapshots and a lot more. If you really want to go through the hassle of switching to non-default storage driver for Docker, then Btrfs with its features and performance might be the way to go.

If you want to explore these drivers in more detail in relation to Docker, you can check out the comparison of drivers in Docker docs. That said, unless you really know what you're doing (at which point you wouldn't be reading this article), then you should just stick with the default overlay2, which will be also used in the rest of this article for demonstrations.

## #But Why?
In the previous section we mentioned some reason why this type of a filesystem might be useful, but why is it a good choice for Docker and containers in general?

Many images that we use to spin up our containers are quite bulky whether it's ubuntu with size of 72MB or nginx with size of 133MB. It would be quite expensive to allocate that much space every time we'd like to create a container from these images. Thanks to union filesystem, Docker only needs to create thin layer on top of the image and rest of it can be shared between all the containers. This also provides the added benefit of reduced start time, as there's no need to copy the image files and data.

Union filesystem also provides isolation, because containers have read-only access to the shared image layers. If they ever need to modify any of the read-only shared files, they use copy-on-write strategy (discussed little later) to copy the content up to their top writable layer where it can be safely modified.

## #How Does It Work?
Now it's time to ask the important question - how does it actually work? From all the things described above, it might seem like the whole union filesystem is some kind of a black magic, but it isn't really the case. Let's start off by explaining how it works in general (non-container) case - let's imagine that we would like to union mount two directories (upper and lower) onto same mount point and have a unioned view of them:
```console
.
├── upper
│   ├── code.py  # Content: `print("Hello Overlay!")`
│   └── script.py
└── lower
    ├── code.py  # Content: `print("This is some code...")`
    └── config.yaml
```
In union mount terminology, these directories are called branches. Each of these branches is assigned precedence. This precedence is used to determine which file will show up in the merged view in case there are files with same name in multiple source branches. Looking at the files and directories above - it's clear that if we try to overlay them, we will create this kind of conflict (code.py file). So, let's try and see what shows up:
```console
~ $ mount -t overlay \
    -o lowerdir=./lower,\
       upperdir=./upper,\
       workdir=./workdir \
    overlay /mnt/merged
~ $ ls /mnt/merged
code.py  config.yaml  script.py

~ $ cat /mnt/merged/code.py
print("Hello Overlay!")
```

In the example above we used mount command with type overlay to combine lower directory (read-only; lower priority) and upper directory (read-write; higher priority) into merged view in /mnt/merged. We also included workdir=./workdir option which serves as place for preparing merged view of lowerdir and upperdir before it's moved to /mnt/merged in atomic action.

Also looking at the output of cat command above, we can see that indeed the contents of the files in upper directory took precedence in merged view.

So, now we know how to merge 2 directories and what happens if there's conflict, but what happens if we try to modify some of the files from merged view? That's where copy-on-write (CoW) comes into play. So, what exactly is it? CoW is an optimization technique where if two callers ask for the same resource, you can give them pointer to the same resource without copying it. Copying becomes necessary only when one of the callers attempts to write to their "copy" - hence the term copy on (first attempt to) write.

In case of union mount that means that when we try to modify shared file (or read-only file), it first gets copied up to the top writeable branch (upperdir) which has higher priority than read-only lower branches (lowerdir). Then - when it's in the writeable branch - it can be safely modified and it's new content will be visible in merged view because the top layer has higher priority.

Last operation that we might want to perform is deletion of files. To perform "deletion", a whiteout file is created in writeable branch to clear the file which we want deleted. This means that the file isn't actually deleted, but rather hidden in the merged view.

We talked a bunch about how union mount works in general, but how does it all relate to Docker and its containers? To connect it all back together, let's look at Docker layered architecture. A sandbox of a container is composed of some image branches - or as we all know them - layers. These layers are the read-only (lowerdir) part of the merged view and the container layer is the thin writeable top (upperdir) part.

Other then this architecture terminology, it's really the same thing - the image layers you pull from registry are lowerdir and when you run a container the upperdir is attached to the top of image layers to provide writeable workspace for your container. Sounds quite straightforward, right? So, let's try it out!

## #Trying It Out
To demonstrate how OverlayFS is used by Docker, we will try emulate how Docker mounts the container and image layers. Before we do this, we first need to clear our workspace and get an image to play with:
```console
~ $ docker image prune -af
...
Total reclaimed space: ...MB
~ $ docker pull nginx
Using default tag: latest
latest: Pulling from library/nginx
a076a628af6f: Pull complete
0732ab25fa22: Pull complete
d7f36f6fe38f: Pull complete
f72584a26f32: Pull complete
7125e4df9063: Pull complete
Digest: sha256:10b8cc432d56da8b61b070f4c7d2543a9ed17c2b23010b43af434fd40e2ca4aa
Status: Downloaded newer image for nginx:latest
docker.io/library/nginx:latest
We have an image (nginx) to play with, so next, let's checkout it's layers. We can inspect image layers by either running docker inspect on the image and checking the GraphDriver fields or by going through /var/lib/docker/overlay2 directory where all image layers are stored. So, let's do both and see what's inside:
~ $ cd /var/lib/docker/overlay2
~ $ ls -l
total 0
drwx------. 4 root root     55 Feb  6 19:19 3d963d191b2101b3406348217f4257d7374aa4b4a73b4a6dd4ab0f365d38dfbd
drwx------. 3 root root     47 Feb  6 19:19 410c05aaa30dd006fc47d8c23ba0d173c6d305e4d93fdc3d9abcad9e78862b46
drwx------. 4 root root     72 Feb  6 19:19 685374e39a6aac7a346963bb51e2fc7b9f5e2bdbb5eac6c76ccdaef807abc25e
brw-------. 1 root root 253, 0 Jan 31 18:15 backingFsBlockDev
drwx------. 4 root root     72 Feb  6 19:19 d487622ece100972afba76fda13f56029dec5ec26ffcf552191f6241e05cab7e
drwx------. 4 root root     72 Feb  6 19:19 fb18be50518ec9b37faf229f254bbb454f7663f1c9c45af9f272829172015505
drwx------. 2 root root    176 Feb  6 19:19 l

~ $ tree 3d963d191b2101b3406348217f4257d7374aa4b4a73b4a6dd4ab0f365d38dfbd/
3d963d191b2101b3406348217f4257d7374aa4b4a73b4a6dd4ab0f365d38dfbd/
├── diff
│   └── docker-entrypoint.d
│       └── 20-envsubst-on-templates.sh
├── link
├── lower
└── work

~ $ docker inspect nginx | jq .[0].GraphDriver.Data
{
  "LowerDir": "/var/lib/docker/overlay2/fb18be50518ec9b37faf229f254bbb454f7663f1c9c45af9f272829172015505/diff:
    /var/lib/docker/overlay2/d487622ece100972afba76fda13f56029dec5ec26ffcf552191f6241e05cab7e/diff:
    /var/lib/docker/overlay2/685374e39a6aac7a346963bb51e2fc7b9f5e2bdbb5eac6c76ccdaef807abc25e/diff:
    /var/lib/docker/overlay2/410c05aaa30dd006fc47d8c23ba0d173c6d305e4d93fdc3d9abcad9e78862b46/diff",
  "MergedDir": "/var/lib/docker/overlay2/3d963d191b2101b3406348217f4257d7374aa4b4a73b4a6dd4ab0f365d38dfbd/merged",
  "UpperDir": "/var/lib/docker/overlay2/3d963d191b2101b3406348217f4257d7374aa4b4a73b4a6dd4ab0f365d38dfbd/diff",
  "WorkDir": "/var/lib/docker/overlay2/3d963d191b2101b3406348217f4257d7374aa4b4a73b4a6dd4ab0f365d38dfbd/work"
}
```
Looking at the output above, it looks quite similar to what we've seen with mount command, right? More specifically:

* LowerDir: Is the directory with read-only image layers separated by colons
* MergedDir: Merged view of all the layers from image and container
* UpperDir: Read-write layer where changes are written
* WorkDir: Working directory used by Linux OverlayFS to prepare merged view
Next, let's go a step further and run a container and inspect its layers:
```console
~ $ docker run -d --name container nginx
~ $ docker inspect container | jq .[0].GraphDriver.Data
{
  "LowerDir": "/var/lib/docker/overlay2/59bcd145c580de3bb3b2b9c6102e4d52d0ddd1ed598e742b3a0e13e261ee6eb4-init/diff:
    /var/lib/docker/overlay2/3d963d191b2101b3406348217f4257d7374aa4b4a73b4a6dd4ab0f365d38dfbd/diff:
    /var/lib/docker/overlay2/fb18be50518ec9b37faf229f254bbb454f7663f1c9c45af9f272829172015505/diff:
    /var/lib/docker/overlay2/d487622ece100972afba76fda13f56029dec5ec26ffcf552191f6241e05cab7e/diff:
    /var/lib/docker/overlay2/685374e39a6aac7a346963bb51e2fc7b9f5e2bdbb5eac6c76ccdaef807abc25e/diff:
    /var/lib/docker/overlay2/410c05aaa30dd006fc47d8c23ba0d173c6d305e4d93fdc3d9abcad9e78862b46/diff",
  "MergedDir": "/var/lib/docker/overlay2/59bcd145c580de3bb3b2b9c6102e4d52d0ddd1ed598e742b3a0e13e261ee6eb4/merged",
  "UpperDir": "/var/lib/docker/overlay2/59bcd145c580de3bb3b2b9c6102e4d52d0ddd1ed598e742b3a0e13e261ee6eb4/diff",
  "WorkDir": "/var/lib/docker/overlay2/59bcd145c580de3bb3b2b9c6102e4d52d0ddd1ed598e742b3a0e13e261ee6eb4/work"
}

~ $ tree -l 3 /var/lib/docker/overlay2/59bcd145c580de3bb3b2b9c6102e4d52d0ddd1ed598e742b3a0e13e261ee6eb4/diff  # The UpperDir
/var/lib/docker/overlay2/59bcd145c580de3bb3b2b9c6102e4d52d0ddd1ed598e742b3a0e13e261ee6eb4/diff
├── etc
│   └── nginx
│       └── conf.d
│           └── default.conf
├── run
│   └── nginx.pid
└── var
    └── cache
        └── nginx
            ├── client_temp
            ├── fastcgi_temp
            ├── proxy_temp
            ├── scgi_temp
            └── uwsgi_temp
```
The above output shows that the same directories that were listed in output of docker inspect nginx earlier as MergedDir, UpperDir and WorkDir (with id 3d963d191b2101b3406348217f4257d7374aa4b4a73b4a6dd4ab0f365d38dfbd) are now part of container's LowerDir. The LowerDir here is composed of all the nginx image layers stacked on top of each other. On top of them is the writeable layer in UpperDir, which contains /etc, /run and /var. Also if we listed the MergedDir above, you would see whole filesystem available to container, including all the content from UpperDir and LowerDir.

Finally, to emulate the behavior of Docker, we can use these same directories to manually create our own merged view:
```console
~ $ mount -t overlay -o \
lowerdir=/var/lib/docker/overlay2/59bcd145c580de3bb3b2b9c6102e4d52d0ddd1ed598e742b3a0e13e261ee6eb4-init/diff:
    /var/lib/docker/overlay2/3d963d191b2101b3406348217f4257d7374aa4b4a73b4a6dd4ab0f365d38dfbd/diff:
    /var/lib/docker/overlay2/fb18be50518ec9b37faf229f254bbb454f7663f1c9c45af9f272829172015505/diff:
    /var/lib/docker/overlay2/d487622ece100972afba76fda13f56029dec5ec26ffcf552191f6241e05cab7e/diff:
    /var/lib/docker/overlay2/685374e39a6aac7a346963bb51e2fc7b9f5e2bdbb5eac6c76ccdaef807abc25e/diff:
    /var/lib/docker/overlay2/410c05aaa30dd006fc47d8c23ba0d173c6d305e4d93fdc3d9abcad9e78862b46/diff,\
upperdir=/var/lib/docker/overlay2/59bcd145c580de3bb3b2b9c6102e4d52d0ddd1ed598e742b3a0e13e261ee6eb4/diff,\
workdir=/var/lib/docker/overlay2/59bcd145c580de3bb3b2b9c6102e4d52d0ddd1ed598e742b3a0e13e261ee6eb4/work \
overlay /mnt/merged

~ $ ls /mnt/merged
bin   dev                  docker-entrypoint.sh  home  lib64  mnt  proc  run   srv  tmp  var
boot  docker-entrypoint.d  etc                   lib   media  opt  root  sbin  sys  usr

~ $ umount overlay
```
Here we just grabbed the values from previous snippet and passed them to appropriate arguments in mount command, only difference is that we used /mnt/merged for the merged view instead of /var/lib/docker/overlay2/.../merged.

And this is really what the whole OverlayFS in Docker boils down to - a single mount command across many stacked layers. Below is a part of the Docker code responsible for this - the substitution of lowerdir=...,upperdir=...,workdir=... values, followed by unix.Mount
```go
// https://github.com/moby/moby/blob/1ef1cc8388165b2b848f9b3f53ec91c87de09f63/daemon/graphdriver/overlay2/overlay.go#L580
opts := fmt.Sprintf("lowerdir=%s,upperdir=%s,workdir=%s", strings.Join(absLowers, ":"), path.Join(dir, "diff"), path.Join(dir, "work"))
mountData := label.FormatMountLabel(opts, mountLabel)
mount := unix.Mount
mountTarget := mergedDir

rootUID, rootGID, err := idtools.GetRootUIDGID(d.uidMaps, d.gidMaps)
// ...
```
## #Conclusion
When looking at Docker interface from the outside, it might seem like a black box with a lot of obscure technologies inside. These technologies - while obscure - are quite interesting and useful, and while you don't need to understand them to use Docker effectively, it's still - in my opinion - a worthwhile effort to learn about them and understand them. Having deeper understanding of the tool makes it easier to make correct decisions - in this case - about performance optimization or security implications. As a bonus it also helps you to discover some cool technology which can have many more use-cases for you in the future.

In this article we've explored just of part of Docker architecture - the filesystem - and there are other parts worth diving into - such as cgroups or Linux namespaces. So, if you liked this article keep an eye out for follow up(s) where we'll dig into those technologies as well. 😉
