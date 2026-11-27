# AI Investigation Assistant Backend

## Requirements

- Python 3.14 (developed and tested with Python 3.14.3)
- Git
- An OpenAI API key

## Setup on Windows (PowerShell)

1. Clone the repository and enter its folder:

   ```powershell
   git clone https://github.com/JuergenPower/ai-assistant-backend.git
   cd ai-assistant-backend
   ```

2. Check that Python 3.14 is installed:

   ```powershell
   py -3.14 --version
   ```

3. Create and activate a project virtual environment:

   ```powershell
   py -3.14 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   The prompt should start with `(.venv)`. Activate the environment again in
   each new terminal session.

4. Install the project dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

5. Create a local environment file from the example:

   ```powershell
   Copy-Item .env.example .env
   ```

   Edit `.env` and set:

   - `OPENAI_API_KEY` to your OpenAI API key.
   - `OPENAI_MODEL` to a model available to your OpenAI project. example: gpt-5.6-luna
   - `BACKEND_ACCESS_TOKEN` to a long, random token used by clients to access
     this backend.

   Keep `.env` private; it is excluded from Git.

   Alternative to hide OPENAI_API_KEY from your dev AI:

   ```powershell
   $secureKey = Read-Host "OpenAI API key" -AsSecureString
   $env:OPENAI_API_KEY = (New-Object System.Net.NetworkCredential("", $secureKey)). Password
   $env:OPENAI_MODEL = "HIER_DEIN_MODELLNAME"
   $env:BACKEND_ACCESS_TOKEN = python -c "import secrets; print(secrets.   token_urlsafe(32))"
   $env:BACKEND_ACCESS_TOKEN
   ```

## Run the development server

With the virtual environment activated and `.env` configured, run:

```powershell
python -m uvicorn main:app --reload --env-file .env
```

or if you set the secrets manually in the powershell session just run

```powershell
python -m uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.
`GET /health` checks that the backend is running.

Click "Authorize" and enter the BACKEND_ACCESS_TOKEN value to test the endpoints requiring authorization. 

Press `Ctrl+C` in the terminal to stop the server.

## Build and publish the backend image

Build and run the image locally from the repository root:

```powershell
docker build -t ai-assistant-backend:local .
docker run --rm --env-file .env -p 8000:8000 ai-assistant-backend:local
```

The image does not contain `.env` or application secrets. Pass configuration
such as `OPENAI_API_KEY`, `OPENAI_MODEL`, and `BACKEND_ACCESS_TOKEN` when the
container is run.

To publish an image manually, open **Actions**, select **Build and publish
backend image**, and choose **Run workflow**. The workflow publishes
`ghcr.io/juergenpower/ai-assistant-backend` with both a `latest` tag and a
commit-SHA tag. The workflow does not run on pushes.

After the first successful publish, change the package visibility to **Public**
in the package settings on GitHub if the VPS should pull the image without
authenticating.
