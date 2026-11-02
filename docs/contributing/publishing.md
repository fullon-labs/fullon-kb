# 文档维护与 GitHub Pages 发布

## 本地预览

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-docs.txt
python scripts/check_docs.py
mkdocs build --strict
mkdocs serve
```

`mkdocs.yml` 管理导航、主题和搜索。正文只维护 `docs/` 的 Markdown 文件；不要手改生成的 `site/`。

## GitHub Pages

1. 在仓库 Settings → Pages 选择 **GitHub Actions** 为来源。
2. 提交文档改动并发起 PR；Documentation 工作流会检查链接并严格构建。
3. 合并到 `main` 后工作流构建并上传 Pages artifact，再部署到 `github-pages` 环境。
4. 在 Actions 查看构建和部署结果；以部署步骤返回 URL 为准。

默认站点地址：[fullon-labs.github.io/fullon-kb](https://fullon-labs.github.io/fullon-kb/)。此链接是配置目标，是否已发布应以实际部署结果为准。

## 目录约定

- `01_Core_Chain/`：通用概念与规格。
- `06_User_Guides/`：面向终端用户的操作。
- `10_Developer_Guides/`：开发教程与节点入门。
- `03_Operators/`：深入 RPC 与节点参考，保留已有链接。
- `04_FAQ/`：短答、官方 FAQ 整合记录。
- `contributing/`：维护、核验与发布。

新增页面后更新导航和相关指南。尚未核验的参数明确标注，不填猜测值。

## 中英文维护

中文使用原 `.md`，英文使用同目录同名 `.en.md`。两种语言都链接规范 `.md` 路径，由构建器解析到当前语言。不要在正文硬编码 `/en/`；代码、字段、来源版本和核验范围应保持一致。新增页面须同步提供双语版本。

`mkdocs build --strict` 会生成双语并分别建立搜索索引。发布前运行 `python scripts/check_bilingual_site.py`，验证覆盖、切换链接、搜索隔离和站内资源。
