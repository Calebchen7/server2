from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import markdown
from markdown.extensions import codehilite, toc, extra

# 初始化FastAPI应用
app = FastAPI(title="Markdown实时预览服务")

# 挂载静态资源目录（CSS/JS等）
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置模板目录（指向templates文件夹）
templates = Jinja2Templates(directory="templates")

# Markdown转HTML核心接口
@app.post("/api/md2html", response_class=JSONResponse)
async def markdown_to_html(request: Request):
    try:
        # 接收前端传入的Markdown文本
        request_data = await request.json()
        markdown_content = request_data.get("markdown", "")

        # 配置Markdown扩展（支持代码高亮、表格、数学公式等）
        md_parser = markdown.Markdown(
            extensions=[
                "extra",               # 支持表格、脚注等基础扩展
                "codehilite",          # 代码高亮核心扩展
                "toc",                 # 自动生成目录
                "pymdownx.arithmatex" # 数学公式LaTeX支持
            ],
            extension_configs={
                "codehilite": {
                    "css_class": "highlight",
                    "linenums": False,
                    "guess_lang": True
                },
                "pymdownx.arithmatex": {
                    "generic": True
                }
            }
        )

        # 转换为HTML
        html_result = md_parser.convert(markdown_content)
        return JSONResponse(content={"status": "success", "html": html_result})

    except Exception as e:
        return JSONResponse(content={"status": "error", "msg": str(e)}, status_code=500)

# 根路径：返回前端主页面
@app.get("/", response_class=HTMLResponse)
async def get_index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
