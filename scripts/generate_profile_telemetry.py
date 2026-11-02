#!/usr/bin/env python3
"""Generate the profile telemetry SVGs (activity + stack, light and dark).

Data comes from the public GitHub API for USER's repositories: commit
timestamps, languages and repo metadata. Writes:
  assets/profile-activity-light.svg / profile-activity-dark.svg
  assets/profile-stack-light.svg    / profile-stack-dark.svg
  assets/profile-telemetry.json

Uses GH_TOKEN or GITHUB_TOKEN from the environment when present (the
refresh workflow provides one); unauthenticated runs also work for
public data, just with lower rate limits.
"""
import json
import os
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

USER = "gour4v97"
FALLBACK_DESC = {
    "3d-cardiovascular-risk-explorer":
        "Educational ML app - coronary risk prediction, FastAPI + scikit-learn + SHAP, 3D heart",
    "glasstab":
        "Comet-style glassmorphism New Tab extension for Brave/Chrome - vanilla JS, Manifest V3",
}
ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

LANG_COLORS = {
    "Python": "#3776ab", "C#": "#178600", "HTML": "#e34c26",
    "CSS": "#563d7c", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "Dockerfile": "#384d54", "Makefile": "#427819", "Shell": "#89e051",
}
FALLBACK_COLORS = ["#0f766e", "#2563eb", "#d97706", "#dc2626", "#7c3aed", "#0891b2"]

THEMES = {
    "light": {"bg": "#ffffff", "border": "#e2e8f0", "text": "#0f172a",
              "muted": "#64748b", "track": "#eef2f7", "accent": "#0f766e",
              "accent2": "#2563eb", "grid": "#e2e8f0"},
    "dark": {"bg": "#0d1117", "border": "#30363d", "text": "#e6edf3",
             "muted": "#8b949e", "track": "#1c2430", "accent": "#2dd4bf",
             "accent2": "#60a5fa", "grid": "#21262d"},
}


def api(path):
    req = urllib.request.Request(f"https://api.github.com{path}")
    req.add_header("Accept", "application/vnd.github+json")
    req.add_header("User-Agent", "profile-telemetry")
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def collect():
    repos = [r for r in api(f"/users/{USER}/repos?per_page=100&sort=created")
             if not r["fork"] and r["name"] != USER]
    projects, all_dates, lang_bytes = [], [], Counter()
    for repo in repos:
        name = repo["name"]
        langs = api(f"/repos/{USER}/{name}/languages")
        for lang, size in langs.items():
            lang_bytes[lang] += size
        dates, page = [], 1
        while True:
            batch = api(f"/repos/{USER}/{name}/commits?per_page=100&page={page}")
            if not batch:
                break
            for commit in batch:
                stamp = commit["commit"]["author"]["date"]
                dates.append(datetime.fromisoformat(stamp.replace("Z", "+00:00")))
            if len(batch) < 100:
                break
            page += 1
        all_dates.extend(dates)
        projects.append({
            "name": name,
            "description": repo.get("description") or FALLBACK_DESC.get(name, ""),
            "language": repo.get("language") or "",
            "languages": langs,
            "commits": len(dates),
            "created": repo["created_at"][:10],
            "pushed": repo["pushed_at"][:10],
            "url": repo["html_url"],
        })
    projects.sort(key=lambda p: p["pushed"], reverse=True)
    return projects, sorted(all_dates), lang_bytes


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def style_block():
    return """<style>
@keyframes rise{from{transform:scaleY(0)}to{transform:scaleY(1)}}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes fade{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
.rise,.grow{transform-box:fill-box}
.rise{transform-origin:50% 100%;animation:rise .7s cubic-bezier(.2,.7,.2,1) both}
.grow{transform-origin:0 50%;animation:grow .9s cubic-bezier(.2,.7,.2,1) both}
.fade{animation:fade .6s ease-out both}
text{font-family:'Segoe UI',system-ui,-apple-system,Arial,sans-serif}
</style>"""


def stat_tile(x, theme, label, value, sub=""):
    sub_svg = (f'<text x="{x}" y="132" font-size="12" fill="{theme["muted"]}">{esc(sub)}</text>'
               if sub else "")
    return (f'<text x="{x}" y="86" font-size="12" fill="{theme["muted"]}">{esc(label.upper())}</text>'
            f'<text x="{x}" y="114" font-size="26" font-weight="700" fill="{theme["text"]}">{esc(value)}</text>'
            + sub_svg)


