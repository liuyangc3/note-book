# what is 
go kit 是构建微服务组件

# design
设计理念

1 Transport layer

2 Endpoint layer

3 Service layer

请求从 1 到 3, 响应从 3 到 1

## Transports
对应协议层, 例如 HTTP gRPC, 微服务可以支持多种 transports, 这样,你可以在一个微服务里同时为原有HTTP服务和RPC服务

## Endpoints 
类似 controller 里的  action/handler, 具体是处理逻辑, 如果你实现了 2 个 transports
那么你需要有2个发送请求到同一个endpoint的方法

## services
业务逻辑, 一个 service 应粘连多个 endpoints.在 go kit services 是接口, 接口的实现是业务逻辑
根据clean 架构和六边形架构,业务逻辑无需知道 endpoints