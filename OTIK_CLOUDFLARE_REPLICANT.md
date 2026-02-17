# Otík Cloudflare Replicant

**Otík Cloudflare Replicant** je hybridní proxy systém, který distribuuje provoz mezi Cloudflare Edge location a lokální proxy server. V jádře využívá Cloudflare Tunnel (cloudflared) pro bezpečné připojení lokálních služeb do edge sítě, zatímco lokální proxy (např. nginx/Caddy) řeší rozvíjení, TLS terminate a routování uvnitř domácí sítě.

**Edge layer** zajišťuje globální distribuci, DDoS ochranu, caching a DNS routing — vše běží na Cloudflare side. **Local proxy layer** zpracovává vnitřní route, mění host header, vkládá HEADERS a provádí kontextovou úpravu odpovědí před doručením klientovi.

Provufování probíhá tak, že klient přistupuje přes Cloudflare hostname → edge router (Cloudflare) → TLS tunnel do domácí sítě → cloudflared → lokální proxy → cílová služba. Tato architektura zajišťuje šifrovaný provoz bez otevřených portů.

Výhodou je nulový konfigurační overhead na straně klienta (žádné IP/端口 potřeba), automatické obnovování certifikátů a možnost kombinovat edge strategie (např. A/B testing) s lokalizovanou logikou.

Replicant se liší od klasického reverse proxy tím, že automaticky synchronizuje konfiguraci mezi edge a local layer pomocí metadatových výměn přes HTTP headers nebo DNS TXT zápisy.
