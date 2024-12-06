const reportsByStage = document.getElementById("reportsByStage");
const reportsByPlugin = document.getElementById("reportsByPlugin");
const dropdown = document.getElementById("dropdown");

const toggleReports = () => {
    if (dropdown.value == "reportsByStage") {
        reportsByStage.style.display = "flex";
        reportsByPlugin.style.display = "none";
    } else if (dropdown.value == "reportsByPlugin") {
        reportsByStage.style.display = "none";
        reportsByPlugin.style.display = "flex";
    }
};
