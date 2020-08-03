# Jenkins学习笔记
[TOC]

《Jenkins2 权威指南》学习笔记

## 基础

### 语法

#### 脚本式流水线和声明式流水线

1. 脚本式流水线：在流水线中定义逻辑和程序流程，更依赖于Groovy语言和结构
2. 声明式流水线：代码被编排在段落中，这些流水线的主要区域声明了我们所期望的流水线的状态和输出。

#### 系统：主节点、节点、代理节点、执行器


- 主节点（master）：是一个实例（instance）的主要控制系统，能够访问所有配置选项和任务。如果没有指定其他系统，也是默认的任务执行节点。**不要在主节点安排高负载任务**
- 节点（node）：代表了任何可以执行jenkins任务的系统，包含主节点和代理节点，也可以是一个容器Docker。
- 代理节点（agent）：早期版本被称为从节点（slave），代表了非主节点的系统。由主节点管理，按需分配执行执行特定的任务。例如可以分配不同的代理节点针对不同的操作系统执行构建任务，或者并发的运行测试任务。代理节点在节点上运行。在脚本式流水线中，节点特指开一个运行代理节点的系统，而在声明式流水线中，其指代一个特定的代理节点来分配节点。

> note和agent除了语法之外，区别并不是很明显，只要知道note用于脚本式流水线，而agent用于声明式流水线。

- 执行器（execute）：执行器是节点\代理节点执行任务的一个插槽。一个节点可以由任意多的执行器，其数量定义了节点并发任务的数量。当主节点分配任务时，该节点必须有空余的执行器插槽来执行该任务，否则就会被挂起。

#### DSL和Groovy

Jenkins的流水线DSL基于Groovy语言实现。

声明式流水线禁止使用定义结构之外的几乎所有的Groovy代码。

#### 节点（node）

节点在```管理jenkins -> 管理节点```中定义。node的参数为节点的**标签**，后边的代码为该标签的节点下运行的任务。如果忽略名称，则在第一个有效的执行器下运行。
节点的标签可以使用逻辑运算符来定义多个属性，例如
```groovy
node("linux && east")
```
#### 阶段（stage）

只是用于描述，本质上并没有做什么事情。

#### 步骤（step）

实际的DSL命令，是最基本的功能。它不是groovy命令，但是可以和它搭配使用。

*如果命令的参数只有一个，则可以省略参数名称* 

> 总结： 一个节点包含若干阶段，一个阶段包含若干步骤

## 流水线执行流程

### 触发任务

#### 触发条件

- 如果是脚本式流水线，则在代码中指定一个properties代码块定义触发条件
- 如果是声明式流水线，通过triggers指令定义触发类型

#### 在其他项目构建后构建

比如一个脚本式流水线，在任务Job1成功后构建你的流水线，语法如下：

```groovy
properties([
    pipelineTriigers([
        upstream(
            threshold: hudson.model.Result.SUCCESS,
            upstreamProjects: 'Job1'
        )
    ])
])
```
#### 周期式构建

提供了一种cron类型的功能，可以按照某个时间间隔启动任务。

脚本流水线——周一到周五上午9点运行

```groovy
properties([pipeineTriggers([cron('0 9 * * 1-5)])])
```

声明式流水线

```groovy
triggers{ cron(0 9 * * 1-5)}
```

这里的五个字段分别代表分钟，小时，日，月，一周中的第几天。

`*/<value>`代表`每隔<value>`，例如`*/5`代表每隔5分钟。

符号H可以用于任何字段，表示使用项目名称的散列值计算出唯一的偏移量，这个偏移量与番位的最小值相加后，用于定义范围内的实际执行时间。

```groovy
//在每小时前半个小时的某个时间点启动流水线
triggers{cron(H(0,30) * * * *)}
```
cron还有很多高级用法，真正用到的时候在查吧。

#### 使用GitHub钩子触发器来触发构建

如果代码源是GitHub项目，那么可以在GitHub上设置推钩来触发项目构建。当设置好后，当有代码推送到代码库就会发射推钩触发Jenkins，从而调用Jenkins SCM轮询功能。

脚本中的属性语法如下：
```groovy
properties([pipelineTriggers([githubPush()])])
```

#### SCM轮询功能

周期性的扫描源码版本控制系统，如果发现更新，就会处理这些变化。

```groovy
properties([pipelineTriggers([pollSCM('*/30 * * * *')])])
```

#### 静默期

构建触发到执行之间的等待时间

#### 远程构建触发

访问特定的URL来触发构建

### 输入

任务可以根据用户输入改变其行为
（具体的参数设置用到的时候在查吧）

### 流程控制

#### 超时（TimeOut）

限制某个行为发生时脚本花费的时间。

```groove
node {
    def response
    stage('input') {
        try {
            timeout(time:10, unit:'SECOND') {
                response  = input message :'USER',
                parameters:[string(defaultValue: 'user1',
                description:'Enter Userid:', name:'userid')]
            }
        }
        catch (err) {
            response = 'user1'
        }
    }
}
```
#### 重试（retry）

将代码有异常发生时，重试的闭包代码会发生n次。

#### 睡眠(sleep)

```groove
sleep time:5, unit: 'MINUTES'
```

#### 等待直到(waitUntil)

```groove
waitUntil { //返回true或false的过程}
```

### 处理并发

- 可以使用lock对节点的资源加锁
- 使用milestone来控制并发数量
- 使用disableConcurrentBuilds()在多分支流水线中限制并发

在传统的并行语法中，Jenkins可以在空闲的节点或指定的节点中运行parallel步骤。

```groove
node('worker_node1') {
    stage("parallel Demo") {
        //并行的运行步骤

        //用于存储步骤的映射
        def stepToRun = [:]

        for (int i =1; i <5; i++) {
            stepsToRun["steps{i}"] = {node {
                echo "start" sleep 5
                echo "done"
            }}
        }
        //这里才是真正的并行运行开始
        //以一个映射作为参数
        parallel stepsToRun
    }
}
```



