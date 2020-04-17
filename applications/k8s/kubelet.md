# Dynamic Kubelet Configuration

https://github.com/kubernetes/enhancements/issues/281

https://kubernetes.io/docs/tasks/administer-cluster/reconfigure-kubelet/


# HTTP Server

## debug handlers

--enable-debugging-handlers(DEPRECATED: This parameter should be set via the config file specified by the Kubelet's --config flag. See https://kubernetes.io/docs/tasks/administer-cluster/kubelet-config-file/ for more information.)

https://github.com/kubernetes/kubernetes/blob/master/pkg/kubelet/server/server.go#L531, endpoints: ["/run/", "/exec/", "/attach/", "/portForward/", "/containerLogs/",
		"/runningpods/", "/debug/pprof/"(pprofBasePath), "/logs/"(logsPath)]
    
## metrics  
"/metrics", "/metrics/cadvisor", "/metrics/resource", "/metrics/probes"
