#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iSyslab website builder
=======================

Reads the markdown files in ``content/`` and renders them into the marked
regions of the HTML templates at the repository root, then writes the finished
site into ``_site/``.

Only ``content/*.md`` is meant to be edited by hand. The HTML templates carry
regions delimited like this:

    <!-- BUILD:publications -->
      ... generated, do not edit by hand ...
    <!-- /BUILD:publications -->

Everything between the markers is regenerated on every build.

Usage
-----
    python tools/build.py                 # build into _site/
    python tools/build.py --out docs      # build into another folder

No third-party packages are required.
"""

import argparse
import html
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(ROOT, "content")

# ---------------------------------------------------------------- site config
GITHUB_ORG = "ISYSLAB-HUST"          # used in the repositories sub-heading
ASSET_DIRS = ["assets"]              # copied verbatim into the output
EXTRA_FILES = ["CNAME", "robots.txt", "favicon.ico", "logo-review.html"]

MONTHS_EN = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

PEOPLE_GROUPS = [
    ("faculty", "Faculty", "指导教师"),
    ("collaborators", "Collaborating Faculty", "合作指导教师"),
    ("staff", "Postdoc & Staff", "博士后与专职研究人员"),
    ("students", "Current Students", "在读学生"),
    ("alumni", "Colleagues & Alumni", "同事与校友"),
]

# Groups that are empty on purpose. They still render a "to be added" note so
# the page structure is visible from day one instead of silently vanishing.
EMPTY_GROUP_NOTES = {
    "students": ("To be added — current members of the group will be listed here.",
                 "待补充——在读学生名单将在此列出。"),
    "alumni": ("To be added — former members, colleagues and their next steps will be listed here.",
               "待补充——往届成员与共事过的同事将在这里列出。"),
    "collaborators": ("To be added — academic and industry collaborators will be listed here.",
                      "待补充——合作单位与研究伙伴将在此列出。"),
}

EMPTY_LIST_NOTES = {
    "patents": ("To be added — Chinese invention patents and utility models will be listed here.",
                "待补充——中国发明专利与实用新型将在此列出。"),
    "teaching": ("To be added — course listings will be announced here.",
                 "待补充——开课信息将在此列出。"),
    "books": ("To be added — textbooks and monographs will be listed here.",
              "待补充——教材与专著将在此列出。"),
}


# ============================================================ small helpers
def esc(text):
    """Escape for HTML text content."""
    return html.escape(str(text or ""), quote=False)


def attr(text):
    """Escape for an HTML attribute value."""
    return html.escape(str(text or ""), quote=True)


def bi(en, zh):
    """Render one string in both languages.

    ``<html data-lang>`` decides which half is painted (see styles.css).
    When there is no translation the plain English string is emitted, so the
    markup stays clean and nothing ever disappears.
    """
    en = (en or "").strip()
    zh = (zh or "").strip()
    if not zh or zh == en:
        return esc(en)
    return ('<span class="bi">'
            '<span lang="en">%s</span>'
            '<span lang="zh">%s</span>'
            '</span>') % (esc(en), esc(zh))


def _ymd(value):
    m = re.match(r"^(\d{4})(?:-(\d{1,2}))?(?:-(\d{1,2}))?$", (value or "").strip())
    if not m:
        return None, None, None
    return (int(m.group(1)),
            int(m.group(2)) if m.group(2) else None,
            int(m.group(3)) if m.group(3) else None)


def date_en(value):
    y, mo, _ = _ymd(value)
    if not y:
        return value
    return "%s %d" % (MONTHS_EN[mo - 1], y) if mo else str(y)


def date_zh(value):
    y, mo, _ = _ymd(value)
    if not y:
        return value
    return "%d年%d月" % (y, mo) if mo else "%d年" % y


def num_of(record, index, key="no"):
    raw = str(record.get(key, "")).strip()
    if raw:
        return raw
    return "%02d" % (index + 1)


def truthy(value):
    return str(value or "").strip().lower() in ("true", "yes", "1", "on")


# ============================================================ markdown reader
_COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
_FIELD_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.*)$")


def _next_is_field(lines, start):
    """True when the next non-blank line still looks like a ``key: value``."""
    for line in lines[start:]:
        if line.strip() == "":
            continue
        return bool(_FIELD_RE.match(line))
    return False


def _parse_block(chunk):
    lines = chunk.split("\n")
    fields, body, in_body = {}, [], False
    for index, line in enumerate(lines):
        if in_body:
            body.append(line)
            continue
        if line.strip() == "":
            # A blank line only ends the field list once fields have started,
            # and only when what follows is free prose rather than another
            # `key: value` line. That keeps a blank-separated, easy-to-read
            # field block intact while prose still starts after the fields.
            if fields and not _next_is_field(lines, index + 1):
                in_body = True
            continue
        m = _FIELD_RE.match(line)
        if m:
            fields[m.group(1).lower()] = m.group(2).strip()
        else:
            in_body = True
            body.append(line)
    text = "\n".join(body).strip()
    if text:
        fields["body"] = text
    return fields


def read(name):
    """Parse ``content/<name>`` into a list of field dictionaries."""
    path = os.path.join(CONTENT_DIR, name)
    if not os.path.isfile(path):
        raise SystemExit("content file not found: %s" % path)
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    raw = _COMMENT_RE.sub("", raw)
    records = []
    for chunk in re.split(r"(?m)^[ \t]*---[ \t]*$", raw):
        if not chunk.strip():
            continue
        record = _parse_block(chunk)
        if any(str(v).strip() for v in record.values()):
            records.append(record)
    return records


def sort_by_date_desc(records):
    def key(rec):
        y, mo, d = _ymd(rec.get("date", ""))
        return (y or 0, mo or 0, d or 0)
    return sorted(records, key=key, reverse=True)


# ============================================================ marker injection
def inject(page_html, name, lines, problems):
    pattern = re.compile(
        r"([ \t]*)<!--\s*BUILD:" + re.escape(name) +
        r"\s*-->.*?<!--\s*/BUILD:" + re.escape(name) + r"\s*-->", re.S)

    def repl(match):
        indent = match.group(1)
        inner = "\n".join(
            (indent + "  " + ln) if ln.strip() else ""
            for ln in lines)
        return "%s<!-- BUILD:%s -->\n%s\n%s<!-- /BUILD:%s -->" % (
            indent, name, inner, indent, name)

    if not pattern.search(page_html):
        problems.append("marker BUILD:%s not found" % name)
        return page_html
    return pattern.sub(repl, page_html)


