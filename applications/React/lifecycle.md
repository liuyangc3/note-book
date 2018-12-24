 
 
## react lifecycle methods
http://projects.wojtekmaj.pl/react-lifecycle-methods-diagram/
```
                    +---------------------------------+  +-------------------------------------------+  +--------------------------+
                    |                                 |  |                                           |  |                          |
                    |             Mouting                                Updating                    |  |        Unmouting         |
                    |                                 |  |                                           |  |                          |
                    |                                 |  |                                           |  |            |             |
                    |  +---------------------------+  |  |                                           |  |            |             |
                    |  |       constructor         |  |  |  New props   setState()   force Update()  |  |            |             |
                    |  +--------------+------------+  |  |      |           |             |          |  |            |             |
                    |                 |               |  |      |           |             |          |  |            |             |
                    |                 v               |  |      v           v             v          |  |            |             |
"Render phase"      |  +--------------+---------------+--+----------------------------------------+  |  |            |             |
                    |  |                          getDerivedStateFromProps                        |  |  |            |             |
                    |  +-----------------------------+---+----------------------------------------+  |  |            |             |
                    |                 |               |  |      |          |              |          |  |            |             |
                    |                 |               |  |      v          v              |          |  |            |             |
                    |                 |               |  |  +-------------------------+   |          |  |            |             |
                    |                 |               |  |  |  shouldComponentUpdate  |   |          |  |            |             |
                    |                 |               |  |  +-------------------------+   |          |  |            |             |
                    |                 |               |  |                |\              |          |  |            |             |
                    |                 v               |  |                v x             v          |  |            |             |
                    |  +--------------------------------------------------------------------------+  |  |            |             |
                    |  |                                render                                    |  |  |            |             |
                    |  +--------------------------------------------------------------------------+  |  |            |             |
                    |                 |               |  |                     |                     |  |            |             |
                    |                 |               |  |                     v                     |  |            |             |
................... |                 |               |  |  +-------------------------------------+  |  |            |             |
"Pre-commit phase"  |-----------------+---------------------+       getSnapshotBeforeUpdate       +--------------------------------+
................... |                 |               |  |  +-------------------------------------+  |  |            |             |
                    |                 |               |  |                     |                     |  |            |             |
                    |                 v               |  |                     v                     |  |            |             |
                    |  +--------------------------------------------------------------------------+  |  |            |             |
"Commit phase"      |  |                        React updates DOM and refs                        |  |  |            |             |
                    |  +--------------------------------------------------------------------------+  |  |            |             |
                    |                 |               |  |                     |                     |  |            |             |
                    |                 v               |  |                     v                     |  |            V             |
                    |  +---------------------------+  |  |  +-------------------------------------+  |  | +----------------------+ |
                    |  |    componentDidMount      |  |  |  |         componentDidUpdate          |  |  | | componentwillunmount | |
                    |  +---------------------------+  |  |  +-------------------------------------+  |  | +----------------------+ |
                    |                                 |  |                                           |  |                          |
                    +---------------------------------+  +-------------------------------------------+  +--------------------------+
```

## getDerivedStateFromProps
https://reactjs.org/docs/react-component.html#static-getderivedstatefromprops

getDerivedStateFromProps 在 render 前调用, 初始 mount 和 update 时都会调用

开发时应该避免使用这个函数

https://reactjs.org/blog/2018/06/07/you-probably-dont-need-derived-state.html#what-about-memoization
 
```js
import memoize from "memoize-one";

class Example extends Component {
  // State only needs to hold the current filter text value:
  state = { filterText: "" };

  // Re-run the filter whenever the list array or filter text changes:
  filter = memoize(
    (list, filterText) => list.filter(item => item.text.includes(filterText))
  );

  handleChange = event => {
    this.setState({ filterText: event.target.value });
  };

  render() {
    // Calculate the latest filtered list. If these arguments haven't changed
    // since the last render, `memoize-one` will reuse the last return value.
    const filteredList = this.filter(this.props.list, this.state.filterText);

    return (
      <Fragment>
        <input onChange={this.handleChange} value={this.state.filterText} />
        <ul>{filteredList.map(item => <li key={item.id}>{item.text}</li>)}</ul>
      </Fragment>
    );
  }
}
```

memoize 默认使用 `===` 来对比两次传入的函数的参数, 如果想进行深对比可以自己传入对比函数



