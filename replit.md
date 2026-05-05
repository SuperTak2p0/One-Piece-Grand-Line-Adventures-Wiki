# One-Piece-Grand-Line-Adventures-Wiki

A simple static HTML wiki page for the One Piece Grand Line Adventures Minecraft mod.

## Project Structure

- `index.html` — Main HTML page ("Hello World" placeholder)
- `HelloWorldSeite` — Duplicate HTML file
- `README.md` — Project description with CurseForge link

## Tech Stack

- Static HTML (no frameworks, no build tools)
- Python 3.11 `http.server` for local development serving

## Running the App

The app is served with Python's built-in HTTP server on port 5000:

```
python3 -m http.server 5000 --bind 0.0.0.0
```

## Deployment

Configured as a static site deployment with the project root as the public directory.
