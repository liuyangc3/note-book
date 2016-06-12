

add a new file ${heka_root}/cmake/plugin_loder.cmake, and add your plugin repo. 
```
add_external_plugin(git https://github.com/liuyangc3/test.git master test)
```

build on Linux
----------
```
yum install cmake fakeroot html2text dpkg-devel
rpm -ivh ftp://ftp.pbone.net/mirror/ftp5.gwdg.de/pub/opensuse/repositories/home:/heliochissini/CentOS_CentOS-6/noarch/debhelper-9.20120115ubuntu2-5.2.noarch.rpm
```


build on windows
------------
requirement :
* mingGW
* cmake 
* patch http://gnuwin32.sourceforge.net/downlinks/patch-bin-zip.php




see also
------
http://hekad.readthedocs.io/en/v0.10.0/developing/plugin.html

http://hekad.readthedocs.io/en/v0.10.0/installing.html#build-include-externals
