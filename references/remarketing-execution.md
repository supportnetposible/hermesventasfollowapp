# Remarketing — Estado del pipeline y protocolo de ejecución

**Última ejecución verificada:** 2026-06-06

---

## Estado actual de las columnas de remarketing

| Columna | List ID | Cards (lead cards) | Notes |
|---------|---------|---------------------|-------|
| En seguimiento | `674d9fe5597e7148c6517994` | ~22 leads | Todos ya tienen `✏️ Remarketing R1` |
| Listo para comprar | `692847f9b7e6ad5dd2de23f7` | ~8 leads | Todos ya tienen `✏️ Remarketing R1` |

> **Filas resumen a excluir:** tarjetas cuyo nombre sea "TOTAL VEHÍCULOS: ..." — no son leads reales.

---

## Labels de remarketing existentes

| Label | Color | ID | Uses |
|-------|-------|----|------|
| ✏️ Remarketing R1 | yellow | `6a23f05e143a3f56a7e0591c` | 29 |
| ✏️ Remarketing R2 | orange | `6a23f066b49b36974826ebbc` | 0 — ya existe, no crear |
| ✏️ Remarketing R3 | red | `6a23f067d4658a9ecaa46bf6` | 0 — ya existe, no crear |

---

## Números bloqueados por n8n (sheet: `1JcsHW3_6cwNlnm_arJslmMuND2GWq_0mAn6z7mjU8wg`)

Solo 2 números activos en la sheet al 2026-06-06:
- `5493804114324`
- `5493804793255`

> **Nota:** la sheet requiere `curl -sL` (follow redirect) para obtener el CSV. URL directa con `export?format=csv` hace redirect a `doc-0o-8g-sheets.googleusercontent.com`.

---

## Protocolo de la Ronda 1 — siguiente ejecución

La Ronda 1 está aplicada a todos los leads existentes. No hay leads frescos sin label.

**Para la próxima ejecución (cuando haya leads sin label de remarketing):**
1. Leer todos los cards de `En seguimiento` + `Listo para comprar`
2. Filtrar los que NO tienen ningún label `✏️ Remarketing R*`
3. Para cada uno:
   - Extraer nombre y teléfono del nombre de la tarjeta (formato `#Followapp Nombre // +54 9 ...`)
   - Generar audio TTS con texto Ronda 1
   - Enviar manualmente por WhatsApp Business API
   - Agregar label `✏️ Remarketing R1` al card en Trello

---

## Textos de las rondas

**Ronda 1:**
> "Hola [nombre]! Soy Tomás de FollowApp. Te escribo porque quedamos en charlar sobre el tema del monitoreo de tus vehículos. ¿Tuviste oportunidad de verlo? Si precisás te paso el link y te lo muestro en 5 minutos."

**Ronda 2:**
> "Hola [nombre]! Sigo acá de parte de FollowApp. Te quería preguntar: ¿el tema de saber dónde están los vehículos es algo que necesitás resolver ahora o lo ves para más adelante? Te hago un resumen rápido de lo que hacemos."

**Ronda 3:**
> "Hola [nombre]! Te molesto una última vez de parte de FollowApp. El tema del control de flota es algo que resolvimos con muchísimas empresas acá en Córdoba. Si te parece, te mando un video corto de 2 minutos y charlamos. ¿Dale?"

---

## API Trello — comandos clave

```bash
# Leer cards de una lista (incluye labels)
curl -s "https://api.trello.com/1/lists/<LIST_ID>/cards?key=<KEY>&token=<TOKEN>&fields=name,labels,shortUrl,desc&label_fields=name,color"

# Agregar label a card (usar id del label existente)
curl -s -X POST "https://api.trello.com/1/cards/<CARD_ID>/labels?key=<KEY>&token=<TOKEN>&idLabel=<LABEL_ID>"

# Eliminar label de card
curl -s -X DELETE "https://api.trello.com/1/cards/<CARD_ID>/labels/<LABEL_ID>?key=<KEY>&token=<TOKEN>"
```

**Credenciales:** key=`<KEY>`, token=`<TOKEN>`