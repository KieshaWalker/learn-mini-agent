# Mini AI (Tiny Chatbot)

A tiny rule-based chatbot to learn basics of intents, simple entity extraction, and templated responses.

## Features
- Intents and responses from YAML
- Regex-based matching (case-insensitive)
- Simple name extraction: "I'm Alice", "I am Bob", "My name is Carol"
- Interactive CLI

## Quick start

1) Create a virtual environment (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependency

```bash
pip install -r requirements.txt
```

3) Run the chat

```bash
python run_chat.py

run_chat.py = terminal-only, no server, fastest way to test responses.
run_api.py = runs a web server + React page, shows how a frontend calls the bot over HTTP.

Type `exit` to quit.

## Run the mini web demo (React + FastAPI)

This repo includes a tiny web demo with a minimal React page and a FastAPI backend.

1) Install extra dependencies

```bash
pip install -r requirements.txt
```

2) Start the API server

```bash
python run_api.py
```

3) Open the web page

Visit http://127.0.0.1:8000 in your browser. Type messages and see replies.

Notes:
- The page is served from `web/index.html` via the FastAPI server.
- The page makes `POST /chat` requests to the backend.

## Project structure

- `src/mini_ai/engine.py` — core logic for matching and responding
- `src/mini_ai/cli.py` — interactive command-line interface
- `data/intents.yml` — intents, patterns, and responses
- `run_chat.py` — convenience runner that adds `src/` to `PYTHONPATH`
- `run_api.py` — runs the FastAPI backend for the web demo
- `smoke_test.py` — quick script to exercise the bot in code

## Customize
Edit `data/intents.yml` to add new intents with `patterns` (regex) and `responses`. You can use placeholders like `{name}` which will be filled when the bot detects a name.

---

## Walkthrough: Files, paths, and how to edit

This section explains what each important file does and where to edit when you want to change behavior.

### Core bot logic

- `src/mini_ai/engine.py`
	- Purpose: The tiny "brain" of the bot. Loads intents from YAML, matches messages with regex, extracts a simple name entity, and builds a reply.
	- Edit when you want to:
		- Change how intents are matched (e.g., change regex logic, match priority).
		- Add new entity extraction (beyond just `{name}`).
		- Add dynamic responses (e.g., current time, simple calculator).
	- How: Open the file and modify functions like `predict_intent` or `respond`. Add helper functions for new features.

- `data/intents.yml`
	- Purpose: The bot’s knowledge base. Each intent has `name`, `patterns` (regex), and `responses`.
	- Edit when you want to:
		- Add new Q&A (FAQ-style) or small-talk.
		- Adjust patterns to be more/less strict.
	- Tips:
		- Use single quotes for regex that contain backslashes, e.g., `'good\\s*morning'`.
		- Put more specific patterns before general ones. Keep `fallback` last.
		- You can use `{name}` in responses; it will be filled if detected.

### Command-line experience (terminal)

- `run_chat.py`
	- Purpose: Starts a terminal chat (CLI). Adds `src/` to `PYTHONPATH` so you don’t need to install the package.
	- Edit when you want to:
		- Change how the CLI launches or passes the intents path.
	- Run:
		```bash
		python run_chat.py
		```

- `src/mini_ai/cli.py`
	- Purpose: Implements the CLI loop and command-line args (like `--intents`).
	- Edit when you want to:
		- Add CLI options (e.g., load a different intents file, enable debug).
		- Change prompts or how input/output is displayed.

### Web experience (browser + API)

- `src/mini_ai/server.py`
	- Purpose: FastAPI server with two routes:
		- `GET /` serves the minimal React page.
		- `POST /chat` accepts `{ "message": "..." }` and returns `{ "reply": "..." }`.
	- Edit when you want to:
		- Add new API endpoints.
		- Customize CORS or change where the page is served from.
		- Add session/memory (store user details between requests).
	- Session memory:
		- The server sets a cookie `mini_ai_sid` per browser to remember simple info such as your `{name}`.
		- Memory is kept in-process (cleared when you restart the server).
		- To clear memory for your browser, delete the cookie or use a new private window.

- `run_api.py`
	- Purpose: Starts the FastAPI app via `uvicorn`. Keeps it simple for local dev.
	- Run:
		```bash
		python run_api.py
		# open http://127.0.0.1:8000
		```
	- Edit when you want to:
		- Change host/port or adjust logging (e.g., `access_log=False`).

- `web/index.html`
	- Purpose: A single HTML file that renders a tiny React chat UI and calls `/chat`.
	- Edit when you want to:
		- Change the UI (styles, layout, message bubbles).
		- Add keyboard shortcuts (e.g., Enter to send), autofocus, or UI hints.
		- Add client-side features like showing a typing indicator.
	- Notes:
		- Uses React and Babel via CDN; `type="text/babel"` transpiles JSX in the browser.
		- We use modern Babel Standalone v7 and only the React preset.

### Utilities and support files

- `smoke_test.py`
	- Purpose: Quick checks to ensure basic intent matching works.
	- Run:
		```bash
		python smoke_test.py
		```

- `src/mini_ai/__init__.py`
	- Purpose: Defines the Python package exports (`engine`, `cli`).

- `requirements.txt`
	- Purpose: Python dependencies (`PyYAML`, `fastapi`, `uvicorn`).
	- Edit when you add server features that need new libraries.

---

## Common edits (recipes)

- Add a new FAQ/small-talk intent:
	1) Edit `data/intents.yml` and add under `intents:`
		 ```yaml
		 - name: thanks
			 patterns:
				 - 'thanks'
				 - 'thank you'
			 responses:
				 - 'You\'re welcome!'
				 - 'Happy to help!'
		 ```
	2) Save and run either `python run_chat.py` or refresh the web page.

- Add a dynamic "current time" response (example outline):
	1) In `data/intents.yml`, add a `time` intent with a pattern, e.g., `'what time is it'`.
	2) In `engine.py`, inside `respond`, detect that intent and return `datetime.now().strftime(...)` instead of a static template.
	3) If using the web server, restart it after changes (Ctrl+C then `python run_api.py`).

- Change server port:
	- Edit `run_api.py` and modify `port=8000` to your preferred port.

---

## Troubleshooting

- Browser console shows a Babel or syntax error
	- We use Babel Standalone v7 with `data-presets="react"`. If you added advanced JS features, keep them compatible with your browser or move to a bundler later.

- Server logs show `404` for `/favicon.ico` or `/.well-known/...`
	- Harmless. Browser/DevTools probing. You can ignore or add a tiny route that returns `204`.

- Changes in `intents.yml` don’t seem to apply in the browser
	- Restart the server (`Ctrl+C` then `python run_api.py`) because the bot is loaded at startup.
	- Then refresh the browser page.

---

## Integrate into an existing React/Node app (step by step)

There are many ways to wire this in; here are simple, proven paths. The idea is: run the Python bot server alongside your React app and call `POST /chat` from the frontend.

### Approach A: Keep FastAPI as a separate service

1) Add the bot to your repo (or keep it as a sibling project)
	 - Copy these into a folder like `ai-bot/`:
		 - `src/mini_ai/` (package)
		 - `data/intents.yml`
		 - `run_api.py`
		 - `requirements.txt`

2) Create a virtual environment and install deps
```bash
cd ai-bot
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