# ============================================================ renderers
def render_pub_links(item):
    """The DOI, as a real link, plus any extra link words on the record.

    A DOI is the one identifier every record already carries, so it is worth
    making clickable rather than printing the word "DOI" next to nothing.
    """
    parts = []
    doi = (item.get("doi") or "").strip()
    if doi:
        url = doi if doi.startswith("http") else "https://doi.org/" + doi
        parts.append('<a href="%s" target="_blank" rel="noopener">DOI</a>' % attr(url))
    extra = (item.get("links") or "").strip()
    if extra:
        parts.append(esc(extra))
    return ' · '.join(parts)


def render_pub_venue(item, year):
    """`journal · year`, flagged when the article itself is written in Chinese."""
    text = bi(item.get("venue"), item.get("venue_zh"))
    if (item.get("lang") or "").strip().lower() in ("zh", "cn", "chinese"):
        text += ' ' + bi("(in Chinese)", "（中文）")
    return '%s · %s' % (text, year)


def render_publications(items):
    out = []
    years = sorted({i.get("year", "") for i in items if i.get("year")},
                   key=lambda y: -int(y))

    out.append('<div class="year-filter">')
    out.append('  <button class="chip active" data-year="all" '
               'data-i18n="pub.filter.all">All</button>')
    for year in years:
        out.append('  <button class="chip" data-year="%s">%s</button>' % (year, year))
    out.append('</div>')

    for year in years:
        out.append("")
        out.append('<section class="pub-group" data-year="%s">' % year)
        out.append('  <div class="pub-year">%s</div>' % year)
        for item in [i for i in items if i.get("year") == year]:
            out.append('  <div class="pub-item bordered">')
            out.append('    <div class="pub-main">')
            out.append('      <p class="pub-title">%s</p>'
                       % bi(item.get("title"), item.get("title_zh")))
            out.append('      <p class="pub-authors">%s</p>'
                       % bi(item.get("authors"), item.get("authors_zh")))
            if item.get("ref"):
                out.append('      <p class="pub-ref">%s</p>' % esc(item["ref"]))
            links = render_pub_links(item)
            if links:
                out.append('      <p class="paper-links">%s</p>' % links)
            out.append('    </div>')
            out.append('    <p class="pub-venue">%s</p>' % render_pub_venue(item, year))
            out.append('  </div>')
        out.append('</section>')
    return out


def _pub_span(items):
    """Shared count + year span, so the subtitle and the meta tag never disagree."""
    years = sorted(int(i["year"]) for i in items if str(i.get("year", "")).isdigit())
    lo, hi = (years[0], years[-1]) if years else ("", "")
    return lo, hi, len(items)


def render_pub_sub(items):
    """The subtitle under the page title — counts are read off the data."""
    lo, hi, n = _pub_span(items)
    span = "%d–%d" % (lo, hi) if lo != "" else ""
    en = "%d publications, %s.  # co-first authors · * co-corresponding authors." % (n, span)
    zh = "%s 年共 %d 篇论文。 # 共同第一作者 · * 共同通讯作者。" % (span, n)
    return ['<p class="page-sub">%s</p>' % bi(en, zh)]


def render_pub_meta(items):
    """The <head> description, driven by the same count as the page subtitle."""
    lo, hi, n = _pub_span(items)
    desc = "%d publications, %d–%d — iSyslab, Intelligent Systems Lab, Huazhong University of Science and Technology." % (n, lo, hi)
    return ['<meta name="description" content="%s">' % attr(desc)]


