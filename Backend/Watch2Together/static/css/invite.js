document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modal");
    const openModalButton = document.getElementById("openModalButton");
    const closeModalButton = document.getElementById("closeModalButton");

    openModalButton.addEventListener("click", function () {
        modal.style.display = "block";
    });

    closeModalButton.addEventListener("click", function () {
        modal.style.display = "none";
    });

    window.addEventListener("click", function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    });
});
