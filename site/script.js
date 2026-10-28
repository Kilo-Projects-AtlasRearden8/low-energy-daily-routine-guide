// Low-Energy Routine Guide — small interactive enhancements
// Asdale Dynamics, LLC — Copyright (c) 2026 Asdale Dynamics, LLC

(() => {
  'use strict';

  // Energy tracker: compute simple suggestion from 1-5 ratings
  const form = document.getElementById('energy-form');
  const result = document.getElementById('energy-result');
  if (form && result) {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      const values = [
        Number(form.elements['morning'].value),
        Number(form.elements['midday'].value),
        Number(form.elements['evening'].value)
      ];
      const avg = (values[0] + values[1] + values[2]) / 3;
      let suggestion = 'Rest today. Doing nothing is the right choice.';
      if (avg >= 4) suggestion = 'You have energy for one or two small tasks. Start with just one.';
      else if (avg >= 3) suggestion = 'One small task, then rest. That is enough.';
      else if (avg >= 2) suggestion = 'Basic self-care only. Water, food, rest.';
      result.textContent = suggestion;
      result.style.display = 'block';
      result.focus();
    });
  }

  // Smooth reveal for cards (reduced motion respected)
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const observer = window.IntersectionObserver && !prefersReduced
    ? new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
          }
        });
      }, { threshold: 0.1 })
    : null;

  document.querySelectorAll('.section-card, .card-link').forEach((el) => {
    if (!prefersReduced) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(12px)';
      el.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
      observer.observe(el);
    } else {
      el.style.opacity = '1';
    }
  });
})();