def render_home_publications(items, limit=3):
    featured = [i for i in items if truthy(i.get("featured"))]
    for item in items:
        if len(featured) >= limit:
            break
        if item not in featured:
            featured.append(item)
    out = []
    for item in featured[:limit]:
        out.append('<div class="paper-card">')
        out.append('  <p class="paper-title">%s</p>'
                   % bi(item.get("title"), item.get("title_zh")))
        out.append('  <p class="paper-authors">%s · %s, %s</p>' % (
            bi(item.get("authors"), item.get("authors_zh")),
            bi(item.get("venue"), item.get("venue_zh")), esc(item.get("year"))))
        links = render_pub_links(item)
        if links:
            out.append('  <p class="paper-links">%s</p>' % links)
        out.append('</div>')
    return out


def _empty_list(name):
    """A friendly placeholder for a list whose markdown file is still empty."""
    en, zh = EMPTY_LIST_NOTES[name]
    return ['<section class="pub-group first">',
            '  <p class="alumni-note">%s</p>' % bi(en, zh),
            '</section>']


def render_patents(items):
    """Patent / software-copyright list grouped by year.

    Reuses the publications markup (.year-filter / .pub-group / .pub-item) so
    the year chips and the click-to-filter behaviour come along for free.
    """
    years = sorted({i.get("year", "") for i in items if i.get("year")},
                   key=lambda y: -int(y))
    if not years:
        return _empty_list("patents")

    out = ['<div class="year-filter">']
    out.append('  <button class="chip active" data-year="all" '
               'data-i18n="pat.filter.all">All</button>')
    for year in years:
        out.append('  <button class="chip" data-year="%s">%s</button>' % (year, year))
    out.append('</div>')

    for year in years:
        out.append("")
        out.append('<section class="pub-group" data-year="%s">' % year)
        out.append('  <div class="pub-year">%s</div>' % year)
        for item in [i for i in items if i.get("year") == year]:
            out.append('  <div class="pub-item bordered">')
            out.append('    <div class="pub-main">')
            out.append('      <p class="pub-title">%s</p>'
                       % bi(item.get("title") or item.get("title_zh"),
                            item.get("title_zh") or item.get("title")))
            out.append('      <p class="pub-authors">%s</p>'
                       % bi(item.get("inventors") or item.get("inventors_zh"),
                            item.get("inventors_zh") or item.get("inventors")))
            details = []
            if item.get("number"):
                details.append(esc(item["number"]))
            if item.get("status") or item.get("status_zh"):
                details.append(bi(item.get("status"), item.get("status_zh")))
            if item.get("note") or item.get("note_zh"):
                details.append(bi(item.get("note"), item.get("note_zh")))
            if details:
                out.append('      <p class="pub-ref">%s</p>' % " · ".join(details))
            out.append('    </div>')
            kind = bi(item.get("kind") or item.get("kind_zh"),
                      item.get("kind_zh") or item.get("kind"))
            out.append('    <p class="pub-venue">%s</p>' % " · ".join(
                p for p in (kind, year) if p.strip()))
            out.append('  </div>')
        out.append('</section>')
    return out


def render_teaching(items):
    """Course list — grouped by instructor, courses flowing left to right.

    The instructor name gets a line of its own and that instructor's courses
    sit under it as compact pills that wrap left to right, so the page reads
    as "who teaches what" instead of six full-width cards stacked up. Group
    order (and course order inside a group) follows the markdown file, so
    regrouping or reordering is a content edit, not a code change.
    """
    if not items:
        return _empty_list("teaching")

    groups = []          # [{"en": .., "zh": .., "items": [..]}]
    index = {}           # lecturer key -> position in `groups`
    for item in items:
        en = (item.get("lecturer") or "").strip()
        zh = (item.get("lecturer_zh") or "").strip()
        key = en or zh
        if key not in index:
            index[key] = len(groups)
            groups.append({"en": en or zh, "zh": zh or en, "items": []})
        groups[index[key]]["items"].append(item)

    out = ['<div class="course-groups">']
    for group in groups:
        out.append('  <div class="course-group">')
        out.append('    <div class="course-lecturer">%s</div>'
                   % bi(group["en"], group["zh"]))
        out.append('    <div class="course-grid">')
        for item in group["items"]:
            # Course codes are deliberately not shown on the page, so `code`
            # is never part of the pill even if a content file carries it.
            level = item.get("level") or item.get("level_zh")
            level_zh = item.get("level_zh") or item.get("level")
            meta_en = [p for p in (level, ) if p]
            meta_zh = [p for p in (level_zh, ) if p]
            if item.get("credits"):
                meta_en.append("%s credits" % item["credits"])
                meta_zh.append("%s 学分" % item["credits"])
            if item.get("hours"):
                meta_en.append("%s hours" % item["hours"])
                meta_zh.append("%s 学时" % item["hours"])
            tag = ('<span class="course-level">%s</span>'
                   % bi(" · ".join(meta_en), " · ".join(meta_zh))
                   ) if meta_en else ""
            title = bi(item.get("title") or item.get("title_zh"),
                       item.get("title_zh") or item.get("title"))
            if item.get("url"):
                out.append('      <a class="course-chip" href="%s" title="%s">'
                           '<span class="course-name">%s</span>%s</a>'
                           % (attr(item["url"]), attr(item["url"]), title, tag))
            else:
                out.append('      <span class="course-chip">'
                           '<span class="course-name">%s</span>%s</span>'
                           % (title, tag))
        out.append('    </div>')
        # A blurb cannot live inside a pill without breaking the rhythm, so
        # whenever one is present it drops to its own muted line under the
        # grid. No course carries a desc today; this keeps the field honoured
        # the day one does.
        notes = [i for i in group["items"] if i.get("desc") or i.get("desc_zh")]
        for item in notes:
            out.append('    <p class="course-note">%s%s</p>'
                       % (bi(item.get("title") or item.get("title_zh"),
                             item.get("title_zh") or item.get("title")) + " — ",
                          bi(item.get("desc"), item.get("desc_zh"))))
        out.append('  </div>')
    out.append('</div>')
    return out


