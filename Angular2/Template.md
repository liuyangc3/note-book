https://angular.io/docs/ts/latest/guide/template-syntax.html

https://vsavkin.com/angular-2-template-syntax-5f2ee9f13c6a


# Template expressions
一个模板表达式(template expression)产生一个值，angular 将这个值赋予绑定目标的属性上。绑定目标可以是一个 HTML 元素，一个组件，
或者一个指令。

模板表达式一版写在双花括号内，{{1 + 1}}.

## Expression context
模板表达式内不能引用任何全局命名空间内的任何东西，例如 window 或 document。也不能调用 console.log 或 Math.max。
只能引用表达式上下文内的成员。

典型的表达式上下文是组件实例，例如看到 {{title}}，我们就知道 title 是一个绑定组件的属性。
当我们看到 [disabled]="isUnchanged", 就知道 disabled 引用了组件的 isUnchanged 属性。


# Input and Output Properties
Input 和 output 属性是一个指令的公共API.
数据通过指令的 inputs 流入，从 outputs 流出.
通过使用属性绑定(property bindings)你可以更新 input 属性.
通过事件绑定(event bindings)你可以订阅 output 属性.


# Property Bindings
`[]`单向绑定
```
<todo-cmp [target]="expression"></todo-cmp>
```
`[]`实际上是`bind-`的语法糖
```
<todo-cmp bind-target="expression"></todo-cmp>
```


当 `myTodo` 变化后，Angular 需要
 
# Event Bindings
template statement 对应一个由绑定目标引起的事件，一般写作 (event)="statement"。
```
<todo-cmp (complete)="statement"></todo-cmp>
```
`()` 是 `on-`的语法糖
```
<todo-cmp on-complete="statement"></todo-cmp>
```

# * and <template>
`NgFor`, `NgIf` , `NgSwitch` 指令前面有 *，它是 <template> 标签的语法糖