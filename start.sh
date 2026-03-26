#!/bin/bash

# 颜色配置
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 欢迎信息
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}   Markdown 实时预览服务 - 一键启动${NC}"
echo -e "${GREEN}=====================================${NC}"

# 1. 检查conda环境
if ! command -v conda &> /dev/null; then
    echo -e "${RED}错误：未检测到conda，请先安装miniconda/anaconda${NC}"
    exit 1
fi

# 2. 激活my_project环境
echo -e "${YELLOW}正在激活my_project环境...${NC}"
source ~/miniconda3/etc/profile.d/conda.sh
conda activate my_project

if [[ "$CONDA_DEFAULT_ENV" != "my_project" ]]; then
    echo -e "${RED}错误：无法激活my_project环境，请检查环境是否存在${NC}"
    exit 1
fi

# 3. 安装项目依赖
echo -e "${YELLOW}正在安装项目依赖...${NC}"
pip install -r requirements.txt

# 4. 停止旧的服务进程
echo -e "${YELLOW}正在清理旧的服务进程...${NC}"
pkill -f 'uvicorn main:app' > /dev/null 2>&1

# 5. 后台启动服务
echo -e "${YELLOW}正在启动服务...${NC}"
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

# 6. 等待服务启动
sleep 2

# 7. 检查服务是否启动成功
if pgrep -f 'uvicorn main:app' > /dev/null; then
    # 获取本机IP
    SERVER_IP=$(hostname -I | awk '{print $1}')
    echo -e "${GREEN}✅ 服务启动成功！${NC}"
    echo -e "${GREEN}🌐 访问地址：http://${SERVER_IP}:8000${NC}"
    echo -e "${GREEN}📝 日志文件：server.log${NC}"
    echo -e "${YELLOW}🛑 停止服务命令：pkill -f 'uvicorn main:app'${NC}"
else
    echo -e "${RED}❌ 服务启动失败，请查看日志：cat server.log${NC}"
    exit 1
fi
