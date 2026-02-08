# 🔄 Sync Ollama Models Helper

Automatická synchronizace Ollama modelů do OpenClaw konfigurace.

## Použití

```bash
cd ~/.openclaw/workspace/scripts
./sync-ollama-models.sh
```

## Co dělá

1. ✅ Získá seznam všech lokálních Ollama modelů (`ollama list`)
2. ✅ Zobrazí aktuální OpenClaw konfiguraci
3. ✅ Zeptá se, jestli chceš synchronizovat
4. ✅ Vytvoří kompletní model config (včetně context window, max tokens)
5. ✅ Odešle config patch na gateway API
6. ✅ Gateway se automaticky restartuje

## Automatická detekce

Skript rozpozná:
- **Qwen modely** → 32K context
- **Llama Vision** → 131K context  
- **Standard Llama** → 32K context
- **Cloud modely** (`:cloud` suffix) → zachová původní config

## Příklad výstupu

```
🔍 Zjišťuji Ollama modely...
📋 Dostupné Ollama modely:
     1	qwen2.5:14b
     2	qwen2.5:7b
     3	llama3.2-vision:11b
     4	kimi-k2.5:cloud

📝 Aktuální OpenClaw konfigurace:
  - kimi-k2.5:cloud (Kimi K2.5 Cloud)
  - qwen2.5:7b (Qwen 2.5 7B (Local))

🔄 Chceš synchronizovat všechny Ollama modely do OpenClaw? (y/n)
y
  ✅ Přidán: qwen2.5:14b
  ✅ Přidán: qwen2.5:7b
  ✅ Přidán: llama3.2-vision:11b
  ℹ️  Přidávám cloud modely...
📤 Odesílám config patch na gateway...
✅ Konfigurace aktualizována!
🔄 Gateway se restartuje...
✨ Hotovo! Nové modely jsou k dispozici.
```

## Kdy použít

- Po `ollama pull <nový-model>`
- Po update existujících modelů
- Když chceš vyčistit konfigurace nepoužívaných modelů
- Po přeinstalaci Ollama

## Poznámky

- Cloud modely (`:cloud`) jsou zachovány
- Gateway se automaticky restartuje
- Fallback chain zůstává nezměněna (musíš upravit ručně nebo přes `gateway config.patch`)
