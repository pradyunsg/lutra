import debounceAnimationFrame from "debounce-animation-frame";

export class ScrollObserver {
  show_page_title_offset: number;
  back_to_top_offset: number;
  lastScrollTop = window.scrollY || document.documentElement.scrollTop;
  links: Array<HTMLAnchorElement>;
  sections: Array<HTMLElement>;

  constructor(
    back_to_top_offset: number = 64,
    show_page_title_offset: number = 128
  ) {
    this.back_to_top_offset = back_to_top_offset;
    this.show_page_title_offset = show_page_title_offset;
    this.links = Array.from(
      document.querySelectorAll<HTMLAnchorElement>(
        ".toc-container ul a[href^='#']:not([href='#'])"
      )
    );
    this.sections = Array.from(document.getElementsByTagName("section"));
  }

  observe() {
    window.addEventListener(
      "scroll",
      debounceAnimationFrame(this.callback.bind(this)),
      { passive: true }
    );

    // Trigger it once, to populate the initial state.
    this.callback();
  }

  private callback() {
    const position = window.scrollY || document.documentElement.scrollTop;
    this.updateActiveTocAnchor(position);
    this.updatePageTitleAndBackToTop(position);
    this.lastScrollTop = position;
  }

  private updateActiveTocAnchor(position: number) {
    const content = document.getElementById("lutra-main-content")!;
    const sectionMargin = content.offsetTop;

    // Clear existing links.
    this.links.forEach((anchor) => {
      anchor.classList.remove("previous");
      anchor.classList.remove("current");
    });

    // Locate the first section (from the end) that is visible.
    let current = [...this.sections].reverse().find((section) => {
      return position >= section.offsetTop - sectionMargin;
    });
    if (current === undefined) {
      console.debug("[ScrollObserver] No relevant section is visible.");
      return;
    }

    const currentLinkIndex = this.links.findIndex((anchor) => {
      return anchor.hash === `#${current?.id}`;
    });
    if (currentLinkIndex === -1) {
      console.debug("[ScrollObserver] No link found for section:", current);
      return;
    }

    // Highlight the current link and mark the previous ones.
    console.debug("[ScrollObserver] Current section:", current);
    console.debug("[ScrollObserver] Current link index:", currentLinkIndex);
    this.links[currentLinkIndex]?.classList.add("current");
    this.links.slice(0, currentLinkIndex).forEach((anchor) => {
      anchor.classList.add("previous");
    });
  }

  private updatePageTitleAndBackToTop(position: number) {
    if (position > this.show_page_title_offset) {
      document.documentElement.classList.add("show-page-title");
      if (position < this.lastScrollTop) {
        document.documentElement.classList.add("show-back-to-top");
      } else if (position > this.lastScrollTop) {
        document.documentElement.classList.remove("show-back-to-top");
      }
    } else {
      document.documentElement.classList.remove("show-page-title");
    }
    if (position < this.back_to_top_offset) {
      document.documentElement.classList.remove("show-back-to-top");
    }
  }
}
