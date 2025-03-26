document.getElementById('add-item-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    const productName = document.getElementById('product-name').value;
    const quantity = document.getElementById('quantity').value;
    const price = document.getElementById('price').value;
    const address = document.getElementById('address').value;
    const phone = document.getElementById('phone').value;
    const duration = document.getElementById('duration').value;

    const data = {
        product_name: productName,
        quantity: quantity,
        price: price,
        address: address,
        phone: phone,
        duration: duration
    };

    try {
        const response = await fetch('/add-item', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        alert(result.message);
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to add item. Please try again.');
    }
});
