aws-load-balancer-controller
```go
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

Type: The type of load balancer. The default is application. Allowed values: `application` | `gateway` | `network`, so the `LoadBalancerSpec.Type` decide which kind LB CF will create
