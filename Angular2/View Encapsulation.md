http://blog.thoughtram.io/angular/2015/06/29/shadow-dom-strategies-in-angular2.html

样式里讲到，组件里的样式会出现在 head 里，如果我们使用了native Shadow DOM，它们会出现在 组件模板里，
这篇文章将介绍 Angular 如何使用 native Shadow DOM，并且介绍其他的 view encapsulation 方案，
即以为什么他们会出现。

# 理解 shadow DOM
Shadow DOM 的概念可以从 http://www.html5rocks.com/en/search?q=Shadow+DOM 学习。

一句话概括 Shadow DOM是 Web Components 标准的一部分，允许 DOM 和 style 封装在一起。

# Shadow DOM in Angular 2
众所周知，我们在 Angular 2 里构建组件，组件是一个有自己模板和样式的 controller class。
但是组件并不是 Web components，但是它利用了 Web components 优点。
  
当我们创建一个组件时，Angular 把它的模板放入一个 `shadowRoot`,这个节点是组件的 Shadow DOM，
这样样式和 DOM 树都被封装在组件里。如果浏览器不支持 Shadow DOM 还能使用 Angular 2 吗？
可以，Angular 并不使用原生的 Shadow DOM ，它仅仅是模拟，所以准确的说并没有创建 `shadowRoot`。

这样做的原因是大多数浏览器并不支持 shadow DOM，为了兼容而为之。但是我们可以让 Angualr 使用原生
shadow DOM，如何做？

# View Encapsulation Types
Angular View Encapsulation 特许允许使用 Shadow DOM 或者模拟它，有3中模式：

* ViewEncapsulation.None - 不用 Shadow DOM。因此不会有样式的封装。
* ViewEncapsulation.Emulated - 不使用 Shadow DOM，但是模拟样式封装。
* ViewEncapsulation.Native - 原生 Shadow DOM。

# ViewEncapsulation.None
不用 Shadow DOM，样式会越过组件，直接写入文档的 head。
```typescript
import {ViewEncapsulation } from '@angular/core';

@Component({
  moduleId: module.id,
  selector: 'my-zippy',
  templateUrl: 'my-zippy.component.html',
  styles: [`
    .zippy {
      background: green;
    }
  `],
  encapsulation: ViewEncapsulation.None
})
class ZippyComponent {
  @Input() title: string;
}
```

# ViewEncapsulation.Emulated
这是默认值