document.addEventListener("DOMContentLoaded", function () {
    fetchBuyers();
    fetchAuctionItems();
});

async function fetchBuyers() {
    try {
        const response = await fetch("http://127.0.0.1:5000/get-buyers");
        const buyers = await response.json();
        const buyerList = document.getElementById("buyer-list");
        
        buyers.forEach(buyer => {
            const li = document.createElement("li");
            li.textContent = buyer;
            buyerList.appendChild(li);
        });
    } catch (error) {
        console.error("Error fetching buyers:", error);
    }
}

async function fetchAuctionItems() {
    try {
        const response = await fetch("http://127.0.0.1:5000/get-items");
        const items = await response.json();
        const auctionContainer = document.getElementById("auction-container");
        
        items.forEach(item => {
            const box = document.createElement("div");
            box.classList.add("auction-box");
            
            box.innerHTML = `
                <h3>${item.name}</h3>
                <p>Quantity: ${item.quantity}</p>
                <p>Current Price: $<span id="price-${item.id}">${item.price}</span></p>
                <p>Ends in: ${item.duration} hrs</p>
                <button class="bid-btn" onclick="placeBid(${item.id}, ${item.price})">Bid</button>
            `;
            auctionContainer.appendChild(box);
        });
    } catch (error) {
        console.error("Error fetching auction items:", error);
    }
}

async function placeBid(itemId, currentPrice) {
    try {
        const newPrice = currentPrice + 100; // Increase by 100

        const response = await fetch("http://127.0.0.1:5000/place-bid", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ item_id: itemId, new_price: newPrice })
        });
        
        const result = await response.json();
        if (result.message) {
            document.getElementById(`price-${itemId}`).textContent = newPrice;
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error("Error placing bid:", error);
    }
}
