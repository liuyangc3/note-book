# aws-load-balancer-controller creates a cliassic LB insead of ALB or NLB

I got controller log by `kubectl logs -f -n kube-system --selector 'app.kubernetes.io/instance=aws-load-balancer-controller'`

```
{"level":"info","ts":1626390838.5239894,"logger":"controllers.ingress","msg":"successfully built model","model":"{\"id\":\"sms-api/sms-api\",\"resources\":{\"AWS::EC2::SecurityGroup\":{\"ManagedLBSecurityGroup\":{\"spec\":{\"groupName\":\"k8s-smsapi-smsapi-49025deb34\",\"description\":\"[k8s] Managed SecurityGroup for LoadBalancer\",\"tags\":{\"Environment\":\"prod\"},\"ingress\":[{\"ipProtocol\":\"tcp\",\"fromPort\":80,\"toPort\":80,\"ipRanges\":[{\"cidrIP\":\"0.0.0.0/0\"}]}]}}},\"AWS::ElasticLoadBalancingV2::Listener\":{\"80\":{\"spec\":{\"loadBalancerARN\":{\"$ref\":\"#/resources/AWS::ElasticLoadBalancingV2::LoadBalancer/LoadBalancer/status/loadBalancerARN\"},\"port\":80,\"protocol\":\"HTTP\",\"defaultActions\":[{\"type\":\"fixed-response\",\"fixedResponseConfig\":{\"contentType\":\"text/plain\",\"statusCode\":\"404\"}}],\"tags\":{\"Environment\":\"prod\"}}}},\"AWS::ElasticLoadBalancingV2::ListenerRule\":{\"80:1\":{\"spec\":{\"listenerARN\":{\"$ref\":\"#/resources/AWS::ElasticLoadBalancingV2::Listener/80/status/listenerARN\"},\"priority\":1,\"actions\":[{\"type\":\"forward\",\"forwardConfig\":{\"targetGroups\":[{\"targetGroupARN\":{\"$ref\":\"#/resources/AWS::ElasticLoadBalancingV2::TargetGroup/sms-api/sms-api-sms-api:80/status/targetGroupARN\"}}]}}],\"conditions\":[{\"field\":\"host-header\",\"hostHeaderConfig\":{\"values\":[\"sms-api.f2pool.com\"]}},{\"field\":\"path-pattern\",\"pathPatternConfig\":{\"values\":[\"/\"]}}],\"tags\":{\"Environment\":\"prod\"}}}},\"AWS::ElasticLoadBalancingV2::LoadBalancer\":{\"LoadBalancer\":{\"spec\":{\"name\":\"k8s-smsapi-smsapi-1952b82286\",\"type\":\"application\",\"scheme\":\"internal\",\"ipAddressType\":\"ipv4\",\"subnetMapping\":[{\"subnetID\":\"subnet-0493ea8db050e52fd\"},{\"subnetID\":\"subnet-04ede54adf273f0f4\"},{\"subnetID\":\"subnet-0b0e589bfd6b2ed74\"}],\"securityGroups\":[{\"$ref\":\"#/resources/AWS::EC2::SecurityGroup/ManagedLBSecurityGroup/status/groupID\"}],\"tags\":{\"Environment\":\"prod\"}}}},\"AWS::ElasticLoadBalancingV2::TargetGroup\":{\"sms-api/sms-api-sms-api:80\":{\"spec\":{\"name\":\"k8s-smsapi-smsapi-6b9f413ac6\",\"targetType\":\"instance\",\"port\":31769,\"protocol\":\"HTTP\",\"protocolVersion\":\"HTTP1\",\"healthCheckConfig\":{\"port\":\"traffic-port\",\"protocol\":\"HTTP\",\"path\":\"/\",\"matcher\":{\"httpCode\":\"200\"},\"intervalSeconds\":15,\"timeoutSeconds\":5,\"healthyThresholdCount\":2,\"unhealthyThresholdCount\":2},\"tags\":{\"Environment\":\"prod\"}}}},\"K8S::ElasticLoadBalancingV2::TargetGroupBinding\":{\"sms-api/sms-api-sms-api:80\":{\"spec\":{\"template\":{\"metadata\":{\"name\":\"k8s-smsapi-smsapi-6b9f413ac6\",\"namespace\":\"sms-api\",\"creationTimestamp\":null},\"spec\":{\"targetGroupARN\":{\"$ref\":\"#/resources/AWS::ElasticLoadBalancingV2::TargetGroup/sms-api/sms-api-sms-api:80/status/targetGroupARN\"},\"targetType\":\"instance\",\"serviceRef\":{\"name\":\"sms-api\",\"port\":80},\"networking\":{\"ingress\":[{\"from\":[{\"securityGroup\":{\"groupID\":{\"$ref\":\"#/resources/AWS::EC2::SecurityGroup/ManagedLBSecurityGroup/status/groupID\"}}}],\"ports\":[{\"protocol\":\"TCP\"}]}]}}}}}}}}"}
```


