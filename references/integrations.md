# Integraciones - Credenciales y Configuración

## Telegram Bot Avisos

- **Bot:** `@Moni_Avisos_bot`
- **Token:** `<TELEGRAM_BOT_TOKEN>`
- **Canal:** `t.me/followappavisos` (canal privado)

### Setup del canal (para futuras referencias)

1. Crear canal privado en Telegram
2. Agregar `@Moni_Avisos_bot` como administrador con permisos de publicación
3. Obtener el chat ID del canal usando `getUpdates` o pasando el link al bot

### Para enviar alertas

```bash
curl -s "https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/sendMessage" \
  -d "chat_id=@followappavisos" \
  -d "text=[$(date '+%d/%m/%Y %H:%M')] Moni Avisos: {mensaje}"
```

---

## Trello CRM

- **API Key:** `<KEY>`
- **Token:** `<TOKEN>`
- **Board:** `CRM FollowApp` (ID: `674d9fe5597e7148c6517990`)

---

## Google Sheets

- **Leads Followapp Whatsapp:** `1_7tbIwzgtuouM5fbyqLCzCBqX2EfiUgjYX8rUKXgqPo`
- **Chats N8n (bloqueo):** `1JcsHW3_6cwNlnm_arJslmMuND2GWq_0mAn6z7mjU8wg`
