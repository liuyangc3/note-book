```go
type canceler interface {
	cancel(removeFromParent bool, err error)
	Done() <-chan struct{}
}

// cancelCtx 实现了 canceler 接口
type cancelCtx struct {
	Context

	done chan struct{} // closed by the first cancel call.

	mu       sync.Mutex
	children map[canceler]struct{} // set to nil by the first cancel call
	err      error                 // set to non-nil by the first cancel call
}

func (c *cancelCtx) Done() <-chan struct{} {
	return c.done
}




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