and event 
```
Failed deploy model due to RequestError: send request failed caused by: Post "https://wafv2.ap-east-1.amazonaws.com/": dial tcp 13.248.36.219:443: i/o timeout
```


```go
func (r *serviceReconciler) buildAndDeployModel(ctx context.Context, svc *corev1.Service) (core.Stack, *elbv2model.LoadBalancer, error) {
	stack, lb, err := r.modelBuilder.Build(ctx, svc)
	if err != nil {
		r.eventRecorder.Event(svc, corev1.EventTypeWarning, k8s.ServiceEventReasonFailedBuildModel, fmt.Sprintf("Failed build model due to %v", err))
		return nil, nil, err
	}
	stackJSON, err := r.stackMarshaller.Marshal(stack)
	if err != nil {
		r.eventRecorder.Event(svc, corev1.EventTypeWarning, k8s.ServiceEventReasonFailedBuildModel, fmt.Sprintf("Failed build model due to %v", err))
		return nil, nil, err
	}
	r.logger.Info("successfully built model", "model", stackJSON)

	if err = r.stackDeployer.Deploy(ctx, stack); err != nil {
		r.eventRecorder.Event(svc, corev1.EventTypeWarning, k8s.ServiceEventReasonFailedDeployModel, fmt.Sprintf("Failed deploy model due to %v", err))
		return nil, nil, err
	}
	r.logger.Info("successfully deployed model", "service", k8s.NamespacedName(svc))

	return stack, lb, nil
}
```

r.stackDeployer.Deploy failed, so the evnet will get  `Failed deploy model due to RequestError: send request failed caused by: Post "https://wafv2.ap-east-1.amazonaws.com/ ": dial tcp 13.248.36.219:443: i/o timeout`.  

I think the reason is wafv2 service is not in private link, so controller can not access the API. This issue list all the service used in controller https://github.com/kubernetes-sigs/aws-load-balancer-controller/issues/1855

To disable this service we can set flags `--enable-shield=false -enable-waf=false  --enable-wafv2=false` for controller, or set thess values `false` in helm
```
# Enable Shield addon for ALB (default true)
enableShield:

# Enable WAF addon for ALB (default true)
enableWaf:

# Enable WAF V2 addon for ALB (default true)
enableWafv2:
```

