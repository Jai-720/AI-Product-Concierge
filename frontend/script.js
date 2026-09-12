const queryInput = document.querySelector("#searchInput");
const form = document.querySelector("#user");
const results = document.querySelector("#results");
const resultCount = document.querySelector("#result-count");

function escapeHtml(value) {
    return String(value).replace(/[&<>'"]/g, (character) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "'": "&#39;",
        '"': "&quot;"
    }[character]));
}

function showMessage(title, message, icon = "!") {
    results.innerHTML = `
        <div class="empty-state">
            <span class="empty-icon" aria-hidden="true">${icon}</span>
            <h3>${title}</h3>
            <p>${message}</p>
        </div>`;
}

form.addEventListener("submit", async function (e) {
    e.preventDefault();
    const query = queryInput.value.trim();
    if (!query) {
        queryInput.focus();
        showMessage("Tell me what you need", "Add a product description to start a search.");
        return;
    }

    results.setAttribute("aria-busy", "true");
    resultCount.textContent = "Searching...";
    results.innerHTML = '<div class="loading-state" role="status">Finding your best matches<span class="loading-dots">...</span></div>';

    try {
        const response = await fetch("http://127.0.0.1:8000/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            throw new Error(`Search failed with status ${response.status}`);
        }

        const data = await response.json();
        resultCount.textContent = `${data.length} ${data.length === 1 ? "match" : "matches"}`;

        if (data.length === 0) {
            showMessage("No close matches yet", "Try adding a category, use case, or maximum budget to your request.");
            return;
        }

        results.innerHTML = data.map((product) => `
            <article class="product-card">
                <div class="product-image" aria-hidden="true">&#10022;</div>
                <div class="product-body">
                    <div class="product-meta">
                        <span class="category">${escapeHtml(product.category)}</span>
                        <span class="rating">Recommended</span>
                    </div>
                    <h3>Product ${escapeHtml(product.id)}</h3>
                    <p>A catalog match selected for your search.</p>
                    <div class="product-footer">
                        <span class="price">$${Number(product.price).toFixed(2)}</span>
                        <span class="product-tag">Available</span>
                    </div>
                </div>
            </article>`).join("");
    } catch (error) {
        resultCount.textContent = "Search unavailable";
        showMessage("We could not reach the concierge", "Make sure the FastAPI server is running, then try again.");
        console.error(error);
    } finally {
        results.setAttribute("aria-busy", "false");
    }
});


// 1. Clear the innerHTML of the 'results' div so old searches are wiped out.
// 2. Check if the 'data' array is empty (length === 0). If it is, display a "No products found" message in the div.
// 3. Loop over each item in the 'data' array using a for...of loop.
// 4. Inside the loop, build an HTML string using backticks (template literals) that creates a simple card (e.g., a <div> containing the item's category and price).
// 5. Append (+=) that HTML string to the innerHTML of the 'results' div.