context 用来结束 goroutine，一般 用于goroutine 里嵌套 goroutine 的情况，避免 memory leak  

结束方式使用 select
```go
// goroutine 传入 ctx
select {
    case <-ctx.Done():
        // do some clean...
}
```

```go
func TestContext(t *testing.T) {
	var wg sync.WaitGroup
	ctx, cancel := context.WithCancel(context.Background())

	wg.Add(2)
	
	// 第一个 goroutine
	go func(ctx context.Context, id int) {
		defer wg.Done()
		fmt.Printf("worker : %d  begin work\n", id)
		select {
		case <-ctx.Done():
			fmt.Printf("worker: %d canceled\n", id)
		case <-time.After(3 * time.Second):
		    // do work
			fmt.Printf("worker : %d end work\n", id)
		}
	}(ctx, 1)

    // 第二个 goroutine
	go func(ctx context.Context, id int) {
		defer wg.Done()
		fmt.Printf("worker : %d  begin work\n", id)

		subctx, _ := context.WithCancel(ctx)
		// 第三个 goroutine
		go func(ctx context.Context, id int) {
			fmt.Printf("worker : %d  begin work\n", id)
			cancel()  // 结束所有 goroutine
			fmt.Printf("run cancel in worker : %d\n", id)
			select {
			case <-ctx.Done():
			    fmt.Printf("worker: %d canceled\n", id)
			}
		}(subctx, 3)

		select {
		case <-ctx.Done():
			fmt.Printf("worker: %d canceled\n", id)
		case <-time.After(3 * time.Second):
			fmt.Printf("worker : %d end work\n", id)
		}
	}(ctx, 2)
	
	wg.Wait()
}
```
输出如下
```
worker : 2  begin work
worker : 1  begin work
worker : 3  begin work
run cancel in worker : 3
worker: 3 canceled
worker: 1 canceled
worker: 2 canceled
```
可以看到当在 goroutine 3 里运行 cancel 后， 所有 goroutine 都结束了， 



# 细节

context 包提供了4个方法:
* WithCancel 返回一个 cancelCtx 类型的 Context
* WithDeadline 返回一个 timerCtx 类型
* WithTimeout 是 WithDeadline 的特殊形式
```go
func WithTimeout(parent Context, timeout time.Duration) (Context, CancelFunc) {
	return WithDeadline(parent, time.Now().Add(timeout))
}
```
* WithValue

前3个方法通过传入父节点创建子节点，都会返回一个 CancelFunc

调用 parent context 的 CancelFunc 会通调用所有子 context cancel


cancelCtx 结构
```go
type canceler interface {
	cancel(removeFromParent bool, err error)
	Done() <-chan struct{}
}

// cancelCtx 同时实现了 canceler 和 Context 接口
type cancelCtx struct {
	Context

	done chan struct{} // closed by the first cancel call.

	mu       sync.Mutex
	children map[canceler]struct{} // set to nil by the first cancel call
	err      error                 // set to non-nil by the first cancel call
}

//  timerCtx 是 cancelCtx 的包装
type timerCtx struct {
	cancelCtx
	timer *time.Timer // Under cancelCtx.mu.

	deadline time.Time
}

// valueCtx 是 Context 包装
type valueCtx struct {
	Context
	key, val interface{}
}
```

WithCancel 函数
```go
type CancelFunc func()
// WithCancel returns a copy of parent with a new Done channel. The returned
// context's Done channel is closed when the returned cancel function is called
// or when the parent context's Done channel is closed, whichever happens first.
//
// Canceling this context releases resources associated with it, so code should
// call cancel as soon as the operations running in this Context complete.
func WithCancel(parent Context) (ctx Context, cancel CancelFunc) {
	// 首先构造一个 cancelCtx 函数原型
	//func newCancelCtx(parent Context) cancelCtx {
 	//return cancelCtx{
 	//	Context: parent,
 	//	done:    make(chan struct{}),
 	//}}
	c := newCancelCtx(parent)


	//  	
	propagateCancel(parent, &c)
	return &c, func() { c.cancel(true, Canceled) }
}
```


# 其他
当不确定使用 context 做什么，仅仅是占用参数，可以先传 context.TODO 


