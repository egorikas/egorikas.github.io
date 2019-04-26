---
title:  "Using goroutines on loop iterator variables can hurt"
description: "Using goroutines on loop iterator variables can lead to painfull behaivor of the program."
modified: 2019-04-26T12:20:00-03:00
tags:
  - go
  - goroutines
  - concurrent programming
---


Hi everyone! Today I want to share some personal experience about painfull behaivor of a program, If you're mistaken in using goroutines on loop iterator.
Last 9 months I work with `Go` as a primary programming language. Today, I saw method with this common mistake and decided to write an article about it.

## What is the problem?
When you are itterating collection in Go, sometimes you are calling the result of itterating in gorutine. For example, you might write something like this:

```go
items := []string{"first", "second", "third"}

for _, item := range items {
	go func() {
		println(item)
	}()
}
```

If you run the example, it is highly possible, the output will be :
```
third
third
third
```

It's not an expected result, you might say. it happens due to `item` variable is actually a single variable. When we are itterating through a slice, each element of it, just is put to `item` variable. Because the closures (`println(item)`) just bound the variable, there is a change that when you are running the code, you will see `third`, because this is a last element of the slice, and `for loop` works a bit faster then running `gorutines`. Usually gorotines are run after finishing itterating through small collections. When it happens, we will have an unexpected behaviour of our programms.


The better way to write that type of a loop is:

```go
items := []string{"first", "second", "third"}

for _, item := range items {
	go func(item string) {
		println(item)
	}(item)
}
```

If you run the example, it is highly possible, the output will be :
```
first
third
second
```

When we add `item` as a parameter to the close, `item` is bound by closure on every iteration and every goroutine has its own `item`, that is placed on the stack of every goroutine.
Also, it's important that order of output isn't consistent, because ordering of `goroutines` isn't guaranteed. 

## Additional info

For more info you can read [this](https://github.com/golang/go/wiki/CommonMistakes) and [that](https://www.calhoun.io/5-useful-ways-to-use-closures-in-go/)

## Conclusion

That’s all, thank you for you attention!
