http://blog.thoughtram.io/angular/2016/01/22/understanding-zones.html

http://blog.thoughtram.io/angular/2016/02/01/zones-in-angular-2.html

# Zone
Zone 是 Angular 团队写的一个 lib，简单来说一个 Zone 就是异步操作的一个执行上下文(execution context)。
为了理解执行上下文，我们来看看 Zone 试图解决什么样的问题，先看看下面的 JavaScript 代码：
```javascript
foo();
bar();
baz();

function foo() {//...}
function bar() {//...}
function baz() {//...}
```
三个函数按照顺序执行，如果想记录函数的执行时间，只需稍微扩展
```javascript
var start, time = 0;
timer = performance ? performance.now : Date.now;

// start timer
start = timer();
foo();
bar();
baz();
// stop timer
time = timer() - start;
// log time in ms
console.log(Math.floor(time*100) / 100 + 'ms');
```
当我们要做一些异步的工作，例如使用 AJAX 从服务器请求数据，或者调度工作到下个frame。无论这些异步工作是什么，
它们总是在声明的时候异步地执行。也就是说这些操作并不被我们的计时器考虑，如下
```javascript
function doSomething() {
  console.log('Async task');
}

// start timer
start = timer();
foo();
setTimeout(doSomething, 2000);
bar();
baz();
// stop timer
time = timer() - start;
```
我们加入了异步操作，它如何影响我们的计时器？我们将会看到并没有不同。

由于多了一个操作，整个代码的执行时间应该会长一些，但是当 `setTimeout()` 返回时，真正的执行时间，并没有在总开销里。
这是因为异步操作被加入了浏览器的事件队列(event queue)，操作最终被 event loop 清理，

所以应该如何解决这个问题？我们需要异步操作发生时，有一个基本的 hook 来允许我们进行记时。
当然我们可以手动地为每个异步事件创建一个 timer，但是在原本的操作顺序里加入异步代码会显得很乱。

这正是 Zone 施展的地方，Zones 可以执行操作- 例如启动和停止 timer，保存堆栈信息 - 每当代码进入或离开一个 zone，
他可以在我们的代码里覆写方法，甚至关联不同zone的数据