def render_books(items):
    """Textbook list — one card per book, newest first.

    Same card markup as the teaching page, so it inherits the existing look.
    The imprint line (publisher · date · ISBN) is what a reader actually needs
    to cite or order the book, so it gets its own line rather than being
    buried inside the blurb.
    """
    if not items:
        return _empty_list("books")

    out = ['<div class="paper-list">']
    for item in sort_by_date_desc(items):
        title = item.get("title") or item.get("title_zh")
        title_zh = item.get("title_zh") or item.get("title")
        authors = item.get("authors") or item.get("authors_zh")
        authors_zh = item.get("authors_zh") or item.get("authors")
        role = item.get("role", "")
        role_zh = item.get("role_zh", "")
        # Some books spell the role out inside `authors` (e.g. a title shared
        # between an editor-in-chief and associate editors). Only append it
        # when it is not already there, so the card never says it twice.
        if role and role.lower() not in (authors or "").lower():
            authors = "%s — %s" % (authors, role)
        if role_zh and role_zh not in (authors_zh or ""):
            authors_zh = "%s——%s" % (authors_zh, role_zh)

        imprint = " · ".join(p for p in (
            item.get("publisher"),
            date_en(item.get("date", "")),
            ("ISBN " + item["isbn"]) if item.get("isbn") else "") if p)
        imprint_zh = " · ".join(p for p in (
            item.get("publisher_zh") or item.get("publisher"),
            date_zh(item.get("date", "")),
            ("ISBN " + item["isbn"]) if item.get("isbn") else "") if p)

        out.append('  <div class="paper-card">')
        out.append('    <p class="paper-title">%s</p>' % bi(title, title_zh))
        if authors:
            out.append('    <p class="paper-authors">%s</p>' % bi(authors, authors_zh))
        out.append('    <p class="paper-authors">%s</p>' % bi(imprint, imprint_zh))
        if item.get("series") or item.get("series_zh"):
            out.append('    <p class="paper-note">%s</p>'
                       % bi(item.get("series"), item.get("series_zh")))
        if item.get("note") or item.get("note_zh"):
            out.append('    <p class="paper-note">%s</p>'
                       % bi(item.get("note"), item.get("note_zh")))
        out.append('  </div>')
    out.append('</div>')
    return out


def render_news(items, limit=None, long_text=False):
    key = "text_long" if long_text else "text"
    key_zh = "text_long_zh" if long_text else "text_zh"
    rows = sort_by_date_desc(items)
    if limit:
        rows = rows[:limit]

    out = []
    for item in rows:
        text = item.get(key) or item.get("text", "")
        text_zh = item.get(key_zh) or item.get("text_zh", "")
        body = bi(text, text_zh)
        if item.get("link"):
            body = '<a href="%s" target="_blank" rel="noopener">%s</a>' % (
                attr(item["link"]), body)
        out.append('<div class="news-row">')
        out.append('  <span class="news-date">%s</span>'
                   % bi(date_en(item.get("date", "")), date_zh(item.get("date", ""))))
        out.append('  <span class="news-text">%s</span>' % body)
        out.append('  <span class="news-tag">%s</span>'
                   % bi(item.get("tag", "Paper"), item.get("tag_zh", "")))
        out.append('</div>')
    return out


def render_tools(items):
    count = len(items)
    out = []
    out.append('<div class="section-head-left">')
    out.append('  <div class="head-left-title" data-i18n="sw.sec1" data-i18n-html>'
               'Online Servers &amp; Databases</div>')
    out.append('  <div class="head-left-sub">%s</div>'
               % bi("%d tool%s" % (count, "" if count == 1 else "s"),
                    "%d 个在线工具" % count))
    out.append('</div>')
    out.append('<div class="tool-grid">')
    for item in items:
        label = item.get("label") or re.sub(r"^https?://", "", item.get("url", ""))
        out.append('  <div class="tool-card">')
        out.append('    <div class="tool-name">%s</div>' % esc(item.get("name")))
        out.append('    <p class="tool-desc">%s</p>'
                   % bi(item.get("desc"), item.get("desc_zh")))
        out.append('    <a class="tool-link" href="%s" target="_blank" rel="noopener">%s</a>'
                   % (attr(item.get("url")), esc(label)))
        out.append('  </div>')
    out.append('</div>')
    return out


