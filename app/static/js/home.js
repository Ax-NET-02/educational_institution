document.addEventListener("DOMContentLoaded", function () {
    // 显示加载遮罩层
    showLoadingOverlay();

    // 模拟异步加载，您可以替换成实际加载数据的操作
    setTimeout(function () {
        // 隐藏加载遮罩层
        hideLoadingOverlay();

        // 显示主页内容
        document.getElementById("main-content").style.display = "block";
    }, 1); // 模拟加载时间为2秒
});

function showLoadingOverlay() {
    document.getElementById("loading-overlay").style.display = "flex";
}

function hideLoadingOverlay() {
    document.getElementById("loading-overlay").style.display = "none";
}
