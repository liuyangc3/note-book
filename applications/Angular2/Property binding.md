source: https://vsavkin.com/the-core-concepts-of-angular-2-c3d6cbe04d04

# Property Bindings
Angular 使用 property bindings 在它们之间同步
* component tree with the model
* DOM with the component tree

假设 app 有一个 component tree，并且带有一个 model，我们用 JavaScript object 来表示
```
{
  "filters": { "speaker": "Rich Hickey" }, 
  "talks": [ 
    { 
      "title": "Are we there yet?", 
      "speaker": "Rich Hickey", 
      "yourRating": null,  
      "avgRating": 9.0 
    } 
  ] 
}
```
想象一下，有个时间修改了这个 model，例如我们将 avgRating 改为 9.9。

如果我必须找到所有依赖这个新值得地方，并且手动修改他们，这将是复杂而极易出错的过程。
我希望 app 自动地反射这个修改。这就是 poperty bindings 的目的。

在一轮 VM 结束时，Angular 会检查 component tree 中的每个 component，具体来说就是 property binding
(每个中括号，双花括号里)，并且更新 component。同时更新 DOM 以匹配 component tree 的状态。

使用 property bindings 只有 input properties 可以被更新。

## Zones
Angular 1 使用 scope.$apply 来进行检测，而 Angular 2 使用 Zones 来知道什么时候来检查。
这样使用三方库时就无需调用 scope.$apply。


