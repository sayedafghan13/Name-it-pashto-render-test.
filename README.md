# Pashto rendering feasibility test

This is a small, disposable test app — not part of the main Pashto Translator
project. Its only job is to answer one question: can Pillow's Linux build
correctly join the Pashto-only letters (ت ډ ړ ږ ښ ګ ڼ ځ څ) that currently
require Windows' GDI+ engine on the desktop/local server?

If `/render` shows these letters correctly joined (not disconnected), it
means the main app's image-translation feature could be ported to run on
cheap/free Linux hosting instead of needing a full Windows VM. If not, we
know that immediately, before investing further effort.

## Deploy to Render (free tier)

1. Push this folder to a new GitHub repository.
2. In Render, choose "New +" → "Blueprint", connect the repo (Render will
   read `render.yaml` automatically), and deploy.
3. Once live, open the deployed URL — it shows two renderings of nine test
   Pashto words side by side: one using real shaping (RAQM/HarfBuzz), one
   without (BASIC), so you can visually compare letters that should be
   connected.
