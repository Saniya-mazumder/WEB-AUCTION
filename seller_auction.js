document.addEventListener("DOMContentLoaded", function () {
    fetchSellerAuctions();
});

async function fetchSellerAuctions() {
    try {
        const response = await fetch("http://127.0.0.1:5000/get-items");
        const items = await response.json();
        const auctionContainer = document.getElementById("seller-auction-container");
        
        items.forEach(item => {
            const box = document.createElement("div");
            box.classList.add("auction-box");
            
            box.innerHTML = `
                <h3>${item.name}</h3>
                <p>Quantity: ${item.quantity}</p>
                <p>Current Price: $<span id="price-${item.id}">${item.price}</span></p>
                <p>Highest Bidder: <span id="bidder-${item.id}">${item.highest_bidder || 'None'}</span></p>
                <p>Ends in: ${item.duration} hrs</p>
                <button class="approve-btn" onclick="approveBid(${item.id})" ${item.highest_bidder ? '' : 'disabled'}>Approve Bid</button>
            `;
            auctionContainer.appendChild(box);
        });
    } catch (error) {
        console.error("Error fetching seller auctions:", error);
    }
}

async function approveBid(itemId) {
    try {
        const response = await fetch("http://127.0.0.1:5000/approve-bid", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ item_id: itemId })
        });
        
        const result = await response.json();
        if (result.message) {
            alert("Bid approved successfully!");
            location.reload();
        } else {
            alert("Error: " + result.error);
        }
    } catch (error) {
        console.error("Error approving bid:", error);
    }
}
