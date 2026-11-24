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
            throw new Error("Market data unavailable.");
        }

        const data = await response.json();

        // Ignore outdated requests
        if (marketRequest !== controller) {
            return;
        }

        recipes = data;

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
            "Market data is unavailable for the selected market.";

        errorMessage.hidden = false;
        resultsCount.textContent = "Market unavailable.";

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
// Currency Formatting
// =========================

function formatCurrency(copper) {

    const sign = copper < 0 ? "-" : copper > 0 ? "+" : "";

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

        // Recipe Name
        const nameCell = row.insertCell();
        nameCell.textContent = recipe.name;

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
        
        profitCell.innerHTML = formatCurrency(recipe.profit);

        if (recipe.profit > 0) {

            profitCell.classList.add("profit-positive");

        } else if (recipe.profit < 0) {

            profitCell.classList.add("profit-negative");

        } else {

            profitCell.classList.add("profit-neutral");
        }
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