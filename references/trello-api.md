# Trello API — CRM FollowApp

## Credenciales

| Dato | Valor |
|------|-------|
| **API Key** | `<KEY>` |
| **Token** | `<TOKEN>` |

## Board principal

| Dato | Valor |
|------|-------|
| **Board** | CRM FollowApp |
| **Board ID** | `674d9fe5597e7148c6517990` |

## Listas (columnas del pipeline)

| Lista | ID |
|-------|-----|
| En seguimiento Sin remarketing | `6939813d9b4c352c70847cca` |
| Visitantes | `674d9fe5597e7148c6517992` |
| Leads | `67fe66c5d460e87faa45344a` |
| Leads calificados | `674d9fe5597e7148c6517993` |
| En seguimiento | `674d9fe5597e7148c6517994` |
| DEMO | `6998c71d8404303ffd039371` |
| Listo para comprar | `692847f9b7e6ad5dd2de23f7` |
| On-Boarding Prepago | `674d9fe5597e7148c6517997` |
| On-Boarding | `68e54b44f323fdc3fc714a3d` |
| Clientes | `674d9fe5597e7148c6517995` |
| Clientes en soporte | `674d9fe5597e7148c6517996` |
| Clientes suspendidos | `67b8d8e4bee8ab9dae90d4d6` |
| Clientes Deudores | `6a19f87970486d429de6cbef` |
| Ex Clientes | `674d9fe5597e7148c6517991` |

## Labels principales

| Label | Color | ID |
|-------|-------|-----|
| prepago | blue | `6894cd2932deabb2a82a43f8` |
| Llamada pendiente | lime_dark | `674d9fe5597e7148c6517a24` |
| Comodato | purple_dark | `6894cd11a65300468617a579` |
| Problemas con el pago | orange | `674d9fe5597e7148c6517a28` |
| Grandes Empresas | green_dark | `686bca6b58120a04a4f94cca` |
| Por instalar | sky | `674d9fe5597e7148c6517a1e` |
| Interesado en Corta-Corriente | orange_dark | `69f3472323398b9cf9501bc8` |
| SIN RESPUESTA | green_light | `69a06bc68de4addccb95a627` |
| Soporte técnico | red_light | `674d9fe5597e7148c6517a26` |
| Ex Cliente Problemático | red_dark | `69a06a861a780d0a90cbdbaf` |
| Legales | red | `67ca0d3575ab6ee7e99a7edd` |
| Cámaras | sky_dark | `698f0bc57803ac8b71daa335` |
| ⭐ | yellow_dark | `69b9b0f0642f7322c8c2997b` |
| Revendedor | pink_dark | `68d68ff947e54424c404ed44` |
| Le parece caro | black | `6a046c5313f356fc658dbf9c` |
| Videollamada | blue_light | `6a171536ec200188cecb6b0d` |
| ILOCALIZABLE | purple_light | `69a06cf8af4e6a92375ab6f1` |
| PROBLEMAS ECONÓMICOS | pink_light | `69a06b78ba373a9617daa818` |
| EX CLIENTE DEUDOR | orange_light | `69a6c501a041670d1eb48288` |
| NEGATIVA DE PAGO | black_light | `69a06b0bb33ef2546dc7347d` |

## Uso rápido de la API

```bash
# Obtener miembro
curl -s "https://api.trello.com/1/members/me?key=<KEY>&token=<TOKEN>"

# Listar tableros
curl -s "https://api.trello.com/1/members/me/boards?key=<KEY>&token=<TOKEN>&filter=open"

# Listar listas de un board
curl -s "https://api.trello.com/1/boards/<BOARD_ID>/lists?key=<KEY>&token=<TOKEN>&filter=open"

# Listar labels de un board
curl -s "https://api.trello.com/1/boards/<BOARD_ID>/labels?key=<KEY>&token=<TOKEN>"

# Crear tarjeta
curl -s -X POST "https://api.trello.com/1/cards?key=<KEY>&token=<TOKEN>" \
  -d "name=Test&desc=Prueba&idList=<LIST_ID>&idBoard=<BOARD_ID>"

# Mover tarjeta
curl -s -X PUT "https://api.trello.com/1/cards/<CARD_ID>?key=<KEY>&token=<TOKEN>&idList=<LIST_ID>"

# Agregar label
curl -s -X POST "https://api.trello.com/1/cards/<CARD_ID>/labels?key=<KEY>&token=<TOKEN>&color=<COLOR>&name=<LABEL_NAME>"
```

> **Nota:** el token tiene `expiration=never`, así que es válido indefinidamente mientras no se revoque desde Trello.