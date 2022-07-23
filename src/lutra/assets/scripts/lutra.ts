import "instant.page";
import { ScrollObserver } from "./scrollspy";

////////////////////////////////////////////////////////////////////////////////
// Scroll Handling
////////////////////////////////////////////////////////////////////////////////
function setupScrollHandler() {
  if (document.getElementById("lutra-main-content") === null) {
    console.debug("No main content, skipping scroll handler.");
    return;
  }
  const observer = new ScrollObserver();
  observer.observe();
}

////////////////////////////////////////////////////////////////////////////////
// Theme Toggle
////////////////////////////////////////////////////////////////////////////////
enum Theme {
  LIGHT = "light",
  DARK = "dark",
  AUTO = "auto",
}

function setTheme(mode: Theme, class_to_set: Theme.DARK | Theme.LIGHT) {
  // TODO: Tooltips.

  // Sanitize the incoming values.
  if (!(<any>Object).values(Theme).includes(mode)) {
    console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
    mode = Theme.AUTO;
  }
  if (![Theme.LIGHT, Theme.DARK].includes(class_to_set)) {
    console.error(
      `Got invalid theme class: ${class_to_set}. Resetting to light.`
    );
    class_to_set = Theme.LIGHT;
  }

  document.body.dataset.theme = mode;
  localStorage.setItem("theme", mode);
  if (class_to_set == Theme.LIGHT) {
    document.documentElement.classList.remove("dark");
  } else {
    document.documentElement.classList.add("dark");
  }
  console.debug(`Changed to ${mode} mode (${class_to_set}).`);
}

function cycleThemeOnce() {
  const currentTheme = localStorage.getItem("theme") || "auto";
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  if (prefersDark) {
    // Auto (dark) -> Light -> Dark
    if (currentTheme === "auto") {
      setTheme(Theme.LIGHT, Theme.LIGHT);
    } else if (currentTheme == Theme.LIGHT) {
      setTheme(Theme.DARK, Theme.DARK);
    } else {
      setTheme(Theme.AUTO, Theme.DARK);
    }
  } else {
    // Auto (light) -> Dark -> Light
    if (currentTheme === Theme.AUTO) {
      setTheme(Theme.DARK, Theme.DARK);
    } else if (currentTheme == Theme.DARK) {
      setTheme(Theme.LIGHT, Theme.LIGHT);
    } else {
      setTheme(Theme.AUTO, Theme.LIGHT);
    }
  }
}

function setupTheme() {
  // Attach event handlers for toggling themes.
  const buttons = document.getElementsByClassName("theme-toggle");
  Array.from(buttons).forEach((btn) => {
    btn.addEventListener("click", cycleThemeOnce);
  });
  // Watch for theme changes and update accordingly.
  window
    .matchMedia("(prefers-color-scheme: dark)")
    .addEventListener("change", (e) => {
      const _currentTheme = localStorage.getItem("theme") || "auto";
      const currentTheme: Theme = _currentTheme as Theme;
      if (currentTheme === Theme.AUTO) {
        setTheme(Theme.AUTO, e.matches ? Theme.DARK : Theme.LIGHT);
      } else {
        // This is necessary to update the tooltips.
        setTheme(currentTheme, currentTheme);
      }
    });
}

////////////////////////////////////////////////////////////////////////////////
// Search
////////////////////////////////////////////////////////////////////////////////
interface HeaderSearchForm extends HTMLFormElement {
  q: HTMLInputElement;
}

function setupHeaderSearch() {
  const search_link = document.getElementById("lutra-header-search-link");
  if (search_link === null) {
    console.debug("No search link, skipping header search.");
    return;
  }
  const search_container = document.getElementById("lutra-header-search-form")!;
  const search_overlay = document.getElementById(
    "lutra-header-search-overlay"
  )!;

  function searchDeactivate() {
    search_container.classList.remove("active");
    search_overlay.removeEventListener("click", searchDeactivate);
  }

  function searchDeactivateOnEscape(e: KeyboardEvent) {
    if (e.key === "Escape") {
      searchDeactivate();
      window.removeEventListener("keydown", searchDeactivateOnEscape, true);
    }
  }

  search_overlay.addEventListener("click", searchDeactivate);
  search_link.addEventListener("click", (e) => {
    e.preventDefault();
    search_container.classList.add("active");

    const search_form = search_container.children[0] as HeaderSearchForm;
    search_form.q.focus();

    window.addEventListener("keydown", searchDeactivateOnEscape, true);
  });
}

////////////////////////////////////////////////////////////////////////////////
// Sidebar collapse
////////////////////////////////////////////////////////////////////////////////
function setupSidebarCollapse() {
  const button = document.getElementById("lutra-site-navigation-collapse-icon");
  if (button === null) {
    console.debug("No sidebar collapse button, skipping sidebar collapse.");
    return;
  }
  const container = document.getElementById("lutra-primary-sidebar-container")!;

  if (document.body.classList.contains("collapsed-site-navigation")) {
    container.setAttribute("aria-hidden", "true");
  }

  button.addEventListener("click", () => {
    console.debug("Clicked collapse.");
    if (document.body.classList.contains("collapsed-site-navigation")) {
      document.body.classList.remove("collapsed-site-navigation");
      document.body.classList.add("expanded-site-navigation");
      container.setAttribute("aria-hidden", "false");
      localStorage.setItem("collapsed", "false");
    } else {
      document.body.classList.remove("expanded-site-navigation");
      document.body.classList.add("collapsed-site-navigation");
      container.setAttribute("aria-hidden", "true");
      localStorage.setItem("collapsed", "true");
    }
    document.body.classList.add("animated");
  });
}

////////////////////////////////////////////////////////////////////////////////
// Main entrypoint
////////////////////////////////////////////////////////////////////////////////
function main() {
  document.documentElement.classList.remove("no-js");

  setupSidebarCollapse();
  setupTheme();
  setupScrollHandler();
  setupHeaderSearch();
}

document.addEventListener("DOMContentLoaded", main);