## shouldComponentUpdate
sub topic:
- PureComponent
- shallowEqual

在普通 Component 里, prop 和 state 产生变化,组件就会重新 render, shouldComponentUpdate 可以手动控制组件是否进行 render.

### PureComponent 
PureComponent 默认实现了 shouldComponentUpdate(), 自动对变化前后的 prop 和 state 进行浅对比.

```js
https://github.com/facebook/react/blob/v16.7.0/packages/react-reconciler/src/ReactFiberClassComponent.js#L280
if (ctor.prototype && ctor.prototype.isPureReactComponent) {
  return (
    !shallowEqual(oldProps, newProps) || !shallowEqual(oldState, newState)
  );
}
```
代码很好理解,当组件类型是 PureComponent时, 调用`shallowEqual` 进行props 和 state 浅对比

function 组件没有 shouldComponentUpdate Hook,  手动实现 props 的比较需要自己缓存上次的 props.

也可以使用第三方库 recompose.pure 实现类似 PureComponent 的效果.

React v16.6.0 引入了 React.memo, 等同于 recompose.pure.


### shallowEqual
代码 https://github.com/facebook/react/blob/v16.7.0/packages/shared/shallowEqual.js
所谓浅对比, 是指当
- 对比对象是基本类型 用 [Object.is](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object/is) 比较
- 对比的类型为object, 并且key的长度相等的时候，浅比较也仅仅是用 Object.is() 对 Object 的 value 做了一个基本数据类型的比较

Array 和 Function 是如何对比的?

>https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Indexed_collections_Arrays_and_typed_Arrays
Arrays are regular objects for which there is a particular relationship between integer-key-ed properties and the 'length' property.

首先 Array 也是对象, 每个元素的的 `key` 是 元素的index.toString(), 而对象的浅对比, 会对每个子属性进行 Object.is 对比
```js
var x = {foo: 1}
var y = {foo: 1}
Object.is(x, y)     // false
shallowEqual(x, y)  // true

var x = [1, 2, 3]
var y = [1, 2, 3]
Object.is(x, y)     // false
shallowEqual(x, y)  // true

var x = {a: {foo: 1}, b: {bar: 2}}
var y = {a: {foo: 1}, b: {bar: 2}}
shallowEqual(x, y)  // false

var x = [{foo: 1}, {bar: 2}]
var y = [{foo: 1}, {bar: 2}]
shallowEqual(x, y)  // false
```

> https://developer.mozilla.org/en-US/docs/Web/JavaScript/Data_structures#Normal_objects_and_functions
Functions are regular objects with the additional capability of being callable.

Function 也是对象,附带了被调用的能力

需要注意的是声明一致 function 是不同的, 必须是同一个引用
```js
shallowEqual(()=> null,()=> null)  // false

var f = () => null
shallowEqual(f, f)  // true
``
PureComponents 仅在 prop 和 state 浅对比不同时, 进行 rerender, 相比 Component 减小了不必要的 render, 提高了性能.

### 一些陷阱和坑
1 inline prop function

经常可以看到这样 inline的写法
```js
<Child onToggle={() => {
  this.setState({ IsOpen: true })
}}/>
```
如果 Child 是 PureComponent, 当父组件重新 render 时, 虽然每次 onToggle 的函数声明是一样的, 但是是不同的函数, Child 会重新 render

应该采用这种写法 有一篇详细说明 inline function https://cdb.reacttraining.com/react-inline-functions-and-performance-bdff784f5578
```js
//...
onToggle = () => this.setState({ IsOpen: true });
render() {
  return <Child onToggle={this.onToggle}/>
}
```
2 PureComponent or React.memo with children

https://blog.cloudboost.io/react-purecomponents-children-979e3da15ba8 
```
// rerender every time
<Child onToggle={this.onToggle}>
  <p>I am a child</p>
</Child>

// not rerender
<Child onToggle={this.onToggle}>1</Child>
```
如果有 Child 的children 是 element, 每次都会 rerender
因为在React 里 prop.children 里 element 都是表示成数组或者 Object, 浅对比会失败, 而 prop.children 是 基本类型就没关系(第二个例子)

解决方式是把 children 写成函数 [functions as children](https://reactjs.org/docs/jsx-in-depth.html#functions-as-children)





