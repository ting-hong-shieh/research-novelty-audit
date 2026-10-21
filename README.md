# Research Novelty Audit — 多代理、現象導向的文獻查新 Skill

**目的：** 幫研究者回答「這個現象是否早有研究？既有文獻解釋了哪些部分？我們真正能貢獻什麼？下一個最便宜、能推翻假設的實驗是什麼？」

**狀態：v0.1 experimental（尚未以實際科研題目完成端到端驗證）。**

這是一個符合 [Agent Skills 標準](https://agentskills.io/specification) 的原創流程包，不是自動發布論文的工具，也不保證論文具原創性。預設輸出繁體中文，保留英文論文名稱。

## 結構

- `SKILL.md`：研究流程、何時派出子代理、成本及證據守則。
- `references/search-protocol.md`：檢索、證據強度與停止規則。
- `references/subagent-contract.md`：子代理工作契約與回報格式。
- `assets/research-brief-template.md`：研究問題輸入範本。
- `assets/novelty-audit-template.md`：包含「Closest Prior Work / Known Findings / Research Gap / Claimed Contribution / Strongest Objection / Fallback Contribution」的完整結果範本。
- `agents/claude/`、`agents/codex/`：四個分工明確的子代理定義；**僅有 SKILL.md 不會自動配置這些自訂代理**，需使用安裝程式或手動複製。
- `scripts/install.py`：安裝到個人或目前專案的適當目錄；預設不覆蓋使用者檔案。
- `scripts/validate_report.py`：檢查報告的基本結構（**不會驗證論文真實性**）。

## 安裝（GitHub）

先將倉庫複製到本機，再從倉庫的上層目錄執行安裝程式：

```bash
git clone https://github.com/ting-hong-shieh/research-novelty-audit.git
python research-novelty-audit/scripts/install.py --platform both --scope user
```

可用 `--dry-run` 先檢查安裝位置。預設不覆寫已存在且內容不同的檔案；如需更新已有的 Skill，先確認差異再使用 `--force`。

或僅安裝在目前專案：

`python research-novelty-audit/scripts/install.py --platform claude --scope project --project-dir /path/to/repo`

`python research-novelty-audit/scripts/install.py --platform codex --scope project --project-dir /path/to/repo`

安裝位置：

| 系統 | Skill | 自訂子代理 |
|---|---|---|
| Claude Code | `~/.claude/skills/research-novelty-audit/` 或 `.claude/skills/...` | `~/.claude/agents/novelty-*.md` 或 `.claude/agents/...` |
| Codex | `~/.agents/skills/research-novelty-audit/` 或 `.agents/skills/...` | `~/.codex/agents/novelty_*.toml` 或 `.codex/agents/...` |

關於兩個平台的具體規則，請以官方文件為準：[Claude Code skills](https://code.claude.com/docs/en/skills)、[Claude Code subagents](https://code.claude.com/docs/en/sub-agents)、[Codex skills](https://developers.openai.com/codex/skills)、[Codex subagents](https://developers.openai.com/codex/subagents)。如 agent 目錄是第一次建立，可能需要重新啟動 Claude Code 工作階段才會載入。Codex 如被禁用多代理功能需先調整設定。**請勿對不明來源 Skill 任意執行安裝程式**。

## 使用

Claude Code：

```text
/research-novelty-audit 我想研究 LLM coding agent 在大型 repository 上的失敗原因。請用 standard 模式，派出真正的子代理調查最近的 closest prior work、跨領域文獻與反對證據。驗證最接近的五篇論文，最後交付 Novelty Audit 六問題表，以及兩個能區分競爭假說的實驗。不要把假說寫成已證實的發現。
```

Codex（若技能顯示在你的技能選單，也可明確指名）：

```text
Use the research-novelty-audit skill for the following phenomenon, spawn independent native subagents for closest prior art, cross-domain search, and red-teaming, then verify the strongest source claims separately. Return the final audit in Traditional Chinese. [填入研究問題]
```

可以不安裝自訂 agent 定義而使用本 Skill：若執行環境有原生 subagents，Orchestrator 仍可給原生代理不同任務；如果沒有，則順序執行各角色，並明確註明**沒有真正派出子代理**。

## 省錢原則

1. 先檢索標題、摘要、引用關係，再精讀最相關的全文；不要讓每個代理完整重複全部工作。
2. `quick` 作初篩；只對有潛力的題目進入 `standard`；投稿前才用 `deep`。
3. 多個代理同時支持某個論文，不代表有多份獨立證據。最終以**可查證的原始來源**為準。
4. 子代理通常增加 token/工具用量；本套件只**規定工作預算**，不含付費模型費用，也不會自動購買資料。

## 驗證

```bash
cd research-novelty-audit
python -m unittest discover -s tests -v
```

這只檢查安裝程式的安全性、複製與重複執行，不會驗證學術資料，也不等同完整端到端實驗。

## 授權與來源

這個工作流程是獨立撰寫的範本，參考：

- https://github.com/yananlong/codex-skills/tree/main/research/research-novelty-review
- https://github.com/xingtaxueshu/literature-review-skills
- https://github.com/llv22/AutoResearchWithEyes/blob/main/skills/novelty-check/SKILL.md
- https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/literature-review

未複製上述專案的 Skill 正文或程式碼。套件中的示例情境僅為**假說**，不是對特定論文的已完成檢索。驗證方式請見 `scripts/validate_report.py`。
