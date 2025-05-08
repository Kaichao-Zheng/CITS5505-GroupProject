const displayToastMessage = (messages) => {
    const container = document.getElementById('toastContainer');
  
    messages.forEach((msg, index) => {
      const toastId = `toast-${Date.now()}-${index}`;
      
      const toastElement = document.createElement('div');
      toastElement.className = 'toast';
      toastElement.id = toastId;
      toastElement.setAttribute('role', 'alert');
      toastElement.setAttribute('aria-live', 'assertive');
      toastElement.setAttribute('aria-atomic', 'true');
      toastElement.setAttribute('data-bs-delay', '3000'); // Auto-hide after 3s
  
      toastElement.innerHTML = `
        <div class="toast-header">
          <strong class="me-auto">Notification</strong>
          <small class="text-muted">just now</small>
          <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">${msg}</div>
      `;
  
      container.appendChild(toastElement);
  
      const $toast = $(`#${toastId}`);
      $toast.toast({ autohide: true });
      $toast.toast('show');
  
      // Optional: remove from DOM after hidden
      $toast.on('hidden.bs.toast', function () {
        this.remove();
      });
    });
  }
  