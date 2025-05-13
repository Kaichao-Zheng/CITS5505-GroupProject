// after page load bonding the click event to the share button 
$(document).ready(function() {
    // listen for the click event on the share button
    $('#shareButton').on('click', function(event) {
        event.preventDefault();  // stop the default action of the button

        const productId = $('#product-id').val();  // 获取商品 ID
        const senderId = $('#sender-id').val();  // 获取发送者 ID
        const receiverId = $('#receiver-id').val();  // 获取接收者 ID

        $.ajax({
            url: '/api/share',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                product_id: productId,
                sender_id: senderId,
                receiver_id: receiverId
            }),
            success: function(response) {
                if (response.status === 'shared') {
                    alert('Product shared successfully!');
                }
            },
            error: function(error) {
                console.error('Error sharing product:', error);
                alert('An error occurred while sharing the product.');
            }
        });
    });
});
