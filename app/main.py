from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown_converter  # 导入你的转换逻辑

app = FastAPI()

# 托管静态文件（CSS/JS）
app.mount("/static", StaticFiles(directory="static"), name="static")
# 加载HTML模板
templates = Jinja2Templates(directory="templates")

# 你的其他API接口...
@app.get("/convert")
def convert_markdown(text: str):
    return {"html": markdown_converter.to_html(text)}

# 前端页面入口
@app.get("/")
async def get_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
