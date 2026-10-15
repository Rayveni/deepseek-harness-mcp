from pathlib import Path
import re


ASSETS_ROOT = (Path(__file__).parent.parent / 'assets').resolve()
TEXT_EXT = {'.md', '.txt', '.json', '.yaml', '.yml', '.rst'}


def _available_skills() -> list[str]:
    if not ASSETS_ROOT.is_dir():
        return []
    return sorted(p.name for p in ASSETS_ROOT.iterdir() if p.is_dir())


def _skill_dir(skill: str) -> Path:
    """Validate skill and return its resolved directory."""
    if not skill or any(c in skill for c in ('/', '\\', '..')):
        raise ValueError(f'Invalid skill name: {skill!r}')
    base = (ASSETS_ROOT / skill).resolve()
    if base.parent != ASSETS_ROOT or not base.is_dir():
        raise ValueError(
            f'Unknown skill {skill!r}. Available: {_available_skills()}'
        )
    return base


def _category_dir(skill: str, category: str) -> Path:
    base = _skill_dir(skill)
    if not category or any(c in category for c in ('/', '\\', '..')):
        raise ValueError(f'Invalid category name: {category!r}')
    cat = (base / category).resolve()
    if cat.parent != base or not cat.is_dir():
        available = sorted(p.name for p in base.iterdir() if p.is_dir())
        raise ValueError(
            f'Unknown category {category!r} in skill {skill!r}. '
            f'Available: {available}'
        )
    return cat


def _resolve(skill: str, category: str, name: str) -> Path:
    cat = _category_dir(skill, category)
    if not name or any(c in name for c in ('..',)):
        raise ValueError(f'Invalid asset name: {name!r}')
    target = (cat / name).resolve()
    if not target.is_relative_to(cat):
        raise ValueError(f'Path traversal rejected: {name!r}')
    if not target.is_file():
        available = sorted(p.name for p in cat.rglob('*') if p.is_file())
        raise FileNotFoundError(
            f'Asset not found: {skill}/{category}/{name}. '
            f'Available: {available}'
        )
    return target


def _read_text(path: Path) -> str:
    if path.suffix.lower() not in TEXT_EXT:
        raise ValueError(f'Not a text asset: {path.name}')
    return path.read_text(encoding='utf-8')


def _load(skill: str, category: str, name: str) -> str:
    return _read_text(_resolve(skill, category, name))


def _extract_section(text: str, heading: str) -> str | None:
    pat = re.compile(rf'^(#{{1,6}})\s+{re.escape(heading)}\s*$', re.MULTILINE)
    m = pat.search(text)
    if not m:
        return None
    level = len(m.group(1))
    start = m.end()
    nxt = re.compile(rf'^#{{1,{level}}}\s+\S', re.MULTILINE).search(text, start)
    end = nxt.start() if nxt else len(text)
    return text[start:end].strip()


def register(mcp) -> None:

    @mcp.tool
    def list_skills() -> list[str]:
        """List all skills available under assets/."""
        return _available_skills()

    @mcp.tool
    def list_skill_categories(skill: str) -> list[str]:
        """List all categories within one skill (templates, references, ...).

        Raises ValueError with the list of available skills if `skill` is unknown.
        """
        base = _skill_dir(skill)
        return sorted(p.name for p in base.iterdir() if p.is_dir())

    @mcp.tool
    def list_assets(skill: str, category: str | None = None) -> list[dict]:
        """List assets within one skill; optionally filter by category.

        Raises ValueError with available names if `skill` or `category` is unknown.
        """
        cats = [category] if category else list_skill_categories(skill)
        base = _skill_dir(skill)
        out: list[dict] = []
        for cat in cats:
            cat_dir = _category_dir(skill, cat)
            for p in sorted(cat_dir.rglob('*')):
                if p.is_file() and p.suffix.lower() in TEXT_EXT:
                    out.append(
                        {
                            'category': cat,
                            'name': p.relative_to(cat_dir).as_posix(),
                        }
                    )
        return out

    @mcp.tool
    def get_asset(
        skill: str, category: str, name: str, section: str | None = None
    ) -> str:
        """Return raw content of an asset.

        section: return only the body under that markdown heading (token saver).
        Raises with the list of available assets if `name` is unknown.
        """
        text = _load(skill, category, name)
        if section:
            chunk = _extract_section(text, section)
            if chunk is None:
                raise ValueError(
                    f"Section '{section}' not found in {skill}/{category}/{name}"
                )
            return chunk
        return text

    @mcp.tool
    def render_asset(
        skill: str,
        category: str,
        name: str,
        variables: dict[str, str],
    ) -> str:
        """Fill an asset by replacing {{KEY}} placeholders.

        variables: e.g. {
            "НАЗВАНИЕ ЗАДАЧИ/ПРОЕКТА": "CRM sync",
            "ДАТА": "2026-10-14",
            "АВТОР": "Иван Петров",
        }.
        Unresolved placeholders remain as-is so the caller can spot gaps.
        """
        text = _load(skill, category, name)
        for key, value in variables.items():
            text = text.replace('{{' + key + '}}', str(value))
        return text

    @mcp.tool
    def unresolved_placeholders(text: str) -> list[str]:
        """Return {{...}} placeholders still present after rendering."""
        return sorted(set(re.findall(r'\{\{([^}]+)\}\}', text)))
