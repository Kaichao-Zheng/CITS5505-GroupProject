function scrollToSearch() {
  const searchBox = document.getElementById('search-input');
  searchBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
  searchBox.focus();
}