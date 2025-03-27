document.addEventListener("DOMContentLoaded", async function () {
    const itemsContainer = document.getElementById("items-container");

    try {
        const response = await fetch("http://127.0.0.1:5000/get-items");
        const items = await response.json();

        if (items.error) {
            itemsContainer.innerHTML = `<p>Error fetching items: ${items.error}</p>`;
            return;
        }

        items.forEach(item => {
            const itemCard = document.createElement("div");
            itemCard.classList.add("item-card");
            itemCard.innerHTML = `
                <h3>${item.name}</h3>
                <p><strong>Price:</strong> $${item.price}</p>
                <p><strong>Available Quantity:</strong> ${item.quantity}</p>
                <p><strong>Bidding Time:</strong> ${item.duration} hours</p>
                <button onclick="buyItem(${item.id})">Buy Now</button>
            `;
            itemsContainer.appendChild(itemCard);
        });

    } catch (error) {
        itemsContainer.innerHTML = `<p>Failed to load items.</p>`;
    }
});

function buyItem(itemId) {
    alert(`Buying item with ID: ${itemId}`); 
    // Further implementation can be added for purchasing logic
}