def render_repos(items):
    count = len(items)
    out = []
    out.append('<div class="section-head-left">')
    out.append('  <div class="head-left-title" data-i18n="sw.sec2">Open-source Repositories</div>')
    out.append('  <div class="head-left-sub">%s</div>'
               % bi("%d repositor%s · github.com/%s"
                    % (count, "y" if count == 1 else "ies", GITHUB_ORG),
                    "%d 个代码仓库 · github.com/%s" % (count, GITHUB_ORG)))
    out.append('</div>')
    out.append('<div class="repo-list">')
    out.append("")
    for item in items:
        meta = []
        if item.get("lang"):
            meta.append('<span class="m">%s</span>' % esc(item["lang"]))
        if item.get("license"):
            meta.append('<span class="m">%s</span>' % esc(item["license"]))
        if item.get("updated"):
            meta.append('<span class="m dim">%s</span>'
                        % bi("Updated " + date_en(item["updated"]),
                             "更新于 " + date_zh(item["updated"])))
        out.append('  <div class="repo-card">')
        out.append('    <div class="repo-main">')
        out.append('      <div class="repo-name">%s</div>' % esc(item.get("name")))
        out.append('      <p class="repo-desc">%s</p>'
                   % bi(item.get("desc"), item.get("desc_zh")))
        if meta:
            out.append('      <div class="repo-meta">%s</div>' % "".join(meta))
        out.append('    </div>')
        out.append('    <a class="repo-link" href="%s" target="_blank" rel="noopener" '
                   'data-i18n="sw.view">View on GitHub</a>' % attr(item.get("url")))
        out.append('  </div>')
        out.append("")
    out.append('</div>')
    return out


def render_people(items):
    known = {key for key, _, _ in PEOPLE_GROUPS}
    labels = {key: (en, zh) for key, en, zh in PEOPLE_GROUPS}
    order = [key for key, _, _ in PEOPLE_GROUPS]
    for item in items:
        group = (item.get("group") or "staff").strip()
        if group not in order:
            order.append(group)
            labels.setdefault(group, (group, group))

    groups = [(g, [i for i in items if (i.get("group") or "staff").strip() == g])
              for g in order]
    groups = [g for g in groups if g[1] or g[0] in EMPTY_GROUP_NOTES]
    if not groups:
        return []

    out = []
    for index, (group, members) in enumerate(groups):
        is_first = index == 0
        is_last = index == len(groups) - 1
        cls = "people-section"
        if is_last and not is_first:
            cls += " last"
        elif not is_first:
            cls += " follow"
        en_label, zh_label = labels[group]

        out.append('<section class="%s">' % cls)
        out.append('  <h2 class="people-h2">%s</h2>' % bi(en_label, zh_label))

        if not members:
            note = EMPTY_GROUP_NOTES.get(group)
            if note:
                out.append('  <p class="alumni-note">%s</p>' % bi(note[0], note[1]))
            out.append('</section>')
            continue

        # Collaborators use the same rich card as faculty — they carry a photo
        # and a bio, and a bare initial-circle card would under-sell them.
        if group in ("faculty", "collaborators"):
            for member in members:
                out.extend(_faculty_card(member))
        elif group == "students":
            out.extend(_roster_grid(members))
        else:
            out.append('  <div class="member-row">')
            for member in members:
                out.extend(_member_card(member))
            out.append('  </div>')
        out.append('</section>')
    return out


def _roster_grid(members):
    """Students render as a dense roster — name, cohort, email in three
    columns, no avatars. Twenty-plus cards would push the page far down for
    information that is really just a list."""
    out = ['  <div class="roster-grid">']
    for member in members:
        out.append('    <div class="roster-item">')
        out.append('      <div class="roster-name">%s</div>'
                   % bi(member.get("name"), member.get("name_zh")))
        meta = bi(member.get("role"), member.get("role_zh") or member.get("role"))
        email = member.get("email", "")
        if email:
            meta += ('<span class="roster-sep"> · </span>'
                     '<a class="roster-mail" href="mailto:%s">%s</a>'
                     % (attr(email), esc(email)))
        out.append('      <div class="roster-meta">%s</div>' % meta)
        out.append('    </div>')
    out.append('  </div>')
    return out


def _person_name(member):
    name = member.get("name", "")
    name_zh = member.get("name_zh", "")
    role = member.get("role", "")
    role_zh = member.get("role_zh", "")
    joined = " · ".join(p for p in (name, role) if p)
    joined_zh = " · ".join(p for p in (name_zh or name, role_zh or role) if p)
    return bi(joined, joined_zh)


def _avatar(member, cls):
    if member.get("photo"):
        return '    <img class="%s" src="%s" alt="%s">' % (
            cls, attr(member["photo"]), attr(member.get("name")))
    return '    <div class="%s"></div>' % cls


