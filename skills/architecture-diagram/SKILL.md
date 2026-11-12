---
name: architecture-diagram
description: Draw a system or architecture diagram as one self-contained HTML page with inline SVG (deployment zones, components, numbered connections, a connection table and a zoom-in of the key part) in a chosen accent colour (orange, blue, green, teal, purple, red, graphite or a brand colour), readable in light and dark mode. Use when asked for a system diagram, block diagram, architecture or flow diagram, "how X connects to Y", "how the app/chat/VM fit together", or to recolour or update a page made this way.
---

# Architecture diagram

Produces one HTML page with an overview of the whole system, a table of what each
connection carries, a zoom-in of the part that matters most, and the rules the layout
enforces. `template.html` shows the finished result.

## Files in this skill

Paths are relative to this skill's folder, written `<skill>` below: the base directory
shown when the skill loads (in Claude Code, `~/.claude/skills/architecture-diagram`).

| File | Use |
| --- | --- |
| `template.html` | A finished, real page (the LLM Harness system). Copy it. Keep its `<style>` block exactly; replace **all** of the content. None of its names, numbers or rules belong in a new diagram. |
| `reference/primitives.md` | Copy-paste SVG for zones, boxes, chips, edges, labels, badges, legend, plus spacing rules. Read it before placing anything. |
| `scripts/accent.py` | `check PAGE` verifies every accent's contrast. `make "#hex" NAME` builds a brand accent. |

## Workflow

1. **Collect facts from the code, not memory.** Find each component, how it is
   deployed, and every connection: protocol, port, auth or key, limits, who holds the
   secret. Search for things like `fetch(`, `listen(`, `ssh`, `docker`, env var names,
   infra files. Record the commit hash and anything optional you leave out.
   If there is no code to read (the user describes the system, or it lives elsewhere),
   use what they give you, ask about gaps that change the picture, and say in your
   reply which details you assumed.
2. **Write the connection table first.** One row per connection, in the order a request
   travels: # · Connection (A → B or A ↔ B) · How it connects · What it carries.
   These numbers become the badges.
3. **Choose the zones** (deployment boundaries: a device, a service, a VM, a shared
   service) and the **1–3 highlighted components** (what the reader should come away
   understanding). Everything else is neutral.
4. **Sketch the grid.** Request path down the centre column; external services in side
   zones left and right; storage at the bottom; deploy-only things in a corner.
5. **Copy `template.html`** to the output path, set the accent, then replace the content
   section by section using `reference/primitives.md`. Output path: the one the user
   names; otherwise, in a repo with a `docs/` folder, `docs/<topic>/<name>.html`;
   otherwise, in a chat with no project folder, the place this environment uses for
   files it hands to the user; otherwise ask. Updating an existing page: edit it in
   place, keep its accent.
6. **Draw the zoom-in** of the highlighted part, one level deeper (processes, ports,
   protocols), using the same classes and its own marker ids (`a2`, `h2`, `d2`).
7. **Check the result** (see the end of this file) and fix what you find before reporting.

## Page structure (always this order)

1. `h1` "How <system> fits together" + `p.lede`: one sentence that traces a request
   end to end.
2. `h2` "The whole system": the overview figure (legend inside the SVG, numbered
   badges), `p.hint`, and a one- or two-sentence `figcaption` giving the main idea.
3. `h2` "What each connection carries": the table, one row per badge.
4. `h2` "Inside the <part>: how each <piece> connects": one-sentence intro, zoom-in
   figure, caption.
5. `h2` "Rules this layout enforces": 3–6 bullets, each starting with a bold
   one-sentence rule followed by the reason or limit.
6. `footer`: the commit hash, the deployed image or version, the date, and optional
   connections not drawn.

Drop a section only when it truly has nothing to say (e.g. no zoom-in for a system with
no interesting inside). Never add other sections.

## What the visual elements mean

Keep these meanings fixed so every diagram reads the same way.

