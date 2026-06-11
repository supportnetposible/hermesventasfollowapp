# WhatsApp Reconnection — QR y Sesión

## Cuándo usar esta guía

Cuando el bridge de WhatsApp muestra `❌ Logged out` en el log o el bot no puede enviar/recibir mensajes.

## Workflow completo de reconexión

### Paso 1 — Identificar el estado

```bash
# Ver el estado del bridge
cat /root/.hermes/whatsapp/bridge.log | tail -20
curl -s http://localhost:3000/health
```

Estados posibles:
- `disconnected` → necesita reconexión
- `connected` → bridge OK, el problema es otro
- Puerto 3000 libre → bridge no está corriendo

### Paso 2 — Si el bridge no está corriendo o está en logged out

```bash
# Matar cualquier proceso en puerto 3000
fuser -k 3000/tcp 2>/dev/null

# Eliminar sesión vieja (si dice "logged out")
rm -rf /root/.hermes/whatsapp/session

# Reiniciar bridge en background
cd /usr/local/lib/hermes-agent/scripts/whatsapp-bridge && node bridge.js > /tmp/wa_bridge.log 2>&1 &
```

### Paso 3 — Obtener el QR

El bridge原始 expone el QR solo en el log como ASCII art. Para obtenerlo como imagen:

**Opción A — Endpoint /qr (si se parchó el bridge):**

El bridge parcheado tiene un endpoint `/qr` que devuelve el QR en base64:

```bash
# Obtener QR como JSON con imagen base64
curl -s http://localhost:3000/qr

# Guardar como imagen PNG
curl -s http://localhost:3000/qr | python3 -c "
import sys, json, base64
data = json.load(sys.stdin)
img_data = data['image'].split(',')[1]
with open('/tmp/qr_whatsapp.png', 'wb') as f:
    f.write(base64.b64decode(img_data))
"
```

**Opción B — Copiar desde el log (ASCII art):**

```bash
# El QR aparece como arte ASCII en el log
grep -A100 "Scan this QR code" /tmp/wa_bridge.log | head -40
```

### Paso 4 — Parchar bridge.js para exponer QR (si no tiene el endpoint)

Solo necesario si el bridge no tiene el endpoint `/qr`. El bridge original (sin parchear) solo imprime el QR en el log.

**Parche necesario en bridge.js:**

```javascript
// Agregar variable global al inicio (cerca de "let sock = null;")
let lastQR = null;

// En el connection.update handler, capturar el QR:
if (qr) {
  lastQR = qr;  // AGREGAR ESTA LÍNEA
  console.log('\n📱 Scan this QR code with WhatsApp on your phone:\n');
  qrcode.generate(qr, { small: true });
}

// Agregar endpoint antes de app.listen:
app.get('/qr', async (req, res) => {
  if (!lastQR) return res.status(503).json({ error: 'No QR code available yet' });
  try {
    const QRCode = await import('qrcode');
    const url = await QRCode.toDataURL(lastQR, { width: 300, margin: 2 });
    res.json({ qr: lastQR, image: url });
  } catch (err) {
    return res.status(500).json({ error: 'Failed to generate QR image' });
  }
});
```

**Dependencia necesaria:**

```bash
cd /usr/local/lib/hermes-agent/scripts/whatsapp-bridge && npm install qrcode
```

## Enviar QR al canal Telegram

```bash
# Enviar texto
curl -s -X POST "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/sendMessage" \
  -d "chat_id=-1003844465265" \
  -d "text=📱 Escaneá este QR con WhatsApp para reconectar a Tomas" \
  -d "parse_mode=Markdown"

# Enviar imagen
curl -s -X POST "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/sendPhoto" \
  -F "chat_id=-1003844465265" \
  -F "photo=@/tmp/qr_whatsapp.png" \
  -F "caption=Escaneá con WhatsApp → Ajustes → Dispositivos vinculados → Vincular dispositivo"
```

## Verificar conexión

```bash
# Salud del bridge
curl -s http://localhost:3000/health
# Respuesta esperada: {"status":"connected","queueLength":0,"uptime":N}

# Ver logs
tail -f /tmp/wa_bridge.log
```

## Problemas comunes

| Problema | Causa | Solución |
|----------|-------|----------|
| `EADDRINUSE` en puerto 3000 | Bridge anterior sigue corriendo | `fuser -k 3000/tcp` |
| `require is not defined` en /qr | Bridge usa ESM, no CommonJS | Usar `await import('qrcode')` en vez de `require()` |
| QR muestra pero no scanea | Sesión corrupta | `rm -rf /root/.hermes/whatsapp/session` y reiniciar |
| Bridge inicia pero no levanta QR | Baileys no pudo conectar | Verificar credenciales de WhatsApp Web |