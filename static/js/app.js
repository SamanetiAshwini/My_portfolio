/**
 * Ashwini Samaneti — Portfolio Client Engine
 * Handles theme toggling, interactive constellation background,
 * project filtering, details modal, and navigation state.
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initHeaderScroll();
  initMobileNav();
  initActiveNavSpy();
  initAmbientCanvas();
  initProjectFilters();
  initProjectModals();
  initActionTooltips();
});

/* ===================================================================
   1. Theme Management (Dark Midnight Default with Light Mode Option)
   =================================================================== */
function initTheme() {
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const savedTheme = localStorage.getItem('ashwini_portfolio_theme') || 'dark';

  document.documentElement.setAttribute('data-theme', savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('ashwini_portfolio_theme', newTheme);
    });
  }
}

/* ===================================================================
   2. Header Scroll Effect
   =================================================================== */
function initHeaderScroll() {
  const header = document.querySelector('.site-header');
  if (!header) return;

  const handleScroll = () => {
    if (window.scrollY > 30) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

/* ===================================================================
   3. Mobile Navigation Menu
   =================================================================== */
function initMobileNav() {
  const toggleBtn = document.getElementById('mobileNavToggle');
  const navMenu = document.getElementById('navMenu');

  if (!toggleBtn || !navMenu) return;

  toggleBtn.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('open');
    toggleBtn.setAttribute('aria-expanded', isOpen);
  });

  // Close menu when clicking any nav link
  navMenu.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
      toggleBtn.setAttribute('aria-expanded', 'false');
    });
  });
}

/* ===================================================================
   4. ScrollSpy Navigation Active Highlighting
   =================================================================== */
function initActiveNavSpy() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  if (!sections.length || !navLinks.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach(link => {
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });
      }
    });
  }, {
    rootMargin: '-30% 0px -60% 0px'
  });

  sections.forEach(section => observer.observe(section));
}

/* ===================================================================
   5. Interactive Ambient Constellation Canvas
   =================================================================== */
function initAmbientCanvas() {
  const canvas = document.getElementById('ambientCanvas');
  if (!canvas) return;

  // Skip animations if user prefers reduced motion
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    canvas.style.display = 'none';
    return;
  }

  const ctx = canvas.getContext('2d');
  let width = (canvas.width = window.innerWidth);
  let height = (canvas.height = window.innerHeight);

  window.addEventListener('resize', () => {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
  });

  const particleCount = Math.min(Math.floor((width * height) / 22000), 55);
  const particles = [];

  for (let i = 0; i < particleCount; i++) {
    particles.push({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.45,
      vy: (Math.random() - 0.5) * 0.45,
      radius: Math.random() * 1.8 + 0.8,
      color: Math.random() > 0.5 ? 'rgba(139, 92, 246, 0.45)' : 'rgba(6, 182, 212, 0.45)'
    });
  }

  let mouse = { x: null, y: null };
  window.addEventListener('mousemove', (e) => {
    mouse.x = e.clientX;
    mouse.y = e.clientY;
  });

  window.addEventListener('mouseleave', () => {
    mouse.x = null;
    mouse.y = null;
  });

  function render() {
    ctx.clearRect(0, 0, width, height);

    for (let i = 0; i < particles.length; i++) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0) p.x = width;
      if (p.x > width) p.x = 0;
      if (p.y < 0) p.y = height;
      if (p.y > height) p.y = 0;

      // Draw particle
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      ctx.fillStyle = p.color;
      ctx.fill();

      // Connect near particles
      for (let j = i + 1; j < particles.length; j++) {
        const p2 = particles[j];
        const dx = p.x - p2.x;
        const dy = p.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 130) {
          ctx.beginPath();
          ctx.strokeStyle = `rgba(139, 92, 246, ${0.18 * (1 - dist / 130)})`;
          ctx.lineWidth = 0.8;
          ctx.moveTo(p.x, p.y);
          ctx.lineTo(p2.x, p2.y);
          ctx.stroke();
        }
      }

      // Gentle mouse interaction
      if (mouse.x !== null && mouse.y !== null) {
        const mdx = p.x - mouse.x;
        const mdy = p.y - mouse.y;
        const mdist = Math.sqrt(mdx * mdx + mdy * mdy);
        if (mdist < 100) {
          p.x += (mdx / mdist) * 0.8;
          p.y += (mdy / mdist) * 0.8;
        }
      }
    }

    requestAnimationFrame(render);
  }

  render();
}

/* ===================================================================
   6. Projects Search & Technology Filter
   =================================================================== */
