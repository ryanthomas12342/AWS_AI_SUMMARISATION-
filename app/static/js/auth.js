// Function to check if user is authenticated
function checkAuth() {
  // With cookie-based auth, we rely on server-side checks
  return true;
}

// Function to handle navigation with auth check
function checkAuthAndNavigate(event, url) {
  // With cookie-based auth, we can navigate directly

  event.preventDefault();
  window.location.href = url;
}

// Function to handle logout
function handleLogout(event) {
  event.preventDefault();

  fetch("/auth/api/logout", {
    method: "POST",
    credentials: "include", // Important for cookies
  })
    .then((response) => {
      if (response.ok) {
        window.location.href = "/auth/login";
      } else {
        throw new Error("Logout failed");
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("Failed to logout. Please try again.");
    });
}

// Function to get headers for API requests
function getAuthHeaders() {
  return {
    "Content-Type": "application/json",
  };
}
