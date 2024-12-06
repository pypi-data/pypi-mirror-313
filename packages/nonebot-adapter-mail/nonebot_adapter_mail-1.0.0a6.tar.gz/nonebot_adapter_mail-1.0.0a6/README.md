<!-- markdownlint-disable MD033 MD041 -->
<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" alt="nonebot-adapter-mail"></a>
</p>

<div align="center">

# NoneBot-Adapter-Mail

<!-- prettier-ignore-start -->
<!-- markdownlint-disable-next-line MD036 -->
_✨ Mail Adapter ✨_
<!-- prettier-ignore-end -->

<p align="center">
  <a href="https://raw.githubusercontent.com/mobyw/nonebot-adapter-mail/master/LICENSE">
    <img src="https://img.shields.io/github/license/mobyw/nonebot-adapter-mail" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-adapter-mail">
    <img src="https://img.shields.io/pypi/v/nonebot-adapter-mail" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.9+-blue" alt="python">
  <a href="https://results.pre-commit.ci/latest/github/mobyw/nonebot-adapter-mail/master">
    <img src="https://results.pre-commit.ci/badge/github/mobyw/nonebot-adapter-mail/master.svg" alt="pre-commit" />
  </a>
</p>

</div>

## 配置

修改 `.env` 或 `.env.*` 文件以配置 Mail 适配器。

### MAIL_BOTS

- `id`: 电子邮件地址
- `name`: 显示名称
- `password`: 登录密码
- `subject`: 默认邮件主题
- `imap`: IMAP 配置
  - `host`: IMAP 主机
  - `port`: IMAP 端口
  - `tls`: 是否使用 TLS
- `smtp`: SMTP 配置
  - `host`: SMTP 主机
  - `port`: SMTP 端口
  - `tls`: 是否使用 TLS

配置示例：

```dotenv
MAIL_BOTS='
[
  {
    "id": "i@example.com",
    "name": "Name",
    "password": "p4ssw0rd",
    "subject": "Sent by NoneBot",
    "imap": {
      "host": "imap.example.com",
      "port": 993,
      "tls": true
    },
    "smtp": {
      "host": "smtp.example.com",
      "port": 465,
      "tls": true
    }
  }
]
'
```

## 适配器默认行为

- 邮件主题按以下优先级解析：
  1. 调用发送时传入的 `subject` 参数
  2. 消息中的 `MessageSegment.subject` 段
  3. 回复时使用 `Re: 原邮件主题`
  4. 使用配置中的默认 `subject`
- 发送函数可选参数：
  - `cc`: 抄送列表
  - `bcc`: 密送列表
  - `subject`: 邮件主题
  - `in_reply_to`: 所回复的邮件的 Message ID
  - `references`: 邮件线程中的邮件 Message ID 列表
  - `reply_to`: 接收方回复邮件时的默认地址列表
- 发送函数中未指定 `references` 但已指定 `in_reply_to` 时，`references` 默认设置为 `in_reply_to`
- 快捷发送函数 `bot.send` 的 `reply=True` 时的配置：
  - `subject` 未指定时使用 `Re: 原邮件主题`
  - `in_reply_to` 未指定时使用原邮件的 Message ID
  - `references` 未指定时使用原邮件的 Message ID
- 消息中含有多个 `MessageSegment.subject` 或 `MessageSegment.reply` 时，只取第一个
