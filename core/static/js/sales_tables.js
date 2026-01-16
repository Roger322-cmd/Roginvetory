// sales_tables.js
// Currency switch, search, client-side sort for sales records.

document.addEventListener("DOMContentLoaded", function () {
    const currencySelect = document.getElementById("currency-switcher");
    const searchInput = document.getElementById("sales-search");
    const table = document.getElementById("sales-table");
    if (!table) return;

    const tbody = table.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));

    rows.forEach(row => {
        row.querySelectorAll("td").forEach(cell => {
            cell.dataset.original = cell.innerText;
        });
    });

    function updateCurrency() {
        if (!currencySelect) return;
        const rate = parseFloat(currencySelect.value || "1");
        const symbol = currencySelect.selectedOptions[0].dataset.symbol || "";
        document.querySelectorAll(".money-field").forEach(cell => {
            const base = parseFloat(cell.dataset.base || "0");
            cell.innerText = `${symbol} ${ (base * rate).toFixed(2) }`;
        });
     // Update totals
        document.querySelectorAll(".money-total").forEach(el => {
            const base = parseFloat(el.dataset.base || "0");
            el.innerText = `${symbol} ${ (base * rate).toFixed(2) }`;
        });
       
    }

    function filterTable() {
        const term = (searchInput ? searchInput.value : "").toLowerCase().trim();
        rows.forEach(row => {
            const rowText = row.innerText.toLowerCase();
            row.style.display = (!term || rowText.includes(term)) ? "" : "none";
        });
    }

    if (searchInput) {
        searchInput.addEventListener("input", filterTable);
        searchInput.addEventListener("keyup", e => {
            if (e.key === "Enter") filterTable();
        });
    }

    const headers = table.querySelectorAll("thead th[data-sort]");
    const sortState = {};

    headers.forEach(header => {
        header.style.cursor = "pointer";
        header.addEventListener("click", function () {
            const index = Array.from(header.parentNode.children).indexOf(header);
            const field = header.dataset.sort;
            const direction = sortState[field] === "asc" ? "desc" : "asc";
            sortState[field] = direction;

            const sorted = rows.slice().sort((a, b) => {
                const cellA = a.children[index];
                const cellB = b.children[index];
                const valA = (cellA.dataset.original || cellA.innerText).trim();
                const valB = (cellB.dataset.original || cellB.innerText).trim();
                const numA = parseFloat(valA.replace(/,/g, ""));
                const numB = parseFloat(valB.replace(/,/g, ""));
                let comp;
                if (!isNaN(numA) && !isNaN(numB)) comp = numA - numB;
                else comp = valA.localeCompare(valB);
                return direction === "asc" ? comp : -comp;
            });

            tbody.innerHTML = "";
            sorted.forEach(r => tbody.appendChild(r));
            filterTable();
            updateCurrency();
        });
    });

    updateCurrency();
    filterTable();
});
document.querySelectorAll(".money-field").forEach(cell => {
  const base = parseFloat(cell.dataset.base || "0");
  cell.innerText = `${symbol} ${ (base * rate).toFixed(2) }`;
});
