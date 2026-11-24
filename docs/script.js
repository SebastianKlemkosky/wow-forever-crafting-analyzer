// =========================
// Profession Mapping
// =========================

const PROFESSIONS = {
    164: "Blacksmithing",
    165: "Leatherworking",
    171: "Alchemy",
    182: "Herbalism",
    185: "Cooking",
    186: "Mining",
    197: "Tailoring",
    202: "Engineering",
    333: "Enchanting",
    356: "Fishing",
    393: "Skinning",
    129: "First Aid",
    40: "Poisons"
};

let recipes = [];
let marketRequest = null;

// =========================
// Market Elements
// =========================

const regionFilter = document.getElementById("region");
const rulesetFilter = document.getElementById("ruleset");
const factionFilter = document.getElementById("faction");
const marketInfo = document.getElementById("market-info");
const lastUpdated = document.getElementById("last-updated");
// =========================
// Recipe Filter Elements
// =========================

const professionFilter = document.getElementById("profession");
const searchFilter = document.getElementById("recipe-search");
const skillFilter = document.getElementById("skill-level");
const sortOrder = document.getElementById("sort-order");
const profitableOnly = document.getElementById("profitable-only");
const includeUnknown = document.getElementById("include-unknown");
const resetButton = document.getElementById("reset-filters");

// =========================
// Results Elements
// =========================

const tableBody = document.getElementById("recipe-table-body");
const resultsCount = document.getElementById("results-count");
const errorMessage = document.getElementById("error-message");

// =========================
// Load Market Data
// =========================