# 创建 forking 扩展 Zones
Zones 实际上是编程语言 Dart 的特性，Dart 也可以编译为 JavaScript，所以我们可以在 JavaScript 里实现同样的功能。
Brian 就是这么做的，他创造了JS 版本的[zone.js](https://github.com/angular/zone.js)，同时也是 Angular2 的依赖库。
在我们使用 Zone 测量我们的代码前，我们先看看 Zone 是如何创建的。

一旦我们在浏览器引入了 zone.js，我们就可以获得 zone 对象，zone 包含一个 run() 方法，可以传入一个需要在 zone 里执行的函数。
```javascript
function main() {
  foo();
  setTimeout(doSomething, 2000);
  bar();
  baz();
}

zone.run(main);
```
为了设置 hook，我们需要 fork 方法来复制现在的 zone，返回一个新 zone，继承与"父" zone，并且可以扩展新的行为。
```javascript
var myZone = zone.fork();

myZone.run(main);
```
新 zone 和老 zone 有一样的能力，我们加入 hooks，需要把 ZoneSpecification 传入 fork，有如下 hook：
* onZoneCreated - zone fork 时运行
* beforeTask - zone.run执行后，在一个函数运行前运行
* afterTask - 在一个函数运行后运行
* onError - 当传入 zone.run() 的函数 thorw 时运行

下面扩展我们的代码
```javascript
var myZoneSpec = {
  beforeTask: function () {
    console.log('Before task');
  },
  afterTask: function () {
    console.log('After task');
  }
};

var myZone = zone.fork(myZoneSpec);
myZone.run(main);

// Logs:
// Before task
// After task
// Before task
// Async task <---
// After task
```
为什么每个 hook 执行了2次，zone.run 显然也被认为是 task， 而 setTimeout() 也被认为是 task，这怎么可能？

# Monkey-patched Hooks
事实证明，还有其他的 hook，实际上它们不是 hooks，但  monkey-patched methods 在全局范围，当加载 zone.js 进来后，
差不多所有可以进行异步操作的的方法都会在新 zone 内运行。

例如，调用  setTimeout() 实际上是调用 Zone.setTimeout()，当使用 zone.fork() 创建新 zone 时，是 Zone.setTimeout
被执行，这就是为什么我们的 hook 也执行了。因为新 zone 继承了父zone。

还有一些方法覆盖默认hooks:
* Zone.setInterval()
* Zone.alert()
* Zone.prompt()
* Zone.requestAnimationFrame()
* Zone.addEventListener()
* Zone.removeEventListener()

我们可能奇怪 为什么 alert() 和 promptI() 也被 patched。

# Creating a Profiling Zone

```javascript
var profilingZone = (function () {
  var time = 0,
      timer = performance ?
                  performance.now.bind(performance) :
                  Date.now.bind(Date);
  return {
    beforeTask: function () {
      this.start = timer();
    },
    afterTask: function () {
      time += timer() - this.start;
    },
    time: function () {
      return Math.floor(time*100) / 100 + 'ms';
    },
    reset: function () {
      time = 0;
    }
  };
}());
```
这和之前的代码没什么区别，只是包装在  zone specification 里了，并且加入2个函数 .time() and .reset()，下面是调用 zone 的代码：
```javascript
zone
  .fork(profilingZone)
  .fork({
    '+afterTask': function () {
      console.log('Took: ' + zone.time());
    }
  })
  .run(main);
```
`+` 是 DSL，用来扩展父 zone 的 hook 

# Zone in Angular
Zone 在 Angular 内用来实现变化检测(change detection)，你有没有问过自己，为什么时候和为什么 Angular 执行 change detection？
是告诉 Angular "嗨，老兄，我的app有个变化，你能来检测一下吗？"

在进入上面的问题前，我们先想想是什么导致了 app 的 change。或者什么可以 change app 的状态，状态变化有下面几种情况：
* Events - 用户事件，例如 click, change, input, submit, …
* XMLHttpRequests - 从服务器获取数据
* Timers - setTimeout(), setInterval()

可以发现这些事情有共同点，那就是他们都是 __异步__ 的！

为什么知道这个很重要，因为他们是 Angular 更新 view 时需要关心的。我们看看一个 Angular 2 component 处理按钮的 click

```typecript
Component({
  selector: 'my-component',
  template: `
    <h3>We love {{name}}</h3>
    <button (click)="changeName()">Change name</button>
  `
})
class MyComponent {
  name:string = 'thoughtram';
  changeName() {
    this.name = 'Angular';
  }
}
```
当按钮被点击，changeName就执行了，会改变 component 的 name 属性。这样的变化需要反映在 DOM 上，
Angular 会更新 view 上绑定的 {{name}},好像是魔法一样。

我们还可以用 setTimeout() 来更新 name，现在我们删除了 button
```typecript
@Component({
  selector: 'my-component',
  template: `
    <h3>We love {{name}}</h3>
  `
})
class MyComponent implements OnInit {

  name:string = 'thoughtram';

  ngOnInit() {
    setTimeout(() => {
      this.name = 'Angular';
    }, 1000);
  }
}
```
我们无需额外的操作去告诉框架有变化了，不用 ng-click, 不用 $timeout, $scope.$apply()。

下面的代码是告诉 Augular 执行变化检测当 VM 周期结束时
```typecript
ObservableWrapper.subscribe(this.zone.onTurnDone, () => {
  this.zone.run(() => {
    this.tick();
  });
});

tick() {
  // perform change detection
  this.changeDetectorRefs.forEach((detector) => {
    detector.detectChanges();
  });
}
```
当 Angular的 zone 发送 `onTurnDone` 事件，它会执行一个 task 检查整个项目的变化。
但是 onTurnDone 事件怎么来的？它并不是 Zone 的 API，下面介绍 Angular 自己的 Zone `NgZone`。

# NgZone in Angular 2
NgZone 是一个 fork zone，有额外的扩展 API，其中一部分就是自定义的事件，我们可以订阅，因为他们是 observable 流。

* onTurnStart() - 在 Angular’s 事件开始前通知订阅者. 每个浏览器 task 被 Angular 处理，就发送一个事件。
* onTurnDone() - 在 Angular的 zone 处理完当前周期后，并且任何 micro tasks 在周期中被调度，立刻通知订阅者。
* onEventDone() - 在最后的 onTurnDone() 回掉后和在 ending VM 事件前，立刻通知订阅者。用来测试 application 状态。

"Observables" 和 "流" 是 rxjs 的概念
 
Angular 加入自己的事件发送器替代 beforeTask 和 afterTask 的原因是跟踪定时器和其他 micro tasks。
Observables 也作为 API 来处理这些事件也非常棒。

# Running code outside Angular’s zone
因为 NgZone 是全局 zone 的 fork，Angular 可以控制什么时候运行 zone 内部的变化检测什么后不运行。
当异步操作发生，NgZone 通知框架执行变化检测，当然它也可以从 `mousemove` 这样的事件可以触发变化检测。

但是我们可能不会让每次`mousemove`都进行变化检测，这样会拖慢 app。

这就是为什么 API runOutsideAngular 可以执行 NgZone 的父 zone 的 task，并且不会发送 onTurnDone 事件，
阻止了变化检测执行。下面的代码展示这个有用的特性。
```typecript
@Component({
  selector: 'progress-bar',
  template: `
    <h3>Progress: {{progress}}</h3>
    <button (click)="processWithinAngularZone()">
      Process within Angular zone
    </button>
  `
})
class ProgressBar {

  progress: number = 0;

  constructor(private zone: NgZone) {}

  processWithinAngularZone() {
    this.progress = 0;
    this.increaseProgress(() => console.log('Done!'));
  }
}
```
当模板 button 被点击后，调用组件的 processWithinAngularZone 方法，内部调用了 increaseProgress，我们来看看
```typecript
increaseProgress(doneCallback: () => void) {
  this.progress += 1;
  console.log(`Current progress: ${this.progress}%`);

  if (this.progress < 100) {
    window.setTimeout(() => {
      this.increaseProgress(doneCallback);
    }, 10);
  } else {
    doneCallback();
  }
}
```
progress 数量小于100时，increaseProgress 每十秒调用自己(progress数量加1)，progress 数量到100后，doneCallback 执行。

这段代码在浏览器执行，基本上每次 setTimeout() 调用，Angular 都会检查变化，这样我们可以在页面上看到每10秒 progress的变化量，
如果代码在 Angular 的 zone 外执行会很有趣，我们加入一个新方法来做这件事
```typecript
processOutsideAngularZone() {
  this.progress = 0;
  this.zone.runOutsideAngular(() => {
    this.increaseProgress(() => {
      this.zone.run(() => {
        console.log('Outside Done!');
      });
    });
  });
}
```
虽然新方法 processOutsideAngularZone 也调用了 increaseProgress，但是由于使用了 runOutsideAngularZone，
导致 Angular 无法在每次 timeout 时被通知。我们可以通过在组件里注入 NgZone 来访问 Angular 的 zone。

随着 progress 增加 UI 不会更新，但是一旦 increaseProgress 结束，我们通过使用  zone.run() 在Angular 的 zone 内
执行另一个 task，就可以使 Angular 执行变化检测，并更新视图。换句话说，上面的代码用最终完成时更新视图，替代了之前每次 progress 增加更新视图。

Zones 同时被提议成为 TC39 标准，这也是为什么我们详细观察它的因素。

