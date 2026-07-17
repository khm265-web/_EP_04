# Seed Audio 1.0 — TXT Block 結構規則

適用範圍：`04_AUDIO/` pipeline 內所有 Seed Audio 1.0 job 的 `.txt` prompt 檔案。

---

## Block 順序（固定）

```
1. REFERENCE BLOCK    (必須放最前)
2. SCENE/STYLE BLOCK  (一次性，定調全場)
3. [SFX BLOCK / DIALOGUE BLOCK] 交替重複...
4. TRANSITION/FREEZE BLOCK (收尾，可選)
5. META/LANGUAGE BLOCK (必須放最尾)
```

---

## 1. REFERENCE BLOCK

```
[Character reference image: {KEY}. Use only to inform the vocal identity and mood — <角色聲音基本描述>. <額外限制說明，例如多角色共用同一 reference 時要點分辨>]
```

- `{KEY}` 對應 `assets.json`：
  - **audio reference** → key 用 `VOICE_` prefix（例如 `VOICE_CHAR_A`），主程式會轉做 `@Audio1` / `@Audio2` / `@Audio3`
  - **image reference** → key 唔用 `VOICE_` prefix（例如 `CHAR_A`），主程式會移除 `{KEY}`（唔用 `@tag` 引用，另外以 `image_url` 傳）
- 必須明確講明 reference「只用嚟做咩」，唔好留白等 model 自由發揮
- 多角色共享同一 reference 時，必須講清楚要靠咩分辨（例如「純靠情緒演繹，唔靠 pitch/timbre」）

---

## 2. SCENE/STYLE BLOCK

```
[<場景類型>. <環境/氣氛描述>. <全局 audio 規則，例如有冇配樂、diegetic-only>.]
```

- 全文一次性出現，唔重複
- 講明全局規則（例如「No music score, diegetic sound only」），避免 model 自行加料

---

## 3a. SFX BLOCK

```
[<音效來源> <動作/狀態>, <可選：情緒/強度連動>]
```

- 短句，方括號包住，穿插喺 dialogue block 之間
- 可講明強度隨對白升溫（例如「grows louder, tied directly to the rising argument」），令 SFX 同 dialogue tension 同步遞增

---

## 3b. DIALOGUE BLOCK

```
SPEAKER (<descriptor1>, <descriptor2>, <descriptor3...>): "<對白內容>"
```

- 每句必須三元素：speaker 名 + 至少 2-3 個情緒/語氣 descriptor + 引號包住嘅對白
- descriptor 建議按情緒推進排列（例如 calm → hardening → nearly shouting），等 model 讀到遞進感
- 對白斷句/cut short 可用「——」表示未完，配合下一個 SFX block 承接

---

## 4. TRANSITION/FREEZE BLOCK（可選）

```
[<收結指令>, <指定邊啲聲音元素受影響>]
```

- 控制場景收尾方式（例如所有聲音同時停）

---

## 5. META/LANGUAGE BLOCK（必須，放最尾）

```
Language: <語言>. <整體表演 summary，講返每個角色嘅情緒弧線>.
```

- 一定要有 `Language:` 聲明（尤其粵語呢類非預設語言，用嚟強化 model 理解）
- 用一兩句總結各角色情緒曲線，等 model 有個宏觀理解

---

## 硬性規則

| 規則 | 說明 |
|---|---|
| 字數上限 | 全文（含所有 block）合計 **不可超過 2048 字元**，長對話要拆做多個 job |
| 禁止negative語言 | 唔可以用 "no X"、"without X"、"avoid X"，全部要正面描述 |
| Reference互斥 | 一個 job 唔可以同時混用 audio reference（`VOICE_`）同 image reference |
| Image reference數量 | 最多 1 張 |
| Audio reference數量 | 最多 3 個（`MAX_AUDIO_REFS`） |
| `{KEY}` 轉換 | audio mode 轉 `@Audio1/@Audio2/@Audio3`；image mode 移除 `{KEY}`（唔用 tag） |

---

## 已知限制

- Image reference 係**推斷式**（vocal personality inference），唔係 fixed 聲紋 lock，同一張圖每次生成可能有音色漂移
- 需要跨 job 穩定一致嘅聲音，應改用 **audio reference**（`VOICE_` key）
- `volume` 參數只控制輸出增益（0.5–2.0），唔應用嚟表達劇情強弱——情緒強度應由 dialogue descriptor 表達
- 冇 `duration` 參數，時長由內容自動生成，上限 2 分鐘

---

## 範例（完整 job）

```
[Character reference image: {CHAR_A}. Use only to inform the vocal identity and mood — a young adult male voice matching this reference. Both MIRROR and PROTAGONIST share this same reference image, since MIRROR is PROTAGONIST's exact visual double; their voices should sound like the same person, distinguished only by emotional performance as directed below — not by pitch or timbre.]

[Cinematic short-film dialogue scene. Surreal collapsing coastal concrete city, pale misty light. No music score, diegetic sound only.]

MIRROR (calm, cold, quietly certain): "你已經留喺呢度太耐，我要帶你返去。"

PROTAGONIST (tense, defensive, voice tightening toward panic): "你到底係邊個！？"

[spinning-top whirr begins rising faintly under the voices]

MIRROR (hardening, sentence accelerating): "童年遊戲係時候要結束。"

[the losing top disintegrates into a brittle clattering scatter]

MIRROR (final line, sharp, nearly shouting): "唔好再逃避現實喇，醒下啦！"

[hard freeze — every sound stops dead on the same frame]

Language: Cantonese. MIRROR: cold, controlled, escalating only at the very end. PROTAGONIST: defensive from the first line, cracking further with each exchange.
```
