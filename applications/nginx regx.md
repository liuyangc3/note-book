# nginx location 正则指南
语法格式：
```
location [ = | ~ | ~* | ^~ | @ ] uri { ... }
```
## 前缀

`~`表示大小写相关

`~*`表示大小写无关

`^~`表示匹配到普通表达式后停止正则表达式的匹配

`=` 表示严格精确匹配
## uri表达式

uri的分为普通表达式和正则表达式

其中带有前缀 `~` 和 `~*`的uri是正则表达式

而带有前缀`=`、`^~`、`@`和没有任何前缀的uri是普通表达式

普通表达式中会忽略正则写法

## HTTP请求匹配规则
对于一个特定的 HTTP 请求,uri是url中除去域名的部分。

例如一个HTTP请求的url是http://wiki.dbn.cn/Nginx/regex, uri就是`/Nginx/regex`

那么 Nginx location 如何匹配rui呢?

匹配规则是：先匹配`普通表达式`,再匹配`正则表达式`,如果`正则表达式`没有匹配结果，那么就使用`普通表达式` 的匹配结果。

我们先看看多个`普通表达式`直接是如何匹配的

首先普通表达式的匹配,跟Nginx配置文件的编写顺序是无关的,匹配方式是最大前缀匹配。

举个例子,假设访问的uri是`/prefix/mid/some.html`

现在有两个location满足:
```
location /prefix {
    [configure A]
    }

location /prefix/mid/ {
    [configure B]
    }
```
最终Nginx会执行第二行的代码命令，因为`/prefix/mid/`相比于`/prefix`更符合最大前缀原则

普通表达式匹配到结果后,Nginx还需要检查正则表达式。如果继续搜索的正则表达式也有匹配上的，那么就使用正则表达式后面的代码块。

例如访问的uri是`/prefix/mid/some.html`

而 location 的配置是
```
location /prefix {
    [configure A]
    }

location /prefix/mid/ {
    [configure B]
    }

location ~ /prefix/mid/.*\.html {
    [configure C]
    }
```
首先先进性普通匹配,那么根据最大前缀原则,Nginx会匹配到第二个location。

然后Nginx会发现还有一个正则匹配,于是进行正则匹配,这里的url的格式刚好被正则匹配规则匹配到,所以Nginx会执行正则匹配的代码块,即`[configure C]`

注意：多个正则location匹配原则是按照配置文件的顺序进行的,并且只要匹配到一条正则location，就不再考虑后面的。

当然你可以让Nginx进行普通匹配后终止正则匹配

通过在普通匹配前面加上`^~` 或者`=`会终止正则匹配
