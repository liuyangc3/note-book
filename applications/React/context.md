# 使用场景
1 dont want props nested between in components.

2 sometimes the `same data` needs to be accessible by many components in the tree and at different nesting levels.
Context lets you “broadcast” such data, and changes to it, to all components below.

# 注意事项
Provider value 不要写成 inline 形式, 否则每次父组件 re-render, value 都会变化, 导致 Consumer 子组件也会 re-render.
```js
// bad
<Provider value={{something: 'something'}}>
  <Toolbar />
</Provider>

// good
<Provider value={this.state.something}>
  <Toolbar />
</Provider>
```

# refs
https://reactjs.org/docs/context.html
