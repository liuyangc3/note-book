 
 
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

memoize 默认使用 === 来对比两次传入的函数的参数, 如果想进行深对比可以自己传入对比函数



## React.PureComponent
Component 没有实现 shouldComponentUpdate(), 而 PureComponent 默认实现了 prop 和 state 的浅对比

浅对比指, 当对比的类型为Object的时候并且key的长度相等的时候，浅比较也仅仅是用 Object.is() 对 Object 的 value 做了一个基本数据类型的比较
 
PureComponents 仅在 prop 和 state 浅对比不同时进行 rerender, 相比 Component 提高了性能

function 组件可以使用 recompose.pure 实现 PureComponent 的效果

React v16.6.0 引入了 React.memo, 等同于 recompose.pure.


