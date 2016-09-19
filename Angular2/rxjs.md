响应式编程 
# Observable
一个数据流，这个流可以被观察、订阅，官方术语中把流称为“观察的对象”("Observable")。

使用Rx.Observable.create()方法可以自定义你需要的流。你需要明确通知观察者(或者订阅者)数据流的到达(onNext()) 或者错误的发生(onError())
```
observable = Rx.Observable.create(
    onNext => {}, //  
    () => {}, // onCompleted
    onError => {}
);
```

```
observable = Rx.Observable.just('https://api.github.com/users');
```


可观察对象(Observable)是 Promise 的超集，你可以从 Promise 对象创建 Observable
```
stream = Rx.Observable.fromPromise(promise)
```
Promise 可以看做只能发射单值的可观察对象，Rx流则允许返回多个值。


# Observer 
Observable 推送数据的消费者。它是由三个函数组成的对象
```
observer = {
    next: data => console.log('Observer got a next value: ' + data),
    error: err => console.error('Observer got an error: ' + err),
    complete: () => console.log('Observer got a complete notification'),
};
```

通过 subscribe 将 Observer 传入 Observable
```
observable.subscribe(observer);
```
三个函数不是必须的，在 next、error 和 complete 处理逻辑部分缺失的情况下，Observable 仍然能正常运行。

也可以更直接的写
```
observable.subscribe(
    data => console.log('Observer got a next value: ' + data)
    err => console.error('Observer got an error: ' + err),
    () => console.log('Observer got a complete notification')
);
```


# Subscription
Subscription是一个代表可以终止资源的对象，表示一个Observable的执行过程。Subscription有一个重要的方法：`unsubscribe`。这个方法不需要传入参数，调用后便会终止相应的资源。
```
subscription = observable.subscribe(x => console.log(x));
subscription.unsubscribe();
```

Subscription可以嵌套使用：你可以调用一个Subscription的unsubscribe() 方法来取消一系列嵌套的Subscription。通过add方法，便可以实现Subscription的嵌套：
```
subscription1 = observable1.subscribe(x => console.log('first: ' + x));
subscription2 = observable2.subscribe(x => console.log('second: ' + x));
subscription1.add(subscription2);
subscription.unsubscribe();
```

# Subject
在RxJS中，Subject是一类特殊的Observable，它可以向多个Observer多路推送数值。普通的Observable并不具备多路推送的能力（每一个Observer都有自己独立的执行环境），而Subject可以共享一个执行环境。

Subject是一种可以多路推送的可观察对象。与EventEmitter类似，Subject维护着自己的Observer。

每一个Subject都是一个Observable（可观察对象） 对于一个Subject，你可以订阅（subscribe）它，Observer会和往常一样接收到数据。从Observer的视角看，它并不能区分自己的执行环境是普通Observable的单路推送还是基于Subject的多路推送。

Subject的内部实现中，并不会在被订阅（subscribe）后创建新的执行环境。它仅仅会把新的Observer注册在由它本身维护的Observer列表中，这和其他语言、库中的addListener机制类似。

每一个Subject也可以作为Observer（观察者） Subject同样也是一个由next(v)，error(e)，和 complete()这些方法组成的对象。调用next(theValue)方法后，Subject会向所有已经在其上注册的Observer多路推送theValue。

下面的例子中，我们在Subject上注册了两个Observer，并且多路推送了一些数值：
```
var subject = new Rx.Subject();

subject.subscribe({
  next: (v) => console.log('observerA: ' + v)
});
subject.subscribe({
  next: (v) => console.log('observerB: ' + v)
});

subject.next(1);
subject.next(2);
```
控制台输出结果如下：
```
observerA: 1
observerB: 1
observerA: 2
observerB: 2
```
https://segmentfault.com/a/1190000005069851
# Operators

Observable 的数据流是不可变的，但是我们的某个观察者对数据有特殊要求怎么办？当然可以这么做
```
observable.subscribe(
    data => transfrom(data)
);
transfrom(data) { 
    // do something 
    return newData
}
```
但是每个 Observer 都这么写岂不是很麻烦，可以通过 Operators 对数据进行转换，Operators 没有修改 Observable 的数据，而是生产了新的 Observable。

## map
原始的流上，附加了新的流
```
observable.map(data => transform(data))
    .subscribe(newData => console.log(newData))
```
## flatmap
