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