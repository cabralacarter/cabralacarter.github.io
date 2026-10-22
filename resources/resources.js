(() => {
  'use strict';

  const search = document.querySelector('#resource-search');
  const cards = [...document.querySelectorAll('[data-resource]')];
  const topics = [...document.querySelectorAll('[data-topic-filter]')];
  const count = document.querySelector('#resource-count');
  const empty = document.querySelector('#empty-results');
  const reset = document.querySelector('#reset-filters');
  const clearSearch = document.querySelector('#clear-search');
  const params = new URLSearchParams(window.location.search);
  const validTopics = new Set(topics.map(button => button.dataset.topicFilter));
  let selectedTopic = validTopics.has(params.get('topic')) ? params.get('topic') : 'all';

  const normalize = value => value.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase();

  function filterResources(updateAddress = true) {
    const terms = normalize(search.value.trim()).split(/\s+/).filter(Boolean);
    let visible = 0;

    cards.forEach(card => {
      const matchesTopic = selectedTopic === 'all' || card.dataset.topics.split(' ').includes(selectedTopic);
      const text = normalize(card.dataset.search);
      card.hidden = !(matchesTopic && terms.every(term => text.includes(term)));
      if (!card.hidden) visible += 1;
    });

    topics.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.topicFilter === selectedTopic)));
    const isFiltered = selectedTopic !== 'all' || terms.length > 0;
    count.textContent = `${visible} ${visible === 1 ? 'resource' : 'resources'}${isFiltered ? ' found' : ' to explore'}`;
    empty.hidden = visible !== 0;
    reset.hidden = !isFiltered;
    clearSearch.hidden = search.value.length === 0;

    if (updateAddress) {
      const next = new URL(window.location.href);
      next.hash = '';
      if (selectedTopic === 'all') next.searchParams.delete('topic');
      else next.searchParams.set('topic', selectedTopic);
      if (search.value.trim()) next.searchParams.set('q', search.value.trim());
      else next.searchParams.delete('q');
      try { window.history.replaceState(null, '', next); } catch (_) { /* Filtering also works from a downloaded copy. */ }
    }
  }

  function resetFilters() {
    selectedTopic = 'all';
    search.value = '';
    filterResources();
    search.focus({ preventScroll: true });
  }

  search.value = params.get('q') || '';
  search.addEventListener('input', () => filterResources());
  document.querySelector('#resource-search-form').addEventListener('submit', event => event.preventDefault());
  topics.forEach(button => button.addEventListener('click', () => {
    selectedTopic = button.dataset.topicFilter;
    filterResources();
  }));
  reset.addEventListener('click', resetFilters);
  document.querySelector('#empty-reset').addEventListener('click', resetFilters);
  clearSearch.addEventListener('click', () => {
    search.value = '';
    filterResources();
    search.focus();
  });

  document.querySelectorAll('[data-start-resource]').forEach(link => link.addEventListener('click', () => {
    selectedTopic = 'all';
    search.value = '';
    filterResources();
    const target = document.getElementById(link.dataset.startResource);
    if (target) {
      target.setAttribute('tabindex', '-1');
      requestAnimationFrame(() => target.focus({ preventScroll: true }));
    }
  }));

  window.addEventListener('popstate', () => {
    const next = new URLSearchParams(window.location.search);
    selectedTopic = validTopics.has(next.get('topic')) ? next.get('topic') : 'all';
    search.value = next.get('q') || '';
    filterResources(false);
  });

  document.querySelector('#resource-controls').hidden = false;
  filterResources(false);
})();
