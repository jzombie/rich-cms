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
  }
});
