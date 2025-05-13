$(document).ready(function() {
    // when the modal is shown, load the merchants from the backend 
    $('#modal-upload').on('shown.bs.modal', function () {
        $.ajax({
            url: '/api/merchants',  // backend API to get merchants
            method: 'GET',
            success: function(merchants) {
                // clear existing options
                $('#merchant-dropdown').empty();

                // add a default option
                $('#merchant-dropdown').append('<option value="" disabled selected hidden>Select a merchant</option>');

                // add merchants to the dropdown
                merchants.forEach(function(merchant) {
                    $('#merchant-dropdown').append('<option value="' + merchant.name + '">' + merchant.name + '</option>');
                });
            },
            error: function(error) {
                console.error('Error loading merchants:', error);
                alert('Failed to load merchants. Please try again later.');
            }
        });
    });
    $('#uploadImageForm').on('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);

        $.ajax({
            url: '/api/upload_csv',
            method: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            dataType: 'json',
            success(res) {
                displayToastMessage([ res.message || 'Upload successful!' ]);
                this.reset();
                $('#uploadModal').modal('hide');
            },
            error(xhr) {
                console.error('Error uploading file:', xhr);
                const msg = xhr.responseJSON?.error || 'Upload failed. Please try again.';
                displayToastMessage([ msg ]);
            }
        });
    });
});
