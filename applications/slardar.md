# init


## 加载 consul
```lua
slardar = require "config" -- global config variable

local ok, init_ok = pcall(consul.init, slardar)
```
配置 config 传入 consul.init， 然后把 consul 的内容写入 config  

```lua
-- consul.init

function _M.init(config)
    
    -- 初始化配置
    local consul = config.consul or {}
    local key_prefix = consul.config_key_prefix or ""
    local consul_cluster = consul.cluster or {}
    local opts = { decode=utils.parse_body, default={} }

    
    
    -- 获取 upstream keys
    -- key_prefix .. upstreams_prefix .. "?keys" 默认情况下为
    -- "config/slardar/http_upstreams?keys"
    local upstream_keys = api.get_kv_blocking(consul_cluster, key_prefix .. upstreams_prefix .. "?keys", opts)
    if not upstream_keys then
        return false
    end
```
get_kv_blocking 是从consul里取kv值


获取到的 upstream_keys 格式应该是 [key1, key2 ...]

```lua
-- consul.init

    -- 遍历 upstream_keys 中所有的 key
    for _, key in ipairs(upstream_keys) do repeat
        -- key_prefix = "config/slardar/"
        -- upstreams_prefix = "http_upstreams"
        local skey = str_sub(key, #key_prefix + #upstreams_prefix + 2)
        
        
        -- 从 consul  http://host:port/v1/kv/<key>?raw 取到 servers 配置
        -- {
        --      "servers": [{"host": "127.0.0.1","port": 8001,"weight": 1,"max_fails": 6,"fail_timeout": 30}]
        --      "keepalive" :
        --      "try": 
        -- }
        local servers = api.get_kv_blocking(consul_cluster, key .. "?raw", opts)
        
        -- 对 servers 进行检查后存入 config
        config[skey]["cluster"] = { 
            servers = servers["servers"],
            keepalive = tonumber(servers["keepalive"]),
            try =  tonumber(servers["try"]),
        }
        
        
        -- fit config.lua format
        for k, v in pairs(servers) do
            -- copy other values
            if k ~= "servers" and k ~= "keepalive" and k ~= "try" then
                config[skey][k] = v
            end
        end
        
        -- 修改 config 的索引
        setmetatable(config, {
            __index = load_config,
        }) 
    end
```

# init_worker
```lua
checkups.prepare_checker(slardar)

-- only one checkups timer is active among all the nginx workers
checkups.create_checker()

mload.create_load_syncer()
```
prepare_checker
```lua
-- prepare_checker(config)

-- 把 config 里的配置都保存到 base.upstream 里
base.upstream.start_time = localtime()
base.upstream.conf_hash = config.global.conf_hash
base.upstream.checkup_timer_interval = config.global.checkup_timer_interval or 5
base.upstream.checkup_timer_overtime = config.global.checkup_timer_overtime or 60
base.upstream.checkups = {}
base.upstream.ups_status_sync_enable = config.global.ups_status_sync_enable
base.upstream.ups_status_timer_interval = config.global.ups_status_timer_interval or 5
base.upstream.checkup_shd_sync_enable = config.global.checkup_shd_sync_enable
base.upstream.shd_config_timer_interval = config.global.shd_config_timer_interval
    or base.upstream.checkup_timer_interval
base.upstream.default_heartbeat_enable = config.global.default_heartbeat_enable


for skey, ups in pairs(config) do
    -- 把 config 里带 cluster 的配置项保存到 base.upstream.checkups
    -- 注意 init 阶段已经将consul里的 servers 配置保存到 config[skey]["cluster"] 中
        if type(ups) == "table" and type(ups.cluster) == "table" then
            base.upstream.checkups[skey] = base.table_dup(ups)
            
            -- extract_servers_from_upstream 抽取servers
            for level, cls in pairs(base.upstream.checkups[skey].cluster) do
                base.extract_servers_from_upstream(skey, cls)
            end
            
            -- 每个skey配置项由workid为0的进程放到共享缓存
            if base.upstream.checkup_shd_sync_enable then
                if shd_config and worker_id then
                    local phase = get_phase()
                    -- if in init_worker phase, only worker 0 can update shm
                    if phase == "init" or
                        phase == "init_worker" and worker_id() == 0 then
                        local key = dyconfig._gen_shd_key(skey)
                        shd_config:set(key, cjson.encode(base.upstream.checkups[skey]))
                    end
                    -- skey 存入 skeys
                    skeys[skey] = 1
end            
            
-- skeys 存入共享缓存
if phase == "init" or phase == "init_worker" and worker_id() == 0 then
    shd_config:set(base.SHD_CONFIG_VERSION_KEY, 0)
    shd_config:set(base.SKEYS_KEY, cjson.encode(skeys))
end
```
create_checker
```lua

```