def _faculty_card(member):
    lead = truthy(member.get("lead"))
    root = "lead" if lead else "faculty"
    out = []
    out.append('  <div class="%s-card">' % root)
    out.append(_avatar(member, "%s-avatar" % root))
    out.append('    <div class="%s-info">' % root)
    out.append('      <div class="%s-name">%s</div>' % (root, _person_name(member)))
    if member.get("affiliation"):
        out.append('      <p class="faculty-affil">%s</p>'
                   % bi(member.get("affiliation"), member.get("affiliation_zh")))
    if member.get("bio"):
        out.append('      <p class="%s-bio">%s</p>'
                   % (root, bi(member.get("bio"), member.get("bio_zh"))))
    if member.get("email"):
        out.append('      <a class="%s-email" href="mailto:%s">%s</a>'
                   % (root, attr(member["email"]), esc(member["email"])))
    out.append('    </div>')
    out.append('  </div>')
    return out


def _member_card(member):
    initial = (member.get("initial")
               or (member.get("name") or "?").strip()[:1].upper())
    has_bio = bool(member.get("bio") or member.get("bio_zh"))
    out = []
    out.append('    <div class="member-card%s">' % (" has-bio" if has_bio else ""))
    if member.get("photo"):
        out.append('      <img class="avatar-photo" src="%s" alt="%s">'
                   % (attr(member["photo"]), attr(member.get("name"))))
    else:
        out.append('      <div class="avatar-circle">%s</div>' % esc(initial))
    out.append('      <div class="member-name">%s</div>'
               % bi(member.get("name"), member.get("name_zh")))
    role = member.get("role", "")
    role_zh = member.get("role_zh", "")
    # Collaborators usually need their home institution on the card.
    affil = member.get("affiliation", "")
    affil_zh = member.get("affiliation_zh") or affil
    email = member.get("email", "")
    line_en = " · ".join(p for p in (role, affil, email) if p)
    line_zh = " · ".join(p for p in (role_zh or role, affil_zh, email) if p)
    out.append('      <div class="member-role">%s</div>' % bi(line_en, line_zh))
    # Staff and students often carry a one-line research focus instead of a
    # full bio — show it under the role when present.
    if member.get("bio") or member.get("bio_zh"):
        out.append('      <div class="member-bio">%s</div>'
                   % bi(member.get("bio"), member.get("bio_zh")))
    out.append('    </div>')
    return out


def render_research_rows(items):
    out = []
    for index, item in enumerate(items):
        title = item.get("title", "")
        title_zh = item.get("title_zh", "")
        no = num_of(item, index)
        eyebrow = item.get("eyebrow", "")
        out.append('<section class="dir-row%s">' % (" alt" if index % 2 else ""))
        out.append('  <div class="dir-copy">')
        out.append('    <div class="dir-eyebrow">%s</div>'
                   % bi("%s / %s" % (no, eyebrow), "%s / %s" % (no, title_zh)))
        out.append('    <h2 class="dir-title">%s</h2>' % bi(title, title_zh))
        out.append('    <div class="dir-cn">%s</div>' % bi(title_zh, title))
        out.append('    <p class="dir-desc">%s</p>'
                   % bi(item.get("desc"), item.get("desc_zh")))
        if item.get("tags"):
            out.append('    <p class="dir-tags">%s</p>'
                       % bi(item.get("tags"), item.get("tags_zh")))
        out.append('  </div>')
        if item.get("image"):
            out.append('  <img class="dir-img" src="%s" alt="%s">'
                       % (attr(item["image"]), attr(title)))
        out.append('</section>')
    return out


def render_research_cards(items, href="research.html"):
    out = []
    for index, item in enumerate(items):
        title = item.get("title", "")
        title_zh = item.get("title_zh", "")
        out.append('<a class="card" href="%s">' % href)
        out.append('  <span class="card-num">%s</span>' % num_of(item, index))
        out.append('  <span class="card-title-en">%s</span>' % bi(title, title_zh))
        out.append('  <span class="card-title-cn">%s</span>' % bi(title_zh, title))
        desc = item.get("short") or item.get("desc", "")
        desc_zh = item.get("short_zh") or item.get("desc_zh", "")
        out.append('  <p class="card-desc">%s</p>' % bi(desc, desc_zh))
        out.append('</a>')
    return out


# ============================================================ join
def _join_records(kind):
    return [r for r in JOIN if (r.get("kind") or "").strip() == kind]


def _join_header():
    return next(iter(_join_records("header")), {})


def render_join_header():
    rec = _join_header()
    out = []
    if rec.get("eyebrow"):
        out.append('<div class="eyebrow-text">%s</div>'
                   % bi(rec["eyebrow"], rec.get("eyebrow_zh")))
    if rec.get("title"):
        out.append('<h1 class="page-title">%s</h1>'
                   % bi(rec["title"], rec.get("title_zh")))
    if rec.get("sub"):
        out.append('<p class="page-sub">%s</p>'
                   % bi(rec["sub"], rec.get("sub_zh")))
    return out


