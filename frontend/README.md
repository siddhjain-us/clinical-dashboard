# Clinical dashboard — frontend

Vite + React UI for the Flask API in `../backend/`.

## Run (demo order)

1. **Backend first** (port **8000**):

   ```bash
   cd /path/to/hackathon-project/backend
   source venv/bin/activate
   python app.py
   ```

2. **Frontend** in another terminal:

   ```bash
   cd /path/to/hackathon-project/frontend
   npm install
   npm run dev
   ```

3. Open the URL Vite prints (e.g. **http://localhost:5173**).

4. If the table is **empty**, seed the API (with the API still running):

   ```bash
   cd /path/to/hackathon-project/backend
   source venv/bin/activate
   python -c "from seed_patients import load; load()"
   ```

   Then refresh the browser.

## API URL

- Default: [`.env.development`](.env.development) sets `VITE_API_BASE=http://127.0.0.1:8000`. Change it if your backend uses another host or port.
- Restart `npm run dev` after changing env.

## Build

```bash
npm run build
npm run preview
```

## Judge / demo script

See **[`../JUDGE_PITCH.md`](../JUDGE_PITCH.md)** for a 2–3 minute pitch outline and run order.
