# 北航教务工具集 | BUAA JW Utils

## 简介

这是一个使用 selenium + Python + 一点点 JavaScript 实现的北航教务工具集

## 使用环境

- python 3.7
- selenium
- chromedriver & chrome

## 工具列表

- 自动评教工具 [autoscore](https://github.com/APassbyDreg/BUAA_JW_utils/tree/master/autoscore)
- 自动换课工具 [exchanger](https://github.com/APassbyDreg/BUAA_JW_utils/tree/master/exchanger)

---

## 自动评教工具

解放双手，让脚本为你评教

提供了三种模式：
- 彩虹屁：评分最高
- 祖安人：评分最低
- 猴：在前三项中随机选择评分

### step 1

配置好各种环境，注意 `chromedriver` 的路径需要在 `PATH` 中

### step 2

按照 `./autoscore/user_profiles_sample.json` 的内容，在 `./autoscore` 中创建并填写文件 `user_profiles.json`

### step 3

```shell
cd {PATH_TO_REPOSITORY}/autoscore
python autoscore.py
```

---

## 自动换课工具

通过精确到秒的时间控制，它可以让你在非常短的时间内（< 1s）同时完成退课和选课操作，降低被其他脚本截胡的可能（目前的逻辑换的是一般专业课，但是理论上可以通过修改具体逻辑来达到换任何课程的效果，欢迎有能 MAN 改进，提 pull request 或咨询我本人均可）

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

### 注意事项

- 脚本有风险，使用需谨慎
- 为了您的人身安全着想，请勿将本代码修改为自动抢课脚本，这是不道德的行为
- 脚本使用过程中可能出现卡在某个网页没加载出来的情况，请注意关注运行情况
