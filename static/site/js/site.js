const toggle = document.querySelector(".nav-toggle");
const nav = document.querySelector(".site-nav");
const workDropdown = document.querySelector(".nav-dropdown");
const workButton = document.querySelector(".nav-dropdown .nav-link--button");
const workMenu = document.querySelector(".nav-dropdown .nav-dropdown__menu");
const auroraParticles = document.querySelector("#aurora-particles");
const auroraDrops = document.querySelector("#aurora-drops");

if (toggle && nav) {
  toggle.addEventListener("click", () => {
    const isOpen = nav.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
}

if (workDropdown && workButton) {
  let closeTimer = null;
  const mobileQuery = window.matchMedia("(max-width: 780px)");

  const closeWorkDropdown = () => {
    if (closeTimer) {
      window.clearTimeout(closeTimer);
      closeTimer = null;
    }
    workDropdown.classList.remove("is-open");
    workButton.setAttribute("aria-expanded", "false");
  };

  const scheduleClose = () => {
    if (closeTimer) {
      window.clearTimeout(closeTimer);
    }
    closeTimer = window.setTimeout(() => {
      closeWorkDropdown();
    }, 180);
  };

  const cancelClose = () => {
    if (closeTimer) {
      window.clearTimeout(closeTimer);
      closeTimer = null;
    }
  };

  const openWorkDropdown = () => {
    cancelClose();
    workDropdown.classList.add("is-open");
    workButton.setAttribute("aria-expanded", "true");
  };

  workButton.addEventListener("click", (event) => {
    event.preventDefault();
    cancelClose();
    const isOpen = workDropdown.classList.toggle("is-open");
    workButton.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });

  document.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof Node)) {
      return;
    }

    if (!workDropdown.contains(target)) {
      closeWorkDropdown();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      closeWorkDropdown();
    }
  });

  workDropdown.addEventListener("mouseenter", () => {
    if (!mobileQuery.matches) {
      openWorkDropdown();
    }
  });
  workDropdown.addEventListener("mouseleave", () => {
    if (!mobileQuery.matches) {
      scheduleClose();
    }
  });

  if (workMenu) {
    workMenu.addEventListener("mouseenter", cancelClose);
  }
}

if (auroraParticles) {
  const particleCount = 18;

  for (let index = 0; index < particleCount; index += 1) {
    const particle = document.createElement("span");
    const size = Math.random() * 3 + 1;
    particle.className = "aurora-particle";
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    particle.style.animationDelay = `${Math.random() * 6}s`;
    particle.style.animationDuration = `${6 + Math.random() * 8}s`;
    auroraParticles.appendChild(particle);
  }
}

window.addEventListener("mousemove", (event) => {
  const x = event.clientX / window.innerWidth;
  const y = event.clientY / window.innerHeight;

  document.documentElement.style.setProperty("--pointer-x", `${x}`);
  document.documentElement.style.setProperty("--pointer-y", `${y}`);
});

if (auroraDrops) {
  let lastDropTime = 0;

  window.addEventListener("mousemove", (event) => {
    const now = performance.now();
    if (now - lastDropTime < 80) {
      return;
    }
    lastDropTime = now;

    const drop = document.createElement("span");
    drop.className = "aurora-drop";
    drop.style.left = `${event.clientX}px`;
    drop.style.top = `${event.clientY}px`;
    auroraDrops.appendChild(drop);

    window.setTimeout(() => {
      drop.remove();
    }, 900);
  });
}
