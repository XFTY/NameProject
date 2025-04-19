
// 打字动画逻辑
const titles = [
    "让我们一同进步",
    "高效、便捷的点名工具",
    "智能点名解决方案",
    "快速课堂管理工具",
    "教师必备点名工具"
];

let currentIndex = 0;
let isDeleting = false; // 是否正在删除
let text = ''; // 当前显示的文本
let speed = 100; // 打字速度（毫秒）
let showDuration = 5000; // 每个标题展示5秒

function type() {
    const titleElement = document.getElementById('dynamicTitle');
    const fullText = titles[currentIndex];

    if (!isDeleting && text.length < fullText.length) {
        // 添加字符
        text += fullText.charAt(text.length);
        titleElement.textContent = text;
        speed = 100; // 正常打字速度
    } else if (isDeleting && text.length > 0) {
        // 删除字符
        text = text.slice(0, text.length - 1);
        titleElement.textContent = text;
        speed = 50; // 快速删除速度
    } else if (text.length === 0) {
        // 删除完成后切换到下一个标题
        isDeleting = false;
        currentIndex = (currentIndex + 1) % titles.length;
    } else if (text.length === fullText.length) {
        // 打印完成后等待5秒再开始删除
        isDeleting = true;
        speed = showDuration; // 设置为展示时间
    }

    setTimeout(type, speed);
}

// 弹窗显示逻辑
function openDownloadModal() {
    const modal = document.getElementById('downloadModal');
    if (modal) {
        modal.style.display = 'block'; // 显示弹窗
    }
}

function closeDownloadModal() {
    const modal = document.getElementById('downloadModal');
    if (modal) {
        modal.style.display = 'none'; // 隐藏弹窗
    }
}

type(); // 开始打字动画
