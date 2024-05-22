// static/js/add_company.js
document.addEventListener("DOMContentLoaded", function () {
    var selectElement = document.querySelector(".add-company-select");
    if (selectElement) {
        var addButton = document.createElement("a");
        addButton.href = "/add-company/";
        addButton.textContent = "Add Company";
        addButton.className = "button";

        selectElement.parentNode.appendChild(addButton);
    }
});