function initProjectFilters() {
  const searchInput = document.getElementById('projectSearchInput');
  const filterPills = document.querySelectorAll('.tech-filter-pill');
  const projectCards = document.querySelectorAll('.project-card');

  let activeTech = 'all';
  let searchQuery = '';

  const applyFilters = () => {
    projectCards.forEach(card => {
      const cardTech = (card.getAttribute('data-tech') || '').toLowerCase();
      const cardTitle = (card.getAttribute('data-title') || '').toLowerCase();
      const cardDesc = (card.getAttribute('data-desc') || '').toLowerCase();

      const matchesTech = activeTech === 'all' || cardTech.includes(activeTech.toLowerCase());
      const matchesSearch = !searchQuery || 
        cardTitle.includes(searchQuery) || 
        cardDesc.includes(searchQuery) || 
        cardTech.includes(searchQuery);

      if (matchesTech && matchesSearch) {
        card.style.display = 'grid';
      } else {
        card.style.display = 'none';
      }
    });
  };

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value.trim().toLowerCase();
      applyFilters();
    });
  }

  filterPills.forEach(pill => {
    pill.addEventListener('click', () => {
      filterPills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      activeTech = pill.getAttribute('data-filter') || 'all';
      applyFilters();
    });
  });
}

/* ===================================================================
   7. Project Details Modal
   =================================================================== */
