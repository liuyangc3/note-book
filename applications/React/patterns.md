# React Patterns
总结一些常见的 React 代码组织模式

## space in variable
变量里无论有多少个空格, 渲染后都是一个
```
var s = 'Hello    World'
<span>{s}</span>
```
out in page
```html
Hello World
```
解决方式:

1 use `&nbsp;`, 但是没法在变量里使用
```html
<span>Hello&nbsp;&nbsp;&nbsp;World</span>
```
2  使用 `\u00A0` 替换空格
```js
var s = 'Hello    World'.replace(/ /g, '\u00A0')
```

## conditionally render
使用条件控制组件渲染
```js
<div>
  {showHeader && <Header />}
  <Content />
</div>
```
因为 `{}` 内的 boolean, null, undefined 类型的变量不会被渲染

## render props
在 props上写 render 函数, render 逻辑可以由父级组件控制, 其的参数可以是组件内部的数据
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

## debounce
例如下面的组件,用户每次在 input 输入后,会从后台搜索用户的输入,并将结果展示出来
```
class Search extends React.Component {
  state = { 
    value: '',
    result: ''
  };
  
  handleChange = e => {
    const vaule = e.target.value;
    this.setState({ value });
    
    fetch('/api/search')
    .then(
      resp => resp.json
    ).then(
      result => this.setState({ result });
    );
  }
  
  render() {
    return (
      <input value={this.state.value} onChange={this.handleChange} />
      <span>{this.state.result}</span>
    );
  }
}
```
每次输入产生变化就取后端搜索性能很低,会有大量请求, 比如我想用户输停止输入 1s后 再去后台搜索,应该如何做?

```js
function debounce(func, wait) {
  let timer;
  return function () {
    const context = this;
    const args = arguments;

    // 每次函数调用时清除定时器
    // 这样 timer 里的 func
    // 在超时前就不会正真被执行
    clearTimeout(timer);

    return new Promise((resolve, reject) => {
      // 重新设置新的定时器
      timer = setTimeout(() => {
        timer = null;
        resolve(func.apply(context, args));
      }, wait);
    });
  };
};
```
每1s内只会请求后端1次
```js
const debouncedFetch = debounce(fetch, 1000);
handleChange = e => {
  const vaule = e.target.value;
  this.setState({ value });

  debouncedFetch('/api/search')
  .then(
    resp => resp.json
  ).then(
    result => this.setState({ result });
  );
}
```
不想自己实现的话, 可以使用 lodash 的 debounce 函数
