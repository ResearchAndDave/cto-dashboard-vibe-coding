/**
 * CTO Dashboard JavaScript functionality
 */

document.addEventListener("DOMContentLoaded", function () {
  // Initialize filter functionality
  initializeFilters();

  // Set up search functionality
  initializeSearch();

  // Register HTMX event handlers
  registerHtmxEvents();
});

/**
 * Initialize project filtering functionality
 */
function initializeFilters() {
  const statusFilter = document.querySelector(
    'select[aria-label="Filter by status"]'
  );
  const projectCards = document.querySelectorAll(".card");

  if (statusFilter) {
    statusFilter.addEventListener("change", function () {
      const selectedStatus = this.value;

      if (selectedStatus === "All" || selectedStatus === "Filter by status") {
        // Show all projects
        projectCards.forEach((card) => {
          card.style.display = "block";
        });
      } else {
        // Filter projects by status
        projectCards.forEach((card) => {
          const statusBadge = card.querySelector(".badge");
          if (
            statusBadge &&
            statusBadge.textContent.trim() === selectedStatus
          ) {
            card.style.display = "block";
          } else {
            card.style.display = "none";
          }
        });
      }
    });
  }

  // Sort functionality
  const sortSelect = document.querySelector('select[aria-label="Sort by"]');
  if (sortSelect) {
    sortSelect.addEventListener("change", function () {
      // Implementation would depend on how we want to handle sorting
      // This would likely involve sending a request to the server
      // or re-ordering elements in the DOM
      console.log("Sorting by:", this.value);
    });
  }
}

/**
 * Initialize search functionality
 */
function initializeSearch() {
  const searchInput = document.querySelector(
    'input[aria-label="Search projects"]'
  );
  const projectCards = document.querySelectorAll(".card");

  if (searchInput) {
    searchInput.addEventListener("input", function () {
      const searchTerm = this.value.toLowerCase();

      projectCards.forEach((card) => {
        const projectName = card
          .querySelector(".card-title")
          .textContent.toLowerCase();
        const projectDesc = card
          .querySelector(".text-sm.text-gray-500")
          .textContent.toLowerCase();

        if (
          projectName.includes(searchTerm) ||
          projectDesc.includes(searchTerm)
        ) {
          card.style.display = "block";
        } else {
          card.style.display = "none";
        }
      });
    });
  }
}

/**
 * Register HTMX event handlers
 */
function registerHtmxEvents() {
  // When a project card is updated via HTMX
  document.body.addEventListener("htmx:afterSwap", function (event) {
    // If the target is a modal
    if (event.detail.target.id === "modal-content") {
      // Focus on the modal title for accessibility
      const modalTitle = document.getElementById("modal-title");
      if (modalTitle) {
        modalTitle.focus();
      }
    }
  });

  // When HTMX starts a request
  document.body.addEventListener("htmx:beforeRequest", function (event) {
    // Add loading state to the element that triggered the request
    const trigger = event.detail.elt;
    if (trigger.tagName === "BUTTON") {
      trigger.classList.add("loading");
    }
  });

  // When HTMX completes a request
  document.body.addEventListener("htmx:afterRequest", function (event) {
    // Remove loading state
    const trigger = event.detail.elt;
    if (trigger.tagName === "BUTTON") {
      trigger.classList.remove("loading");
    }
  });

  // When the modal is closed
  const modal = document.getElementById("htmx-modal");
  if (modal) {
    modal.addEventListener("close", function () {
      // Return focus to the element that opened the modal
      const modalOpener = document.querySelector(
        '[hx-target="#modal-content"]'
      );
      if (modalOpener) {
        modalOpener.focus();
      }
    });
  }
}

/**
 * Format a date for display
 * @param {Date|string} date - The date to format
 * @returns {string} Formatted date string
 */
function formatDate(date) {
  if (!date) return "N/A";

  const dateObj = typeof date === "string" ? new Date(date) : date;
  return dateObj.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

/**
 * Calculate and return status color class
 * @param {string} status - Project status
 * @returns {string} CSS class for status
 */
function getStatusClass(status) {
  switch (status.toLowerCase()) {
    case "on track":
      return "bg-success text-white";
    case "at risk":
      return "bg-warning text-white";
    case "delayed":
      return "bg-error text-white";
    default:
      return "bg-gray-500 text-white";
  }
}