3) Run the API with auto-reload during dev
```bash
python -m uvicorn mini_ai.server:app --host 127.0.0.1 --port 8000 --reload
```

4) Point your React dev server to the API
	 - Create React App (CRA): add a proxy in `package.json`
```json
{
	"proxy": "http://127.0.0.1:8000"
}
```
	 - Vite: in `vite.config.js`
```js
// vite.config.js
export default {
	server: {
		proxy: {
			'/chat': 'http://127.0.0.1:8000'
		}
	}
}
```

5) Call the API from your React app
```js
// anywhere in your React code
async function askBot(message) {
	const res = await fetch('/chat', {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ message }),
	});
	const data = await res.json();
	return data.reply; // string
}
```

6) Run both dev servers
```bash
# in one terminal
cd ai-bot && source .venv/bin/activate && python -m uvicorn mini_ai.server:app --reload

# in another terminal
cd your-react-app && npm start
```

Notes:
- CORS is already enabled to allow requests from your app during dev.
- After changing `data/intents.yml` or Python code, reload happens automatically with `--reload` (or restart if you use `run_api.py`).

### Optional: use nodemon to supervise the Python server

If you prefer nodemon (many Node devs do), you can have it restart the Python API when `.py` or `.yml` files change.

1) Install nodemon in your JS workspace
```bash
npm i -D nodemon
```

2) Add a `nodemon.json` next to your `ai-bot/` folder (adjust paths as needed)
```json
{
	"watch": ["ai-bot/src/mini_ai", "ai-bot/data"],
	"ext": "py,yml",
	"exec": "bash -lc 'cd ai-bot && source .venv/bin/activate && python -m uvicorn mini_ai.server:app --host 127.0.0.1 --port 8000'"
}
```

3) Run it
```bash
npx nodemon
```

### Approach B: Proxy through your existing Node/Express backend

If you have an Express server, proxy `/chat` to the Python API so the browser only talks to your Node server.

1) Start the Python API on `127.0.0.1:8000` (as above)

2) Add a proxy route in Express using `http-proxy-middleware`
```bash
npm i http-proxy-middleware
```
```js
// server/index.js (Express)
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const app = express();

app.use('/chat', createProxyMiddleware({
	target: 'http://127.0.0.1:8000',
	changeOrigin: true,
}));

app.listen(3001, () => console.log('Express on http://127.0.0.1:3001'));
```

3) In React, call `/chat` (which hits your Node server, which proxies to Python)

### Approach C: Python-only stack

If your app is Python-based (Flask/Django/FastAPI), mount `mini_ai.server:app` or call `MiniAI` directly from your routes.

---

### Production hint

Run the API with Uvicorn or behind a reverse proxy (NGINX/Caddy). Example:
```bash
python -m uvicorn mini_ai.server:app --host 0.0.0.0 --port 8000
```

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

Third‑party dependencies are licensed by their respective authors:
- PyYAML (MIT) — YAML parsing
- FastAPI (MIT) — web framework
- Uvicorn (BSD) — ASGI server
- React (MIT) — frontend UI library (loaded via CDN in the demo)
- @babel/standalone (MIT) — in-browser JSX transpilation (CDN in the demo)

---

## Configuration (.env)

You can control the server and API behavior via environment variables. Create a `.env` file (already git-ignored) in the project root. Example:

```
APP_HOST=127.0.0.1
APP_PORT=8000
LOG_LEVEL=info
ACCESS_LOG=true
INTENTS_PATH=./data/intents.yml
CORS_ALLOW_ORIGINS=*
SESSION_COOKIE=mini_ai_sid
SECRET_KEY=change-me-in-production
```

Notes:
- `APP_HOST`, `APP_PORT` — where the API binds.
- `LOG_LEVEL` — `critical|error|warning|info|debug|trace`.
- `ACCESS_LOG` — set to `false` to silence per-request logs.
- `INTENTS_PATH` — path to your YAML intents.
- `CORS_ALLOW_ORIGINS` — comma-separated origins (e.g., `http://localhost:3000,http://127.0.0.1:5173`).
- `SESSION_COOKIE` — cookie name used for simple session memory.
- `SECRET_KEY` — placeholder for future features (JWT, signing); keep secret in production.


