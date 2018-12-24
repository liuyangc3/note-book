 
 
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



## React.PureComponent
Component 没有实现 shouldComponentUpdate(), 而 PureComponent 默认实现了 prop 和 state 的浅对比

```js
https://github.com/facebook/react/blob/v16.7.0/packages/react-reconciler/src/ReactFiberClassComponent.js#L280
if (ctor.prototype && ctor.prototype.isPureReactComponent) {
  return (
    !shallowEqual(oldProps, newProps) || !shallowEqual(oldState, newState)
  );
}
```
PureComponent 的`ShouldComponentUpdate` 自动通过函数 `shallowEqual` 进行props 和 state 浅对比

function 组件可以使用 recompose.pure 实现 PureComponent 的效果

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


PureComponents 仅在 prop 和 state 浅对比不同时, 进行 rerender, 相比 Component 减小了不必要的 render, 提高了性能.




