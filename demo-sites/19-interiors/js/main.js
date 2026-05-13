(() => {
  const signature = {"site": "interiors", "interaction": "Moodboard filter, room selector, material palette interaction", "mode": "commerce"};
  const body = document.body;
  const header = document.querySelector('[data-header]');
  const menuToggle = document.querySelector('[data-menu-toggle]');
  const backToTop = document.querySelector('[data-back-to-top]');
  const cookieBanner = document.querySelector('[data-cookie-banner]');
  const acceptCookie = document.querySelector('[data-cookie-accept]');
  const idle = (task) => ('requestIdleCallback' in window ? requestIdleCallback(task, { timeout: 1600 }) : setTimeout(task, 1));
  const setCookie = (name, value) => { document.cookie = `${name}=${value}; path=/; max-age=31536000; SameSite=Lax`; };
  const hasCookie = (name) => document.cookie.split('; ').some((row) => row.startsWith(`${name}=`));
  const track = (event) => window.dispatchEvent(new CustomEvent('ashtra:track', { detail: { event } }));
  const updateChrome = () => {
    const y = window.scrollY || 0;
    if (header) header.classList.toggle('is-scrolled', y > 24);
    if (backToTop) backToTop.classList.toggle('is-visible', y > 800);
  };
  updateChrome();
  window.addEventListener('scroll', updateChrome, { passive: true });
  if (menuToggle) {
    menuToggle.addEventListener('click', () => {
      const open = !body.classList.contains('menu-open');
      body.classList.toggle('menu-open', open);
      menuToggle.setAttribute('aria-expanded', String(open));
    });
  }
  document.querySelectorAll('#site-menu a').forEach((link) => link.addEventListener('click', () => {
    body.classList.remove('menu-open');
    if (menuToggle) menuToggle.setAttribute('aria-expanded', 'false');
  }));
  if (backToTop) backToTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  if (cookieBanner && !hasCookie('ashtra_consent')) cookieBanner.classList.add('is-visible');
  if (acceptCookie && cookieBanner) acceptCookie.addEventListener('click', () => {
    setCookie('ashtra_consent', 'yes');
    cookieBanner.classList.remove('is-visible');
    track('consent_interiors');
  });
  idle(() => {
    document.documentElement.dataset.staticSite = "interiors";
    document.documentElement.dataset.footerPattern = document.querySelector('.hand-footer')?.className.match(/hand-footer-(\w+)/)?.[1] || 'site';
    if (body.dataset.assetSystem === 'true') track('asset_system_view_interiors');

    document.querySelectorAll('[data-component-id]').forEach((section, index) => {
      section.style.setProperty('--section-seq', String(index + 1));
      section.dataset.wpReady = 'true';
      section.setAttribute('tabindex', section.hasAttribute('tabindex') ? section.getAttribute('tabindex') : '-1');
    });
    document.querySelectorAll('[data-layout-variation*="category-faq"], [data-layout-variation*="searchable-faq"]').forEach((section) => {
      const details = Array.from(section.querySelectorAll('details'));
      details.forEach((item, itemIndex) => {
        const summary = item.querySelector('summary');
        if (!summary) return;
        summary.addEventListener('keydown', (event) => {
          if (!['ArrowDown','ArrowUp','Home','End'].includes(event.key)) return;
          event.preventDefault();
          const nextIndex = event.key === 'Home' ? 0 : event.key === 'End' ? details.length - 1 : itemIndex + (event.key === 'ArrowDown' ? 1 : -1);
          details[(nextIndex + details.length) % details.length]?.querySelector('summary')?.focus();
        });
      });
    });
    document.querySelectorAll('[data-whatsapp-widget] a').forEach((link) => link.addEventListener('click', () => track(`whatsapp_open_${signature.site}`)));
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const revealTargets = Array.from(document.querySelectorAll('.section, .mini-card, .price-card, .resource-card, .metric-card, .target-stage, .hand-footer'));
    revealTargets.forEach((item) => item.classList.add('reveal-ready'));
    if ('IntersectionObserver' in window && !reduceMotion) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
        });
      }, { rootMargin: '0px 0px -10% 0px', threshold: 0.06 });
      revealTargets.forEach((item) => observer.observe(item));
    } else {
      revealTargets.forEach((item) => item.classList.add('is-visible'));
    }
    document.querySelectorAll('[data-contact-form]').forEach((form) => {
      const status = form.querySelector('[data-form-status]');
      let started = false;
      form.addEventListener('input', () => { if (!started) { started = true; track(`form_start_${signature.site}`); } });
      form.addEventListener('submit', async (event) => {
        event.preventDefault();
        if (!form.checkValidity()) { form.reportValidity(); return; }
        const submit = form.querySelector('button[type="submit"]');
        if (status) status.textContent = 'Sending your enquiry...';
        if (submit) submit.disabled = true;
        try {
          const response = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
          if (!response.ok) throw new Error('Form service unavailable');
          window.location.href = 'thanks.html';
        } catch (error) {
          if (status) status.textContent = 'We could not send the form. Use the contact link or try again.';
          if (submit) submit.disabled = false;
        }
      });
    });
    document.querySelectorAll('[data-signature]').forEach((panel) => {
      const output = panel.querySelector('[data-signature-output]');
      panel.querySelectorAll('[data-option]').forEach((button) => button.addEventListener('click', () => {
        panel.querySelectorAll('[data-option]').forEach((item) => item.setAttribute('aria-pressed', 'false'));
        button.setAttribute('aria-pressed', 'true');
        if (output) output.textContent = `${button.textContent.trim()} route selected.`;
        track(`${panel.getAttribute('data-signature')}_${button.getAttribute('data-option')}`);
      }));
    });
    document.querySelectorAll('[data-component="faq"] details').forEach((item) => item.addEventListener('toggle', () => { if (item.open) track(`faq_open_${signature.site}`); }));
    document.querySelectorAll('[data-track]').forEach((element) => element.addEventListener('click', () => track(element.getAttribute('data-track'))));
  });
})();
