import "instant.page";
// import VanillaScrollspy from "vanillajs-scrollspy";
// import scrollSpy from "@sidsbrmnn/scrollspy";

////////////////////////////////////////////////////////////////////////////////
// Scroll Handling
////////////////////////////////////////////////////////////////////////////////
var lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;
const SHOW_PAGE_TITLE_OFFSET = 128;
const GO_TO_TOP_OFFSET = 64;

function scrollHandler(position) {
  if (position > SHOW_PAGE_TITLE_OFFSET) {
    document.documentElement.classList.add("show-page-title");
    if (position < lastScrollTop) {
      document.documentElement.classList.add("show-back-to-top");
    } else if (position > lastScrollTop) {
      document.documentElement.classList.remove("show-back-to-top");
    }
  } else {
    document.documentElement.classList.remove("show-page-title");
  }
  if (position < GO_TO_TOP_OFFSET) {
    document.documentElement.classList.remove("show-back-to-top");
  }
  lastScrollTop = position;
}
////////////////////////////////////////////////////////////////////////////////
// Theme Toggle
////////////////////////////////////////////////////////////////////////////////
function setTheme(mode, class_to_set) {
  // TODO: Tooltips.
  if (mode !== "light" && mode !== "dark" && mode !== "auto") {
    console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
    mode = "auto";
  }
  if (class_to_set !== "light" && class_to_set !== "dark") {
    console.error(
      `Got invalid theme class: ${class_to_set}. Resetting to light.`
    );
    class_to_set = "light";
  }

  document.body.dataset.theme = mode;
  localStorage.setItem("theme", mode);
  if (class_to_set == "light") {
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
      setTheme("light", "light");
    } else if (currentTheme == "light") {
      setTheme("dark", "dark");
    } else {
      setTheme("auto", "dark");
    }
  } else {
    // Auto (light) -> Dark -> Light
    if (currentTheme === "auto") {
      setTheme("dark", "dark");
    } else if (currentTheme == "dark") {
      setTheme("light", "light");
    } else {
      setTheme("auto", "light");
    }
  }
}

////////////////////////////////////////////////////////////////////////////////
// Search
////////////////////////////////////////////////////////////////////////////////
function setupSearch() {
  const search_link = document.getElementById("lutra-header-search-link");
  const search_container = document.getElementById("lutra-header-search-form");
  const search_overlay = document.getElementById("lutra-header-search-overlay");

  search_link.addEventListener("click", (e) => {
    e.preventDefault();
    search_container.classList.add("active");
    search_container.children[0].q.focus();
  });

  search_overlay.addEventListener("click", () => {
    search_container.classList.remove("active");
  });
}

////////////////////////////////////////////////////////////////////////////////
// Setup
////////////////////////////////////////////////////////////////////////////////
function setupScrollHandler() {
  // Taken from https://developer.mozilla.org/en-US/docs/Web/API/Document/scroll_event
  var last_known_scroll_position = 0;
  var ticking = false;

  window.addEventListener("scroll", function (e) {
    last_known_scroll_position = window.scrollY;

    if (!ticking) {
      window.requestAnimationFrame(function () {
        scrollHandler(last_known_scroll_position);
        ticking = false;
      });

      ticking = true;
    }
  });
  window.scroll();

  const list = document.querySelector(".toc-container > ul > li > ul");
  console.log(list);

  // const scrollspy = VanillaScrollspy(list);
  // scrollspy.init();

  // scrollSpy(list, {
  //   offset: 100,
  //   activeClass: "active",
  // });
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
      const currentTheme = localStorage.getItem("theme") || "auto";
      if (currentTheme === "auto") {
        setTheme("auto", e.matches ? "dark" : "light");
      } else {
        // This is necessary to update the tooltips.
        setTheme(currentTheme, currentTheme);
      }
    });
}

function setupSidebarCollapse() {
  const button = document.getElementById("lutra-site-navigation-collapse-icon");
  const container = document.getElementById("lutra-primary-sidebar-container");

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

function setup() {
  setupSidebarCollapse();
  setupTheme();
  setupScrollHandler();
  setupSearch();
  // setupScrollSpy();
}

////////////////////////////////////////////////////////////////////////////////
// Main entrypoint
////////////////////////////////////////////////////////////////////////////////
function main() {
  document.body.parentNode.classList.remove("no-js");

  setup();
}

document.addEventListener("DOMContentLoaded", main);
