# CisuMusiC 新版知识库复核与生产同步方案（2026-11-23）

## 范围和交付状态

核对本地 cisum-app-new bf096129（含本次尚未提交的“退出回首页”修改）、openclaw 87490a81b0、fullon-kb 测试分支 staging/cisum-app-new-support-20261106 的 9eb0f7b。本轮重点复核三份操作文档与近期新增功能，并检查测试及生产主机配置。不是对所有经济模型、会员权益、正式隐私条款或动态艺人资讯的重新事实审计。

三份操作文档已本地修订，未提交、推送或同步索引。退出回首页和群聊拍摄有客户端版本条件，不得把本地实现直接当作所有已安装版本的行为。保留此前审计的 14 文件范围，未把维护记录放进客服知识库。

## 内容差异及修订

| 项目 | 旧说明 | 当前源码依据与本轮修订 |
| --- | --- | --- |
| 登录入口 | 只有手机号与密码/SMS流程 | 增补验证码登录、Google、iOS Apple；Android 原生不显示 Apple。见 account/presentation/social_login_buttons.dart、login_page.dart、phone_login_page.dart |
| 登录与交易密码 | 未区分登录成功和钱包可用 | 补充交易时设密、换机验证、恢复处理中；不承诺授权即能交易。见 social_wallet_page.dart、phone_login_page.dart |
| 忘记密码 | 一律手机号短信 | 按原身份类型区分手机与 Google/Apple 重新认证。见 social_reset_page.dart、social_login_page.dart |
| 修改密码 | 设置入口始终存在 | 仅已设密且状态可用显示；修改成功仍需重新登录。见 settings/application/change_password_available_provider.dart、reset_password_page.dart |
| 主动退出 | 未明确落点 | 新修改回首页；与改密后回登录分开，注明较早版本差异 |
| 自动翻译 | 没有说明 | 艺人介绍、提供入口的贴文/评论、Vlog评论；可切原文，不承诺视频音轨或所有字幕翻译。见 space_home_page.dart、post_translation_toggle.dart、vlog_detail_page.dart |
| 群聊拍摄 | 没有说明 | 补拍照、最长15秒短视频、权限及版本/资格条件。见 group_attachment_sheet.dart、group_camera_controller.dart |
| 资产入口 | 我的→资产 | 当前源码仍有 cisum-profile-assets，保留；不能因其他 worktree 的删除计划而改写当前版本 |
| 抢票、票券、反馈 | 已按新版修订 | 保留页面流程和当前活动规则限制；反馈描述500字、最多3图不改 |

本轮修改：注册/登录流程、页面操作指南、FAQ。9份背景/历史/权益资料沿用上次的范围限制，2份隐私文件不变。范围提示不构成检索硬隔离，旧资料仍可能干扰操作问题；须用真实检索回归验证。

## 环境核对事实

- 测试：cisum-hk-tc，部署目录 `/mnt/data1/docker-instances`。GitHub 源指向测试分支；supportagent bundle 绑定 `cisumusic`。workspace AGENTS.md 含 Customer-Facing Product Guidance，但实际 bundle prompt 未包含该段。bundle 另有多语言与 RagFlow 演出核验规则，更新时应保留。
- 检查开始时测试 OpenClaw/Qdrant/reranker 容器均不存在；镜像、Compose、`.openclaw`、dense/sparse 的 `qdrant_storage` 都保留。目录存在只证明数据文件尚在，不证明索引可用；恢复启动后需通过 API 检查。
- 生产：prod-ai，运行镜像 `v1.1.4-60c0f53e92ca-8`；GitHub 源为 main。
- 生产 Qdrant registry 的 `cisumusic` 项目有18份文档，无新版页面指南；仍有内部讨论稿、完整项目介绍、归因架构、竞品分析、加密法案5份上次已移出的资料。文档 updated_at 仍为2026-06-09；项目元数据日期不是文档更新日期。
- 生产 supportagent bundle 绑定 `cisumusic-app`，registry 无此项目记录或文档；实际项目是 `cisumusic`。这是配置不一致，需修正并验证实际请求的过滤条件，不能仅凭配置断言所有历史问答均检索失败。
- 生产 workspace 与 bundle 均缺少 Customer-Facing Product Guidance。仅发布源码模板不会自动证明运行中的 bundle 已更新。

## 生产同步步骤

