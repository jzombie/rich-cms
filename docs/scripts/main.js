document.addEventListener("DOMContentLoaded", function () {
  var button = document.getElementById("menu-toggle-button");
  var tocContainer = document.querySelector("nav.toc");

  if (button && tocContainer) {
    // Hide the button by default
    button.style.display = "none";

    (() => {
      const prevScrollPosition = { x: 0, y: 0 };

      button.addEventListener("click", function () {
        if (tocContainer.style.display != "block") {
          // Cache current position
          prevScrollPosition.x = window.scrollX;
          prevScrollPosition.y = window.scrollY;
        }

        tocContainer.style.display =
          tocContainer.style.display === "none" ? "block" : "none";

        if (tocContainer.style.display === "block") {
          // Scroll to top
          window.scrollTo(0, 0);
        } else {
          // Restore previous position
          window.scrollTo(prevScrollPosition.x, prevScrollPosition.y);
        }
      });
    })();

    // Show the button when JavaScript is enabled
    button.style.display = "block";

    (() => {
      function handleResize() {
        tocContainer.style.display =
          window.innerWidth <= 768 ? "none" : "block";
      }

      window.addEventListener("resize", handleResize);

      handleResize();
    })();

    // Article heading links
    (() => {
      const maxHeadingLevels = 10;

      const articles = document.getElementsByTagName("article");

      for (const article of articles) {
        const headings = [];
        for (let i = 1; i <= maxHeadingLevels; i++) {
          const levelHeadings = article.getElementsByTagName(`h${i}`);
          [...levelHeadings].forEach((heading) => headings.push(heading));
        }

        // Add the link element and set its attributes
        headings.forEach((heading) => {
          heading.style.position = "relative";

          const link = document.createElement("a");
          link.href = `#${heading.id}`;
          link.className = "heading-link";

          // Add the Font Awesome link icon
          link.innerHTML = '<i class="fas fa-link"></i>';

          // Prepend link
          heading.insertBefore(link, heading.firstChild);
        });
      }
    })();
  }
});
