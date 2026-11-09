# Frases de San Miguel Garicoïts

Sitio web estático con **608 frases breves** tomadas de la correspondencia de San Miguel Garicoïts (1797–1863), fundador de la Congregación del Sagrado Corazón de Jesús de Betharram. Cada frase lleva su referencia (tomo y número de carta), el destinatario, el año y una nota de contexto que explica a quién escribía y por qué.

**Sitio publicado:** https://gzacur.github.io/smg-quotes-web/

## Qué permite hacer

- Ver las frases como tarjetas y filtrarlas por **tema** (10), **destinatario** (4 tipos) y **tomo** (I, II, III).
- Buscar por palabra, nombre o lugar en la frase, el destinatario o el contexto (sin distinguir acentos).
- Ver la **selección esencial** (25 frases) o solo las **marcadas**.
- Abrir el **detalle** de una frase: en escritorio, en un panel fijo a la derecha; en celular y tablet, en una vista de pantalla completa con «Volver a la lista» y «Anterior / Siguiente».
- Pasar de frase con ← → del teclado (con el foco en la lista o el detalle) o deslizando el dedo en el celular.
- Copiar la frase con su cita, copiar un enlace directo a la frase (`#n-<id>`) y marcarla como favorita.

## Estructura del repositorio

```
smg-quotes-web/
├── index.html                          Página principal: lector con filtros (generado)
├── frase/<id>/index.html               Una página estática por frase, 608 en total (generado)
├── tema/<slug>/index.html              Una página por tema, 10 en total (generado)
├── sitemap.xml · robots.txt · 404.html Archivos para buscadores (generados)
├── .nojekyll                           Desactiva Jekyll en GitHub Pages
├── assets/
│   ├── page.css                        Estilos de las páginas de frase y de tema (generado)
│   ├── og-image.png                    Imagen de vista previa para redes (1200×630)
│   ├── favicon.svg · apple-touch-icon.png
├── src/
│   └── template.html                   Plantilla de la página principal: HTML, CSS y JS
├── data/
│   ├── frases.json                     Datos que usa el sitio (608 registros)
│   └── Frases_San_Miguel_Garicoits.md  Fuente de datos legible: frases clasificadas con referencia y contexto
├── scripts/
│   └── build.py                        Genera todo el sitio a partir de la plantilla y los datos
└── docs/
    └── DESIGN.md                       Sistema de diseño: colores, tipografía, espaciado y componentes
```

## Tecnología

