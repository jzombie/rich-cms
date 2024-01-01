document.addEventListener("DOMContentLoaded", function () {
  var button = document.getElementById("menu-toggle-button");
  var tocContainer = document.querySelector(".toc-container");

  if (button && tocContainer) {
    // Hide the button by default
    button.style.display = "none";

    button.addEventListener("click", function () {
      tocContainer.style.display =
        tocContainer.style.display === "none" ? "block" : "none";

      // Scroll to top if TOC container is shown
      if (tocContainer.style.display === "block") {
        window.scrollTo(0, 0);
      }
    });

    // Show the button when JavaScript is enabled
    button.style.display = "block";

    // Hide the TOC by default on mobile
    if (window.innerWidth <= 768) {
      tocContainer.style.display = "none";
    }
  }
});
