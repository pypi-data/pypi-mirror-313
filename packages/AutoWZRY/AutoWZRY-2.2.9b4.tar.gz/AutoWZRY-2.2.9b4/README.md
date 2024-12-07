# AutoWZRY

* 此项目用于将 WZRY 子模块发布到 AutoWZRY@PyPI。

* 仅用于镜像WZRY的代码, 用于在无法访问github的情况下获取WZRY代码.

## 没有发布独立PyPI模块的计划
* 一堆要改的, 太麻烦了

## 构建发布过程
### 初始化仓库
[添加 WZRY 子模块](how_to_use_submodule.md)


### clone仓库
```
git clone --recurse-submodules  git@github.com:cndaqiang/AutoWZRY.git
```

### 更新代码
```
bash pull.sub.sh
```
### 发布
```
./build.ps1
```