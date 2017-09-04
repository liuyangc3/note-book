# Annotations 
注解

Angular 团队对 JavaScript 做了扩展成为 AtScript，AtScript 有下面的特性

* Type Annotations
* Field Annotations
* MetaData Annotations

这里主要关注  metadata annotations，先看看下面的组件
```typescript
@Component({
  selector: 'tabs',
  template: `
    <ul>
      <li>Tab 1</li>
      <li>Tab 2</li>
    </ul>
  `
})
export class Tabs {}
```
类 Tabs 有一个 annotation 叫 `@Component`，如果删掉 `@Component` 就只剩一个没有任何意义的空类，
所以 `@Component` 肯定向类里加入了一些元数据，这是一种声明式的加入元数据的代码。

`@Component` 来自 angular 
```typescript
import { ComponentMetadata as Component } from '@angular/core';
// ComponentMetadata 实现
export class ComponentMetadata extends DirectiveMetadata {
    ...
}
```
可以看到 ComponentMetadata 也是个类，为什么可以改变其他类的行为，为什么前面要加个`@`?
这些代码在浏览器里无法运行，需要转换，有很多翻译器，如 Babel, Traceur, TypeScript。
实际上 annotations 是实现来自 AtScript: Traceur。

上面的代码由 Traceur 翻译后是这样
```
var Tabs = (function () {
  function Tabs() {}

  Tabs.annotations = [
    new ComponentMetadata({...}),
  ];

  return Tabs;
})
```
实际上类也是个object，所有的 ComponentMetadata 配置都保存在 annotations 属性里，
还有一种以参数定义 annotations 的方式
```typescript
class MyClass {
  constructor(@Annotation() foo) {
    ...
  }
}
```
翻译后是
```
var MyClass = (function () {
  function MyClass() {}

  MyClass.parameters = [[new Annotation()]];

  return MyClass;
})
```
为什么属性 parameter 是个嵌套的数组，是因为一个参数可能是多个 annotation。

Annotations 就是加到类里一些元数据，Angular 会检查类里的 annotations 和 parameters 属性，
如果类里没有这些属性，Angular 无法取得元数据。

作为使用者，自己决定把元数据加入到哪里是不是很酷，这就是 decorators  的用处了。



# Decorators 装饰器

装饰器是ECMAScript 2016提议标准，和 annotations 很像
```
@decoratorExpression
class MyClass { }
```
和 annotations 很相似，但还是不同，我们可以控制装饰器的行为，上面的代码核能是这样的
```
function decoratorExpression(target) {
   // Add a property on target
   target.annotated = true;
}
```
decorator 就是用来"修饰" target 的，所以我们也可以使用 decorator 来为我们的代码添加元数据。

## Does TypeScript support Annotations or Decorators?
TypeScript 支持 decorators,但它不知道 Angular 2 指定的 annotations，


## refs
http://blog.thoughtram.io/angular/2015/05/03/the-difference-between-annotations-and-decorators.html

https://medium.com/@ttemplier/angular2-decorators-and-class-inheritance-905921dbd1b7#.46jfp1szw

https://medium.com/@ttemplier/component-composition-in-angular2-part-1-33f50f402906#.4z4wx1pz2