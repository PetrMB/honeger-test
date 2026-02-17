---
name: cloudflare-pages-deploy
description: Cloudflare Pages deployment best practices - how to deploy to Pages with GitHub source and custom domains
metadata:
  {
    "openclaw":
      {
        "emoji": "🚀",
        "requires": { "bins": ["wrangler"] },
        "author": "Otík"
      },
  }
---

# Cloudflare Pages Deploy

## Problém

- Pages API nemá Direct Upload (dokumentováno: "no REST API for direct file uploads")
- Wrangler login neprijímá `--api-token` flag
- GitHub webhook někdy neredlaguje (když project není připojený z dashboardu)

## Správný postup

### 1. Vytvoř Pages projekt přes dashboard

1. Přihlas se do Cloudflare dashboardu
2. Workers & Pages → **Create application** → **Pages**
3. **Connect to GitHub**
4. Vyber repo a větev
5. Build configuration (root directory: `./`, Build command: ``, Output directory: `./`)
6. Project name: např. `test1`

**Důležité:** Project musí být vytvořen přes dashboard, aby GitHub webhook fungoval!

### 2. Vytvoř custom domain přes dashboard

1. Workers & Pages → `test1` → **Custom domains**
2. **Set up a custom domain**
3. Zadej: `test1.honeger.com`
4. Klikni **Activate domain**
5. Po 1-5 minutách bude dostupné

**Důležité:** API má bug s "invalid TLD" - custom domain jde jen přes UI.

### 3. Přidání obsahu

- Pushni commits do GitHubu → Pages auto-deployne
- Nebo použij `wrangler pages deploy` s `CLOUDFLARE_API_TOKEN` (viz níže)

## Wrangler s API tokenem (pokud potřebuješ ruční deploy)

```bash
export CLOUDFLARE_ACCOUNT_ID=5470e26fcae9a4c79ec97311fd338cb4
export CLOUDFLARE_API_TOKEN="axoFp-kfDjlfatmhLXrZD4d1Z9ziN9WUzL35WF_b"

cd /path/to/project
wrangler pages deploy . --project-name=test1
```

**Pozor:** Wrangler `login` neprijímá `--api-token`. Použij env proměnné místo loginu.

## Úplný automatizovaný postup (Pages API + Workers proxy)

### 1. Vytvoř Pages projekt přes API

```bash
curl -X POST "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects" \
  -H "Authorization: Bearer {API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name":"{PROJECT_NAME}",
    "production_branch":"main",
    "build_config":{"build_command":"","destination_dir":"/","root_dir":"/"}
  }'
```

Výsledek obsahuje `subdomain` (např. `otto-2m5.pages.dev`).

### 2. Zdeploy obsah přes Wrangler

```bash
export CLOUDFLARE_ACCOUNT_ID={ACCOUNT_ID}
export CLOUDFLARE_API_TOKEN="{API_TOKEN}"

cd /path/to/project
wrangler pages deploy . --project-name={PROJECT_NAME}
```

Výsledek: `https://{DEPLOYMENT_ID}.{PROJECT_SUBDOMAIN}.pages.dev`

### 3. Vytvoř Workers proxy pro custom domain

```bash
curl -X PUT "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{SCRIPT_NAME}-proxy" \
  -H "X-Auth-Key: {GLOBAL_API_KEY}" \
  -H "X-Auth-Email: {EMAIL}" \
  -H "Content-Type: application/javascript" \
  --data-binary @- << 'EOF'
addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

async function handleRequest(request) {
  const url = new URL(request.url)
  const pagesUrl = `https://{DEPLOYMENT_ID}.{PROJECT_SUBDOMAIN}.pages.dev${url.pathname}${url.search}`
  return fetch(pagesUrl, request)
}
EOF
```

### 4. Vytvoř Workers route

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/workers/routes" \
  -H "X-Auth-Key: {GLOBAL_API_KEY}" \
  -H "X-Auth-Email: {EMAIL}" \
  -H "Content-Type: application/json" \
  -d '{"pattern":"{DOMAIN}/*","script":"{SCRIPT_NAME}-proxy"}'
```

### 5. Update DNS záznam na CNAME

```bash
curl -s "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records?name={DOMAIN}" \
  -H "Authorization: Bearer {DNS_TOKEN}" | jq '.result[0].id'

curl -X PATCH "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{DNS_ID}" \
  -H "Authorization: Bearer {DNS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"type":"CNAME","name":"{DOMAIN}","content":"{SCRIPT_NAME}-proxy.{SUBDOMAIN}.workers.dev","ttl":1,"proxied":true}'
```

### Hotovo!

Stránka je dostupná na `https://{DOMAIN}` (např. `otto.honeger.com`)

## Automatizace (script)

Použij `deploy-pages.sh` v `~/.openclaw/workspace/scripts/`:

```bash
# Deploy kanban
./deploy-pages.sh otto

# Deploy jiný projekt
./deploy-pages.sh test1 "PetrMB/otta-kanban" "/path/to/repo"
```

Script automaticky:
1. Načte token z env/proměnných
2. Zdeployí přes Wrangler
3. Vrátí URL nového deploymentu

## URL struktura

- Pages project: `https://test1.honeger-test.pages.dev`
- Custom domain: `https://test1.honeger.com` (přes UI)

## Troubleshooting

| Problém | Řešení |
|---------|--------|
| 404 na Pages | Project není připojený k GitHubu (vytvoř přes dashboard) |
| "invalid TLD" error | API nemá custom domain - použij UI |
| GitHub webhook neredlaguje | Project vytvořen přes API místo UI |
| DNS záznam již existuje | Update stávající DNS record (A → CNAME) |

---

## Mazání (Cleanup)

### 1. Smazání Pages projektu

```bash
curl -X DELETE "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}" \
  -H "Authorization: Bearer {API_TOKEN}"
```

### 2. Smazání Workers skriptu

```bash
curl -X DELETE "https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/workers/scripts/{SCRIPT_NAME}" \
  -H "X-Auth-Key: {GLOBAL_API_KEY}" \
  -H "X-Auth-Email: {EMAIL}"
```

### 3. Smazání Workers route

```bash
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/workers/routes/{ROUTE_ID}" \
  -H "X-Auth-Key: {GLOBAL_API_KEY}" \
  -H "X-Auth-Email: {EMAIL}"
```

### 4. Smazání DNS záznamu

```bash
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{DNS_ID}" \
  -H "Authorization: Bearer {DNS_API_TOKEN}"
```

---

*Otík skill - 2026-02-16*
