source: https://vsavkin.com/the-core-concepts-of-angular-2-c3d6cbe04d04

# Dependency injection
看如下组件 
```typescript
@Component({ 
  selector: 'talk-list', 
  template: `
    <h2>Talks:</h2> 
    <ul>
      <li *ngFor="#t of talks">{{t.name}}</li>
    </ul>
` 
}) 
class TalkList { 
  constructor() { //..get the talks data
  } 
}
```
我们需要一个 service 为我们提供数据,let's mock up
```typescript
class TalksAppBackend { 
  fetchTalks() { 
    return [ 
      { name: 'Are we there yet?' }, 
      { name: 'The value of values' } 
    ]; 
  } 
}
```


如何使用 service，最简单的方式就是在组件里创建 service 的实例
```typescript
class TalkList { 
  constructor() { 
    var backend = new TalksAppBackend(); 
    this.talks = backend.fetchTalks(); 
  } 
}
```
这仅仅算一个演示，不能用在真正的产品里，因为 TalksAppBackend 使用 http 去获取数据，而问题是
我们将 TalkList 和 TalksAppBackend 通过 new 操作符绑定在一起了。

我们可以通过注入一个 TalksAppBackend 实例到 TalkList 构造器里来解决这个问题.
```typescript
class TalkList { 
  constructor(backend:TalksAppBackend) { 
    this.talks = backend.fetchTalks(); 
  } 
}
```
我们可以配置root 组件的 providers，这样服务就可以在任意组件中访问
```typescript
@Component({ 
  selector: 'talk-app', 
  providers: [TalksAppBackend] // registered in the root component,
  // so it can be injected into any component in the app. 
}) 
class AppComponent { }
```
组件可以注入 service 服务(很可能是 singleton 单实例) 和 ElementRef，ElementRef对每个组件来说是全局唯一的。
```typescript
class TalksList { 
  constructor(elRef:ElementRef, backend:TalksAppBackend) { } 
}
```
同样组件里还可以注入其他组件
```typescript
class Component { 
  constructor(ancestor:AncestorCmp) { } 
}
```

```typescript
```