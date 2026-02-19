# QMD Prerequisites

## macOS

### 1. Install Bun

```bash
curl -fsSL https://bun.sh/install | bash
```

Verify:

```bash
bun --version
# → expected: 1.x.x
```

### 2. Install SQLite with extensions

```bash
brew install sqlite
```

### 3. Install QMD CLI

```bash
bun install -g @tobilu/qmd
```

Verify:

```bash
qmd --version
# → expected: v1.x.x
```

---

## Linux (Ubuntu/Debian)

### 1. Install Bun

```bash
curl -fsSL https://bun.sh/install | bash
```

### 2. Install SQLite with extensions

```bash
sudo apt update
sudo apt install sqlite3 libsqlite3-dev
```

### 3. Install QMD CLI

```bash
bun install -g @tobilu/qmd
```

---

## Windows (WSL2 recommended)

1. Install WSL2 + Ubuntu  
2. Follow Linux instructions above  

*(Native Windows support is limited; WSL2 is the recommended approach.)*
