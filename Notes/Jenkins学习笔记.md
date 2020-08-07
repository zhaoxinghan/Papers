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

```groovy
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

```groovy
sleep time:5, unit: 'MINUTES'
```

#### 等待直到(waitUntil)

```groovy
waitUntil { //返回true或false的过程
}
```

### 处理并发

- 可以使用lock对节点的资源加锁
- 使用milestone来控制并发数量
- 使用disableConcurrentBuilds()在多分支流水线中限制并发

在传统的并行语法中，Jenkins可以在空闲的节点或指定的节点中运行parallel步骤。

```groovy
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

#### 获取和保存文件-stash和unstash

stash和unstash函数允许在流水线的节点间和/或阶段间保存和获取文件，通过名称和/或模式来指定一个被包括或被排除的文件的集合，给这些文件的暂存处命名，以便后面通过这个名称使用这些文件。

```groovy
stash name: "<name>" [includes: "<pattern>" excludes: "<pattern>"]

unstash "<name>"  //创建副本
```

一个测试的例子

```groovy
stages("Source") {
    stage("source") {
        git branch: 'test', rul: 'git@diyv:repos/gradle-greetings'
        stash name: 'test-source', includes: 'build.gradle, src/test/'
    }

    ……

    stage("Test") {
        //并行的执行需要的单元测试

        parallel (
            master: {node ('master'){
                unstash 'test-sources'  //这里在master节点上创建副本
                sh '/opt/gradle-2.7/bin/gradle -D test.single = TestExample1 test'
            }}
            worker2: { node ('worker_node2') {
                unstash 'test-sources'
                sh '/opt/gradle-2.7/bin/gradle -D test.single=TestExample2 test'
            }},
        )
    }
}
```

#### 快速失败fastFail

当一个分支失败就快速退出所有步骤时使用fastFail。

使用方法：在parallel的括号的参数中加入`failFast: true`。

### 条件执行

Jenkins中可以使用groovy语言来实现条件执行。

对于脚本式流水线，使用if实现条件执行，其语法规则和java基本一样。

对于声明式流水线，使用when形式来测试一个或者多个表达式模块是否为true,如果为true,阶段中剩下的代码才会执行。

### 构建后的处理

在脚本式流水线，我们可以使用try-catch-finally来实现一系列的执行过程，jenkins还提供了catchError来实现更高级的一些用法。

在声明式的流水线，我们可以通过添加post结构来实现构建后处理。

|条件| 描述|
|--|---|
|always| 总是执行代码中的模块步骤|
|changed| 如果当前构建的状态与先前构建的状态不同，则执行代码块中的步骤|
|success| 如果当前构建状态为成功的，则执行代码块中的步骤 |
|failure| 如果当前构建状态为失败的，则执行代码块中的步骤|
|unstable| 如果当前构建状态为不稳定的，则执行代码块中的步骤|

例子：
```groovy
    }
}   //阶段结尾
post {
    always {
        echo 'build stage complete'
    }
    failure {
        echo 'Build failed'
        mail body: 'build failed', subject: 'build failed', to: 'devops@company.com'
    }
    success {
        echo "build succeeded"
        mail body: 'build succeeded', subject: 'Build Succeeded' to: 'devops@company.com'
    }
}
```

## jenkins里的通知

- 电子邮件
- slack通知
- HipChat通知
- HTML报告

（这一章需要用到的时候在查吧）

## 安全

(同上)

## 声明式流水线

### 传统的脚本式流水线的缺点

1. 传统的Web界面创建脚本是不直观的，页面被分成了不同的部分，虽然不同阶段有不同的元素可用，但是如何将这些元素组装或排序不是非常清晰。
2. 需要掌握Groovy语言，造成额外的学习成本。
3. 为了实现一些熟悉的功能，如发送邮件等，还需要编写一些额外的代码。

### 声明式流水线的结构

#### 代码块

一个代码块实际上指具有开头和结尾的任意一组代码。

#### 部分

声明式流水线的部分是一种方法，用于收集在整个流水线流程的某些特殊点上需要被执行的项目。
主要有三个区域：
|名称|说明|
|-|-|
|stage|定义流水线主体和逻辑的所有但各阶段定义（指令）|
|steps|在一个阶段定义中封装一组DSL步骤。用来吧一系列的步骤与阶段中的其他项目（比如环境定义）分割来|
|posts|这个部分可以封装一些需要被执行的步骤或者检验的条件，可以定义在流水线的结尾或者一个阶段的结尾|

#### 指令

指令可以被认为是可以做任何一下事情的语句或代码块

1. 定义值：比如agent指令，它允许我们指定一个节点或者容器来运行整个流水线或这一个阶段。
2. 配置行为： 好比triggers指令，允许我们配置多长时间一次去检察源码的更新或者触发我们的流水线。
3. 指定要完成的行为： 比如stage指令，往往期望它拥有一个包含那些需要被执行的DSL步骤的steps部分。

#### 步骤

steps部分内部，我们可以合法的使用任何DSL语句。

#### 条件

一个行为应该发生时需要满足的状态或标准。

- when: 它存在与一个stage定义中，用来定义是否这个极端应该被执行的条件。
- conditions代码块： 存在于post部分中，用来定义进行后期处理的条件。这里的标准或条件指的是构建的状态，比如success或failure。

### 构建代码块

![pipeline](/assets/pipline_94xw2z9hh.png)

#### pipeline

流水线必须的，所有其他内容都放在它的闭包里。

#### agent