async function loadMarketData() {

    // Cancel any previous market request
    if (marketRequest) {
        marketRequest.abort();
    }

    const controller = new AbortController();
    marketRequest = controller;

    const region = regionFilter.value;
    const ruleset = rulesetFilter.value;
    const faction = factionFilter.value;

    const path = `./markets/${region}/${ruleset}/${faction}.json`;

    updateMarketInfo();
    lastUpdated.textContent = "Last Updated: Loading...";
    recipes = [];
    tableBody.replaceChildren();

    resultsCount.textContent = "Loading market data...";
    errorMessage.hidden = true;

    updateSummary();

    try {
        const response = await fetch(path, {
            signal: controller.signal,
            cache: "no-cache"
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${path}`);
        }

        const data = await response.json();

        // Ignore outdated requests
        if (marketRequest !== controller) {
            return;
        }

        recipes = Array.isArray(data) ? data : data.recipes;

        if (!Array.isArray(recipes)) {
            throw new Error("Invalid market data format.");
        }

        updateTimestamp(data.last_updated);

        updateSummary();

        marketRequest = null;

        applyFilters();

    } catch (error) {

        if (
            error.name === "AbortError" ||
            marketRequest !== controller
        ) {
            return;
        }

        console.error(error);

        errorMessage.textContent =
            `Market data unavailable: ${error.message}`;

        errorMessage.hidden = false;
        resultsCount.textContent = "Market unavailable.";
        lastUpdated.textContent = "Last Updated: Unavailable";
    } finally {

        if (marketRequest === controller) {
            marketRequest = null;
        }
    }
}

// =========================
// Update Market Information
// =========================

function updateMarketInfo() {

    const region =
        regionFilter.selectedOptions[0].textContent;

    const ruleset =
        rulesetFilter.selectedOptions[0].textContent;

    const faction =
        factionFilter.selectedOptions[0].textContent;

    marketInfo.textContent =
        `${region} | ${ruleset} | ${faction}`;
}


// =========================
// Market Timestamp
// =========================

function updateTimestamp(timestamp) {

    if (!timestamp || Number.isNaN(Date.parse(timestamp))) {
        lastUpdated.textContent = "Last Updated: Unknown";
        return;
    }

    const date = new Date(timestamp);

    const formatted = date.toLocaleString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "numeric",
        minute: "2-digit",
        timeZoneName: "short"
    });

    lastUpdated.textContent = `Last Updated: ${formatted}`;
}


// =========================
// Currency Formatting
// =========================

function formatCurrency(copper, showSign = false) {

    if (copper === null || copper === undefined) {
        return "Unavailable";
    }

    const sign = copper < 0 ? "-" :
        copper > 0 && showSign ? "+" : "";

    copper = Math.abs(copper);

    const gold = Math.floor(copper / 10000);
    const silver = Math.floor((copper % 10000) / 100);
    const remaining = copper % 100;

    return `
        <span>${sign}</span>
        <span class="currency-gold">${gold}g</span>
        <span class="currency-silver">${silver}s</span>
        <span class="currency-copper">${remaining}c</span>
    `;
}

// =========================
// Market Summary
// =========================

function updateSummary() {

    const profitable = recipes.filter(
        recipe => recipe.profit > 0
    );

    const unprofitable = recipes.filter(
        recipe => recipe.profit < 0
    );

    document.getElementById("total-recipes").textContent =
        recipes.length.toLocaleString();

    document.getElementById("profitable-recipes").textContent =
        profitable.length.toLocaleString();

    document.getElementById("unprofitable-recipes").textContent =
        unprofitable.length.toLocaleString();
}

// =========================
// Filter Recipes
// =========================

function applyFilters() {

    // Do not filter while loading or when unavailable
    if (marketRequest || !errorMessage.hidden) {
        return;
    }

    let results = [...recipes];

    const profession = professionFilter.value;
    const search = searchFilter.value.trim().toLowerCase();
    const skill = skillFilter.value;

    // Filter by profession
    if (profession !== "all") {

        results = results.filter(
            recipe => recipe.profession === Number(profession)
        );
    }

    // Filter by recipe name
    if (search !== "") {

        results = results.filter(
            recipe => recipe.name.toLowerCase().includes(search)
        );
    }

    // Filter by skill requirement
    results = results.filter(recipe => {

        if (recipe.required_skill === null) {
            return includeUnknown.checked;
        }

        if (skill === "") {
            return true;
        }

        return recipe.required_skill <= Number(skill);
    });

    // Filter profitable recipes
    if (profitableOnly.checked) {

        results = results.filter(
            recipe => recipe.profit > 0
        );
    }

    sortRecipes(results);
    displayRecipes(results);
}

// =========================
// Sort Recipes
// =========================

function sortRecipes(results) {

    switch (sortOrder.value) {

        case "profit-desc":
            results.sort((a, b) => b.profit - a.profit);
            break;

        case "profit-asc":
            results.sort((a, b) => a.profit - b.profit);
            break;

        case "name-asc":
            results.sort((a, b) =>
                a.name.localeCompare(b.name)
            );
            break;

        case "name-desc":
            results.sort((a, b) =>
                b.name.localeCompare(a.name)
            );
            break;

        case "skill-asc":
            results.sort((a, b) =>
                (a.required_skill ?? Infinity) -
                (b.required_skill ?? Infinity)
            );
            break;

        case "skill-desc":
            results.sort((a, b) =>
                (b.required_skill ?? -Infinity) -
                (a.required_skill ?? -Infinity)
            );
            break;
    }
}


// =========================
// Material Cost Table
// =========================

function createMaterialsTable(recipe) {

    const section = document.createElement("section");
    section.className = "recipe-materials";

    const heading = document.createElement("h3");
    heading.textContent = "Required Materials";
    section.appendChild(heading);

    const table = document.createElement("table");
    table.className = "materials-table";

    table.innerHTML = `
        <thead>
            <tr>
                <th>Material</th>
                <th>Quantity</th>
                <th>Unit Price</th>
                <th>Total Cost</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const body = table.querySelector("tbody");

    for (const material of recipe.materials ?? []) {

        const row = body.insertRow();

        const nameCell = row.insertCell();

        nameCell.appendChild(
            createItemDisplay(
                material.name,
                material.url,
                material.icon_url
            )
        );

        const quantityCell = row.insertCell();
        quantityCell.textContent = material.quantity;

        const priceCell = row.insertCell();
        priceCell.innerHTML = formatCurrency(material.unit_price);

        const totalCell = row.insertCell();
        totalCell.innerHTML = formatCurrency(material.total_cost);
    }

    const footer = table.createTFoot();
    const totalRow = footer.insertRow();

    const labelCell = totalRow.insertCell();
    labelCell.colSpan = 3;
    labelCell.textContent = "Total Material Cost";

    const totalCell = totalRow.insertCell();
    totalCell.innerHTML = formatCurrency(recipe.material_cost);

    section.appendChild(table);

    return section;
}

function createAcquisitionsTable(recipe) {
    const section = document.createElement("section");
    section.className = "recipe-materials";

    const heading = document.createElement("h3");
    heading.textContent = "Recipe Acquisition";
    section.appendChild(heading);

    if (!recipe.acquisitions?.length) {
        const message = document.createElement("p");
        message.textContent = "No recipe acquisition data available.";
        section.appendChild(message);

        return section;
    }

    const table = document.createElement("table");
    table.className = "materials-table";

    table.innerHTML = `
        <thead>
            <tr>
                <th>Recipe Item</th>
                <th>Auction House Price</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const body = table.querySelector("tbody");

    for (const acquisition of recipe.acquisitions) {
        const row = body.insertRow();

        const nameCell = row.insertCell();

        nameCell.appendChild(
            createItemDisplay(
                acquisition.name ?? `Item #${acquisition.item_id}`,
                acquisition.url,
                acquisition.icon_url
            )
        );

        const priceCell = row.insertCell();
        priceCell.innerHTML = formatCurrency(acquisition.price);
    }

    section.appendChild(table);

    return section;
}

