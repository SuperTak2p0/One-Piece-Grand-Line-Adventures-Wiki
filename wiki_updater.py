from bs4 import BeautifulSoup
import re

LOGO_URL = "https://github.com/SuperTak2p0/One-Piece-Grand-Line-Adventures-Wiki/blob/main/images/logo.jpeg?raw=true"
CURSEFORGE_URL = "https://www.curseforge.com/minecraft/mc-mods/one-piece-grand-line-adventures"
BASE_URL = "https://supertak2p0.github.io/One-Piece-Grand-Line-Adventures-Wiki"

FEATURE_PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Grand Line Adventures Wiki</title>
    <link rel="icon" type="image/jpeg" href="{logo_url}"/>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            min-height: 100vh;
        }}

        /* Header */
        header {{
            background: linear-gradient(135deg, #1a0a00 0%, #2d1200 40%, #1a0a00 100%);
            border-bottom: 3px solid #c8960c;
            padding: 0 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 20px rgba(200,150,12,0.3);
        }}
        .header-inner {{
            max-width: 1100px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            height: 70px;
            gap: 1rem;
        }}
        .logo {{
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
        }}
        .logo img {{
            width: 48px;
            height: 48px;
            border-radius: 8px;
            object-fit: cover;
            border: 1px solid rgba(200,150,12,0.3);
        }}
        .logo-title {{
            font-size: 1.1rem;
            font-weight: 800;
            color: #c8960c;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}
        .logo-sub {{
            font-size: 0.68rem;
            color: #8b6914;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }}
        .back-link {{
            margin-left: auto;
            color: #8b949e;
            text-decoration: none;
            font-size: 0.875rem;
            transition: color 0.2s;
        }}
        .back-link:hover {{ color: #c8960c; }}

        /* Hero */
        .hero {{
            background: linear-gradient(180deg, #1a0a00 0%, #0d1117 100%);
            border-bottom: 1px solid #21262d;
            padding: 3rem 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        .hero::before {{
            content: '';
            position: absolute;
            inset: 0;
            background: radial-gradient(ellipse at 50% 0%, rgba(200,150,12,0.12) 0%, transparent 70%);
        }}
        .hero-content {{
            position: relative;
            max-width: 700px;
            margin: 0 auto;
        }}
        .hero h1 {{
            font-size: 2.5rem;
            font-weight: 900;
            color: #f0c040;
            text-shadow: 0 0 30px rgba(240,192,64,0.3);
            margin-bottom: 0.75rem;
        }}
        .hero p {{
            font-size: 1rem;
            color: #8b949e;
            line-height: 1.7;
        }}
        .status-badge {{
            display: inline-block;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 1rem;
        }}
        .status-badge.released {{
            background: rgba(35,134,54,0.2);
            border: 1px solid rgba(46,160,67,0.4);
            color: #2ea043;
        }}
        .status-badge.coming-soon {{
            background: rgba(200,150,12,0.12);
            border: 1px solid rgba(200,150,12,0.35);
            color: #c8960c;
        }}

        /* Page layout */
        .page-layout {{
            max-width: 1100px;
            margin: 2rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: 1fr 270px;
            gap: 2rem;
            align-items: start;
        }}

        /* Content boxes */
        .content-box {{
            background: #161b22;
            border: 1px solid #21262d;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        .content-box:last-child {{ margin-bottom: 0; }}
        .content-box h2 {{
            font-size: 1.05rem;
            font-weight: 700;
            color: #e6edf3;
            margin-bottom: 0.75rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #c8960c;
        }}
        .content-box p {{
            font-size: 0.9rem;
            color: #8b949e;
            line-height: 1.7;
        }}
        .content-box a {{
            color: #f16436;
            font-weight: 700;
            text-decoration: none;
        }}
        .content-box a:hover {{ color: #ff7a50; }}

        /* Sidebar */
        .info-widget {{
            background: #161b22;
            border: 1px solid #21262d;
            border-radius: 10px;
            padding: 1.25rem;
        }}
        .wiki-nav {{
            list-style: none;
            margin: 0;
            padding: 0;
        }}
        .wiki-nav li {{
            padding: 0.35rem 0;
            border-bottom: 1px solid #21262d;
        }}
        .wiki-nav li:last-child {{ border-bottom: none; }}
        .wiki-nav a {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
            color: #8b949e;
            text-decoration: none;
            transition: color 0.2s;
        }}
        .wiki-nav a:hover {{ color: #c8960c; }}
        .wiki-nav a.active {{ color: #c8960c; font-weight: 700; }}
        .wiki-tag-soon {{
            font-size: 0.65rem;
            background: rgba(139,100,20,0.2);
            border: 1px solid rgba(200,150,12,0.25);
            color: #8b6914;
            padding: 0.1rem 0.4rem;
            border-radius: 10px;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}
        .widget-title {{
            font-size: 0.82rem;
            font-weight: 700;
            color: #c8960c;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 0.9rem;
        }}
        .info-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.45rem 0;
            border-bottom: 1px solid #21262d;
            font-size: 0.85rem;
        }}
        .info-row:last-child {{ border-bottom: none; }}
        .info-label {{ color: #8b949e; }}
        .info-value {{
            color: #e6edf3;
            font-weight: 600;
            text-align: right;
        }}
        .info-value.released {{ color: #2ea043; }}
        .info-value.coming-soon {{ color: #c8960c; }}
        .info-value.editing-yes {{ color: #58a6ff; }}
        .info-value.editing-no {{ color: #8b949e; font-weight: 400; }}

        /* Footer */
        footer {{
            border-top: 1px solid #21262d;
            padding: 2rem;
            text-align: center;
            color: #484f58;
            font-size: 0.82rem;
            margin-top: 2rem;
        }}
        footer a {{ color: #8b949e; text-decoration: none; }}
        footer a:hover {{ color: #c8960c; }}

        @media (max-width: 720px) {{
            .page-layout {{ grid-template-columns: 1fr; }}
            .hero h1 {{ font-size: 1.8rem; }}
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-inner">
            <a class="logo" href="https://supertak2p0.github.io/One-Piece-Grand-Line-Adventures-Wiki">
                <img src="{logo_url}" alt="Grand Line Adventures Logo">
                <span>
                    <div class="logo-title">Grand Line Adventures</div>
                    <div class="logo-sub">Minecraft Mod Wiki</div>
                </span>
            </a>
            <a class="back-link" href="https://supertak2p0.github.io/One-Piece-Grand-Line-Adventures-Wiki">Back to Wiki</a>
        </div>
    </header>

    <div class="hero">
        <div class="hero-content">
            <h1>{title}</h1>
            <span class="status-badge {status_class}">{status_label}</span>
            <p>{description}</p>
        </div>
    </div>

    <div class="page-layout">
        <main>
            <div class="content-box">
                <h2>About this Feature</h2>
                <p>{description}</p>
            </div>
            <div class="content-box">
                <h2>More details coming soon</h2>
                <p>
                    This wiki page is being expanded. Check back after updates, or visit the
                    <a href="{curseforge_url}" target="_blank">CurseForge page</a> for the latest news.
                </p>
            </div>
        </main>

        <aside>
            <div class="info-widget">
                <div class="widget-title">Feature Info</div>
                <div class="info-row">
                    <span class="info-label">Status</span>
                    <span class="info-value {status_class}">{status_label}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">{release_date_label}</span>
                    <span class="info-value">{release_date_value}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Mod Version</span>
                    <span class="info-value">{mod_version}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Under Editing</span>
                    <span class="info-value {editing_class}">{under_editing_value}</span>
                </div>
            </div>

            <div class="info-widget" style="margin-top:1rem;">
                <div class="widget-title">Wiki Pages</div>
                <ul class="wiki-nav">
                    <li><a href="{base_url}/index.html">Home</a></li>
                    {wiki_nav_items}
                </ul>
            </div>
        </aside>
    </div>

    <footer>
        <p>
            One Piece: Grand Line Adventures Wiki &mdash;
            <a href="{curseforge_url}" target="_blank">Minecraft Forge Mod</a>.
            One Piece &copy; Eiichiro Oda / Shueisha. Not affiliated with Mojang.
        </p>
    </footer>
</body>
</html>
"""


class WikiUpdater:
    """
    Manages the Grand Line Adventures wiki pages.

    Methods
    -------
    plan_feature(feature_name, description, estimated_date, mod_version)
        Adds a new "Coming Soon" card to index.html and creates a detail page.

    release_feature(feature_name, description, release_date, mod_version, under_editing)
        Marks a feature as released in index.html and creates/updates its detail page.

    Examples
    --------
    updater = WikiUpdater()

    # Add a planned (coming soon) feature:
    updater.plan_feature(
        feature_name="Sea Kings",
        description="Massive sea creatures roam the Grand Line oceans.",
        estimated_date="Q3 2025",
        mod_version="TBD",
    )

    # Mark a feature as released:
    updater.release_feature(
        feature_name="Factions",
        description="Align with the Marines, Pirates, or the World Government.",
        release_date="2025-06-01",
        mod_version="1.2.0",
        under_editing=True,
    )
    """

    INDEX_PATH = "index.html"

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def plan_feature(
        self,
        feature_name: str,
        description: str,
        estimated_date: str = "TBD",
        mod_version: str = "TBD",
    ):
        """
        Adds a Coming Soon feature card to index.html and creates its detail page.

        Args:
            feature_name:    Display name (e.g. "Sea Kings").
            description:     Short description for the card and detail page.
            estimated_date:  Estimated release, e.g. "Q3 2025" or "TBD".
            mod_version:     Target mod version, e.g. "1.3.0" or "TBD".
        """
        with open(self.INDEX_PATH, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        page_slug = self._slugify(feature_name)
        page_file = f"{page_slug}.html"
        page_url = f"{BASE_URL}/{page_file}"

        card_grid = soup.find("div", class_="card-grid")
        if card_grid is None:
            raise RuntimeError("Could not find .card-grid in index.html")

        existing_card = self._find_card(card_grid, feature_name)
        if existing_card:
            print(f'[WikiUpdater] Feature "{feature_name}" already exists — skipping card creation.')
        else:
            new_card = self._build_planned_card(feature_name, description, page_url)
            card_grid.append(new_card)
            print(f'[WikiUpdater] Added planned feature "{feature_name}" to index.html.')

        self._update_sidebar(soup, feature_name, page_url, released=False)

        with open(self.INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(str(soup))

        self._update_all_wiki_navs(soup, skip_file=page_file)
        self._create_detail_page(
            filename=page_file,
            title=feature_name,
            description=description,
            released=False,
            release_date=estimated_date,
            mod_version=mod_version,
            under_editing=False,
            soup=soup,
        )
        print(f'[WikiUpdater] Detail page created: {page_file}')

    def release_feature(
        self,
        feature_name: str,
        description: str,
        release_date: str = "TBD",
        mod_version: str = "TBD",
        under_editing: bool = False,
    ):
        """
        Marks a feature as released in index.html and creates/updates its detail page.

        Args:
            feature_name:   Display name (e.g. "Devil Fruits").
            description:    Short description for the card and detail page.
            release_date:   Actual release date, e.g. "2025-06-01" or "TBD".
            mod_version:    Mod version it shipped in, e.g. "1.2.0" or "TBD".
            under_editing:  True if the wiki page is still being written.
        """
        with open(self.INDEX_PATH, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        page_slug = self._slugify(feature_name)
        page_file = f"{page_slug}.html"
        page_url = f"{BASE_URL}/{page_file}"

        card_grid = soup.find("div", class_="card-grid")
        if card_grid is None:
            raise RuntimeError("Could not find .card-grid in index.html")

        existing_card = self._find_card(card_grid, feature_name)
        if existing_card:
            self._upgrade_card(existing_card, description, page_url)
            print(f'[WikiUpdater] Marked existing feature "{feature_name}" as released.')
        else:
            new_card = self._build_released_card(feature_name, description, page_url)
            card_grid.append(new_card)
            print(f'[WikiUpdater] Added new released feature "{feature_name}" to index.html.')

        self._update_sidebar(soup, feature_name, page_url, released=True)

        with open(self.INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(str(soup))

        self._update_all_wiki_navs(soup, skip_file=page_file)
        self._create_detail_page(
            filename=page_file,
            title=feature_name,
            description=description,
            released=True,
            release_date=release_date,
            mod_version=mod_version,
            under_editing=under_editing,
            soup=soup,
        )
        print(f'[WikiUpdater] Detail page created/updated: {page_file}')

    # ------------------------------------------------------------------ #
    #  Private helpers — index.html                                        #
    # ------------------------------------------------------------------ #

    def _find_card(self, card_grid, feature_name: str):
        for card in card_grid.find_all("div", class_="card"):
            h3 = card.find("h3")
            if h3 and feature_name.lower() in h3.get_text().lower():
                return card
        return None

    def _build_planned_card(self, feature_name: str, description: str, page_url: str):
        html = (
            f'<div class="card">'
            f'<h3>{feature_name} <span class="coming-soon-tag">Coming Soon</span></h3>'
            f'<p>{description}</p>'
            f'<a class="feature-link" href="{page_url}">Read more</a>'
            f'</div>'
        )
        return BeautifulSoup(html, "html.parser").find("div", class_="card")

    def _build_released_card(self, feature_name: str, description: str, page_url: str):
        html = (
            f'<div class="card released">'
            f'<h3>{feature_name} <span class="released-tag">Released</span></h3>'
            f'<p>{description}</p>'
            f'<a class="feature-link" href="{page_url}">Read more</a>'
            f'</div>'
        )
        return BeautifulSoup(html, "html.parser").find("div", class_="card")

    def _upgrade_card(self, card, description: str, page_url: str):
        classes = [c for c in card.get("class", []) if c not in ("released", "card")]
        card["class"] = ["card", "released"] + classes

        desc_tag = card.find("p")
        if desc_tag:
            desc_tag.string = description

        h3 = card.find("h3")
        if h3:
            for tag in h3.find_all("span"):
                tag.decompose()
            span = BeautifulSoup('<span class="released-tag">Released</span>', "html.parser").span
            h3.append(" ")
            h3.append(span)

        link = card.find("a", class_="feature-link")
        if not link:
            a = BeautifulSoup(
                f'<a class="feature-link" href="{page_url}">Read more</a>', "html.parser"
            ).a
            card.append(a)
        else:
            link["href"] = page_url

    def _update_sidebar(self, soup, feature_name: str, page_url: str, released: bool):
        sidebar_ul = None
        for widget in soup.find_all("div", class_="widget"):
            title_el = widget.find("div", class_="widget-title")
            if title_el and "wiki pages" in title_el.get_text().lower():
                sidebar_ul = widget.find("ul")
                break

        if sidebar_ul is None:
            return

        for li in sidebar_ul.find_all("li"):
            a = li.find("a")
            if a and feature_name.lower() in a.get_text().lower():
                a["href"] = page_url
                soon_tag = li.find("span", class_="wiki-tag-soon")
                if soon_tag and released:
                    soon_tag.decompose()
                return

        if released:
            new_li_html = f'<li><a href="{page_url}">{feature_name}</a></li>'
        else:
            new_li_html = (
                f'<li><a href="{page_url}">'
                f'{feature_name} <span class="wiki-tag-soon">Soon</span>'
                f'</a></li>'
            )
        sidebar_ul.append(BeautifulSoup(new_li_html, "html.parser").li)

    # ------------------------------------------------------------------ #
    #  Private helpers — detail page                                       #
    # ------------------------------------------------------------------ #

    def _update_all_wiki_navs(self, soup, skip_file: str = ""):
        """
        After index.html is updated, push the refreshed Wiki Pages nav
        into every existing feature detail page.
        """
        import glob as _glob
        for path in sorted(_glob.glob("*.html")):
            if path == self.INDEX_PATH or path == skip_file:
                continue
            with open(path, "r", encoding="utf-8") as f:
                page_soup = BeautifulSoup(f.read(), "html.parser")
            nav_ul = page_soup.find("ul", class_="wiki-nav")
            if nav_ul is None:
                continue
            new_items_html = self._build_wiki_nav_items(soup, path)
            new_ul = BeautifulSoup(
                f'<ul class="wiki-nav">\n                    {new_items_html}\n                </ul>',
                "html.parser",
            ).ul
            nav_ul.replace_with(new_ul)
            with open(path, "w", encoding="utf-8") as f:
                f.write(str(page_soup))
            print(f'[WikiUpdater] Updated wiki nav in: {path}')

    def _build_wiki_nav_items(self, soup, current_filename: str) -> str:
        """Reads the Wiki Pages sidebar from index.html and returns nav <li> HTML."""
        lines = []
        for widget in soup.find_all("div", class_="widget"):
            title_el = widget.find("div", class_="widget-title")
            if title_el and "wiki pages" in title_el.get_text().lower():
                for li in widget.find_all("li"):
                    a = li.find("a")
                    if not a:
                        continue
                    href = a.get("href", "#")
                    soon = li.find("span", class_="wiki-tag-soon")
                    # Determine if this link points to the current page
                    is_active = href.rstrip("/").endswith(current_filename)
                    active_class = ' class="active"' if is_active else ""
                    label = a.get_text(strip=True).replace("Soon", "").strip()
                    tag = ' <span class="wiki-tag-soon">Soon</span>' if soon else ""
                    lines.append(
                        f'<li><a href="{href}"{active_class}>{label}{tag}</a></li>'
                    )
                break
        return "\n                    ".join(lines)

    def _create_detail_page(
        self,
        filename: str,
        title: str,
        description: str,
        released: bool,
        release_date: str,
        mod_version: str,
        under_editing: bool,
        soup=None,
    ):
        if released:
            status_class = "released"
            status_label = "Released"
            release_date_label = "Release Date"
        else:
            status_class = "coming-soon"
            status_label = "Coming Soon"
            release_date_label = "Est. Release"

        if under_editing:
            editing_class = "editing-yes"
            under_editing_value = "Yes"
        else:
            editing_class = "editing-no"
            under_editing_value = "No"

        if soup is not None:
            wiki_nav_items = self._build_wiki_nav_items(soup, filename)
        else:
            wiki_nav_items = ""

        content = FEATURE_PAGE_TEMPLATE.format(
            title=title,
            description=description,
            logo_url=LOGO_URL,
            curseforge_url=CURSEFORGE_URL,
            base_url=BASE_URL,
            status_class=status_class,
            status_label=status_label,
            release_date_label=release_date_label,
            release_date_value=release_date,
            mod_version=mod_version,
            editing_class=editing_class,
            under_editing_value=under_editing_value,
            wiki_nav_items=wiki_nav_items,
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def _slugify(name: str) -> str:
        slug = name.lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        return slug.strip("-")


if __name__ == "__main__":
    print("WikiUpdater ready.")
    print()
    print("Plan a coming-soon feature:")
    print('  updater.plan_feature("Sea Kings", "Massive creatures of the sea.", estimated_date="Q3 2025", mod_version="TBD")')
    print()
    print("Release a feature:")
    print('  updater.release_feature("Factions", "Join Marines or Pirates.", release_date="2025-06-01", mod_version="1.2.0", under_editing=True)')
