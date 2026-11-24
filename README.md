# AI Investigation Assistant Backend

## Requirements

- Python 3.14 (developed and tested with Python 3.14.3)
- Git

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

3. Create a virtual environment for this project:

   ```powershell
   py -3.14 -m venv .venv
   ```

4. Activate it in the current PowerShell session:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   The prompt should now start with `(.venv)`. Activate the environment again
   whenever you open a new terminal session.

5. Install the project dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Run the development server

With the virtual environment activated, run:

```powershell
python -m uvicorn main:app --reload
```

Open `http://127.0.0.1:8000/health` to check the health endpoint, or
`http://127.0.0.1:8000/docs` to view the interactive API documentation.
Press `Ctrl+C` in the terminal to stop the server.

The current application contains a health endpoint. Authentication and the
OpenAI Responses API integration have not been added yet.
