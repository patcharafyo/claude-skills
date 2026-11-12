# Claude skills

Personal skills for Claude Code and the Claude app. Each folder under `skills/` is one
skill: a `SKILL.md` with its instructions, plus any templates, references and scripts
it uses.

| Skill | What it does |
| --- | --- |
| [architecture-diagram](skills/architecture-diagram/SKILL.md) | Draws a system or architecture diagram as one HTML page: deployment zones, components, numbered connections, a connection table and a zoom-in of the key part. Seven contrast-checked accent colours (orange, blue, green, teal, purple, red, graphite) or a brand colour, in light and dark mode. |

## Use a skill in Claude Code (every project)

Copy the skill into your personal skills folder:

```bash
git clone https://github.com/patcharafyo/claude-skills.git ~/claude-skills
cp -R ~/claude-skills/skills/architecture-diagram ~/.claude/skills/
```

Or link it, so a `git pull` here updates the skill everywhere:

```bash
ln -s ~/claude-skills/skills/architecture-diagram ~/.claude/skills/architecture-diagram
```

New Claude Code sessions pick it up. Ask for it in plain words ("draw the system
diagram for this repo in blue") or call it with `/architecture-diagram`.

## Use a skill in the Claude app (chat)

Zip the skill folder and upload it under **Settings → Capabilities → Skills**:

```bash
cd ~/claude-skills/skills && zip -r ~/Downloads/architecture-diagram.zip architecture-diagram -x '*.DS_Store'
```

The app keeps its own copy, so upload again after changing the skill.

## Change a skill

Edit the files under `skills/<name>/`, then commit and push. If you copied the skill
rather than linking it, copy it into `~/.claude/skills/` again.

For `architecture-diagram`, check the colours after any change to the template's styles:

```bash
python3 skills/architecture-diagram/scripts/accent.py check skills/architecture-diagram/template.html
```
