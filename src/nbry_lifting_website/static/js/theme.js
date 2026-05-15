// Dark mode toggle functionality
// Detects system preference, stores user choice in localStorage,
// applies theme via data-theme attribute on <html>

(function initTheme() {
  const htmlElement = document.documentElement;
  const themeToggleButton = document.getElementById("theme-toggle");
  const STORAGE_KEY = "theme-preference";
  const DARK_THEME = "dark";
  const LIGHT_THEME = "light";

  // Get user's theme preference from localStorage or system preference
  function getThemePreference() {
    const stored = localStorage.getItem(STORAGE_KEY);

    if (stored) {
      return stored;
    }

    // Check system preference
    if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
      return DARK_THEME;
    }

    return LIGHT_THEME;
  }

  // Apply theme to HTML element
  function applyTheme(theme) {
    htmlElement.setAttribute("data-theme", theme);
    localStorage.setItem(STORAGE_KEY, theme);

    // Update button label based on current theme
    if (theme === DARK_THEME) {
      themeToggleButton.setAttribute("aria-label", "Switch to light mode");
      themeToggleButton.textContent = "☀️";
    } else {
      themeToggleButton.setAttribute("aria-label", "Switch to dark mode");
      themeToggleButton.textContent = "🌙";
    }
  }

  // Toggle between light and dark themes
  function toggleTheme() {
    const currentTheme = htmlElement.getAttribute("data-theme");
    const newTheme = currentTheme === DARK_THEME ? LIGHT_THEME : DARK_THEME;
    applyTheme(newTheme);
  }

  // Initialize theme on page load
  const initialTheme = getThemePreference();
  applyTheme(initialTheme);

  // Attach click handler to toggle button
  themeToggleButton.addEventListener("click", toggleTheme);

  // Listen for system preference changes
  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", (event) => {
      const newTheme = event.matches ? DARK_THEME : LIGHT_THEME;
      applyTheme(newTheme);
    });
})();
