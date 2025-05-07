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

    // process the form submission
    $('#uploadImageForm').submit(function(event) {
        event.preventDefault();  // prevent the default form submission 

        const formData = new FormData(this);  // create a FormData object from the form  

        // send AJAX request to the backend to upload the file
        $.ajax({
            url: '/api/upload_csv',  // backend API to upload the file
            method: 'POST',
            data: formData,
            processData: false,  // not letting jQuery process the data 
            contentType: false,  // not setting any content type header
            success: function(response) {
                if (response.message === 'File uploaded successfully') {
                    $('#uploadResult').html('<p>CSV uploaded successfully!</p>');
                } else {
                    $('#uploadResult').html('<p>Error: ' + response.error + '</p>');
                }
            },
            error: function(error) {
                console.error('Error uploading file:', error);
                $('#uploadResult').html('<p>Failed to upload file. Please try again later.</p>');
            }
        });
    });
});
