# Verification Checklist

Before declaring a resource migration complete:

1. [ ] All embedded resource content removed from `SKILL.md`.
2. [ ] All resource files copied to `assets/<skill>/<category>/`.
3. [ ] `SKILL.md` loads resources exclusively via `get_asset` / `render_asset`.
4. [ ] `unresolved_placeholders` checked after any `render_asset` call.
5. [ ] Skill validates with `node scripts/validate.mjs .` (exit 0).
6. [ ] Asset paths use correct pattern: `assets/<skill>/<category>/<name>`.