# Cola de publicación de La Bisagra

Este repo es público y sirve solo de depósito: las tareas de producción dejan acá las piezas TERMINADAS (no se sacan fotos de acá) y la tarea "Publicador Metricool" las carga en Metricool. Metricool copia cada archivo a su propio servidor al crear la publicación, así que los archivos de acá se borran a los 3 días.

`config.json` → `"modo"`: `"aprobacion"` (las publicaciones entran a Metricool como BORRADOR y Tomás las aprueba) o `"automatico"` (se programan y se publican solas). Solo Tomás decide cambiarlo.

## 1. Cómo encolar una pieza (tareas de producción)

1. Clonar: `git clone --depth 1 https://github.com/labisagra0-hub/labisagra-publicaciones pub`.
   Si falla por permisos, llamá a la herramienta `add_repo` (owner `labisagra0-hub`, repo `labisagra-publicaciones`, access `push`) y reintentá una vez.
2. Copiar los archivos finales a `pub/AAAA/MM/DD/` con nombres en minúscula, sin espacios ni tildes (ej. `efem-2026-10-09-1.jpg`, `reel-2026-10-09.mp4`).
   Videos: mp4 H.264 + AAC, máximo 95 MB (si pesa más: `ffmpeg -i in.mp4 -c:v libx264 -crf 26 -preset slow -c:a aac out.mp4`).
3. Escribir el manifiesto `pub/cola/AAAA-MM-DD-HHMM-<pieza>.json` (formato abajo).
4. Subir: `cd pub && git add -A && git -c user.name="La Bisagra" -c user.email="labisagra0@gmail.com" commit -qm "Cola: <pieza> <fecha>" && git push -q origin main`.
   Si el push es rechazado porque otra tarea subió algo: `git pull --rebase -q origin main` y reintentar (hasta 3 veces).
5. No crees nada en Metricool vos: el Publicador corre cada hora a los :20 (de 8:20 a 0:20) y lo hace.

## 2. Formato del manifiesto

```json
{
  "pieza": "pulso | carrusel-efemerides | reel-efemerides | tarjeta-hoy | carrusel-dia | reel-prueba",
  "titulo_interno": "Una línea para identificarla (no se publica)",
  "hora": "2026-10-09T12:30:00-03:00",
  "archivos": ["2026/10/09/efem-2026-10-09-1.jpg", "2026/10/09/efem-2026-10-09-2.jpg"],
  "publicaciones": [
    {"red": "instagram", "tipo": "POST", "texto": "pie completo"},
    {"red": "instagram", "tipo": "STORY", "archivos": ["2026/10/09/efem-2026-10-09-1.jpg"], "hora": "2026-10-09T12:35:00-03:00"},
    {"red": "tiktok", "titulo": "título corto (máx. 90 caracteres)", "texto": "descripción con hashtags"}
  ]
}
```

- `hora` (general o por publicación): cuándo sale. Si ya pasó o faltan menos de 10 minutos, el Publicador usa ahora + 15 minutos.
- `archivos` (general o por publicación): rutas dentro del repo, en orden. Imágenes = carrusel si son varias.
- Tipos válidos:
  - Instagram: `STORY` (sin texto; si la imagen no es 9:16 el Publicador la adapta), `POST` (imagen o carrusel, con `texto`), `REEL` o `TRIAL_REEL` (video, con `texto`). `TRIAL_REEL` = Reel de prueba: Instagram lo muestra primero solo a no seguidores.
  - TikTok: video o carrusel de fotos, con `titulo` y `texto`.
  - YouTube: `{"red":"youtube","tipo":"short","titulo":"... #Shorts","texto":"descripción"}` (solo video).
- Opcionales por publicación: `"ia": true` cuando el video tiene la voz de IA (marca contenido generado/alterado con IA en IG, TikTok y YouTube).
- Textos: los mismos que la tarea ya escribe para cada red (pie de Instagram con gancho en la primera línea, datos, "La bisagra:", pregunta final, "Video completo en YouTube: link en la bio", 5 hashtags con #historiaargentina y #labisagra; TikTok: título de una línea con el dato, 3 hashtags del tema + #historia #geopolitica, "video completo: link en la bio").
- Nunca se encola nada para X (pausado).

## 3. Qué encola cada tarea

| Tarea | Pieza | Publicaciones |
|---|---|---|
| Pulso cada 2 horas | `pulso` | IG `STORY` (ahora) |
| Efemérides: carrusel y reel (11:25) | `carrusel-efemerides` | IG `POST` 12:30 + TikTok carrusel 12:30 + IG `STORY` con la placa 1 a las 12:35 |
| Efemérides: carrusel y reel | `reel-efemerides` | IG `REEL` 12:45 + TikTok 12:45 + YouTube `short` 12:45, todos con `"ia": true` |
| Briefing diario (lun a vie) | `tarjeta-hoy` | IG `STORY` 17:30 + TikTok carrusel de 1 foto 17:30 |
| Carrusel El día en el mundo (20:30) | `carrusel-dia` | IG `POST` 21:30 + TikTok carrusel 21:30 + IG `STORY` con la lámina 1 a las 21:35 |

## 4. Carpetas

- `cola/` manifiestos pendientes · `hechos/` cargados en Metricool (con sus `plannerUrl`) · `errores/` los que fallaron (con el error).
- `AAAA/MM/DD/` piezas. El Publicador borra las carpetas de días con más de 3 días de antigüedad.
- `herramientas/historia916.py` adapta una imagen 4:5 a historia 9:16 (fondo difuminado).