// =========================
// Recipe Details
// =========================

function createRecipeDetails(recipe) {

    const container = document.createElement("div");
    container.className = "recipe-details";

    // Database Links
    const links = document.createElement("div");
    links.className = "recipe-links";

    links.appendChild(
        createItemLink("View Crafted Item", recipe.product?.url)
    );

    links.appendChild(
        createItemLink("View Recipe", recipe.recipe_url)
    );

    container.appendChild(links);

    // Financial Summary
    const summary = document.createElement("div");
    summary.className = "recipe-financial-summary";

    summary.innerHTML = `
        <div>
            <span>Product Value</span>
            <strong>
                ${formatCurrency(recipe.product?.total_value)}
            </strong>
        </div>

        <div>
            <span>Material Cost</span>
            <strong>
                ${formatCurrency(recipe.material_cost)}
            </strong>
        </div>

        <div>
            <span>Profit per Craft</span>
            <strong>
                ${formatCurrency(recipe.profit, true)}
            </strong>
        </div>

        <div>
            <span>Return on Investment</span>
            <strong>
                ${recipe.roi != null
                    ? `${Number(recipe.roi).toFixed(2)}%`
                    : "Unavailable"}
            </strong>
        </div>

        <div>
            <span>Recipe Acquisition Cost</span>
            <strong>
                ${formatCurrency(recipe.acquisition_cost)}
            </strong>
        </div>

        <div>
            <span>Crafts to Break Even</span>
            <strong>
                ${recipe.break_even_crafts != null
                    ? recipe.break_even_crafts
                    : "Unavailable"}
            </strong>
        </div>
    `;

    container.appendChild(summary);

    // Required Materials
    container.appendChild(
        createMaterialsTable(recipe)
    );

    // Recipe Acquisition
    container.appendChild(
        createAcquisitionsTable(recipe)
    );

    return container;
}

// =========================
// Database Links
// =========================

function createItemLink(name, url) {

    if (!url) {
        const text = document.createElement("span");
        text.textContent = name;
        return text;
    }

    const link = document.createElement("a");

    link.textContent = name;
    link.href = url;
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.className = "item-link";

    return link;
}


function createItemDisplay(name, url, iconUrl) {
    const container = document.createElement("div");
    container.className = "item-display";

    if (iconUrl) {
        const icon = document.createElement("img");

        icon.src = iconUrl;
        icon.alt = "";
        icon.className = "item-icon";
        icon.loading = "lazy";

        icon.onerror = () => icon.remove();

        container.appendChild(icon);
    }

    container.appendChild(createItemLink(name, url));

    return container;
}

