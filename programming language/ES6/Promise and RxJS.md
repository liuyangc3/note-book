# Promise

promise 最大的意义在于把嵌套的回调变成了链式调用

```js
//回调风格
doSth(function() {
    doSth2(function() {
        doSth3();
    })
})

//promise风格
Promise.resolve().then(function(){
    return doSth();
}).then(function(){
    return doSth2();
}).then(function(){
    return doSth3();
});
// doSth().then(doSth2).then(doSth);
```

以Promise作为返回值的函数,大致是这样的：
```js
function doSth() {
    return new Promise(function(resolve, reject) {
        //做点什么异步的事情
        //结束的时候调用 resolve，比如：
        setTimeout(function(){
            resolve(); //这里才是真的返回
        },1000)
    })
}
```
如果你不喜欢这样的写法，还可以使用defer风格的promise
```js
function doSth2() {
    var defer = Promise.defer();
    //做点什么异步的事情
    //结束的时候调用 defer.resolve，比如：
    setTimeout(function(){
        defer.resolve(); //这里才是真的返回
    },1000)

    return defer.promise;
}
```

# RxJS
全名 Reactive Extensions for JavaScript,响应式扩展

思路是把随时间不断变化的数据、状态、事件等等转成可被观察的序列(Observable Sequence)，然后订阅序列中那些Observable对象的变化，一旦变化，就会执行事先安排好的各种转换和操作。

适用场景：1.异步操作重，2.同时处理多个数据源。

来个 FRP（响应式编程）的例子，实现点button或5秒后执行某个操作：
```
function wait(duration){
    return new Promise(function(resolve, reject) {
        setTimeout(resolve,duration);
    })
}

function waitFor(element,event,useCapture){
    return new Promise(function(resolve, reject) {
        element.addEventListener(event,function listener(event){
            resolve(event)
            this.removeEventListener(event, listener, useCapture);
        },useCapture)
    })
}

var btn = document.getElementById('button');
Promise.race(wait(5000), waitFor(btn, click)).then(function(){
    console.log('run!')
})
```
RxJS的实现很简洁:
```
var btn = document.getElementById('button');
var logRun = Rx.Observable.fromEvent(btn, 'click')
             .merge(Rx.Observable.timer(3000))
             .subscribe(e => {
               console.log('run!');
               logRun.dispose(); // 如果是一次性的就移除observable
             });
```

从上述的例子中体会一下RxJS的基本用法。Rx.Observable.*创建一个Observable对象，当它发生变化时，以流式的方式触发各种转换（如有需要可以对变化的值做合并、映射、过滤等操作），最后传到订阅回调拿到处理后的最终结果。


# 参考
http://www.w3ctech.com/topic/721

http://www.w3ctech.com/topic/1298
