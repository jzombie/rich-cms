class RichCMS {
  static get isFullScreenSupported() {
    return (
      document.fullscreenEnabled ||
      document.webkitFullscreenEnabled ||
      document.mozFullScreenEnabled ||
      document.msFullscreenEnabled
    );
  }

  static get isFullScreen() {
    return (
      document.fullscreenElement ||
      document.webkitFullscreenElement ||
      document.mozFullScreenElement ||
      document.msFullscreenElement
    );
  }

  static enterFullScreen(element = document.documentElement) {
    if (element.requestFullscreen) {
      element.requestFullscreen();
    } else if (element.webkitRequestFullscreen) {
      element.webkitRequestFullscreen();
    } else if (element.mozRequestFullScreen) {
      element.mozRequestFullScreen();
    } else if (element.msRequestFullscreen) {
      element.msRequestFullscreen();
    }
  }

  static exitFullScreen() {
    if (document.exitFullscreen) {
      document.exitFullscreen();
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen();
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen();
    } else if (document.msExitFullscreen) {
      document.msExitFullscreen();
    }
  }

  static toggleFullScreen(element = document.documentElement) {
    if (RichCMS.isFullScreen) {
      RichCMS.exitFullScreen();
    } else {
      RichCMS.enterFullScreen(element);
    }
  }
}

document.addEventListener("DOMContentLoaded", function () {
  // Display js-only elements
  (() => {
    [...document.getElementsByClassName("js-only")].forEach(
      (element) => (element.style.display = "block")
    );
  })();

  // Full-screen toggle binding
  (() => {
    const buttons = document.getElementsByClassName("full-screen-toggle");

    // Function to create and update the fullscreen icon dynamically
    async function updateFullscreenIcon(button) {
      if (!button.icon) {
        button.icon = document.createElement("i");
      }

      // Sleep to allow view transition to settle
      await new Promise((resolve) => setTimeout(resolve, 50));

      if (RichCMS.isFullScreen) {
        button.icon.className = "fas fa-compress"; // Use Font Awesome's "compress" icon for exit fullscreen
      } else {
        button.icon.className = "fas fa-expand"; // Use Font Awesome's "expand" icon for enter fullscreen
      }

      // Remove any existing icons and append the updated one
      const existingIcon = button.querySelector("i");
      if (existingIcon) {
        button.removeChild(existingIcon);
      }
      button.appendChild(button.icon);
    }

    // Add click event listeners to the full-screen-toggle buttons
    [...buttons].forEach((button) => {
      if (!RichCMS.isFullScreenSupported) {
        button.parentElement.removeChild(button);
      } else {
        button.addEventListener("click", () => {
          RichCMS.toggleFullScreen();
          updateFullscreenIcon(button); // Update the icon when the button is clicked
        });

        // Initialize the icon based on the initial fullscreen state
        updateFullscreenIcon(button);
      }
    });
  })();

  // Handle aside menu toggle
  (() => {
    const button = document.getElementById("menu-toggle-button");
    const asideContainer = document.querySelector("aside");

    const showAsideContainer = () => {
      asideContainer.style.display = "block";

      // Menu close icon
      button.innerHTML = '<i class="fas fa-times"></i>';
    };

    const hideAsideContainer = () => {
      asideContainer.style.display = "none";

      // Menu icon
      button.innerHTML = '<i class="fas fa-bars"></i>';
    };

    const getIsAsideContainerHidden = () =>
      asideContainer.style.display != "block";

    const toggleAsideContainer = () => {
      if (getIsAsideContainerHidden()) {
        showAsideContainer();
      } else {
        hideAsideContainer();
      }
    };

    if (button && asideContainer) {
      // Hide the button by default
      button.style.display = "none";

      (() => {
        const prevScrollPosition = { x: 0, y: 0 };

        button.addEventListener("click", function () {
          if (getIsAsideContainerHidden()) {
            // Cache current position
            prevScrollPosition.x = window.scrollX;
            prevScrollPosition.y = window.scrollY;
          }

          toggleAsideContainer();

          if (!getIsAsideContainerHidden()) {
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

      function handleResize() {
        if (window.innerWidth <= 768) {
          hideAsideContainer();
        } else {
          showAsideContainer();
        }
      }

      window.addEventListener("resize", handleResize);

      handleResize();
    }
  })();

  // Article heading links
  (() => {
    // HTML only defines heading tags from h1 to h6
    const maxHeadingLevels = 6;

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
});
