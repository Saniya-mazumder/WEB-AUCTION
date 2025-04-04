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

async function buyItem(itemId) {
    // Get the current user's username from localStorage
    const username = localStorage.getItem("username");
    
    if (!username) {
        alert("Please log in first to buy items!");
        window.location.href = "auth.html?type=buyer";
        return;
    }
    
    try {
        // Get the current price for the item
        const itemResponse = await fetch(`http://127.0.0.1:5000/get-items`);
        const items = await itemResponse.json();
        const selectedItem = items.find(item => item.id === itemId);
        
        if (!selectedItem) {
            alert("Item not found!");
            return;
        }
        
        // Confirm purchase
        if (confirm(`Are you sure you want to buy ${selectedItem.name} for $${selectedItem.price}?`)) {
            // Send request to backend to record the purchase
            const response = await fetch("http://127.0.0.1:5000/place-bid", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    item_id: itemId,
                    new_price: selectedItem.price,
                    bidder: username  // This is the username, not the ID
                })
            });
            
            const result = await response.json();
            
            if (result.message) {
                // Now immediately approve the bid (finalize the purchase)
                const approveResponse = await fetch("http://127.0.0.1:5000/approve-bid", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        item_id: itemId
                    })
                });
                
                const approveResult = await approveResponse.json();
                
                if (approveResult.message) {
                    alert("Purchase successful!");
                    window.location.href = "view_past_bought.html";
                } else {
                    alert(`Error finalizing purchase: ${approveResult.error || "Unknown error"}`);
                }
            } else {
                alert(`Error placing bid: ${result.error || "Unknown error"}`);
            }
        }
    } catch (error) {
        console.error("Error during purchase:", error);
        alert("An error occurred while processing your purchase. Please try again.");
    }
}
