https://cloud.google.com/apis/desgin

# 面向资源
REST API 是指一组`独立`的`可寻址`的资源,资源通过资源名称引用,通过一组方法变更.

Google REST API 的方法是 `List`,`Get`,`Create`,`Update`, `Delete`
和一些定制化方法

## 设计流程
- 确定一个API提供什么类型的资源
- 确定资源之间的关系
- 基于类型和关系决定资源名称的格式
- 决定资源 schemas
- 最小方法集合附加到资源上

## 资源
资源模型是树形,节点要么是资源要么是一组资源,方便起见一组资源称作集合

- 集合是`同一类型`资源的list
- 资源拥有状态, 0个或多个子资源.

反模式
```json
[
  "p1": {"id": "p1", "name": "Ane", "age": 21},
  "p2": {"id": "p2", "name": "Bob", "age": 20}
]
```

## Method
`List`,`Get`,`Create`,`Update`, `Delete` 这几个方法`应该`映射到 HTTP method 上,
自定义方法`可以`使用, 满足传统RPC API, 例如数据库事务和数据分析.


## 例子
Gmail API

一个用户有
- 一个 message 集合
- 一个 thread 集合
- 一个 labels 集合
- 一个 history 集合
- 一个 profile 资源
- 一个 settings 资源

API 设计

服务 gmail.googleapis.com

用户集合 users/:uid
```json
[
  // user resource
  {
    messages: [ // message ...],
    threads:  [ // thread ...],
    labels:   [ // label ...],
    history:  [ // history ...],
    profile:  { // profile },
    settings: { // settings } 
  }
]
```
资源名称设计
```json
users/:uid
users/:uid/messages/:msgid
users/:uid/threads/:tid
...
users/:uid/profile
users/:uid/settings
```

# 资源名称
资源是有名称的实体, 每个资源`必须`有`唯一`资源名称, 资源名称由
一个自己的ID,任意父资源的IDs,API服务名组成.


```json
#服务名      #集合ID      #资源ID         #资源ID     #资源ID
mail.apis   /users    /user@example   /settings   /customForm 
```
这样 url 通过 split('/')[n], 通过n可以访问层级.

一个服务名可以是DNS域名下面,也可以是单独一个域名(微服务)

## 资源ID
资源ID`可以` 使用用 '/'
```json
#集合ID      #资源ID
/files    /source/py/parser.py
```
资源ID `必须`在文档中指出是谁指定的,例如 服务端,客户端或者其他.在上面的文件资源ID
是客户端指定的, 而用户ID是服务端指定的.

## 集合ID

集合ID必须满足下面要求
- `必须`是合法的语言的identfiers
- `必须`是开头小写复数单词的驼峰格式,单词如果没有复数形式,例如`weather`,`应该`使用单数形式单词
- `必须`是明确的简洁的英文单词


## 资源名称 vs URL
可以直接转成URL, `必须`使用https协议,在名称的`前面`加上主版本号

## 资源名称作为字符串
`必须`使用普通字符串, `应该`可以向通文件路径一样被处理,例如不支持%-编码






