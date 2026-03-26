// 获取DOM元素
const editor = document.getElementById('markdown-editor');
const previewContainer = document.getElementById('preview-container');

// 防抖函数：避免频繁请求后端
function debounce(func, delay = 300) {
    let timer = null;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(this, args), delay);
    };
}

// 核心：Markdown实时渲染
const renderMarkdown = debounce(async () => {
    const markdownText = editor.value.trim();
    try {
        // 调用后端接口转换
        const response = await fetch('/api/md2html', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ markdown: markdownText })
        });

        const result = await response.json();
        if (result.status === 'success') {
            // 渲染HTML
            previewContainer.innerHTML = result.html;
            // 重新触发代码高亮
            hljs.highlightAll();
            // 重新渲染数学公式
            MathJax.typesetPromise();
        } else {
            previewContainer.innerHTML = `<p style="color: red;">渲染失败：${result.msg}</p>`;
        }
    } catch (error) {
        console.error('请求失败：', error);
        previewContainer.innerHTML = '<p style="color: red;">网络错误，无法连接后端服务</p>';
    }
});

// 监听编辑区输入事件
editor.addEventListener('input', renderMarkdown);

// 双向同步滚动
let isSyncing = false;
const syncScroll = (source, target) => {
    if (isSyncing) return;
    isSyncing = true;

    // 计算滚动比例
    const scrollRatio = source.scrollTop / (source.scrollHeight - source.clientHeight);
    // 同步目标滚动位置
    target.scrollTop = scrollRatio * (target.scrollHeight - target.clientHeight);

    setTimeout(() => {
        isSyncing = false;
    }, 100);
};

// 监听编辑区滚动
editor.addEventListener('scroll', () => {
    syncScroll(editor, previewContainer);
});

// 监听预览区滚动
previewContainer.addEventListener('scroll', () => {
    syncScroll(previewContainer, editor);
});

// 页面加载完成后初始化
window.addEventListener('DOMContentLoaded', () => {
    // 初始化示例内容
    editor.value = `# Markdown实时预览示例

## 基础语法
这是**加粗文本**，这是*斜体文本*，这是~~删除线文本~~。

### 列表
1. 有序列表第一项
2. 有序列表第二项
- 无序列表项
- 无序列表项

### 代码块
\`\`\`python
def hello_world():
    print("Hello Markdown!")
    # 代码高亮已生效
\`\`\`

### 数学公式
质能方程：$E=mc^2$

### 表格
| 姓名 | 年龄 | 职业 |
|------|------|------|
| 张三 | 25   | 工程师 |
| 李四 | 28   | 设计师 |
`;
    // 触发首次渲染
    renderMarkdown();
});