def activity_svg(theme_name, projects, dates, months):
    t = THEMES[theme_name]
    total = len(dates)
    active_days = len({d.date() for d in dates})
    latest = dates[-1].strftime("%d %b %Y") if dates else "—"
    max_count = max([c for _, c in months] + [1])
    bars = []
    chart_x, chart_y, chart_w, chart_h = 48, 182, 784, 138
    step = chart_w / len(months)
    for i, (label, count) in enumerate(months):
        h = max(3, chart_h * count / max_count) if count else 3
        x = chart_x + i * step + step * 0.22
        w = step * 0.56
        color = t["accent"] if count else t["track"]
        bars.append(
            f'<rect class="rise" style="animation-delay:{i * 40}ms" x="{x:.0f}" y="{chart_y + chart_h - h:.0f}" '
            f'width="{w:.0f}" height="{h:.0f}" rx="4" fill="{color}"/>'
            f'<text x="{x + w / 2:.0f}" y="{chart_y + chart_h - h - 8:.0f}" font-size="12" font-weight="600" '
            f'fill="{t["text"]}" text-anchor="middle">{count if count else ""}</text>'
            f'<text x="{x + w / 2:.0f}" y="{chart_y + chart_h + 22:.0f}" font-size="11" '
            f'fill="{t["muted"]}" text-anchor="middle">{label}</text>')
    weekday_counts = Counter(d.strftime("%a") for d in dates)
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    wmax = max([weekday_counts.get(d, 0) for d in days] + [1])
    wbars, wx = [], 48
    for i, day in enumerate(days):
        count = weekday_counts.get(day, 0)
        w = 90 * count / wmax if count else 0
        wbars.append(
            f'<text x="{wx}" y="{372 + i * 0}" font-size="0" fill="{t["muted"]}"></text>')
    # weekday shown as one compact row of labelled dots/bars at bottom
    cells = []
    cx = 48
    for i, day in enumerate(days):
        count = weekday_counts.get(day, 0)
        frac = count / wmax if wmax else 0
        r = 5 + 9 * frac
        cy = 428
        cells.append(
            f'<circle class="fade" style="animation-delay:{i * 60}ms" cx="{cx + 28}" cy="{cy}" r="{r:.0f}" '
            f'fill="{t["accent2"]}" opacity="{0.35 + 0.65 * frac:.2f}"/>'
            f'<text x="{cx + 28}" y="{cy + 34}" font-size="11" fill="{t["muted"]}" text-anchor="middle">{day}</text>'
            f'<text x="{cx + 28}" y="{cy - 22}" font-size="11" font-weight="600" fill="{t["text"]}" text-anchor="middle">{count if count else ""}</text>')
        cx += 112
    height = 492
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="880" height="{height}" viewBox="0 0 880 {height}" role="img" aria-labelledby="t d">
<title id="t">Gourav Manjhi — build activity</title>
<desc id="d">{total} commits across {len(projects)} public projects; monthly commits for the last 12 months and commits by weekday.</desc>
{style_block()}
<rect x="1" y="1" width="878" height="{height - 2}" rx="12" fill="{t['bg']}" stroke="{t['border']}"/>
<text x="48" y="34" font-size="19" font-weight="700" fill="{t['text']}">Build activity</text>
<text x="832" y="34" font-size="12" fill="{t['muted']}" text-anchor="end">last 12 months</text>
{stat_tile(48, t, "Commits", str(total), "all public projects")}
{stat_tile(268, t, "Active days", str(active_days))}
{stat_tile(488, t, "Public projects", str(len(projects)))}
{stat_tile(688, t, "Latest commit", latest)}
<line x1="48" y1="150" x2="832" y2="150" stroke="{t['grid']}"/>
{''.join(bars)}
<line x1="48" y1="366" x2="832" y2="366" stroke="{t['grid']}"/>
<text x="48" y="392" font-size="12" fill="{t['muted']}">COMMITS BY WEEKDAY</text>
{''.join(cells)}
</svg>
"""


def stack_svg(theme_name, projects, lang_bytes):
    t = THEMES[theme_name]
    total_bytes = sum(lang_bytes.values()) or 1
    langs = lang_bytes.most_common(6)
    segments, lx = [], 48
    bar_w = 784
    for i, (lang, size) in enumerate(langs):
        w = bar_w * size / total_bytes
        color = LANG_COLORS.get(lang, FALLBACK_COLORS[i % len(FALLBACK_COLORS)])
        segments.append(f'<rect class="grow" style="animation-delay:{i * 90}ms" x="{lx:.0f}" y="118" width="{max(w - 2, 2):.0f}" height="18" rx="4" fill="{color}"/>')
        lx += w
    legend, lx = [], 48
    for i, (lang, size) in enumerate(langs):
        color = LANG_COLORS.get(lang, FALLBACK_COLORS[i % len(FALLBACK_COLORS)])
        pct = 100 * size / total_bytes
        legend.append(
            f'<circle cx="{lx + 5}" cy="158" r="5" fill="{color}"/>'
            f'<text x="{lx + 16}" y="162" font-size="12" fill="{t["text"]}">{esc(lang)} {pct:.0f}%</text>')
        lx += 26 + 9.2 * len(f"{lang} {pct:.0f}%")
    rows = []
    y = 216
    for i, p in enumerate(projects):
        color = LANG_COLORS.get(p["language"], FALLBACK_COLORS[i % len(FALLBACK_COLORS)])
        desc = p["description"]
        if len(desc) > 108:
            desc = desc[:105] + "…"
        rows.append(
            f'<circle cx="56" cy="{y - 5}" r="5" fill="{color}"/>'
            f'<text x="72" y="{y}" font-size="15" font-weight="600" fill="{t["text"]}">{esc(p["name"])}</text>'
            f'<text x="832" y="{y}" font-size="12" fill="{t["muted"]}" text-anchor="end">{p["commits"]} commits · last pushed {p["pushed"]}</text>'
            f'<text x="72" y="{y + 20}" font-size="12" fill="{t["muted"]}">{esc(desc)}</text>')
        y += 52
    height = y + 12
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="880" height="{height}" viewBox="0 0 880 {height}" role="img" aria-labelledby="t d">
<title id="t">Projects and stack</title>
<desc id="d">Language mix by bytes across public projects, and each project with its commit count and last push date.</desc>
{style_block()}
<rect x="1" y="1" width="878" height="{height - 2}" rx="12" fill="{t['bg']}" stroke="{t['border']}"/>
<text x="48" y="34" font-size="19" font-weight="700" fill="{t['text']}">Projects and stack</text>
<text x="48" y="66" font-size="12" fill="{t['muted']}">LANGUAGE MIX (BY BYTES, ALL PUBLIC PROJECTS)</text>
{''.join(segments)}
{''.join(legend)}
<line x1="48" y1="188" x2="832" y2="188" stroke="{t['grid']}"/>
{''.join(rows)}
</svg>
"""


