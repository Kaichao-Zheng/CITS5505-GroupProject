function scrollToSearch() {
  const searchBox = document.getElementById('search-input');
  searchBox.scrollIntoView({ behavior: 'smooth', block: 'center' });
  searchBox.focus();
}
$(function() {
  // every 15 seconds, check for new share notifications
  setInterval(() => {
    $.getJSON('/api/share/notifications')
      .done(notifs => {
        notifs.forEach(n => {
          displayToastMessage([
            `You have a new share from ${n.sender_name}: ${n.product_name}`
          ]);
        });
      })
      .fail(() => console.warn('Failed to fetch share notifications'));
  }, 15000);
});