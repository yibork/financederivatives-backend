// enable_new_company.js
document.addEventListener("DOMContentLoaded", function() {
    const companyNameSelect = document.getElementById("company-name-select");
    const newCompanyNameInput = document.getElementById("new-company-name");

    if (companyNameSelect && newCompanyNameInput) {
        companyNameSelect.addEventListener("change", function() {
            if (companyNameSelect.value === "other") {
                newCompanyNameInput.removeAttribute("disabled");
            } else {
                newCompanyNameInput.setAttribute("disabled", "disabled");
                newCompanyNameInput.value = "";
            }
        });
    }
});
