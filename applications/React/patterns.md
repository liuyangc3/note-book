# React Patterns


## render props
在 props上写 render 函数, render 逻辑可以从外面传入进来
```js
<DataProvider render={data => (
  <h1>Hello {data.target}</h1>
)}/>
```

传统方式下,如果获取组件内部 state 状态, 需要通过 ref.
```js
class App  extends React.Component {
  ref = React.createRef();
  
  componentDidMount() {
    // get DataProvider state 
    console.log(this.ref.current.state);
  }

  render() {
    return (
    <DataProvider ref={this.ref}
    );
  }
}
```

通过`render props` 模式,我们可以把组件内部的 state 曝露出去
```js
class DataProvider extends React.Component {
  state = { data: 'some data' };

  render() {
    return (
      <div>{this.props.render(this.state)}</div>
    );
  }
}

// 这样就可以在调用 DataProvider 的地方拿到内部的 state 了
<DataProvider render={state => {// do sth with state.data}} />
```

或者使用 `Functions as Children` 形式
```js
class DataProvider extends React.Component {
  state = { data: 'some data' };

  render() {
    return (
      <div>{this.props.children(this.state)}</div>
    );
  }
}

<DataProvider>
  {state => (
    <div>state data { state.data } in DataProvider</div>
  )}
</DataProvider>
```
