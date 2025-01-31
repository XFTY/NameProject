# NameProject 5 开发文件
文档最后更新日期：2025/1/31  
Powered by XFTY, 2024  
如果您想阅读英文文档，请访问我们的日志

欢迎来到 NameProject 5 开发文件，这里将存放所有关于 NP5 的源代码。
## 目录
- 介绍
- 文件结构
- 快速开始
- 更多

## 介绍
NameProject 5 是这个点名器项目的第五代产品，如果您想访问历代 NameProject 项目源代码，
请在根目录访问 ```Archive``` 文件夹。

NameProject 5 目前发行的版本均基于 ```Apache License 2.0```协议开源，同时请留意根目录的```NOTICE.zip```文件，
有对该产品使用的补充说明。

## 文件结构
### .mvn 文件
该文件夹用于存放maven的配置文件，包括maven的配置文件、maven的插件配置文件、maven的依赖配置文件等。
### icon 文件
该文件夹用于存放项目图标，包括项目图标、项目图标的PNG格式等。
### src 文件
这里面存放的是 Java 代码和资源文件，点击```java.com.nameproject.nameporject5At```即源代码，点击```resources.com.nameproject.nameporject5At```即资源文件。

## 快速开始
如果您打算对该项目进行二次开发，您可以参阅以下内容：
### 软件要求
   - 集成软件开发工具(IDE): ```IntelliJ IDEA```
   - Java版本：```Java17```及以上版本
### 克隆代码
 先在 Github/Gitee 上下载源代码，然后，使用IntelliJ IEDA打开```NameProject-5```
### 下载依赖
  IntelliJ IDEA 会自动下载依赖，如果您在访问maven镜像时遇到下载速度慢的问题，可以尝试更换镜像源。
  1. 在IDE左边对 ```NameProject-5``` 进行右键，选择 ```Maven```，然后选择 ```创建/打开 settings.xml```。
  2. 输入以下内容后保存，重启IDEA，然后在加载```Maven```项目。
````xml
<?xml version="1.0" encoding="UTF-8"?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
          xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
          xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
    <mirrors>
        <mirror>
            <id>aliyunmaven</id>
            <mirrorOf>*</mirrorOf>
            <name>阿里云公共仓库</name>
            <url>https://maven.aliyun.com/repository/public</url>
        </mirror>
    </mirrors>
</settings>
````
### 运行/编译 项目
#### 首次运行
找到右边的 ```m``` 按钮，这是 Maven，点击后依次展开 ```插件```->```JavaFX```->```javafx:run```点击运行，稍等片刻，窗口弹出及代表运行成功。
#### 入口文件
在左边的```项目```中，依次展开```src```->```main```->```java```->```com.nameproject.nameporject5At```->```NameProjectApplication.java```，双击打开，你可以在 ```start``` 方法中添加你自己的代码。
#### 编译
打开maven，点击后依次展开 ```插件```->```JavaFX```->```javafx:jlink```点击运行，稍等片刻，便会生成target文件。  
进入```bin```文件，找到```app.bat```，即可运行编译后的文件。