```go
// pkg/service/model_builder.go
func (b *defaultModelBuilder) Build(ctx context.Context, service *corev1.Service) (core.Stack, *elbv2model.LoadBalancer, error) {
	stack := core.NewDefaultStack(core.StackID(k8s.NamespacedName(service)))
	task := &defaultModelBuildTask{
		...
	}

	if err := task.run(ctx); err != nil {
		return nil, nil, err
	}
	return task.stack, task.loadBalancer, nil
}

func (t *defaultModelBuildTask) run(ctx context.Context) error {
	if !t.service.DeletionTimestamp.IsZero() {
		return nil
	}
	err := t.buildModel(ctx)
	return err
}

func (t *defaultModelBuildTask) buildModel(ctx context.Context) error {
	scheme, explicitScheme, err := t.buildLoadBalancerScheme(ctx)
	if err != nil {
		return err
	}
	if !explicitScheme && len(t.service.Status.LoadBalancer.Ingress) != 0 {
		scheme, err = t.getExistingLoadBalancerScheme(ctx)
		if err != nil {
			return err
		}
	}
	t.ec2Subnets, err = t.resolveLoadBalancerSubnets(ctx, scheme)
	if err != nil {
		return err
	}
	err = t.buildLoadBalancer(ctx, scheme)
	if err != nil {
		return err
	}
	err = t.buildListeners(ctx, scheme)
	if err != nil {
		return err
	}
	return nil
}


// pkg/service/model_builder.go
func (t *defaultModelBuildTask) buildModel(ctx context.Context) error {
	scheme, explicitScheme, err := t.buildLoadBalancerScheme(ctx)
	if err != nil {
		return err
	}
	if !explicitScheme && len(t.service.Status.LoadBalancer.Ingress) != 0 {
		scheme, err = t.getExistingLoadBalancerScheme(ctx)
		if err != nil {
			return err
		}
	}
	t.ec2Subnets, err = t.resolveLoadBalancerSubnets(ctx, scheme)
	if err != nil {
		return err
	}
	err = t.buildLoadBalancer(ctx, scheme)
	if err != nil {
		return err
	}
	err = t.buildListeners(ctx, scheme)
	if err != nil {
		return err
	}
	return nil
}

// pkg/service/model_build_load_balancer.go
func (t *defaultModelBuildTask) buildLoadBalancer(ctx context.Context, scheme elbv2model.LoadBalancerScheme) error {
	spec, err := t.buildLoadBalancerSpec(ctx, scheme)
	if err != nil {
		return err
	}
	t.loadBalancer = elbv2model.NewLoadBalancer(t.stack, resourceIDLoadBalancer, spec)
	return nil
}

// pkg/model/elbv2/load_balancer.go
// NewLoadBalancer constructs new LoadBalancer resource.
func NewLoadBalancer(stack core.Stack, id string, spec LoadBalancerSpec) *LoadBalancer {
	lb := &LoadBalancer{
		ResourceMeta: core.NewResourceMeta(stack, "AWS::ElasticLoadBalancingV2::LoadBalancer", id),
		Spec:         spec,
		Status:       nil,
	}
	stack.AddResource(lb)
	lb.registerDependencies(stack)
	return lb
}
```

according CF [ELB doucument](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticloadbalancingv2-loadbalancer.html)

Type: The type of load balancer. The default is application. Allowed values: `application` | `gateway` | `network`, so the `LoadBalancerSpec.Type` decide which kind LB CF will create.

we can see the stack json in log that type is `application`
```json
...
    "AWS::ElasticLoadBalancingV2::LoadBalancer": {
      "LoadBalancer": {
        "spec": {
          "name": "k8s-smsapi-smsapi-1952b82286",
          "type": "application",
          "scheme": "internal",
          "ipAddressType": "ipv4",
          "subnetMapping": [
            {
              "subnetID": "subnet-0493ea8db050e52fd"
            },
            {
              "subnetID": "subnet-04ede54adf273f0f4"
            },
            {
              "subnetID": "subnet-0b0e589bfd6b2ed74"
            }
          ],
          "securityGroups": [
            {
              "$ref": "#/resources/AWS::EC2::SecurityGroup/ManagedLBSecurityGroup/status/groupID"
            }
          ],
          "tags": {
            "Environment": "prod"
          }
        }
      }
    },
```

But why it create a classic ELB? the provider in tree also support creating LoadBalancer type service see https://github.com/kubernetes/cloud-provider-aws/blob/master/pkg/providers/v1/aws_loadbalancer.go.
