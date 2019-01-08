 
# Thinking in React

## React 本质是什么?

例如页面上实现一个天气的小组件
```html
<div>
  <h1>你好, 刘洋</h1>
  <h2>今天北京的平均气温是25℃</h2>
</div>
```

如果希望, 不同地区的用户展示当地的天气, 把变化的数据抽离出来
```js
{ "username": "刘洋", "location": "北京", "temperature": 25 }
```

剩下的是不变展示的部分, 用一个函数来表示
```
fuction Temperature(props) {
  return (
    <div>
      <h1>你好, {props.user}</h1>
      <h2>今天{props.location}的平均气温是{props.temperature}℃</h2>
    </div>
    );
}
```
展示天气的时候传入数据即可
```
const props = { "username": "刘洋", "location": "北京", "temperature": 25 }
Temperature(props)

// JSX
<Temperature username="刘洋" location="北京" temperature="25" />
```
实现了 data 与 view 的分离, 提高了抽象程度