consul 里 json 格式
127.0.0.1:1995/upstream/node-dev.upyun.com
```
{"servers":[ 
        {"host":"10.0.5.108", "port": 4001, "weight": 1, "max_fails": 1, "fail_timeout": 1},  // node 1
        {"host":"10.0.5.109", "port": 4001, "weight": 1, "max_fails": 1, "fail_timeout": 1}   // node 2
    ], 
 "keepalive": 20,
 "try": 1
}
```






通过 status 主动检查

127.0.0.1:1995/status
```
{"cls:node-dev.upyun.com":[
    [
        {
            "server": "node-dev.upyun.com:10.0.5.108:4001",
            "msg": null,
            "status": "err",
            "lastmodified" : "2016-07-05 16:23:48",
            "fail_num" : 0
        }, // node 1
        {
            "server": "node-dev.upyun.com:10.0.5.109:4001",
            "msg": "connection refuesd",
            "status": "err",
            "lastmodified" : "2016-07-05 16:23:48",
            "fail_num" : 1  // 失败次数
        }  // node  2
    ]
]}
```

## 加载 mload 
```lua
local mload  = require "modules.load"
local ok, init_ok = pcall(mload.init, slardar)
```
mload.init
```lua
-- 从 http://host:port/v1/kv/config/slardar/lua/?keys 取到 script_keys
script_keys = consul.get_script_blocking(consul_cluster, prefix .. "lua/?keys")

-- 从 script_keys 中取到模块名称， 使用 require 加载
for _, key in ipairs(script_keys) do
    local skey = str_sub(key, #prefix + 5)
    if skey ~= "" then
        local ok = pcall(require, skey)
        
        -- 如果 require 失败
        if not ok then
            -- 从 http://host:port/v1/kv/config/<key>?raw 读取代码 
            code = consul.get_script_blocking(consul_cluster, key .. "?raw", true)
            -- 把代码存入ngx share dict
            local ok, err = load_dict:safe_set(CODE_PREFIX .. skey, code)
            
```
```
tab_insert(package.loaders, module_loader)
```

slardar 中不存在的 key 的访问都会通过 consul.load_config 返回
```
setmetatable(slardar, {
    __index = consul.load_config,
})
```
load_config 优先走 share dict， 如果 consul 的配置里没有配置缓存，则发送 http 请求，请求实际的请求地址是
```
http://consul_address:port/v1/kv/<key_prefix>/<key>?raw
```

至此， init 工作结束 


## init worker
```lua
checkups.create_checker()
mload.create_load_syncer()
```
create_checker
```lua
-- 首先检查当前质量是不是 init_worker
-- 如果是 init_worker lock_timeout 值为 0
-- 这样直接使用 lock:lock() 而不用等待锁
local lock_timeout = get_phase() == "init_worker" and 0 or nil

-- 创建一个定时器 active_checkup 
local ok, err = ngx.timer.at(0, heartbeat.active_checkup)

-- 创建一个定时器 ups_status_checker
if base.upstream.ups_status_sync_enable and not base.ups_status_timer_created then
    local ok, err = ngx.timer.at(0, base.ups_status_checker)
    base.ups_status_timer_created = true
end
```

两个checker都是递归调用的


heartbeat.active_checkup(premature)
```lua
-- 如果传入参数，在 mutex 将 ckey = "checkups:timer:" .. os.time() 存入 ngx.shared.mutex
if premature then
    local ok, err = mutex:set(ckey, nil)
end



for skey in pairs(base.upstream.checkups) do
        cluster_heartbeat(skey)
end
```
base.ups_status_checker(premature)
```lua

```

# 请求处理
```lua

```