- **Zone** (`.zone`): where it runs. One per machine, service or device.
- **Box** (`.box`): one component. A title, and a subtitle of 2–4 facts joined by " · ".
- **Highlighted box** (`.hot`): the 1–3 components the story is about.
- **Chips** (`.chip`): alternatives ("one chosen per task") or instances (Project A, B).
- **Group** (`.group`): related boxes that share something but are not a deployment.
- **Solid arrow** (`.edge`): used while the system runs.
- **Dashed arrow** (`.edge-dash`): used only when deploying or starting.
- **Accent arrow** (`.edge-hot`): the highlighted component's paths in and out.
- **Badge** (`.badge`): a number that matches one table row.

Lines are horizontal or vertical only, never diagonal, never through a box. Every
arrow has a label. The legend lists only the arrow kinds the diagram uses.

## Colour

The page has neutral greys plus **one accent colour**. The accent appears only on
highlighted boxes, their arrows, the focus outline and list bullets. Everything else
stays neutral; that restraint is what makes it look professional.

### Switching the accent

Set one attribute on the `<html>` tag:

```html
<html lang="en" data-accent="green">
```

| Accent | Light | Dark | Good for |
| --- | --- | --- | --- |
| `orange` (default) | `#b4510f` | `#f09a5c` | Warm, stands out; the current house look |
| `blue` | `#1d5bbf` | `#7eaef5` | The safest corporate choice; reviews, exec readers |
| `green` | `#1d7646` | `#63c48e` | Operations, data pipelines, cost, the "healthy path" |
| `teal` | `#0e6f7a` | `#4fc1cc` | Cloud and infrastructure; a calmer alternative to blue |
| `purple` | `#5b45b5` | `#a99bf2` | AI and model features |
| `red` | `#b3262f` | `#f28b8f` | Only when the highlight is a security boundary, a risk or a failure path |
| `graphite` | `#3d4856` | `#b6c0cc` | Monochrome: printing, formal documents, sitting next to another brand. Highlighted lines are drawn thicker to stand out |

Each preset has a light and a dark value and adapts to the viewer's theme on its own.
`data-theme="light"` or `"dark"` on `<html>` forces a theme (e.g. for a screenshot).

If the user just says a colour name ("make it greener", "use navy"), map it to the
nearest preset (navy → `blue`, mint → `green`, grey/black → `graphite`). Use a custom
accent only when they give a brand colour or none of the presets fit.

### Brand colour

```bash
python3 <skill>/scripts/accent.py make "#0b6e4f" brand
```

It adjusts the colour's lightness until it is readable on both light and dark pages,
prints a `:root[data-accent="brand"] { … }` rule and a contrast report. Paste the rule
under the other presets in the page's `<style>`, set `data-accent="brand"`, and say in
your reply if the colour had to be darkened or lightened noticeably.

### Colour rules

- One accent per page. Never add a second highlight colour, status colours or
  per-component colours.
- Never write a hex value in the SVG or inline styles. Use the classes; they read the tokens.
- Every diagram on the page uses the same accent.
- After any colour change, run
  `python3 <skill>/scripts/accent.py check <page>`;
  every preset must show PASS.

## Writing

- Plain words. Box titles are nouns ("Task queue"); arrow labels are short verb
  phrases ("queues the task") or protocol above / auth below ("HTTPS" / "gateway key").
- Use real names for resources, images and limits (e.g. `aigw-ca-prd`, "up to 20 tasks").
- The SVG `aria-label` describes the whole flow as a short paragraph, so the diagram
  makes sense without seeing it.
- The table's "What it carries" column says what data moves and who checks it.
- No marketing words, no emoji, no exclamation marks.

## Check before reporting

1. Open the page in a browser you can drive (the built-in browser pane if there is one,
   otherwise a headless screenshot) at 1440 wide. If nothing here can render a page,
   do the other checks and say the visual check was not done. Look for text overlapping text or
   lines, labels outside their box, arrows that miss their box or cross another box,
   and empty bands at the bottom of an SVG.
2. Switch to dark (`data-theme="dark"`) and to mobile width (375). The SVG should
   scroll sideways with the hint showing; the table should stack.
3. Each badge number has exactly one table row, and every row has a badge.
4. The legend lists exactly the arrow kinds used.
5. `accent.py check <page>` passes.
6. Every fact in the table can be pointed to in the code or config you read.

When reporting, name the output file, the accent used, and anything you left out of
the diagram on purpose.
