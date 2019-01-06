# React Patterns


## render props
在 props上写 render 函数, render 逻辑可以从外面传入进来
```js
<DataProvider render={data => (
  <h1>Hello {data.target}</h1>
)}/>
```

通过这种方式,可以把组件内部的 state 曝露出去
```js
class DataProvider extends React.Component {
  state = { data: 'some data' };

  render() {
    return (
      <div>{this.props.render(this.state.data)}</div>
    );
  }
}
```
