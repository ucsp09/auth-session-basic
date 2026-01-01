from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from aiofile import AIOFile
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_file_content(file_path: str) -> str:
    try:
        async with AIOFile(file_path, 'r') as afp:
            content = await afp.read()
        return content
    except Exception as e:
        return f"<h1>Error loading file: {str(e)}</h1>"

@app.get("/")
async def serve_index_html_page():
    try:
        index_html_file_path = "index.html"
        if os.path.exists(index_html_file_path):
            content = await get_file_content(index_html_file_path)
            return HTMLResponse(content=content)
        else:
            return HTMLResponse(content="<h1>404 Not Found</h1>", status_code=404)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading page: {str(e)}</h1>", status_code=500)

@app.get("/ui/{page}")
async def serve_ui_page(page: str):
    try:
        ui_page_html_file_path = f"ui/{page}.html"
        if os.path.exists(ui_page_html_file_path):
            content = await get_file_content(ui_page_html_file_path)
            return HTMLResponse(content=content)
        else:
            return HTMLResponse(content="<h1>404 Not Found</h1>", status_code=404)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading page: {str(e)}</h1>", status_code=500)

@app.get("/ui/static/{file_path:path}")
async def serve_static_file(file_path: str):
    try:
        static_file_full_path = f"ui/static/{file_path}"
        if os.path.exists(static_file_full_path):
            return FileResponse(static_file_full_path)
        else:
            return HTMLResponse(content="<h1>404 Not Found</h1>", status_code=404)
    except Exception as e:
        return HTMLResponse(content=f"<h1>Error loading file: {str(e)}</h1>", status_code=500)

