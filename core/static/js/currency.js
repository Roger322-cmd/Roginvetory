document.addEventListener("DOMContentLoaded", function () {
  const currencySelect = document.getElementById("currency-switcher");
  if (!currencySelect) return;

  // Base currency is KES
  const baseCurrency = 'KES';

  // Fetch current exchange rates
  async function fetchRates() {
    try {
      const response = await fetch(`https://api.exchangerate-api.com/v4/latest/${baseCurrency}`);
      const data = await response.json();
      const rates = data.rates;

      // Update select options with current rates
      const usdOption = currencySelect.querySelector('option[data-symbol="USD"]');
      const eurOption = currencySelect.querySelector('option[data-symbol="EUR"]');

      if (usdOption) usdOption.value = rates.USD;
      if (eurOption) eurOption.value = rates.EUR;

      // Apply current selection
      updateCurrency();
    } catch (error) {
      console.error('Failed to fetch exchange rates:', error);
      // Fallback to static rates if API fails
      updateCurrency();
    }
  }

  // Update all money fields
  function updateCurrency() {
    const rate = parseFloat(currencySelect.value || "1");
    const symbol = currencySelect.selectedOptions[0].dataset.symbol || "KES";

    // Update money fields
    document.querySelectorAll('.money-field').forEach(el => {
      const original = parseFloat(el.dataset.original || el.textContent.replace(/[^\d.-]/g, ''));
      if (!isNaN(original)) {
        el.textContent = `${symbol} ${(original * rate).toFixed(4)}`;
      }
    });

    // Update charts if on dashboard
    updateCharts(rate);

    // Store selected currency in localStorage
    localStorage.setItem('selectedCurrency', currencySelect.value);
    localStorage.setItem('selectedSymbol', symbol);
  }

  // Update charts (for dashboard)
  function updateCharts(rate) {
    // This will be called if charts exist
    if (typeof updateIncomeCharts === 'function') {
      updateIncomeCharts(rate);
    }
  }

  // Load saved currency
  const savedCurrency = localStorage.getItem('selectedCurrency');
  if (savedCurrency) {
    currencySelect.value = savedCurrency;
  }

  // Fetch rates and update
  fetchRates();

  // Listen for changes
  currencySelect.addEventListener("change", updateCurrency);
});