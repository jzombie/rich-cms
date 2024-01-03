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
          if (
            heading.previousElementSibling &&
            heading.previousElementSibling.tagName.startsWith("H")
          ) {
            // Skip if the previous element is also a heading
            return;
          }

          heading.style.position = "relative";

          const link = document.createElement("a");
          link.href = `#${heading.id}`;
          link.className = "heading-link";

          // Add the Font Awesome link icon
          link.innerHTML = '<i class="fas fa-link"></i>';

          // Prepend link
          heading.insertBefore(link, heading.firstChild);
        });

        (() => {
          // Function to check if an element is in the viewport
          const isInViewport = (element) => {
            const rect = element.getBoundingClientRect();
            return rect.top >= 0 && rect.bottom <= window.innerHeight;
          };

          // Function to update the URL based on the currently visible heading
          const updateUrlBasedOnHeading = () => {
            // Check if the page is scrolled to the top
            if (window.scrollY === 0) {
              // Remove the anchor from the URL
              //
              // This also prevents an issue where if scrolling very fast to the top of the page, the hash could reference an older state
              history.replaceState(null, "", window.location.pathname);
              return;
            }

            for (const heading of headings) {
              if (isInViewport(heading)) {
                const anchorLink = `#${heading.id}`;
                // Update the URL without creating a new history entry
                history.replaceState(null, "", anchorLink);
                break;
              }
            }
          };

          // Add event listener for the scroll event
          window.addEventListener("scroll", updateUrlBasedOnHeading);

          // Initial URL update
          updateUrlBasedOnHeading();
        })();
      }
    })();
  }
});