function initProjectModals() {
  const modalBackdrop = document.getElementById('projectModal');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const viewDetailBtns = document.querySelectorAll('.btn-view-details');

  if (!modalBackdrop) return;

  const closeModal = () => {
    modalBackdrop.classList.remove('active');
    document.body.style.overflow = '';
  };

  const openModal = async (slug) => {
    try {
      const res = await fetch(`/api/projects/${slug}`);
      if (!res.ok) throw new Error('Could not fetch project details');
      const project = await res.json();

      document.getElementById('modalProjectTitle').textContent = project.title;
      document.getElementById('modalProjectTagline').textContent = project.tagline;
      document.getElementById('modalProjectCategory').textContent = project.category;
      document.getElementById('modalProjectProblem').textContent = project.problem;
      document.getElementById('modalProjectSolution').textContent = project.solution;

      // Render Features
      const featList = document.getElementById('modalProjectFeatures');
      featList.innerHTML = '';
      project.features.forEach(feat => {
        const li = document.createElement('li');
        li.textContent = feat;
        featList.appendChild(li);
      });

      // Render Documented Contributions
      const contribList = document.getElementById('modalProjectContributions');
      contribList.innerHTML = '';
      project.contributions.forEach(c => {
        const li = document.createElement('li');
        li.textContent = c;
        contribList.appendChild(li);
      });

      // Render Tech Tags
      const techWrap = document.getElementById('modalProjectTech');
      techWrap.innerHTML = '';
      project.technologies.forEach(t => {
        const span = document.createElement('span');
        span.className = 'tech-tag';
        span.textContent = t;
        techWrap.appendChild(span);
      });

      // Render Modal Actions / GitHub & Publication links
      const actionsWrap = document.getElementById('modalProjectActions');
      if (actionsWrap) {
        actionsWrap.innerHTML = '';
        if (project.github_url) {
          const ghLink = document.createElement('a');
          ghLink.href = project.github_url;
          ghLink.target = '_blank';
          ghLink.rel = 'noopener noreferrer';
          ghLink.className = 'btn btn-primary btn-sm';
          ghLink.style.display = 'inline-flex';
          ghLink.style.alignItems = 'center';
          ghLink.style.gap = '0.5rem';
          ghLink.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
            </svg>
            <span>View GitHub Repository</span>
          `;
          actionsWrap.appendChild(ghLink);
        }

        if (project.paper_url) {
          const paperLink = document.createElement('a');
          paperLink.href = project.paper_url;
          paperLink.target = '_blank';
          paperLink.rel = 'noopener noreferrer';
          paperLink.className = 'btn btn-primary btn-sm';
          paperLink.style.display = 'inline-flex';
          paperLink.style.alignItems = 'center';
          paperLink.style.gap = '0.5rem';
          paperLink.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
              <polyline points="14 2 14 8 20 8"></polyline>
              <line x1="16" y1="13" x2="8" y2="13"></line>
              <line x1="16" y1="17" x2="8" y2="17"></line>
            </svg>
            <span>Read Research Paper (PDF)</span>
          `;
          actionsWrap.appendChild(paperLink);
        }

        if (project.certificate_url) {
          const certLink = document.createElement('a');
          certLink.href = project.certificate_url;
          certLink.target = '_blank';
          certLink.rel = 'noopener noreferrer';
          certLink.className = 'btn btn-outline btn-sm';
          certLink.style.display = 'inline-flex';
          certLink.style.alignItems = 'center';
          certLink.style.gap = '0.5rem';
          certLink.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="8" r="7"></circle>
              <polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline>
            </svg>
            <span>View Springer Certificate</span>
          `;
          actionsWrap.appendChild(certLink);
        }
      }

      // Render Photo Gallery for SMRITI
      let galleryWrap = document.getElementById('modalProjectGallery');
      if (!galleryWrap) {
        galleryWrap = document.createElement('div');
        galleryWrap.id = 'modalProjectGallery';
        galleryWrap.style.marginTop = '1.75rem';
        actionsWrap.parentNode.insertBefore(galleryWrap, actionsWrap);
      }
      galleryWrap.innerHTML = '';

      if (slug === 'smriti') {
        galleryWrap.innerHTML = `
          <h3 class="modal-section-title" style="margin-bottom:0.75rem;">Robotic Hardware &amp; Team Gallery</h3>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:1rem; margin-bottom:1rem;">
            <a href="/static/images/smriti-robot-side.jpg" target="_blank" rel="noopener noreferrer" style="border-radius:var(--radius-md); overflow:hidden; border:1px solid var(--border-subtle); display:block; aspect-ratio:4/3; background:#000;">
              <img src="/static/images/smriti-robot-side.jpg" alt="Smriti Robot Side Angle with OLED Eyes" style="width:100%; height:100%; object-fit:cover; transition:transform 0.3s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            </a>
            <a href="/static/images/smriti-robot-top.jpg" target="_blank" rel="noopener noreferrer" style="border-radius:var(--radius-md); overflow:hidden; border:1px solid var(--border-subtle); display:block; aspect-ratio:4/3; background:#000;">
              <img src="/static/images/smriti-robot-top.jpg" alt="Smriti Robot Top View Raspberry Pi Architecture" style="width:100%; height:100%; object-fit:cover; transition:transform 0.3s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            </a>
            <a href="/static/images/smriti-team.jpg" target="_blank" rel="noopener noreferrer" style="border-radius:var(--radius-md); overflow:hidden; border:1px solid var(--border-subtle); display:block; aspect-ratio:4/3; background:#000;">
              <img src="/static/images/smriti-team.jpg" alt="Ashwini and VJIT Research Team with Dr. Rambabu Pemula" style="width:100%; height:100%; object-fit:cover; transition:transform 0.3s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            </a>
            <a href="/static/images/smriti-certificate.jpg" target="_blank" rel="noopener noreferrer" style="border-radius:var(--radius-md); overflow:hidden; border:1px solid var(--border-subtle); display:block; aspect-ratio:4/3; background:#000;">
              <img src="/static/images/smriti-certificate.jpg" alt="Springer CIGAI 2026 Certificate" style="width:100%; height:100%; object-fit:cover; transition:transform 0.3s;" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
            </a>
          </div>
        `;
      }

      modalBackdrop.classList.add('active');
      document.body.style.overflow = 'hidden';
    } catch (err) {
      console.warn('Modal data load fallback:', err);
    }
  };

  viewDetailBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const slug = btn.getAttribute('data-slug');
      if (slug) openModal(slug);
    });
  });

  if (modalCloseBtn) {
    modalCloseBtn.addEventListener('click', closeModal);
  }

  modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modalBackdrop.classList.contains('active')) {
      closeModal();
    }
  });
}

/* ===================================================================
   8. Configurable Link Toast Notifications
   =================================================================== */
function initActionTooltips() {
  const toastButtons = document.querySelectorAll('.btn-configurable-link');

  toastButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const label = btn.getAttribute('data-label') || 'Repository / Demo Link';
      showToast(`${label}: Configured as placeholder per portfolio specifications.`);
    });
  });
}

function showToast(message) {
  let toast = document.getElementById('appToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'appToast';
    toast.style.position = 'fixed';
    toast.style.bottom = '2rem';
    toast.style.left = '50%';
    toast.style.transform = 'translateX(-50%) translateY(20px)';
    toast.style.background = 'rgba(14, 18, 36, 0.95)';
    toast.style.color = '#F8FAFC';
    toast.style.padding = '0.75rem 1.4rem';
    toast.style.borderRadius = '9999px';
    toast.style.border = '1px solid rgba(6, 182, 212, 0.4)';
    toast.style.boxShadow = '0 8px 24px rgba(0, 0, 0, 0.5)';
    toast.style.fontFamily = 'var(--font-body)';
    toast.style.fontSize = '0.875rem';
    toast.style.zIndex = '300';
    toast.style.opacity = '0';
    toast.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
    toast.style.pointerEvents = 'none';
    document.body.appendChild(toast);
  }

  toast.textContent = message;
  toast.style.opacity = '1';
  toast.style.transform = 'translateX(-50%) translateY(0)';

  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(-50%) translateY(20px)';
  }, 3200);
}
window.showToast = showToast;
