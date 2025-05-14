const displayToastMessage = (messages) => {
    const container = document.getElementById('toastContainer');
  
    messages.forEach((msg, index) => {
      const toastId = `toast-${Date.now()}-${index}`;
      // address bg-color when login/logout/register
      let msgText, msgColor;
      if (Array.isArray(msg)) {
        [msgColor, msgText] = msg;
      } else {
        msgColor = 'bg-primary';
        msgText = msg;
      }
      const toastElement = document.createElement('div');
      toastElement.className = `toast align-items-center text-white ${msgColor}`;
      toastElement.id = toastId;
      toastElement.setAttribute('role', 'alert');
      toastElement.setAttribute('aria-live', 'assertive');
      toastElement.setAttribute('aria-atomic', 'true');
      toastElement.setAttribute('data-bs-delay', '3000'); // Auto-hide after 3s
  
      toastElement.innerHTML = `
        <div class="d-flex">
          <div class="toast-body">${msgText}</div>
          <button type="button" class="btn-close btn-close-white ms-auto me-2"
                  data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
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
  