def render_join_positions():
    rec = _join_header()
    out = []
    if rec.get("pos_h2"):
        out.append('<h2 class="pos-h2">%s</h2>'
                   % bi(rec["pos_h2"], rec.get("pos_h2_zh")))
    out.append('<div class="pos-cards">')
    for item in _join_records("position"):
        out.append('  <div class="pos-card">')
        out.append('    <div class="pos-role">%s</div>'
                   % bi(item.get("role"), item.get("role_zh")))
        out.append('    <p class="pos-req">%s</p>'
                   % bi(item.get("req"), item.get("req_zh")))
        out.append('    <p class="pos-note">%s</p>'
                   % bi(item.get("note"), item.get("note_zh")))
        out.append('  </div>')
    out.append('</div>')
    return out


def render_join_contact():
    rec = _join_header()
    out = []
    if rec.get("contact_h2"):
        out.append('<h2 class="contact-h2">%s</h2>'
                   % bi(rec["contact_h2"], rec.get("contact_h2_zh")))
    out.append('<div class="contact-cards">')
    for item in _join_records("contact"):
        out.append('  <div class="contact-card">')
        out.append('    <div class="contact-label">%s</div>'
                   % bi(item.get("label"), item.get("label_zh")))
        value = bi(item.get("value"), item.get("value_zh"))
        link = (item.get("link") or "").strip()
        if link:
            out.append('    <a class="contact-value" href="%s">%s</a>'
                       % (attr(link), value))
        else:
            out.append('    <div class="contact-value plain">%s</div>' % value)
        out.append('  </div>')
    out.append('</div>')
    maps = _join_records("map")
    if maps:
        m = maps[0]
        out.append('<figure class="map-figure">')
        out.append('  <img class="map-img" src="%s" alt="%s">'
                   % (attr(m.get("image") or "assets/img/map.png"),
                      attr(m.get("alt") or m.get("alt_zh") or "")))
        link = (m.get("link") or "").strip()
        if link:
            out.append('  <a class="map-link" href="%s" target="_blank" '
                       'rel="noopener">%s ↗</a>'
                       % (attr(link), bi(m.get("link_text"), m.get("link_text_zh"))))
        out.append('</figure>')
    return out


def render_stats(pubs, tools, repos, areas):
    rows = [
        (str(len(pubs)), "home.stat.pubs", "Publications"),
        (str(len(tools) + len(repos)), "home.stat.tools", "Software Tools"),
        (str(len(areas)), "home.stat.areas", "Research Areas"),
    ]
    out = []
    for value, key, label in rows:
        out.append('<div class="stat">')
        out.append('  <div class="stat-num">%s</div>' % esc(value))
        out.append('  <div class="stat-label" data-i18n="%s">%s</div>' % (key, esc(label)))
        out.append('</div>')
    return out


# ============================================================ about
def render_about_intro():
    """The one-line lab introduction shown in the home page hero.

    Rendered as an inline bilingual span (`bi`), so <html data-lang> paints
    the right half without a round-trip through the JS string table.
    """
    intro = ABOUT.get("intro", "")
    intro_zh = ABOUT.get("intro_zh", "")
    if not intro and not intro_zh:
        return []
    return ['<span class="bi">'
            '<span lang="en">%s</span>'
            '<span lang="zh">%s</span>'
            '</span>' % (esc(intro or intro_zh), esc(intro_zh or intro))]


def render_build_strings():
    """Emit the handful of strings that still need runtime switching.

    Visible copy is rendered server-side by `bi()`, but <title> / <meta> are
    attributes and cannot hold bilingual spans — those two keys are handed to
    i18n.js instead, which merges them over its own table at boot.
    """
    en, zh = {}, {}
    if ABOUT.get("meta"):
        en["page.home.desc"] = ABOUT["meta"]
    if ABOUT.get("meta_zh"):
        zh["page.home.desc"] = ABOUT["meta_zh"]
    if not en and not zh:
        return []
    payload = json.dumps({"en": en, "zh": zh}, ensure_ascii=False)
    return ['<script>window.BUILD_STRINGS = %s;</script>'
            '<!-- generated from content/about.md -->' % payload]


# ============================================================ build
PAGE_MARKERS = {
    "index.html": [
        ("home.strings", lambda: render_build_strings()),
        ("home.intro", lambda: render_about_intro()),
        ("home.stats", lambda: render_stats(PUBS, TOOLS, REPOS, RESEARCH)),
        ("home.cards", lambda: render_research_cards(RESEARCH)),
        ("home.news", lambda: render_news(NEWS, limit=4)),
        ("home.pubs", lambda: render_home_publications(PUBS)),
    ],
    "publications.html": [
        ("pub.meta", lambda: render_pub_meta(PUBS)),
        ("pub.sub", lambda: render_pub_sub(PUBS)),
        ("publications", lambda: render_publications(PUBS)),
    ],
    "patents.html": [
        ("patents", lambda: render_patents(PATENTS)),
    ],
    "teaching.html": [
        ("teaching", lambda: render_teaching(TEACHING)),
        ("books", lambda: render_books(BOOKS)),
    ],
    "software.html": [
        ("software.tools", lambda: render_tools(TOOLS)),
        ("software.repos", lambda: render_repos(REPOS)),
    ],
    "people.html": [
        ("people", lambda: render_people(PEOPLE)),
    ],
    "news.html": [
        ("news", lambda: render_news(NEWS, long_text=True)),
    ],
    "research.html": [
        ("research", lambda: render_research_rows(RESEARCH)),
    ],
    "join.html": [
        ("join.header", lambda: render_join_header()),
        ("join.positions", lambda: render_join_positions()),
        ("join.contact", lambda: render_join_contact()),
    ],
}