- **HTML, CSS y JavaScript sin dependencias ni framework.** La página principal es un único `index.html` con los datos incrustados como JSON (`<script type="application/json">`), así funciona en GitHub Pages, sin servidor y también abriéndolo desde el disco.
- **Fuentes:** Fraunces (frases) y Plus Jakarta Sans (interfaz), desde Google Fonts, con fuentes de respaldo del sistema.
- **Modo claro y oscuro** automático según el dispositivo (`prefers-color-scheme`), con todos los colores definidos como variables CSS.
- **Responsive:** escritorio (lista en 2 columnas + panel de detalle fijo), tablet (2 columnas + detalle a pantalla completa) y celular (1 columna + detalle a pantalla completa).
- **Accesibilidad:** títulos semánticos (h1/h2), foco visible distinto de la selección, controles con etiquetas, botones táctiles de 44 px en celular, contraste mínimo 4.5:1, respeta `prefers-reduced-motion`.
- **Favoritas:** se guardan en `localStorage` del navegador de cada persona (no se comparten ni se envían a ningún servidor).
- **Analítica:** Google Tag Manager con eventos de uso (ver [Analítica](#analítica-google-tag-manager)).
- **Peso:** ~280 KB sin comprimir, incluidos los datos.

## Datos

### Fuente

Las frases se extrajeron de los tres tomos de la *Correspondencia de San Miguel Garicoïts* (edición del P. Pierre Miéyaa, scj; traducción al español del P. Miguel Martínez y del P. Angelo Recalcati, scj):

| Tomo | Cartas |
|---|---|
| I | 1 – 173 (1825 – 1859) |
| II | 174 – 480 |
| III | *Nuevas cartas*: números con *bis/ter* que completan los tomos anteriores y cartas desde la 485 |

### Proceso

1. Extracción del texto de los PDF (`pdftotext -layout`) y limpieza de notas al pie y números de página.
2. Lectura completa de las cartas y selección de frases **literales** de una línea (≤ ~150 caracteres); «…» indica un recorte, nunca una paráfrasis.
3. Verificación automática de que cada frase aparece en el texto original.
4. Redacción de una nota de contexto por frase a partir de la carta y de las notas del editor.
5. Clasificación por tema y por tipo de destinatario.

El resultado legible es [`data/Frases_San_Miguel_Garicoits.md`](data/Frases_San_Miguel_Garicoits.md); el sitio usa la misma información en [`data/frases.json`](data/frases.json).

### Esquema de `frases.json`

Cada registro es un objeto con estas claves (cortas para reducir el peso):

| Clave | Significado | Ejemplo |
|---|---|---|
| `id` | Identificador único (se usa en el enlace `#n-<id>`) | `195` |
| `t` | Tomo: `I`, `II`, `III` | `"I"` |
| `c` | Número de carta (puede llevar `bis`/`ter`) | `"163"` |
| `d` | Destinatario | `"Al P. Diego Barbé, Superior del Colegio San José"` |
| `p` | Tipo de destinatario: `HC` Hijas de la Cruz · `SCJ` religiosos de Betharram · `CL` obispos y clero · `LA` laicos y familia | `"SCJ"` |
| `y` | Año de la carta (vacío si no figura) | `"1858"` |
| `k` | Tema (ver tabla) | `"GO"` |
| `f` | Frase literal | `"Hay que tomar a los hombres como son…"` |
| `x` | Contexto | `"Hacia 1858…"` |
| `e` | `1` si pertenece a la selección esencial | `0` |

| Código | Tema |
|---|---|
| `VD` | Voluntad de Dios y disponibilidad |
| `OB` | Obediencia y humildad |
| `AM` | Amor de Dios y Sagrado Corazón |
| `CO` | Confianza y abandono en Dios |
| `OR` | Oración, vida interior y santidad |
| `CR` | Cruz, sufrimiento y paciencia |
| `AN` | Ánimo, alegría y paz interior |
| `CF` | Caridad fraterna y vida comunitaria |
| `GO` | Gobierno y acompañamiento |
| `MI` | Misión, celo apostólico y educación |

## SEO

- **Una URL indexable por frase y por tema.** Los enlaces `#n-<id>` del lector no se indexan, así que el build genera `frase/<id>/` (608 páginas) y `tema/<slug>/` (10 páginas) como HTML estático, cada una con su `<title>` y `meta description` únicos, un solo `h1`, URL canónica, migas de pan y enlaces a la frase anterior y siguiente.
- **Contenido en el HTML.** La página principal ya trae escritas las primeras 40 frases, el detalle de la primera y los enlaces a los temas, de modo que los buscadores (y quien no tenga JavaScript) ven contenido sin ejecutar scripts. El JavaScript lo reemplaza al cargar.
- **Datos estructurados (JSON-LD, schema.org):** `WebSite`, `Person` (San Miguel Garicoïts, con enlaces a Wikipedia) y `CollectionPage` en la portada; `Quotation` con autor, fuente (`Book`), tema y año en cada frase; `CollectionPage` + `ItemList` en cada tema; `BreadcrumbList` en las páginas internas.
- **Redes sociales:** Open Graph y Twitter Card con imagen `assets/og-image.png` (1200×630).
- **Rastreo:** `sitemap.xml` con las 619 URL, `robots.txt` que lo declara, `404.html` con `noindex`, `lang="es"`, `meta robots` y `theme-color` para claro y oscuro.
- **Rendimiento:** sin dependencias, `preconnect` a Google Fonts con `display=swap`, estilos de las páginas internas en un archivo compartido y cacheable.

Después de publicar, conviene dar de alta el sitio en **Google Search Console** (propiedad de prefijo de URL `https://gzacur.github.io/smg-quotes-web/`) y enviar `sitemap.xml`.

## Analítica (Google Tag Manager)

El sitio carga el contenedor de Google Tag Manager **`GTM-KQHR3TV3`** en el `<head>` (ver el inicio de `src/template.html`). Además del código provisto, se envía el evento estándar `gtm.js` (`gtm.start`), que GTM necesita para que funcionen los activadores de «Todas las páginas / Vista de página».

Desde el contenedor se puede conectar la etiqueta de Google Analytics 4. Para medir el uso, el sitio envía al `dataLayer` estos eventos personalizados:

| Evento | Cuándo | Parámetros |
|---|---|---|
| `quote_view` | Se abre el detalle de una frase | `quote_id`, `quote_letter`, `quote_volume`, `quote_theme`, `quote_recipient_type`, `view_mode` (`panel` / `pantalla_completa`) |
| `filter_change` | Cambia un filtro | `filter_type` (`tema`, `destinatario`, `tomo`, `seleccion_esencial`, `marcadas`), `filter_value`, `results` |
| `search` | Búsqueda de 3 o más letras (tras 1,2 s sin escribir) | `search_term`, `results` |
| `quote_copy` | «Copiar» | parámetros de la frase |
| `quote_share_link` | «Enlace» | parámetros de la frase |
| `quote_favorite` / `quote_unfavorite` | «Marcar» / desmarcar | parámetros de la frase |

Para verlos en GA4: en GTM crear una variable de capa de datos por parámetro, un activador de **Evento personalizado** con el nombre del evento, y una etiqueta **Evento de GA4** que los envíe.

## Desarrollo

Requisito: Python 3 (solo para regenerar el sitio).

```bash
# 1. Editar la plantilla (src/template.html) o los datos (data/frases.json)
# 2. Regenerar el sitio (index, páginas de frase y de tema, sitemap)
python3 scripts/build.py
# 3. Probar localmente
python3 -m http.server 8000   # y abrir http://localhost:8000
```

Para corregir o agregar una frase, editar `data/frases.json` (y, si se quiere mantener la versión legible al día, `data/Frases_San_Miguel_Garicoits.md`) y volver a ejecutar el script.

## Publicación

GitHub Pages sirve el sitio desde la rama `master`, carpeta raíz (`/`). Cada `push` a `master` actualiza el sitio en uno o dos minutos.

## Diseño

Ver [`docs/DESIGN.md`](docs/DESIGN.md): fondo lino con tarjetas blancas, acento verde salvia, serif Fraunces para las frases. Referencias estudiadas en UXKIN: Gleap, Alden y Craft Docs.

## Derechos

El código del sitio puede reutilizarse libremente. Las frases y su traducción pertenecen a la edición citada de la *Correspondencia*; las notas de contexto son un resumen elaborado para este sitio. Antes de un uso público amplio conviene confirmar el permiso de la Congregación del Sagrado Corazón de Jesús de Betharram.
