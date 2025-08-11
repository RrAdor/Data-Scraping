// Handle form submission
document.getElementById("analyzeForm").addEventListener("submit", function (e) {
  const urlInput = document.getElementById("url");
  const btn = document.getElementById("analyzeBtn");

  if (!urlInput.value) {
    e.preventDefault();
    // Add error animation
    urlInput.style.borderColor = "#ff6b6b";
    urlInput.animate(
      [
        { transform: "translateX(0)" },
        { transform: "translateX(-5px)" },
        { transform: "translateX(5px)" },
        { transform: "translateX(0)" },
      ],
      {
        duration: 300,
        iterations: 2,
      }
    );

    setTimeout(() => {
      urlInput.style.borderColor = "";
    }, 1000);

    return;
  }

  try {
    new URL(urlInput.value);
  } catch {
    e.preventDefault();
    urlInput.style.borderColor = "#ff6b6b";
    urlInput.value = "";
    urlInput.placeholder = "Please include http:// or https://";
    urlInput.focus();
    return;
  }

  // Button loading state
  btn.disabled = true;
  btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

  // Add pulse animation to card
  const card = document.querySelector(".card");
  card.style.animation = "none";
  void card.offsetWidth; // Trigger reflow
  card.style.animation = "pulse 1s";

  // Form will submit automatically to analyzer page
});

function analyze() {
  // Trigger form submission
  document.getElementById("analyzeForm").submit();
}

function useExample() {
  const exampleUrl =
    "https://www.reuters.com/markets/europe/major-economic-policy-changes-announced-european-government-2024-03-15/";
  const urlInput = document.getElementById("url");

  // Animate example insertion
  urlInput.value = "";
  let i = 0;
  const typingEffect = setInterval(() => {
    if (i < exampleUrl.length) {
      urlInput.value += exampleUrl.charAt(i);
      i++;
    } else {
      clearInterval(typingEffect);
      // Auto submit after example is loaded
      setTimeout(() => {
        document.getElementById("analyzeForm").submit();
      }, 500);
    }
  }, 30);
}

// Add keypress listener for Enter key
document.getElementById("url").addEventListener("keypress", (e) => {
  if (e.key === "Enter") analyze();
});

// Add animation on load
document.addEventListener("DOMContentLoaded", () => {
  const inputs = document.querySelectorAll("input");
  inputs.forEach((input) => {
    input.addEventListener("focus", () => {
      input.parentNode.style.transform = "scale(1.01)";
    });
    input.addEventListener("blur", () => {
      input.parentNode.style.transform = "scale(1)";
    });
  });
});