PUBS = TOOLS = REPOS = PEOPLE = NEWS = RESEARCH = PATENTS = TEACHING = BOOKS = []
JOIN = []
ABOUT = {}


def load_content():
    global PUBS, TOOLS, REPOS, PEOPLE, NEWS, RESEARCH, PATENTS, TEACHING, BOOKS, JOIN, ABOUT
    PUBS = read("publications.md")
    TOOLS = read("software.md")
    REPOS = read("projects.md")
    PEOPLE = read("people.md")
    NEWS = read("news.md")
    RESEARCH = read("research.md")
    PATENTS = read("patents.md")
    TEACHING = read("teaching.md")
    BOOKS = read("books.md")
    JOIN = read("join.md")
    about = read("about.md")
    ABOUT = about[0] if about else {}


def build(out_dir, verbose=True):
    load_content()
    problems = []

    # NOTE: the output directory is updated in place rather than wiped.
    # Rebuilding is a routine operation (the preview server does it on every
    # file change), so it must never depend on a bulk-delete being allowed.
    os.makedirs(out_dir, exist_ok=True)
    written = set()

    templates = sorted(f for f in os.listdir(ROOT)
                       if f.endswith(".html") and os.path.isfile(os.path.join(ROOT, f)))
    built = []
    for name in templates:
        with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
            page = fh.read()
        for marker, producer in PAGE_MARKERS.get(name, []):
            page = inject(page, marker, producer(), problems)
        target = os.path.join(out_dir, name)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(page)
        written.add(os.path.normcase(os.path.abspath(target)))
        built.append(name)

    for folder in ASSET_DIRS:
        src = os.path.join(ROOT, folder)
        if os.path.isdir(src):
            dst = os.path.join(out_dir, folder)
            shutil.copytree(src, dst, dirs_exist_ok=True)
            for dirpath, _dirnames, filenames in os.walk(dst):
                for filename in filenames:
                    written.add(os.path.normcase(os.path.join(dirpath, filename)))
    for name in EXTRA_FILES:
        src = os.path.join(ROOT, name)
        if os.path.isfile(src):
            dst = os.path.join(out_dir, name)
            shutil.copy2(src, dst)
            written.add(os.path.normcase(os.path.abspath(dst)))

    # Keep links to the previous site's extensionless URLs working.
    for old, new in {"people": "people.html", "publications": "publications.html",
                     "software": "software.html", "join-us": "join.html",
                     "news": "news.html", "projects": "projects.html",
                     "gallery": "gallery.html"}.items():
        directory = os.path.join(out_dir, old)
        os.makedirs(directory, exist_ok=True)
        target = os.path.join(directory, "index.html")
        with open(target, "w", encoding="utf-8") as fh:
            fh.write('<!doctype html><html lang="en"><meta charset="utf-8">'
                     '<meta http-equiv="refresh" content="0;url=/%s">'
                     '<title>Page moved</title><a href="/%s">Continue</a></html>' % (new, new))
        written.add(os.path.normcase(os.path.abspath(target)))

    nojekyll = os.path.join(out_dir, ".nojekyll")
    # GitHub Pages must not run Jekyll over the built output.
    with open(nojekyll, "w") as fh:
        fh.write("")
    written.add(os.path.normcase(os.path.abspath(nojekyll)))

    # Prune files that are no longer part of the site (rare, a handful at most).
    for dirpath, dirnames, filenames in os.walk(out_dir, topdown=False):
        for filename in filenames:
            path = os.path.normcase(os.path.join(dirpath, filename))
            if path not in written:
                try:
                    os.remove(path)
                except OSError:
                    pass
        if dirpath != out_dir and not os.listdir(dirpath):
            try:
                os.rmdir(dirpath)
            except OSError:
                pass

    if verbose:
        print("built %d pages -> %s" % (len(built), out_dir))
        print("  publications : %d" % len(PUBS))
        print("  tools        : %d" % len(TOOLS))
        print("  repositories : %d" % len(REPOS))
        print("  people       : %d" % len(PEOPLE))
        print("  news         : %d" % len(NEWS))
        print("  research     : %d" % len(RESEARCH))
        print("  patents      : %d" % len(PATENTS))
        print("  courses      : %d" % len(TEACHING))
        print("  textbooks    : %d" % len(BOOKS))
        print("  join records : %d" % len(JOIN))
        if problems:
            print("\n  WARNING — markers not found in the templates:")
            for p in sorted(set(problems)):
                print("    · %s" % p)
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description="Build the iSyslab website into _site/.")
    parser.add_argument("--out", default=os.path.join(ROOT, "_site"),
                        help="output directory (default: _site/)")
    args = parser.parse_args(argv)
    problems = build(os.path.abspath(args.out))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
