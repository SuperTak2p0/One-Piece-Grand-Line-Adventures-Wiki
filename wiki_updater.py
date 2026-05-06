from bs4 import BeautifulSoup
import os
import re


FEATURE_PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Grand Line Adventures Wiki</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #0d1117;
            color: #c9d1d9;
            min-height: 100vh;
        }}
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
            max-width: 1000px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            gap: 1rem;
            height: 70px;
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
        .hero-content {{ position: relative; max-width: 700px; margin: 0 auto; }}
        .hero-icon {{ font-size: 4rem; margin-bottom: 1rem; }}
        .released-badge {{
            display: inline-block;
            background: rgba(35,134,54,0.2);
            border: 1px solid rgba(46,160,67,0.4);
            color: #2ea043;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 1rem;
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
        .content {{
            max-width: 800px;
            margin: 2rem auto;
            padding: 0 2rem;
        }}
        .content-box {{
            background: #161b22;
            border: 1px solid #21262d;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        .content-box h2 {{
            font-size: 1.1rem;
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
    </style>
</head>
<body>
    <header>
        <div class="header-inner">
            <a class="logo" href="/">
                <img src="https://github.com/SuperTak2p0/One-Piece-Grand-Line-Adventures-Wiki/blob/main/images/logo.jpeg?raw=true" alt="Logo">
                <span>
                    <div class="logo-title">Grand Line Adventures</div>
                    <div class="logo-sub">Minecraft Mod Wiki</div>
                </span>
            </a>
            <a class="back-link" href="/">← Back to Wiki</a>
        </div>
    </header>

    <div class="hero">
        <div class="hero-content">
            <div class="hero-icon">{icon}</div>
            <span class="released-badge">✅ Released</span>
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
    </div>

    <div class="content">
        <div class="content-box">
            <h2>About this Feature</h2>
            <p>{description}</p>
        </div>
        <div class="content-box">
            <h2>More details coming soon</h2>
            <p>
                This wiki page is being expanded. Check back after updates, or visit the
                <a href="https://www.curseforge.com/minecraft/mc-mods/one-piece-grand-line-adventures"
                   target="_blank" style="color:#c8960c;">CurseForge page</a> for the latest news.
            </p>
        </div>
    </div>

    <footer>
        <p>
            One Piece: Grand Line Adventures Wiki &mdash;
            <a href="https://www.curseforge.com/minecraft/mc-mods/one-piece-grand-line-adventures" target="_blank">Minecraft Forge Mod</a>.
            One Piece &copy; Eiichiro Oda / Shueisha. Not affiliated with Mojang.
        </p>
    </footer>
</body>
</html>
"""


class WikiUpdater:
    """
    Updates the wiki's index.html to mark a feature as released,
    or add a brand-new released feature box if it wasn't previously planned.
    Also generates a dedicated detail page for the feature.

    Usage:
        updater = WikiUpdater()

        # Mark an existing planned feature as released:
        updater.release_feature(
            feature_name="Devil Fruits",
            description="Discover and consume powerful Devil Fruits!",
            icon="🍎"
        )

        # Add a completely new, unplanned feature and release it immediately:
        updater.release_feature(
            feature_name="Sea Kings",
            description="Massive sea creatures roam the oceans.",
            icon="🐉"
        )
    """

    INDEX_PATH = "index.html"

    def release_feature(self, feature_name: str, description: str, icon: str = "⭐"):
        """
        Marks a feature as released in index.html and creates a detail page.

        Args:
            feature_name:  Display name of the feature (e.g. "Devil Fruits").
            description:   Short description shown on the card and detail page.
            icon:          Emoji icon for the feature card (default ⭐).
        """
        with open(self.INDEX_PATH, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")

        page_slug = self._slugify(feature_name)
        page_file = f"{page_slug}.html"
        page_url = f"/{page_file}"

        card_grid = soup.find("div", class_="card-grid")
        if card_grid is None:
            raise RuntimeError("Could not find .card-grid in index.html")

        existing_card = self._find_card(card_grid, feature_name)

        if existing_card:
            self._upgrade_card(existing_card, description, icon, page_url)
            print(f'[WikiUpdater] Marked existing feature "{feature_name}" as released.')
        else:
            new_card = self._build_released_card(soup, feature_name, description, icon, page_url)
            card_grid.append(new_card)
            print(f'[WikiUpdater] Added new released feature "{feature_name}" to the wiki.')

        self._update_sidebar(soup, feature_name, page_url)

        with open(self.INDEX_PATH, "w", encoding="utf-8") as f:
            f.write(str(soup))

        self._create_detail_page(page_file, feature_name, description, icon)
        print(f'[WikiUpdater] Detail page created: {page_file}')

    def _find_card(self, card_grid, feature_name: str):
        for card in card_grid.find_all("div", class_="card"):
            h3 = card.find("h3")
            if h3 and feature_name.lower() in h3.get_text().lower():
                return card
        return None

    def _upgrade_card(self, card, description: str, icon: str, page_url: str):
        card["class"] = [c for c in card.get("class", []) if c != "released"] + ["card", "released"]

        icon_tag = card.find("div", class_="card-icon")
        if icon_tag:
            icon_tag.string = icon

        desc_tag = card.find("p")
        if desc_tag:
            desc_tag.string = description

        h3 = card.find("h3")
        if h3:
            for tag in h3.find_all("span"):
                tag.decompose()
            released_span = BeautifulSoup(
                '<span class="released-tag">Released</span>', "html.parser"
            ).span
            h3.append(" ")
            h3.append(released_span)

        existing_link = card.find("a", class_="feature-link")
        if not existing_link:
            link = BeautifulSoup(
                f'<a class="feature-link" href="{page_url}">→ View full page</a>',
                "html.parser"
            ).a
            card.append(link)

    def _build_released_card(self, soup, feature_name: str, description: str, icon: str, page_url: str):
        html = f"""
        <div class="card released">
            <div class="card-icon">{icon}</div>
            <h3>{feature_name} <span class="released-tag">Released</span></h3>
            <p>{description}</p>
            <a class="feature-link" href="{page_url}">→ View full page</a>
        </div>
        """
        return BeautifulSoup(html, "html.parser").find("div", class_="card")

    def _update_sidebar(self, soup, feature_name: str, page_url: str):
        sidebar_ul = None
        for widget in soup.find_all("div", class_="widget"):
            title = widget.find("div", class_="widget-title")
            if title and "wiki pages" in title.get_text().lower():
                sidebar_ul = widget.find("ul")
                break

        if sidebar_ul is None:
            return

        for li in sidebar_ul.find_all("li"):
            a = li.find("a")
            if a and feature_name.lower() in a.get_text().lower():
                soon_tag = li.find("span", class_="wiki-tag-soon")
                if soon_tag:
                    soon_tag.decompose()
                a["href"] = page_url
                return

        new_li_html = f'<li><a href="{page_url}">⭐ {feature_name}</a></li>'
        new_li = BeautifulSoup(new_li_html, "html.parser").li
        sidebar_ul.append(new_li)

    def _create_detail_page(self, filename: str, title: str, description: str, icon: str):
        content = FEATURE_PAGE_TEMPLATE.format(
            title=title,
            description=description,
            icon=icon,
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def _slugify(name: str) -> str:
        slug = name.lower()
        slug = re.sub(r"[^a-z0-9]+", "-", slug)
        slug = slug.strip("-")
        return slug
