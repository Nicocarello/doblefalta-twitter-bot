# Tennis API Skill

## Descripción

Esta habilidad define cómo interactuar con la API de Tenis (api-tennis.com) para obtener la agenda de partidos, resultados en vivo e información de los tenistas.

## URL Base

`https://api.api-tennis.com/tennis/`

## Autenticación

Todas las peticiones HTTP deben incluir el parámetro de consulta `APIkey`. (Lee esta clave de las variables de entorno o constantes de configuración provistas por el usuario).

## Endpoints y Métodos

### 1. get_fixtures (Agenda y Resultados)

- **Propósito:** Obtener la lista de partidos de un día específico.
- **Parámetros GET requeridos:**
  - `method=get_fixtures`
  - `date_start` (Formato YYYY-MM-DD)
  - `date_stop` (Formato YYYY-MM-DD)
- **Estructura de respuesta esperada:** Devuelve un JSON donde el nodo `result` contiene un arreglo de diccionarios (partidos). Campos clave a leer: `first_player_key`, `second_player_key`, `event_time`, `event_status`, `tournament_name`, `event_final_result`.

### 2. get_players (Información del Jugador)

- **Propósito:** Obtener detalles específicos de un tenista (nacionalidad, ranking).
- **Parámetros GET requeridos:**
  - `method=get_players`
  - `player_key` (ID numérico del jugador obtenido previamente en get_fixtures).
- **Estructura de respuesta esperada:** JSON donde el nodo `result` contiene datos del jugador. Campos clave a leer: `player_country`, `player_ranking`.

## Reglas de Ejecución para el Agente

Cuando tengas que escribir, refactorizar o modificar código relacionado con esta API en el proyecto, respeta obligatoriamente las siguientes directrices:

1. **Manejo de errores de Red:** Envuelve siempre las llamadas a la API (ej. `requests.get()`) en un bloque `try-except` manejando el timeout y posibles excepciones de conexión.
2. **Validación de la API:** Verifica siempre que el JSON devuelto tenga la clave `"success": 1` antes de intentar iterar o leer el nodo `result`.
3. **Caché obligatoria:** Para no sobrecargar la API ni agotar la cuota, la información obtenida del método `get_players` debe guardarse en memoria (ej. un diccionario `cache_jugadores = {}`). Antes de consultar a un jugador por su `player_key`, verifica primero si ya existe en esta caché.
4. **Acceso seguro a diccionarios:** Usa siempre el método `.get()` de Python para acceder a las claves de los JSON o diccionarios, y provee valores por defecto adecuados si la clave no existe, evitando así lanzar `KeyError`.




# 🎾 Tennis API Documentation (v2.9.4)

Documentación técnica para la integración de datos de tenis en tiempo real.

**Base URL:**`https://api.api-tennis.com/tennis/`

**Auth:** Requiere `APIkey` como parámetro en el query string.

---

## 📌 Índice de Métodos

- [Event Types](#1-event-types) - Tipos de torneos soportados.
- [Tournaments](#2-tournaments) - Lista de torneos por plan.
- [Fixtures](#3-fixtures) - Partidos programados y resultados pasados.
- [Livescore](#4-livescore) - Marcadores en tiempo real.
- [H2H (Head to Head)](#5-h2h-head-to-head) - Comparativa entre dos jugadores.
- [Standings](#6-standings) - Rankings ATP/WTA.
- [Players](#7-players) - Perfiles y estadísticas de jugadores.
- [Odds](#8-odds) - Cuotas de apuestas (Pre-match).
- [Live Odds](#9-live-odds) - Cuotas en vivo.

---

## 🛠 1. Event Types

Devuelve la lista de tipos de eventos (Atp Singles, Wta Doubles, etc.) según tu suscripción.

-**Endpoint:**`?method=get_events`

-**URL Ejemplo:**`https://api.api-tennis.com/tennis/?method=get_events&APIkey=TU_KEY`

---

## 🏆 2. Tournaments

Lista de todos los torneos disponibles.

-**Endpoint:**`?method=get_tournaments`

-**Campos clave:**`tournament_key`, `event_type_key`.

---

## 📅 3. Fixtures

Consulta partidos para un rango de fechas específico.

-**Endpoint:**`?method=get_fixtures`

-**Parámetros:**

  -`date_start` (yyyy-mm-dd) **[Obligatorio]**

  -`date_stop` (yyyy-mm-dd) **[Obligatorio]**

  -`player_key` (opcional)

  -`match_key` (opcional)

---

## ⚡ 4. Livescore

Partidos que se están jugando en este momento.

-**Endpoint:**`?method=get_livescore`

-**Información extra:** Incluye `pointbypoint` y `event_serve` (quién saca).

---

## 🤜🤛 5. H2H (Head to Head)

Historial de enfrentamientos directos entre dos jugadores.

-**Endpoint:**`?method=get_H2H`

-**Parámetros:** - `first_player_key`

  -`second_player_key`

---

## 📈 6. Standings

Clasificación mundial actual.

-**Endpoint:**`?method=get_standings`

-**Parámetros:**`event_type` (Valores: `ATP` o `WTA`).

---

## 👤 7. Players

Perfil detallado de un jugador.

-**Endpoint:**`?method=get_players`

-**Parámetros:**`player_key`

-**Data:** Devuelve cumpleaños, títulos y victorias por superficie (clay, hard, grass).

---

## 💰 8. Odds (Cuotas)

Cuotas de diferentes casas de apuestas (bet365, bwin, 1xbet, etc.).

-**Endpoint:**`?method=get_odds`

-**Mercados:** Home/Away, Correct Score, Set Betting.

---

## 📺 9. Live Odds

Cuotas actualizadas durante el transcurso del partido.

-**Endpoint:**`?method=get_live_odds`

-**Estado:** Indica si la cuota está suspendida (`suspended: Yes/No`).

---

> [!NOTE]

> **Formato de Fecha:** Siempre usa `YYYY-MM-DD`.

> **Timezone:** Por defecto es `Europe/Berlin`. Puedes cambiarlo con el parámetro `&timezone=America/New_York`.
