# Git在添加目录时遇到了Fatal: unpopulated submodule的解决办法

今天，在把以前的一个目录整体拷贝到git的目录下时，在add的时候遇到了报错，提示unpopulated submodule的信息，无法添加。后来经过查证，可以采用如下的方法解决.

针对提示的目录papers

```bash
git rm -rf --cached Papers
git add Papers/* 
```

问题完美解决。