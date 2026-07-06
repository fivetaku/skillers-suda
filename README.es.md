[English](README.md) | [한국어](README.ko.md) | [中文](README.zh.md) | [日本語](README.ja.md) | Español

# skillers-suda

<p align="center">
  <img src="assets/skillers-suda-hero-01.png" alt="skillers-suda" width="320">
</p>

> **Cuatro agentes expertos charlan, debaten y convierten tu idea difusa en una skill de Claude Code que funciona.**

Describes una idea. Cuatro personas —planificador, usuario, experto, revisor— se lanzan como agentes paralelos reales, la debaten entre sí y luego te guían por una entrevista estructurada. Lo que sale al otro lado es una skill, un agente o un comando completamente montado, verificado automáticamente contra 9 criterios de calidad, medido con una eval A/B y con el trigger optimizado para que Claude sepa de verdad cuándo usarlo.

[Inicio rápido](#inicio-rápido) • [¿Por qué skillers-suda?](#por-qué-skillers-suda) • [Cómo funciona](#cómo-funciona) • [Funcionalidades](#funcionalidades) • [Los cuatro expertos](#los-cuatro-expertos) • [Requisitos](#requisitos)

---

## Inicio rápido

### 1. Añade el marketplace (solo una vez)

```
/plugin marketplace add https://github.com/fivetaku/gptaku_plugins.git
```

### 2. Instala el plugin

```
/plugin install skillers-suda
```

### 3. Reinicia Claude Code

### 4. Crea tu primera skill

```
/skillers-suda make a translation skill
```

O simplemente di lo que quieres en lenguaje natural:

```
make me a skill
create an agent
build a command
```

---

## ¿Por qué skillers-suda?

- **No requiere conocimientos de programación** —cada pregunta viene con explicaciones y sus pros y contras; si dudas, elige la opción marcada como (recommended)
- **Agentes reales, no personajes simulados** —cuatro subagentes de Claude corren en paralelo, cada uno analizando tu idea desde un ángulo distinto antes incluso de que empiece la entrevista
- **Diseño de flujos multipaso** —no es una skill de un solo prompt; seis tipos de paso (prompt / script / api_mcp / rag / review / generate) se componen automáticamente según tus respuestas
- **Control de calidad integrado** —9 comprobaciones estructurales se ejecutan justo después de la generación; los FAIL se corrigen solos antes de que veas el resultado
- **Eval A/B de serie** —se comparan automáticamente los resultados con y sin la skill, para que sepas que de verdad aporta
- **Optimización de triggers que funciona** —la description se refina en hasta 5 iteraciones con división train/test para evitar el sobreajuste
- **Modo de análisis incluido** —apúntalo a cualquier skill o agente existente y obtén una crítica desde cuatro perspectivas con sugerencias de mejora accionables

---

## Cómo funciona

```
You: "make a translation skill"
         ↓
Four expert agents spawn in parallel (planner / user / expert / reviewer)
         ↓
"We talked it over — here's what we think..."
         ↓
Structured interview (3–5 questions, each with options + explanations)
         ↓
Workflow design (prompt / script / api_mcp / rag / review / generate steps)
         ↓
SKILL.md + scripts/ + references/ generated automatically
         ↓
Quality verification (9 checks) → FAIL items auto-fixed → re-verified
         ↓
Eval runs (with_skill vs. without_skill A/B comparison)
         ↓
Description optimized (up to 5 iterations, 60/40 train/test split)
         ↓
"Want to test it?" → feedback → refinement loop
```

---

## Funcionalidades

### Flujo de creación de skills (9 fases)

| Fase | Qué ocurre |
|-------|-------------|
| A — Recogida de la idea | Recoge tu idea mediante AskUserQuestion; si ya hay un flujo en el contexto de la conversación, lo extrae |
| B — Despliegue del equipo experto | Cuatro agentes corren en paralelo; cada uno analiza la idea desde la perspectiva de su rol |
| C — Entrevista | 3–5 preguntas estructuradas con opciones, descripciones y valores recomendados |
| D — Confirmación del flujo | Los tipos de paso y su orden se confirman antes de escribir ningún archivo |
| E — Generación de archivos | Se escribe automáticamente el andamiaje SKILL.md + scripts/ + references/ |
| F — Eval | Se comparan escenarios with_skill vs. without_skill; un agente evaluador puntúa cada uno; resultados en eval_review.html |
| G — Verificación de calidad | verify-skill.py comprueba 9 elementos estructurales; corrige los FAIL y vuelve a verificar |
| H — Optimización de la description | run_loop.py genera ~20 consultas trigger/no-trigger e itera hasta 5 veces para encontrar la mejor description |
| I — Prueba y refinado | Bucle de refinado interactivo — ajusta el tono, añade pasos de API, optimiza scripts |

### Verificación de calidad (9 comprobaciones)

| Comprobación | Qué valida |
|-------|-----------------|
| frontmatter | Que la cabecera YAML esté bien formada |
| name | Que la skill tenga nombre |
| description | Que exista la descripción de trigger |
| third_person | Que la description use tercera persona |
| trigger_phrases | Que haya suficientes frases de trigger |
| word_count | Que el contenido no sea demasiado escaso |
| imperative_form | Que las instrucciones usen imperativo |
| references_exist | Que los archivos referenciados en references/ existan |
| progressive_disclosure | Que se use una estructura de revelado progresivo |

Cada comprobación reporta PASS / WARN / FAIL. Los FAIL se corrigen automáticamente antes de entregarte la skill.

### Tipos de paso del flujo

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| prompt | Claude lo resuelve razonando | Análisis de texto, resumen, traducción |
| script | Trabajo repetible / consistente / de API → Python o Bash | Llamadas a APIs, parseo de datos |
| api_mcp | Integración con herramientas externas (API preferida sobre MCP) | Enviar a Slack, consultar una BD |
| rag | Recuperación de conocimiento desde references/ | Glosario, guía de estilo |
| review | Control de calidad (IA o usuario) | Precisión de traducción, calidad del código |
| generate | Producción del resultado final | Creación de archivos, salida de informes |

### Modo de análisis

Ejecuta `/skillers-suda analyze <path>` sobre cualquier skill o agente existente. Los cuatro expertos lo revisan cada uno desde su perspectiva y producen un informe de mejora consolidado.

```
/skillers-suda analyze skills/my-skill/SKILL.md
/skillers-suda analyze .claude/agents/my-agent.md
```

### Selección de componente

Tras la entrevista, la skill determina automáticamente si tu caso de uso pide una skill, un agente o un comando —y genera la estructura de archivos apropiada.

---

## Los cuatro expertos

| Experto | Rol | Pregunta |
|--------|------|------|
| Planificador | Dirección y alcance | "¿Quién lo usa? ¿Qué problema resuelve?" |
| Usuario | Validación de UX | "¿Cómo lo usaría yo en realidad?" |
| Experto | Viabilidad técnica | "Esto es lo que hay que vigilar en este dominio" |
| Revisor | Detección de casos límite | "¿Sigue funcionando en este caso?" |

Los cuatro se lanzan como subagentes paralelos reales de Claude —no es una simulación de roles.

---

## Comandos

| Comando | Descripción |
|---------|-------------|
| `/skillers-suda` | Menú interactivo (nueva skill / analizar / guía de uso) |
| `/skillers-suda [description]` | Empieza la entrevista de inmediato con tu idea |
| `/skillers-suda analyze [path]` | Analiza una skill o agente existente |

### Triggers en lenguaje natural

- "make me a skill"
- "create an agent"
- "build a command"
- "skillers-suda"
- "skill builder"

---

## Requisitos

- CLI de [Claude Code](https://docs.anthropic.com/claude-code)
- Suscripción Claude Max/Pro o una clave de la API de Claude compatible

Sin más dependencias. Sin npm install. Sin paso de build.

---

## Licencia

MIT

---

<div align="center">

**Di una frase. Obtén una skill que funciona.**

</div>
