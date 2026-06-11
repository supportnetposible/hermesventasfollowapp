# GitHub Workflow — heremesventasfollowapp

## Repo
```
git@github.com:supportnetposible/hermesventasfollowapp.git
```

## Setup (one-time)

### 1. Generar SSH key
```bash
ssh-keygen -t rsa -b 4096 -C "hermes@netposible.com" -f ~/.ssh/id_rsa -N ""
cat ~/.ssh/id_rsa.pub
```
→ Agregar la key pública en GitHub: **Settings → SSH and GPG keys → New SSH key**

### 2. Configurar remote
```bash
cd <repo>
git remote add origin git@github.com:supportnetposible/hermesventasfollowapp.git
# o si ya existe:
git remote set-url origin git@github.com:supportnetposible/hermesventasfollowapp.git
```

### 3. Arrancar ssh-agent
```bash
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_rsa
```

### 4. Agregar GitHub a known_hosts
```bash
ssh-keyscan github.com >> ~/.ssh/known_hosts 2>/dev/null
```

---

## Push workflow

### Antes de commit — NUNCA incluir credenciales reales

**Archivos con credenciales que fueron detectadas por secret scanning:**
- `references/integrations.md` — Telegram bot token, Trello key/token
- `references/trello-api.md` — Trello key/token
- `references/remarketing-execution.md` — Trello key/token

**Patrón de reemplazo:**
```
Trello key real:    `<KEY>`  →  (redacted)
Trello token real:  `<TOKEN>`  →  (redacted)
Telegram bot token: `<TELEGRAM_BOT_TOKEN>`  →  (redacted)
```

**Verificar que no queden credenciales reales:**
```bash
grep -rE "<KEY>|<TOKEN>|<TELEGRAM_BOT_TOKEN>" --include="*.md" --include="*.py" .
```

### Push
```bash
git add -A
git commit -m "<mensaje>"
git push -u origin master
```

### Si GH013 — Repository rule violations (secret scanning)

GitHub bloquea el push si detecta secretos en el commit. Solución:

```bash
# 1. Reemplazar credenciales en los archivos con placeholders
# 2. Amend del commit (rebase en el último commit, no crea nuevo)
git add -A
git commit --amend -m "<mensaje actualizado>"

# 3. Force push (el commit original fue rechazado, hay que reemplazarlo)
git push --force
```

---

## Huella de la SSH key registrada en GitHub (jun 2026)
```
SHA256:HXN0eJSVkKYevylu885JgY35c/8hn4E7EmbKEQLnzZE
```
→ Esta huella ya está registrada en GitHub. La key se regeneró en esta máquina y funciona.
