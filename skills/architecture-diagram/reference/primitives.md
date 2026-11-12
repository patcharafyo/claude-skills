# SVG primitives and geometry

Copy-paste building blocks for the diagrams. All of them use the classes in
`template.html`, so colour, dark mode and accent come for free. Coordinates are in
the SVG's own units (viewBox width 1200).

## Canvas

```html
<div class="scroll" tabindex="0" role="region" aria-label="System block diagram, scrollable">
  <svg viewBox="0 0 1200 740" role="img" aria-label="ONE PARAGRAPH: the whole flow in plain prose.">
    <defs>
      <!-- Marker ids must be unique on the page: a/h/d in diagram 1, a2/h2/d2 in diagram 2 -->
      <marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="marker-ink" d="M0 1 L9 5 L0 9 Z"/></marker>
      <marker id="h" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="marker-hot" d="M0 1 L9 5 L0 9 Z"/></marker>
      <marker id="d" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path class="marker-muted" d="M0 1 L9 5 L0 9 Z"/></marker>
    </defs>
    <!-- Draw order: zones → legend → boxes → edges → badges (later items paint on top) -->
  </svg>
</div>
<p class="hint">Scroll sideways to see the whole diagram. The table below lists every connection.</p>
```

Height: overview 600–760, zoom-in 380–460. Pick the smallest height that fits; no
empty band at the bottom (last zone ends 4–20 units above the viewBox bottom).

## Zone: a deployment boundary

```html
<rect class="zone" x="360" y="172" width="480" height="564" rx="14"/>
<text class="z" x="376" y="194">Azure App Service</text>
<text class="s" x="824" y="194" text-anchor="end">one container, one copy</text>
```

- Label at (x+16, y+22). Optional note right-aligned at (x+width−16, y+22).
- First box inside starts at y+34. Inner padding 16–20 on each side.
- Outer gutter 20 from the canvas edge. Gap between zones ≥ 40 (room for an arrow + label).
- A zone inside a zone (e.g. "Application core") uses rx 11 and the same label offsets.

## Box: one component

```html
<rect class="box" x="380" y="206" width="440" height="58" rx="9"/>
<text class="t m" x="600" y="230">Web server (Express)</text>
<text class="s m" x="600" y="249">sign-in · projects · files · live result stream</text>
```

- Text x = box x + width/2. Title baseline ≈ y+24 (58-tall box) to y+30 (72-tall).
  Subtitle baseline = title + 19. Each extra subtitle line: +17.
- Heights: 58 (title + 1 line), 62–72 (roomier), +17 per extra line.
- Width: fit the longest line. Rough text width ≈ 0.55 × font-size × characters
  (13.5px title ≈ 7.4/char, 11.5px subtitle ≈ 6.3/char). Keep 14+ units of side padding.
- Subtitle style: 2–4 short facts joined by " · ". No full sentences.

## Highlighted box: what the story is about

```html
<rect class="hot" x="380" y="540" width="210" height="72" rx="9"/>
```

Same text rules as a box. Use on 1–3 boxes per diagram, never more.

## Chips: alternatives or instances inside a box

```html
<rect class="hot" x="380" y="384" width="440" height="112" rx="10"/>
<text class="t m" x="600" y="406">Harness runtime: one chosen per task</text>
<rect class="chip" x="390" y="420" width="99" height="62" rx="7"/>
<text class="ct m" x="439.5" y="447">DeepSeek</text>
<text class="cs m" x="439.5" y="465">built-in engine</text>
```

- Chips sit 10 in from the parent's sides, 8 apart, all the same width:
  chip width = (parent width − 20 − 8 × (n−1)) / n.
- Chip title baseline ≈ chip y+27, subtitle +18.
- Say how the chips relate in the parent title ("one chosen per task", "up to 20 active").

## Group: related boxes that are not a deployment boundary

```html
<rect class="group" x="36" y="136" width="226" height="258" rx="10"/>
<text class="s m" x="149" y="156">child processes, temporary folders</text>
```

## Edges

| Class | Marker | Means |
| --- | --- | --- |
| `edge` | `#a` | Used while the system runs |
| `edge-dash` | `#d` | Used only at deploy / start-up |
| `edge-hot` | `#h` | The highlighted component's paths in and out |

```html
<!-- one way -->
<line class="edge" x1="600" y1="264" x2="600" y2="294" marker-end="url(#a)"/>
<!-- two way -->
<line class="edge-hot" x1="820" y1="576" x2="936" y2="576" marker-start="url(#h)" marker-end="url(#h)"/>
<!-- around a corner: H and V only -->
<path class="edge" d="M780 85 H1130 V206" marker-end="url(#a)"/>
```

- Endpoints touch the box edge exactly (the marker's refX handles the tip).
- Only horizontal and vertical segments. At most two bends. Never cross a box.
- Avoid crossing other edges. If one must cross a zone border, draw a halo first:
  `<line class="halo" x1="376" y1="576" x2="364" y2="576"/>`.
- Parallel edges between the same two columns: ≥ 60 apart vertically.

## Edge labels

```html
<text class="l" x="636" y="283">queues the task</text>            <!-- beside a vertical edge -->
<text class="l m" x="880" y="558">private VNet</text>              <!-- above a horizontal edge -->
<text class="l m" x="880" y="604">pinned SSH</text>                <!-- below it: auth / key -->
```

- Vertical edge: label starts 12 right of the line (36 when a badge sits there),
  baseline near the vertical middle.
- Horizontal edge: label centred on the gap, 18 above the line; second label 28 below.
- A short verb phrase ("routes by model"), or the protocol above and the auth below.

## Badge: links an edge to a table row

```html
<circle class="badge" cx="600" cy="152" r="10"/><text class="n" x="600" y="156">2</text>
```

- Centre on the edge (cx/cy on the line), number baseline = cy+4.
- On a vertical edge with a label, put the badge on the line and the label 36 right
  of it. On a horizontal edge, put the badge at the midpoint between the two labels.
- Numbers follow the request's path. Twin connections (same meaning) may share a number.

## Legend (inside the overview SVG, top-left, in empty space)

```html
<text class="z" x="20" y="186">How to read this</text>
<line class="edge" x1="20" y1="212" x2="62" y2="212" marker-end="url(#a)"/>
<text class="l" x="74" y="216">Used while the app runs</text>
<line class="edge-dash" x1="20" y1="238" x2="62" y2="238" marker-end="url(#d)"/>
<text class="l" x="74" y="242">Used only when deploying</text>
<line class="edge-hot" x1="20" y1="264" x2="62" y2="264" marker-end="url(#h)"/>
<text class="l" x="74" y="268">The harness and its two paths out</text>
<circle class="badge" cx="41" cy="290" r="10"/><text class="n" x="41" y="294">1</text>
<text class="l" x="74" y="294">Numbered in the table below</text>
```

Rows 26 apart. List only edge kinds the diagram uses. The accent row names the
highlighted thing ("The harness and its two paths out"), not "highlighted".

## Endpoint outside the frame

For a service shown in the overview but outside the zoom-in, end the edge in a bare
title instead of a box:

```html
<line class="edge" x1="1014" y1="127" x2="1100" y2="127" marker-start="url(#a2)" marker-end="url(#a2)"/>
<text class="t" x="1108" y="122">LiteLLM</text>
<text class="t" x="1108" y="140">gateway</text>
```
