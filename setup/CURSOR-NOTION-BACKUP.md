# Záloha znalostí - Notion a Google Drive integrace

**Datum vytvoření:** 2026-01-05  
**Verze:** 1.0  
**Aktuální stav:** Všechny skripty jsou aktualizované a funkční

---

## 📋 Obsah

1. [Přehled systému](#přehled-systému)
2. [Google Drive konfigurace](#google-drive-konfigurace)
3. [Notion konfigurace](#notion-konfigurace)
4. [Dostupné skripty](#dostupné-skripty)
5. [MCP servery](#mcp-servery)
6. [Tokeny a přístupové údaje](#tokeny-a-přístupové-údaje)
7. [Postupy a workflow](#postupy-a-workflow)
8. [Řešení problémů](#řešení-problémů)

---

## 🎯 Přehled systému

### Účel

Systém pro synchronizaci projektů mezi Notion databází "Evidence projektů" a Google Drive složkou "Projekty". Každý projekt v Notionu má odpovídající složku v Google Drive s odkazem v sloupci "Soubory".

### Architektura

- **Notion**: Databáze "Evidence projektů" s projekty
- **Google Drive**: Složka "Projekty" s podsložkami pro každý projekt
- **Synchronizace**: Automatické vytváření složek a aktualizace odkazů

### Konvence názvů

- **Google Drive složky**: `YYYYMMDD_Nazev_projektu`
  - Příklad: `20251229_Svoz_Odpadu`
  - Příklad: `20251222_box_na_koreni`

---

## 📁 Google Drive konfigurace

### Root složka

- **Název**: `Projekty`
- **ID**: `1KuGLtB3KwQK51lSjwpfAuobJBT3u5-Vj`
- **Umístění**: My Drive (Google Drive for desktop)

### Service Account

- **Email**: `cursormacsw@cursormac.iam.gserviceaccount.com`
- **JSON klíč**: `/Users/petrhoneger/Downloads/cursormac-3945d52dcf1a.json`
- **Povolené API**: Google Drive API
- **Poznámka**: Service account nemá vlastní storage kvótu, používá se pro práci se složkami a ACL

### Sdílení složek

- **Typ**: `anyone` (Anyone with the link)
- **Role**: `reader` (viewer)
- **Automaticky nastaveno**: Ano, při vytváření složky

### Konfigurační soubor

**Cesta**: `/Users/petrhoneger/Documents/HLAVA2_2/drive_config.json`

```json
{
  "service_account_file": "/Users/petrhoneger/Downloads/cursormac-3945d52dcf1a.json",
  "projects_root_id": "1KuGLtB3KwQK51lSjwpfAuobJBT3u5-Vj",
  "scopes": {
    "full": [
      "https://www.googleapis.com/auth/drive"
    ],
    "readonly": [
      "https://www.googleapis.com/auth/drive.readonly"
    ]
  }
}
```

---

## 📝 Notion konfigurace

### Databáze "Evidence projektů"

- **Název**: `Evidence projektů`
- **Database ID**: `2bf64878-09ec-8012-b1d4-c4e33ef0d3d9`
- **Data Source ID**: `2bf64878-09ec-808c-87b7-000b4d2baf65`
- **API verze**: `2025-09-03`

### Důležité sloupce

- `Název projektu` (title) - název projektu
- `Pro koho` (text) - pro koho je projekt
- `Typ projektu` (select) - 3D tisk, Grafika, Laser, Kombinovaný, Jiný
- `Stav` (status) - Zadáno, Rozpracováno, Dokončeno, Předáno, Zrušeno
- `Datum zadání` (date) - datum zadání projektu
- `Termín dokončení` (date) - termín dokončení
- `Soubory` (url) - **odkaz na Google Drive složku projektu**

### Databáze "Pezinská"

- **Název**: `Pezinská`
- **Data Source ID**: `dc94ef8e-1a03-49e9-9c75-c3ca340137e2`
- **Účel**: Databáze vstupních čipů

---

## 🔧 Dostupné skripty

### 1. sync_notion_drive.py

**Hlavní synchronizační skript**

**Účel**:
- Najde projekty v Notionu bez složky v Google Drive
- Vytvoří chybějící složky v Google Drive
- Aktualizuje Notion s odkazy na složky

**Použití**:
```bash
cd ~/Documents/HLAVA2_2
python3 sync_notion_drive.py
```

**Funkce**:
- `sanitize_folder_name()` - převede název projektu na název složky
- `get_date_prefix()` - převede datum na YYYYMMDD formát
- `create_drive_folder()` - vytvoří složku v Google Drive s sdílením
- `update_notion_page()` - aktualizuje Notion stránku s odkazem (API 2025-09-03)
- `get_all_projects()` - načte všechny projekty z Notionu (API 2025-09-03)
- `test_notion_connection()` - test připojení k Notion API

**Konfigurace**:
- Notion token: `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`
- Notion API verze: `2025-09-03`
- Notion Database ID: `2bf64878-09ec-808c-87b7-000b4d2baf65`
- Google Drive config: `drive_config.json`

### 2. list_drive_projects.py

**Výpis složek v Google Drive**

**Účel**: Vypíše všechny složky v adresáři "Projekty" v Google Drive

**Použití**:
```bash
cd ~/Documents/HLAVA2_2
python3 list_drive_projects.py
```

**Výstup**: Seznam složek s názvem a ID

---

## 🔌 MCP servery

### Notion MCP Server v2 (API 2025-09-03)

**Doporučeno**: Použij tento server pro nejnovější funkcionalitu

**Umístění**: `/Users/petrhoneger/Documents/HLAVA2_2/notion-mcp-server-v2/`

**Instalace**:
```bash
cd ~/Documents/HLAVA2_2/notion-mcp-server-v2
npm install
```

**Konfigurace v Cursoru** (`settings.json`):
```json
{
  "mcp.servers": {
    "notion-v2": {
      "command": "node",
      "args": ["/Users/petrhoneger/Documents/HLAVA2_2/notion-mcp-server-v2/index.js"],
      "env": {
        "NOTION_API_KEY": "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"
      }
    }
  }
}
```

**Dostupné nástroje**:
- `notion-fetch` - načtení stránky/databáze/data source
- `notion-search` - vyhledávání (podporuje data sources)
- `notion-update-page` - aktualizace stránky
- `notion-get-database` - získání databáze s data sources
- `notion-get-data-source` - získání data source
- `notion-query-data-source` - dotazování data source
- `notion-create-page` - vytvoření stránky v data source

### Notion MCP Server (starší verze)

**Fallback**: Používá se jako záloha

**Konfigurace v Cursoru** (`settings.json`):
```json
{
  "mcp.servers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-notion"],
      "env": {
        "NOTION_API_KEY": "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"
      }
    }
  }
}
```

**Dostupné nástroje**:
- `notion-fetch` - načtení stránky/databáze
- `notion-search` - vyhledávání v Notion
- `notion-update-page` - aktualizace stránky

---

## 🔑 Tokeny a přístupové údaje

### Notion Integration Token

**Aktuální token**: `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`

**Kde se používá**:
- `sync_notion_drive.py` (fallback)
- MCP servery (`notion` a `notion-v2`)
- Cursor settings.json

**Jak získat nový token**:
1. Otevři: https://www.notion.so/my-integrations
2. Vytvoř novou integration nebo uprav existující
3. Zkopíruj Internal Integration Token
4. Aktualizuj token ve všech konfiguračních souborech

**Důležité**: Integration musí mít přístup k databázi "Evidence projektů" (Share → Add integration → Can edit)

### Google Drive Service Account

**JSON klíč**: `/Users/petrhoneger/Downloads/cursormac-3945d52dcf1a.json`  
**Email**: `cursormacsw@cursormac.iam.gserviceaccount.com`  
**Poznámka**: Service account je pouze pro skripty, ne pro agenty mimo tento stroj

---

## 📋 Postupy a workflow

### Vytvoření nového projektu

1. **V Notionu**: Vytvoř nový řádek v databázi "Evidence projektů"
   - Vyplň: Název projektu, Datum zadání, Typ projektu, Stav
2. **Spusť synchronizaci**:
   ```bash
   cd ~/Documents/HLAVA2_2
   python3 sync_notion_drive.py
   ```
3. **Výsledek**:
   - Vytvoří se složka v Google Drive: `YYYYMMDD_Nazev_projektu`
   - Notion se automaticky aktualizuje s odkazem na složku

### Kontrola chybějících složek

1. **Spusť synchronizaci**:
   ```bash
   python3 sync_notion_drive.py
   ```
2. **Skript automaticky**:
   - Načte všechny projekty z Notionu
   - Najde projekty bez složky (prázdný sloupec "Soubory")
   - Vytvoří chybějící složky
   - Aktualizuje Notion s odkazy

### Výpis složek v Google Drive

```bash
python3 list_drive_projects.py
```

### Ruční vytvoření složky

Pokud potřebuješ vytvořit složku ručně, použij `sync_notion_drive.py` - automaticky najde projekty bez složek a vytvoří je.

---

## 🐛 Řešení problémů

### Problém: Token je neplatný (401)

**Řešení**:
1. Zkontroluj token v Notion integrations: https://www.notion.so/my-integrations
2. Zkontroluj, zda má integration přístup k databázi (Share → Add integration)
3. Aktualizuj token ve všech konfiguračních souborech:
   - `sync_notion_drive.py`
   - `settings.json` (MCP servery)

### Problém: MCP servery nejsou dostupné

**Řešení**:
1. Restartuj Cursor
2. Zkontroluj `settings.json` - správná cesta k MCP serveru
3. Zkontroluj, zda je Node.js nainstalovaný: `node --version`
4. Pro notion-v2: zkontroluj, zda jsou nainstalované závislosti: `cd notion-mcp-server-v2 && npm install`

### Problém: Chyba při vytváření složky v Google Drive

**Řešení**:
1. Zkontroluj, zda existuje `drive_config.json`
2. Zkontroluj, zda existuje service account JSON: `/Users/petrhoneger/Downloads/cursormac-3945d52dcf1a.json`
3. Zkontroluj, zda má service account přístup k Google Drive API

### Problém: Notion API vrací 404

**Řešení**:
1. Zkontroluj Database ID - může se změnit při přejmenování databáze
2. Použij `notion-search` k nalezení správného ID
3. Zkontroluj, zda má integration přístup k databázi

---

## 📚 Důležité odkazy

- **Notion API dokumentace**: https://developers.notion.com/
- **Notion API Upgrade Guide 2025-09-03**: https://developers.notion.com/docs/upgrade-guide-2025-09-03
- **Notion Integrations**: https://www.notion.so/my-integrations
- **Google Drive API**: https://developers.google.com/drive
- **MCP dokumentace**: https://modelcontextprotocol.io/

---

## 📝 Poznámky k API 2025-09-03

### Změny v Notion API

- Místo `database_id` se nyní používá `data_source_id` pro většinu operací
- Podpora multi-source databases
- Nové endpointy pro data sources
- Search API vrací data source objekty

### Migrace

- Všechny skripty jsou aktualizované na API 2025-09-03
- MCP server v2 podporuje novou verzi API
- Starší MCP server (`notion`) používá starší verzi API jako fallback

---

## 🔄 Historie změn

**2026-01-05**:
- Aktualizováno na Notion API 2025-09-03
- Vytvořen nový MCP server v2 s podporou data sources
- Sloučeny logicky související skripty
- Smazány zbytečné a duplicitní soubory
- Aktualizován Notion token

**Předchozí verze**:
- Používala se API verze 2022-06-28
- Více samostatných skriptů pro různé úkoly
- Starší MCP server bez podpory data sources

---

## ✅ Kontrolní seznam

### Před použitím systému zkontroluj:

- [ ] Notion token je platný a má přístup k databázi
- [ ] Google Drive service account JSON existuje
- [ ] `drive_config.json` je správně nakonfigurovaný
- [ ] MCP servery jsou nakonfigurované v `settings.json`
- [ ] Node.js je nainstalovaný (pro MCP servery)
- [ ] Python 3 je nainstalovaný (pro skripty)
- [ ] Závislosti jsou nainstalované (`npm install` v notion-mcp-server-v2)

---

**Konec zálohy znalostí**
