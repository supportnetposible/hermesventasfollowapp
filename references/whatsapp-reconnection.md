# WhatsApp Bridge — Reconnection Procedure

## This Installation's WhatsApp Setup

- **Bridge:** `/usr/local/lib/hermes-agent/scripts/whatsapp-bridge/bridge.js`
- **Session dir:** `/root/.hermes/whatsapp/session`
- **HTTP port:** `3000` (127.0.0.1)
- **WhatsApp number:** `5491161254711` (home channel configurado)
- **Bridge log:** `/tmp/wa_bridgeN.log` (N = número sequential)

## Reconnection Procedure

When WhatsApp shows "logged out" or the session is broken:

### Step 1 — Kill existing bridge and clean session
```bash
fuser -k 3000/tcp 2>/dev/null
rm -rf /root/.hermes/whatsapp/session
```

### Step 2 — Patch bridge.js to expose QR as HTTP endpoint
The bridge uses `qrcode-terminal` (ASCII only). Need to add a `/qr` endpoint that returns a PNG.

**Add after line ~177 (after `let connectionState`):**
```js
let lastQR = null;
```

**In the `connection.update` handler, where `if (qr)` fires:**
```js
if (qr) {
  lastQR = qr;  // ADD THIS LINE
  console.log('\n📱 Scan this QR code...\n');
  qrcode.generate(qr, { small: true });
  console.log('\nWaiting for scan...\n');
}
```

**Add endpoint BEFORE the `app.listen()` block:**
```js
// QR code endpoint for pairing
app.get('/qr', async (req, res) => {
  if (!lastQR) {
    return res.status(503).json({ error: 'No QR code available yet' });
  }
  try {
    const QRCode = await import('qrcode');
    const url = await QRCode.toDataURL(lastQR, { width: 300, margin: 2 });
    res.json({ qr: lastQR, image: url });
  } catch (err) {
    return res.status(500).json({ error: 'Failed to generate QR image' });
  }
});
```

**Install qrcode package (ESM, use dynamic import):**
```bash
cd /usr/local/lib/hermes-agent/scripts/whatsapp-bridge
npm install qrcode
```

### Step 3 — Start bridge and get QR
```bash
cd /usr/local/lib/hermes-agent/scripts/whatsapp-bridge
node bridge.js > /tmp/wa_bridge_new.log 2>&1 &
sleep 12
# Get PNG image
curl -s http://localhost:3000/qr | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
img = data['image'].split(',')[1]
with open('/tmp/qr_whatsapp.png', 'wb') as f:
    f.write(base64.b64decode(img))
"
```

### Step 4 — Send QR to user
```python
# Via Telegram channel
send_message(target="telegram:-1003844465265", message="📱 Nuevo QR generado")
send_message(target="telegram:-1003844465265", message="MEDIA:/tmp/qr_whatsapp.png")
```

### Step 5 — Verify connection
```bash
curl http://localhost:3000/health
# {"status":"connected", ...}
```

### Step 6 — Set home channel
```bash
hermes config set WHATSAPP_HOME_CHANNEL 5491161254711
```

## Why this is non-obvious

- The bridge uses `qrcode-terminal` which only prints to stdout — no HTTP endpoint for QR exists by default
- `require('qrcode')` doesn't work in this ESM module — must use `await import('qrcode')`
- The QR data (`lastQR`) must be captured from Baileys' `connection.update` event, not from any API
- The QR expires quickly (~60s) — must be fresh from a newly started bridge process
