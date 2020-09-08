# 北航换课工具 | BUAA course exchanger

## 简介

这是一个使用 selenium + Python + 一点点 JavaScript 实现的自动退课 / 选课脚本

通过精确到秒的时间控制，它可以让你在非常短的时间内（< 1s）同时完成退课和选课操作

（目前的逻辑换的是一般专业课，但是理论上可以通过修改具体逻辑来达到换任何课程的效果）

## 使用环境（经过验证的测试环境样例）

- python 3.7
- selenium 3.141.0
- chrome 85
- chromedriver for chrome 85

## 使用方法

### step 1

配置好各种环境，注意 `chromedriver` 的路径需要在 `PATH` 中

### step 2

按照 `./exchanger/user_profiles_sample.json` 的内容，在 `./exchanger` 中创建并填写文件 `user_profiles.json`

### step 3

退课端：

```shell
cd {PATH_TO_REPOSITORY}/exchanger
python releaser.py
```

选课端：

```shell
cd {PATH_TO_REPOSITORY}/exchanger
python getter.py
```

