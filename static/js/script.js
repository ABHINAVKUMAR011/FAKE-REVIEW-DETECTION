document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".container");
    const fileInput = document.querySelector('input[type="file"]');
    const fileName = document.getElementById("file-name");

    if (container) {
        window.requestAnimationFrame(function () {
            container.classList.add("is-ready");
        });
    }

    if (fileInput) {
        fileInput.addEventListener("change", function () {
            if (!fileName) {
                return;
            }

            if (this.files.length > 0) {
                fileName.textContent = "Selected: " + this.files[0].name;
            } else {
                fileName.textContent = "No file selected";
            }
        });
    }
});