// =========================
// Display Recipes
// =========================

function displayRecipes(results) {

    tableBody.replaceChildren();

    resultsCount.textContent =
        `Showing ${results.length} of ${recipes.length} recipes`;

    if (results.length === 0) {

        const row = tableBody.insertRow();
        const cell = row.insertCell();

        cell.colSpan = 4;
        cell.textContent = "No matching recipes found.";

        return;
    }

    for (const recipe of results) {

        const row = tableBody.insertRow();


                // Recipe Name and Icon
        const nameCell = row.insertCell();

        const recipeContainer = document.createElement("button");
        recipeContainer.type = "button";
        recipeContainer.className = "recipe-name recipe-toggle";
        recipeContainer.setAttribute("aria-expanded", "false");

        if (recipe.icon_url) {
            const icon = document.createElement("img");
            icon.src = recipe.icon_url;
            icon.alt = "";
            icon.className = "recipe-icon";
            icon.loading = "lazy";

            icon.addEventListener("error", () => {
                icon.remove();
            });

            recipeContainer.appendChild(icon);
        }

        const name = document.createElement("span");
        name.textContent = recipe.name;

        recipeContainer.appendChild(name);

        const arrow = document.createElement("span");
        arrow.className = "expand-arrow";
        arrow.textContent = "▸";

        recipeContainer.appendChild(arrow);

        nameCell.appendChild(recipeContainer);

        // Profession
        const professionCell = row.insertCell();

        professionCell.textContent =
            PROFESSIONS[recipe.profession] ?? "Unknown";

        // Required Skill
        const skillCell = row.insertCell();

        skillCell.textContent =
            recipe.required_skill ?? "Unknown";

        if (recipe.required_skill === null) {
            skillCell.classList.add("skill-unknown");
        }

        // Profit
        const profitCell = row.insertCell();

        profitCell.innerHTML = formatCurrency(recipe.profit, true);

        if (recipe.profit > 0) {

            profitCell.classList.add("profit-positive");

        } else if (recipe.profit < 0) {

            profitCell.classList.add("profit-negative");

        } else {

            profitCell.classList.add("profit-neutral");
        }


        // Expandable Recipe Details
        let detailsRow = null;

        recipeContainer.addEventListener("click", () => {

            if (detailsRow !== null) {
                detailsRow.remove();
                detailsRow = null;

                arrow.textContent = "▸";

                recipeContainer.setAttribute(
                    "aria-expanded", "false"
                );

                return;
            }

            detailsRow = document.createElement("tr");
            detailsRow.className = "recipe-details-row";

            const detailsCell = detailsRow.insertCell();
            detailsCell.colSpan = 4;

            detailsCell.appendChild(
                createRecipeDetails(recipe)
            );

            row.after(detailsRow);

            arrow.textContent = "▾";

            recipeContainer.setAttribute(
                "aria-expanded", "true"
            );
        });

    }
}

// =========================
// Reset Recipe Filters
// =========================

function resetFilters() {

    professionFilter.value = "all";
    searchFilter.value = "";
    skillFilter.value = "";
    sortOrder.value = "profit-desc";

    profitableOnly.checked = false;
    includeUnknown.checked = true;

    applyFilters();
}

// =========================
// Market Event Listeners
// =========================

regionFilter.addEventListener("change", loadMarketData);
rulesetFilter.addEventListener("change", loadMarketData);
factionFilter.addEventListener("change", loadMarketData);
// =========================
// Recipe Event Listeners
// =========================

professionFilter.addEventListener("change", applyFilters);
searchFilter.addEventListener("input", applyFilters);
skillFilter.addEventListener("input", applyFilters);
sortOrder.addEventListener("change", applyFilters);
profitableOnly.addEventListener("change", applyFilters);
includeUnknown.addEventListener("change", applyFilters);

resetButton.addEventListener("click", resetFilters);

// =========================
// Initialize Application
// =========================

loadMarketData();