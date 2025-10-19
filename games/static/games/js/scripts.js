// Init UI scripts and filters
document.addEventListener("DOMContentLoaded", () => {
  if (window.lucide && typeof lucide.createIcons === 'function') {
    lucide.createIcons();
  }

  const toggleBtn = document.querySelector('[data-filter-toggle]');
  const content = document.getElementById('filter-content');

  if (toggleBtn && content) {
    const icon = toggleBtn.querySelector('[data-lucide]');

    const setOpen = (open) => {
      toggleBtn.setAttribute('aria-expanded', String(open));
      if (open) {
        content.hidden = false;
        content.style.maxHeight = content.scrollHeight + 'px';
        content.classList.add('open');
        if (icon && window.lucide) icon.setAttribute('data-lucide', 'chevron-up');
      } else {
        content.style.maxHeight = content.scrollHeight + 'px';
        requestAnimationFrame(() => {
          content.style.maxHeight = '0px';
          content.classList.remove('open');
        });
        if (icon && window.lucide) icon.setAttribute('data-lucide', 'chevron-down');
        content.addEventListener('transitionend', () => {
          if (!content.classList.contains('open')) content.hidden = true;
        }, { once: true });
      }
      if (window.lucide && typeof lucide.createIcons === 'function') {
        lucide.createIcons();
      }
    };

    toggleBtn.addEventListener('click', () => {
      const open = toggleBtn.getAttribute('aria-expanded') === 'true';
      setOpen(!open);
    });
  }

  // Dropdown menus (Steam-like)
  const dropdowns = document.querySelectorAll('[data-dropdown]');
  const closeAll = () => dropdowns.forEach(d => {
    const panel = d.querySelector('.dropdown');
    const btn = d.querySelector('[data-dropdown-toggle]');
    if (panel && btn) { panel.hidden = true; btn.setAttribute('aria-expanded','false'); }
  });

  dropdowns.forEach(d => {
    const btn = d.querySelector('[data-dropdown-toggle]');
    const panel = d.querySelector('.dropdown');
    if (!btn || !panel) return;

    // Click toggle (mobile + desktop)
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const open = btn.getAttribute('aria-expanded') === 'true';
      closeAll();
      btn.setAttribute('aria-expanded', String(!open));
      panel.hidden = open;
      if (window.lucide) lucide.createIcons();
    });

    // Hover open for desktop
    d.addEventListener('mouseenter', () => {
      btn.setAttribute('aria-expanded','true');
      panel.hidden = false;
    });
    d.addEventListener('mouseleave', () => {
      btn.setAttribute('aria-expanded','false');
      panel.hidden = true;
    });
  });

  document.addEventListener('click', (e) => {
    if (!(e.target.closest && e.target.closest('[data-dropdown]'))) {
      closeAll();
    }
  });
});
