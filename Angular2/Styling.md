http://blog.thoughtram.io/angular/2015/06/25/styling-angular-2-components.html

# STYLING ANGULAR 2 COMPONENTS
在 Angular 2 中，一个 component 基本上是一个带有 controller class 的 template。
但是 component 还有自己的样式，尤其是重复使用的components。

我们可以写更加模块化和容易扩展的 CSS 代码，如果我们不使用 component，所有样式文件都是连接在
HTML 文档的 head 里，components 并不知道它们的存在。如果我们构建一个 component 并且共享它，
并将样式打包进 component，这将是一个很好的想法。

实际上 Angular 2 components 就是这么设计的，一个 component 有自己的 HTML，javascript 和 style。
我们需要做的仅仅是在 component 里定义 style，有三种定义的方式：component 内联样式，样式 urls，模板内联样式。
我们会一一讲解。

# component 内联样式
在装饰器 @Component 的 styles 属性写样式
```typescript
@Component({
  moduleId: module.id,
  selector: 'my-zippy',
  templateUrl: 'my-zippy.component.html',
  styles: [`
    .zippy {
      background: green;
    }
  `]
})
class ZippyComponent {
  @Input() title: string;
}
```
如何写样式非常简单，但是它们是如何出现在 DOM 里呢？原来是 Angular 将它们写入 HTML 的 head，
这是在浏览器中
```
<!DOCTYPE html>
<html>
  <head>
    <style>
      .zippy { 
        background: green;
      }
    </style>
  </head>
  <body>
  ...
  </body>
</html>
```
样式会出现在哪，是因为我们使用了 `View Encapsulation`。Angular 有三种 view encapsulation，
是为了可以同时在不支持 Shadow DOM 浏览器和其他支持 Shadow DOM 的环境里运行，
view encapsulation 会在另一篇文章介绍，这里我们关注发生了什么。

Angular2 默认使用`Emulated View Encapsulation `，这个类型没有使用任何的 Shadow DOM。
Shadow DOM 非常好的一个特性是样式封装，它允许样式的作用范围仅在 component 内而不影响外界。

为了利用样式封装，样式需要放入一个 component 的 shadowRoot。而基于默认的 view encapsulation 类型，
是没有 shadowRoot 的，所以 Angular 把样式放入 head。

我们看看其他定义样式的方式。

# 样式 urls
通过 styleUrls 属性
```typescript
@Component({
  moduleId: module.id,
  selector: 'my-zippy',
  templateUrl: 'my-zippy.component.html',
  styleUrls: ['my-zippy.component.css']
})
class ZippyComponent {
  @Input() title: string;
}
```
url里样式如何出现？和前面一样，会出现在 head 里，实际上 Angular 会先获取资源里的文本，
并把它们追加到内敛样式后面，所以如果我们这么写 component 
```typescript
@Component({
  moduleId: module.id,
  selector: 'my-zippy',
  templateUrl: 'my-zippy.component.html',
  styles: ['.zippy { background: green; }'],
  // 这里文件的内容是 .zippy { background: blue; }
  styleUrls: ['my-zippy.component.css']
})
class ZippyComponent {
  @Input() title: string;
}
```
那么最终的样式是
```
<!DOCTYPE html>
<html>
  <head>
    <style>
      .zippy { 
        background: green;
      }
    </style>
    <style>
    .zippy {
      background: blue;
    }
    </style>
  </head>
  <body>
  ...
  </body>
</html>
```
# 模板内联样式
我们可以直接将样式写入 DOM，例如
```
<style>
  .zippy {
    background: red;
  }
</style>
<div class="zippy">
  <div (click)="toggle()" class="zippy__title">
    {{ visible ? '&blacktriangledown;' : '&blacktriangleright;' }} {{title}}
  </div>
  <div [hidden]="!visible" class="zippy__content">
    <content></content>
  </div>
</div>
```
模板内联样式有最高优先级，对我来说这挺怪的。
