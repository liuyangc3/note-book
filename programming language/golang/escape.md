reflect 包里有个 escapes 函数，让变量逃逸到 heap
```
func ValueOf(i interface{}) Value {
	if i == nil {
		return Value{}
	}

	// TODO(rsc): Eliminate this terrible hack.
	// In the call to unpackEface, i.typ doesn't escape,
	// and i.word is an integer.  So it looks like
	// i doesn't escape.  But really it does,
	// because i.word is actually a pointer.
  escapes(i)
  
  
  // TODO: Maybe allow contents of a Value to live on the stack.
	// For now we make the contents always escape to the heap. It
	// makes life easier in a few places (see chanrecv/mapassign
	// comment below).
	escapes(i)

	return unpackEface(i)
}
...
// Dummy annotation marking that the value x escapes,
// for use in cases where the reflect code is so clever that
// the compiler cannot follow.
func escapes(x interface{}) {
	if dummy.b {
		dummy.x = x
	}
}

var dummy struct {
	b bool
	x interface{}
}
```


```golang
// Note: some of the noescape annotations below are technically a lie,
// but safe in the context of this package. Functions like chansend
// and mapassign don't escape the referent, but may escape anything
// the referent points to (they do shallow copies of the referent).
// It is safe in this package because the referent may only point
// to something a Value may point to, and that is always in the heap
// (due to the escapes() call in ValueOf).

//go:noescape
func chanrecv(ch unsafe.Pointer, nb bool, val unsafe.Pointer) (selected, received bool)
```

https://utcc.utoronto.ca/~cks/space/blog/programming/GoReflectEscapeHack
