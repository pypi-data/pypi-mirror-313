<!-- markdownlint-disable MD033 MD041 -->

<p align="center">
  <a href="https://nonebot.dev/"><img src="https://github.com/nonebot/nonebug/raw/master/assets/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

# NoneBug

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_✨ NoneBot2 测试框架 ✨_
<!-- prettier-ignore-end -->

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/nonebot/nonebug/master/LICENSE">
    <img src="https://img.shields.io/github/license/nonebot/nonebug" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebug">
    <img src="https://img.shields.io/pypi/v/nonebug" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.9+-blue" alt="python">
  <a href="https://codecov.io/gh/nonebot/nonebug">
    <img src="https://codecov.io/gh/nonebot/nonebug/branch/master/graph/badge.svg?token=LDK2OFR231"/>
  </a>
  <br />
  <a href="https://jq.qq.com/?_wv=1027&k=5OFifDh">
    <img src="https://img.shields.io/badge/qq%E7%BE%A4-768887710-orange?style=flat-square" alt="QQ Chat">
  </a>
  <a href="https://t.me/botuniverse">
    <img src="https://img.shields.io/badge/telegram-botuniverse-blue?style=flat-square" alt="Telegram Channel">
  </a>
  <a href="https://discord.gg/VKtE6Gdc4h">
    <img src="https://discordapp.com/api/guilds/847819937858584596/widget.png?style=shield" alt="Discord Server">
  </a>
</p>

<p align="center">
  <a href="https://nonebot.dev/docs/best-practice/testing/">文档</a>
</p>

## 安装

本工具为 [pytest](https://docs.pytest.org/en/stable/) 插件，需要配合 pytest 异步插件使用。

```bash
poetry add nonebug pytest-asyncio -G test
# 或者使用 anyio
poetry add nonebug anyio -G test
```

```bash
pdm add nonebug pytest-asyncio -dG test
# 或者使用 anyio
pdm add nonebug anyio -dG test
```

```bash
pip install nonebug pytest-asyncio
# 或者使用 anyio
pip install nonebug anyio
```