def main():
    projects, dates, lang_bytes = collect()
    now = datetime.now(timezone.utc)
    months, y, m = [], now.year, now.month
    for _ in range(12):
        months.append((y, m))
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    months.reverse()
    counts = Counter((d.year, d.month) for d in dates)
    month_pairs = [(datetime(y, m, 1).strftime("%b"), counts.get((y, m), 0)) for y, m in months]
    ASSETS.mkdir(exist_ok=True)
    for theme in ("light", "dark"):
        (ASSETS / f"profile-activity-{theme}.svg").write_text(
            activity_svg(theme, projects, dates, month_pairs), encoding="utf-8")
        (ASSETS / f"profile-stack-{theme}.svg").write_text(
            stack_svg(theme, projects, lang_bytes), encoding="utf-8")
    telemetry = {
        "user": USER,
        "generated_at": now.isoformat(),
        "total_commits": len(dates),
        "active_days": len({d.date().isoformat() for d in dates}),
        "months": [{"month": f"{y}-{m:02d}", "commits": c} for (y, m), (_, c) in zip(months, month_pairs)],
        "languages": dict(lang_bytes),
        "projects": projects,
    }
    (ASSETS / "profile-telemetry.json").write_text(
        json.dumps(telemetry, indent=2), encoding="utf-8")
    print(f"{len(dates)} commits, {len(projects)} projects, languages={dict(lang_bytes)}")


if __name__ == "__main__":
    main()
