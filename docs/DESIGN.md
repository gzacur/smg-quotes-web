# DESIGN.md — Frases de San Miguel Garicoïts

**Idea: «Citas», una biblioteca de frases limpia y amable.** El sitio funciona como una app de citas. Las frases aparecen como tarjetas blancas sobre un fondo lino; los filtros (tema, destinatario, tomo, esenciales, marcadas y búsqueda) están siempre a la vista arriba; al tocar una tarjeta, su detalle completo (frase grande, carta, destinatario, año, tema y contexto) aparece en un panel fijo a la derecha, o en una hoja que sube desde abajo en el celular. Un acento verde salvia, suave y luminoso, marca lo seleccionado.

## Referencias (UXKIN)

| Sitio | Qué se toma y dónde se usa |
|---|---|
| **Gleap** | Fondo lino cálido (#edede8) con tarjetas blancas flotando encima; superficie secundaria de piedra salvia; botones en pastilla: grafito (principal), piedra (secundario), fantasma. → Fondo, tarjetas y botones. |
| **Alden** | Tarjetas blancas limpias con filas etiqueta / valor alineadas, y un único acento verde salvia suave en pastilla. → Panel de detalle y color de selección. |
| **Craft Docs** | Serif amable para el contenido junto a una sans neutra; superficies suaves sin sombras duras. → Frases en serif Fraunces. |
| **Headspace** (ronda anterior) | Pastillas de filtro: activa rellena, inactiva con borde fino; texto oscuro cálido. → Fila de temas. |

## Diagrama

```
Escritorio
┌───────────────────────────────────────────────────────────────────┐
│ ● Frases de San Miguel Garicoïts     [ Buscar…            ]  608  │
├───────────────────────────────────────────────────────────────────┤
│ (Todos) (Voluntad de Dios) (Obediencia) (Amor de Dios) …  →       │  temas
│ Destinatario [Todos ▾]  Tomo [Todos ▾]  (★ Esenciales) (Marcadas) │
├──────────────────────────────────────────┬────────────────────────┤
│ ┌──────────┐ ┌──────────┐                 │  DETALLE (fijo)        │
│ │«frase…»  │ │«frase…»  │   tarjetas      │  ● Voluntad de Dios    │
│ │● tema    │ │● tema    │   en 2 col.     │  «frase grande»        │
│ │C.163·1858│ │C.12·1838 │                 │  Carta   163 · Tomo I  │
│ └──────────┘ └──────────┘                 │  Para    P. Barbé      │
│ ┌──────────┐ ┌──────────┐                 │  Año     1858          │
│ │ (activa) │ │          │                 │  Contexto …            │
│ └──────────┘ └──────────┘                 │  [Copiar] [★] [← →]   │
└──────────────────────────────────────────┴────────────────────────┘

Celular: buscador → temas (desplazables) → filtros → tarjetas en 1 col.
Tocar una tarjeta abre una hoja inferior con el detalle completo y ← →.
```

## Color

| Token | Claro | Oscuro | Rol |
|---|---|---|---|
| `--canvas` | `#eeeee9` | `#191b19` | Fondo de página (lino) |
| `--card` | `#ffffff` | `#222522` | Tarjetas y panel de detalle |
| `--stone` | `#e3e4dc` | `#2b2f2b` | Superficie secundaria: buscador, selects, pastillas secundarias |
| `--ink` | `#1f2421` | `#e7e9e3` | Texto principal, botón principal (13.5:1) |
| `--muted` | `#62675f` | `#a3a89f` | Metadatos, etiquetas, contexto (≥ 5:1) |
| `--line` | `#dcddd5` | `#333733` | Bordes finos |
| `--sage` | `#e1ebd3` | `#2c3a24` | Fondo de lo seleccionado (tema activo, tarjeta activa) |
| `--sage-ink` | `#3c5a2a` | `#cfe3b8` | Texto sobre salvia, enlaces, foco (6.3:1) |

Cada tema tiene un punto de color propio, apagado, solo como ayuda para reconocerlo (nunca como texto): salvia, cielo, rosa, arena, lila, arcilla, menta, durazno, pizarra, oliva.

## Tipografía

- **Fraunces** (400, 400 itálica; óptica suave): frases.
- **Plus Jakarta Sans** (400, 500, 600): interfaz, metadatos, contexto.

| Rol | Tamaño / interlínea |
|---|---|
| marca | 17px / 1.2, 600 |
| frase en el detalle | clamp(24px, 2.4vw, 32px) / 1.3 |
| frase en tarjeta | 18px / 1.45 |
| cuerpo / contexto | 16px / 1.6 |
| interfaz | 14px / 1.4 |
| etiqueta (mayúsculas, +0.06em) | 11px / 1.3 |

## Espaciado y forma

- Escala de 4px: 4, 8, 12, 16, 20, 24, 32, 48.
- Contenido: máx. 1280px; lista 1fr / detalle 420px; tarjetas en 2 columnas (1 en celular).
- Radios: 16px en tarjetas y panel; 12px en inputs y selects; 999px en pastillas y botones.
- Sombra única y muy suave solo en la tarjeta activa y la hoja inferior: `0 1px 2px rgba(31,36,33,.06), 0 8px 24px rgba(31,36,33,.06)`.

## Componentes

- **Tarjeta de frase**: blanca, radio 16, padding 20; frase en Fraunces; pie con punto de color + tema y «Carta 163 · 1858». Hover: borde `--line` más oscuro. Activa: fondo `--card` con borde 2px `--sage-ink`.
- **Pastilla de tema**: borde `--line`, punto de color; activa = fondo `--sage`, texto `--sage-ink`, sin borde. Contador al lado.
- **Select**: fondo `--stone`, radio 12, flecha.
- **Botón principal**: pastilla `--ink` con texto `--card`. **Secundario**: pastilla `--stone`. **Fantasma**: solo texto con ícono.
- **Panel de detalle**: tarjeta fija (sticky) con: punto + tema, frase grande, filas etiqueta/valor (Carta, Destinatario, Año, Tomo), bloque de contexto, acciones (Copiar, Marcar, Enlace) y navegación ← → dentro de la lista filtrada.
- **Hoja inferior (celular)**: sube desde abajo con radio 16 arriba, asa, botón Cerrar y la misma información.

## Íconos e imágenes

Sin fotos. Íconos lineales SVG (buscar, copiar, estrella, enlace, flechas, cerrar), trazo 1.6px, extremos redondeados. Nada de emojis.
