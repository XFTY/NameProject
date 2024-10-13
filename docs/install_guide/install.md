# NameProject 安装教程
文章最后更新日期：2024年10月13日

该安装教程将教会您如何快速配置 NameProject 并投入使用。  

## 安装前须知
目前，所有的 NameProject 版本均建议在 **Microsoft Windows** 环境下运行，如果您尝试在 **苹果电脑(Apple MacOS)、Linux** 上运行 NameProject，请你确保您拥有相关知识。  

NameProject 所有版本 **均不支持** 32位操作系统，对于 4.0 及以下版本的NameProject，您可以通过更换 Python 版本来在不支持64位的操作系统上运行 NameProject。

## 第一步：下载 NameProject 发行版

点击 [这里(推荐)](https://github.com/XFTY/NameProject/releases/latest) 访问最新版 NameProject 页面。  
> 如果网页无法打开，您也可以尝试点击 [这里](https://gitee.com/XFTYC/NameProject/releases/latest) 访问 Gitee 国内镜像。

然后，向下滚动页面到最底部，您可以看到 Assets 标签。
>在 gitee 上，您会找到“下载”区域

您会看到有下面3个下载选项：
 - NameProject-3.x.x **.exe**
 - Source code **(zip)**
 - Source code **(tar.gz)**

请点击 **NameProject-3.x.x.exe** 下载 NameProject。  
> 不要点击 Source code 下载，那下载的是源代码！！！是无法运行的！！！

>如果您使用 Gitee 下载 NameProject，您可能需要先注册 Gitee 账号。 


## 第二步：解压文件
> 如果您使用具有安全扫描的浏览器下载此文件，可能会弹出该程序不安全，请您选择继续下载即可。

然后，请将下载好的程序放在您喜欢的位置。
> 可以将下载好的文件放在U盘中，这样您就可以随时随地在任何电脑上使用属于您的 NameProject 。

双击运行软件

点击 **Extract** 按钮，开始解压文件。软件解压完成后窗口会自行消失。

## 第三步：开始配置

解压完成后，在与自解压程序相同的运行目录下，将会多出一个拥有 **NameProject** 字样的文件夹。  
进入该文件夹。

然后，您应该会发现 “ **启动NameProject.exe** ”文件，双击打开文件。

接下来，您可以根据软件安装向导配置 NameProject 。

## 第四步：enjoy🎉🎉🎉

以后，只要您需要使用 NameProject，仅需再次点击“ **启动NameProject.exe** ”文件即可！

## Q&A

》Q: 每次点击“ **启动NameProject.exe** ”文件时，为什么会弹出启动窗口？  
A: 弹出启动窗口是为了让用户选择进入 主程序 还是 设置程序，您可以点击您想进入的窗口进行点名或者设置。

》Q: 为什么我的软件启动时会报错？  
A: 在配置 NameProject 的时候是否曾关闭过窗口？那么安装程序可能会创建一个空的configure.json文件，这个文件和“ **启动NameProject.exe** ”文件在同一运行目录，删除该文件即可恢复正常。

》Q: 我还没启动过一次 NameProject，第一次点击“ **启动NameProject.exe** ”便报错，说什么缺少api-ms-core之类的组件？  
A: 您在使用 Windows 7运行 NameProject 吗？您可能需要更新到 Windows 7 Service Pack 1来解决，  
如果不方便更新，您也可以尝试下载 **dll补全工具** 补全电脑上缺失的运行库。  
当然，我更推荐您在 Windows 10 或 Windows 11 来运行 NameProject。