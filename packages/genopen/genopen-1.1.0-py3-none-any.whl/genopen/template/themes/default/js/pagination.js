const articles = document.querySelectorAll(".post");
const articlesPerPage = 4;
const maxVisibleButtons = 3;
let currentPage = 1;

function displayArticles() {
    const start = (currentPage - 1) * articlesPerPage;
    const end = start + articlesPerPage;

    articles.forEach((article, index) => {
        article.style.display = (index >= start && index < end) ? "flex" : "none";
    });

    renderPagination();
}

function renderPagination() {
    const totalPages = Math.ceil(articles.length / articlesPerPage);
    const paginationContainer = document.querySelector(".pagination");

    paginationContainer.innerHTML = "";

    if (totalPages <= 1) return;

    const prevButton = createButton("<", currentPage > 1, () => {
        if (currentPage > 1) {
            currentPage--;
            displayArticles();
        }
    });
    paginationContainer.appendChild(prevButton);

    const startPage = Math.max(1, currentPage - Math.floor(maxVisibleButtons / 2));
    const endPage = Math.min(totalPages, startPage + maxVisibleButtons - 1);

    const adjustedStartPage = Math.max(1, Math.min(startPage, totalPages - maxVisibleButtons + 1));

    for (let page = adjustedStartPage; page <= endPage; page++) {
        const isActive = page === currentPage;
        const pageButton = createButton(page, true, () => {
            currentPage = page;
            displayArticles();
        });
        if (isActive) pageButton.classList.add("active");
        paginationContainer.appendChild(pageButton);
    }

    if (adjustedStartPage > 1) {
        const dots = document.createElement("span");
        dots.textContent = "...";
        dots.style.margin = "0 0.5rem";
        paginationContainer.insertBefore(dots, paginationContainer.children[1]);
    }

    if (endPage < totalPages) {
        const dots = document.createElement("span");
        dots.textContent = "...";
        dots.style.margin = "0 0.5rem";
        paginationContainer.appendChild(dots);
    }

    const nextButton = createButton(">", currentPage < totalPages, () => {
        if (currentPage < totalPages) {
            currentPage++;
            displayArticles();
        }
    });
    paginationContainer.appendChild(nextButton);
}

function createButton(text, isEnabled, onClick) {
    const button = document.createElement("button");
    button.textContent = text;
    button.classList.add("pagination-button");
    if (!isEnabled) button.classList.add("disabled");
    if (isEnabled) button.addEventListener("click", onClick);
    return button;
}

document.addEventListener("DOMContentLoaded", displayArticles);
