# 发布到 GitHub

目标仓库：[Davidjijinnu/codex-deepseek-maid-pet](https://github.com/Davidjijinnu/codex-deepseek-maid-pet)。

## 通过 GitHub 连接发布

在 Codex 中安装并连接 GitHub 插件，登录 `Davidjijinnu`，然后让助手继续本次发布。当前本地文件已整理完成；应在确认 GitHub 当前连接状态后创建仓库并推送。

## 自己使用 Git 发布

先在 GitHub 创建名为 `codex-deepseek-maid-pet` 的公开仓库，保持为空，不勾选自动生成 README、LICENSE 或 .gitignore。然后在本项目目录执行：

```bash
git remote add origin https://github.com/Davidjijinnu/codex-deepseek-maid-pet.git
git push -u origin main
```

需要先完成 GitHub 身份验证；不要把访问令牌写入仓库文件。若远程仓库已经存在，应先检查其内容并确认它是本项目的目标仓库。

如使用 ZIP 手动上传，先解压，将里面的项目文件上传到仓库根目录，不要只上传 ZIP。请保留 `ARTWORK_NOTICE.md`、`CREDITS.md` 和代码许可说明。

参考：[GitHub 官方文档：将本地代码添加到 GitHub](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github)。
