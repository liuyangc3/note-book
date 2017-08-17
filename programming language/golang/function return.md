```go
func TestDefer(t *testing.T) {
        
    // return 先返回，defer 再执行 
	test := func() int {
		var result int
		defer func() {
			result += 100
			fmt.Printf("result in defer: %d\n", result)
		}()
		return result + 10
	}
	result := test()
	fmt.Printf("result in return: %d\n", result)

    // 如果返回的是指针类型，defer 就可以修改了值了
    test1 := func() *int {
		var result int
		defer func() {
			result += 100
			fmt.Printf("result in defer: %d\n", result)
		}()
		return &result
	}

	fmt.Printf("result in return: %d\n", *test1())

    // defer 可以修改默认返回值，和返回指针的情况类似
	test2 := func() (result int){
		defer func() {
			result += 100
			fmt.Printf("result in defer: %d\n", result)
		}()
		return
	}
	fmt.Printf("result in return: %d\n", test2())
}
```
结果
```
result in defer: 100
result in return: 0

result in defer: 100
result in return: 100

result in defer: 100
result in return: 100
```