1. **先完成测试验收**：恢复原测试服务；确认registry/dense/sparse均可读。修订文档提交到测试分支后，针对 `cisumusic` 同步，更新运行 bundle 的客户可见指导规则，并验证问答。Git 提交与远端发布作为后续明确执行步骤，本轮未执行。
2. **确定发布内容**：将本轮三份操作文档及9eb0f7b中的历史清理按实际差异合入生产 main；生产应发布已验收内容，不应长期追踪 staging。先读远端 main 的当前内容和差异，不直接整仓覆盖，也不改 FullOn 的 docs 项目。确认新客户端已开放的功能，保留旧版和平台差异。
3. **备份生产**：记录当前镜像、GitHub源、agent bundle、workspace提示词、项目元数据和文件清单；保存 dense、sparse、registry 的可恢复快照。记录当前 main 提交，以便回滚内容。备份包含敏感配置时只存受控服务器，不输出密钥。
4. **修正运行配置**：将生产 supportagent 的知识库 projectKey 对齐实际 `cisumusic`，保留 agentId、support audience和权限。向实际 bundle prompt 合入 Customer-Facing Product Guidance；保留生产及测试已经需要的多语言/动态演出核验规则，不用整份测试配置覆盖生产。
5. **定向同步文档**：使用已认证管理端的 `agents.knowledgeDocuments.syncFromGithub`，参数为 `{"agentId":"supportagent","projectKey":"cisumusic"}`。这是网关 RPC，不是可直接拼接的HTTP接口。执行前确认该生产镜像支持对应方法。不要省略projectKey，否则会同步其他项目。
6. **核对同步结果**：响应 `repository`、`branch`、`revision` 对上发布提交；`failedFiles`为空；新增/更新/跳过文件与14文件清单一致。18旧文件变14：移出5份、加入新版指南1份；确认registry及dense/sparse旧切片均不再返回。同步器会删除目标项目中不在源清单的文档，包括可能的手工上传资料，需先审阅并保留应保留项。
7. **问答验收**：新会话与已有会话，各测简中、繁中、英文，抽查泰文。题目包括Google/Apple支持平台、验证码登录、交易密码、第三方忘记密码、换机恢复、改密、退出首页、艺人/Vlog翻译边界、15秒群聊视频、抢票待确认、积分反馈、资产、H5限制。检查没有内部路径/服务器信息、历史收益承诺或将视频音轨当作已翻译。演出日期另外使用动态来源，不用白皮书推断。
8. **观察与回滚**：记录问题/检索来源/模型回答与时间。回滚需同时考虑文档版本、索引和bundle，不能只回滚App或重启OpenClaw；恢复旧文档时避免重新开放已识别的内部资料。不要从测试复制整个Qdrant库覆盖生产，避免混入其它项目或不匹配的向量/元数据。

## 同步实现要点

`openclaw/extensions/qdrant-kb/api.ts` 的 syncKnowledgeDocumentsFromGithub读取项目目录，统一按项目syncAudience及published上传，再删除目标项目清单外文档。项目清单在 `.openclaw/knowledge-projects.json`。仅在文首标“内部/历史”不会自动排除入库。

`openclaw/src/gateway/knowledge-github-sync-service.ts` 默认周期一小时，以revision跳过未变化源。自动周期不是发布验收；配置/prompt变动但revision不变时也不能只等一小时。同步响应中可能有failedFiles，不能只看顶层ok或日志success。

## 验证边界

本次内容修订使用本地源码核验；生产只读检查。在线问答验收、文档发布、生产配置修改和生产索引同步均未完成，不能表述为已上线修复。此前2026-11-16记录中的“未提交”是当时状态；本地9eb0f7b证明清理已进入当前测试分支，是否入运行索引仍应另核实。

## 测试服务恢复及索引复核结果

已使用原镜像和原挂载重建测试 qdrant-dense、qdrant-sparse、reranker、openclaw-gateway、openclaw-chat-bridgerule；重建被清理的 openclaw_default 网络，并补齐 Compose 标签。未改测试分支指向、未写入本轮文档、未修改生产。

恢复后 registry/dense/sparse 均为 green；对应点数53/354/354（是集合总点数，不是客服文件数）。cisumusic项目为14份文档，之前5份移出材料已不在该项目registry清单中。对现有14份文档逐一比较内容哈希：12份与9eb0f7b一致；登录流程、H3F粉丝圈2份不一致，不能把上次同步视为全部成功。本轮远端只读清单保存在remote-document-inventory.json，修订后的本地14文件哈希在document-sha256.json。

发布前必须让登录流程、H3F以及本轮修改的操作指南/FAQ全部达到目标哈希，不能只检查文件总数或updated_at。

网关与bridge容器健康检查均healthy，reranker healthy，网关首页HTTP 200。登录流程与H3F的远端内容哈希准确匹配9d39f95（上次清理之前），不是仅时间戳偏旧。尚未执行完整用户问答回归。

## 本轮继续完善（用户确认后，2026-11-23）

再次fetch确认远端App最新为2f351383，仅修改商城测试；功能源码与bf096129相同。本地退出回首页修改仍未发布，用户文档保留版本适用条件。

已进一步完成：操作指南的忘记密码入口表格与正文统一；注册文档增加平台/版本适用说明和登录后无法交易的排查步骤；FAQ新增Android Apple入口、第三方交易密码找回、换机恢复待生效、不同身份账号、历史会员权益和背景资料使用6个独立问答。

三份俱乐部资料在各节加入历史适用限制，六份其他背景资料加入明确使用边界；保留原始金额、权益和原文，不把未经运营确认的数字改成新承诺。此次共12份客服文档有修改，2份隐私文档保持逐字不变。仍保留14份文件；未实施历史资料独立项目隔离，范围提示仍不是检索硬过滤。

content-validation.json记录本地校验：3份操作文档无内部路由/主机/源码细节；9份参考资料除新增范围说明外原文保留；2份隐私文档与HEAD逐字一致；6个独立FAQ齐全。document-sha256.json已刷新。

本轮只完善知识库工作区；未提交、推送、写入远端索引或更改运行bundle。运行提示词更新、H3F等索引内容同步、以及多语言新旧会话问答回归仍是发布步骤。
