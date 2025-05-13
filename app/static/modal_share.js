$(document).ready(() => {
  const $productSelect    = $('#product-select');
  const $receiverInput    = $('#receiver-input');
  const $form             = $('#shareForm');
  const $toastContainer   = $('#toastContainer');
  const senderId          = Number($form.data('senderId'));

  // 1. 拉产品列表
  $.getJSON('/api/products')
    .done(products => {
      $productSelect
        .empty()
        .append('<option value="">Select a product</option>');
      products.forEach(p =>
        $productSelect.append(
          `<option value="${p.id}">${p.name}</option>`
        )
      );
    })
    .fail(() => showToast('Failed to load products', 'bg-danger'));

  // 2. 表单提交
  $form.on('submit', e => {
    e.preventDefault();

    const productId = Number($productSelect.val());
    const receiverIds = $receiverInput.val()
                            .split(',')
                            .map(s => s.trim())
                            .filter(s => s)
                            .map(s => Number(s));
    const emailList = $('#email-input').val()
                            .split(',')
                            .map(s => s.trim())
                            .filter(s => s);

    if (receiverIds.includes(senderId)) {
      return showToast('Receiver cannot be the same as sender', 'bg-danger');
    }
    if (receiverIds.length === 0 && emailList.length === 0) {
        return showToast('Please enter at least one receiver ID or email', 'bg-warning');
    }

    const payload = {
      product_id:   productId,
      sender_id:    senderId,
      receiver_ids: receiverIds,
      emails:       emailList
    };

    $.ajax({
      url:         '/api/share',
      method:      'POST',
      contentType: 'application/json',
      data:        JSON.stringify(payload),
    })
    .done(() => {
      showToast('Share succeeded!', 'bg-success');
      $form[0].reset();
      $('#shareModal').modal('hide');
    })
    .fail(xhr => {
      const msg = xhr.responseJSON?.message || 'Share failed';
      showToast(msg, 'bg-danger');
    });
  });

  // 3. Toast helper
  function showToast(message, toastClass = 'bg-primary') {
    const id = `toast-${Date.now()}`;
    const tpl = $(`
      <div id="${id}" class="toast align-items-center text-white ${toastClass}"
           role="alert" aria-live="assertive" aria-atomic="true" data-bs-delay="3000">
        <div class="d-flex">
          <div class="toast-body">${message}</div>
          <button type="button" class="btn-close btn-close-white ms-auto me-2"
                  data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
      </div>
    `);
    $toastContainer.append(tpl);
    new bootstrap.Toast(document.getElementById(id)).show();
    tpl.on('hidden.bs.toast', () => tpl.remove());
  }
});
