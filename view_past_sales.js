document.addEventListener("DOMContentLoaded", async function () {
    const username = localStorage.getItem("username");
    if (!username) {
        alert("User not logged in.");
        window.location.href = "auth.html?type=seller";
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/past-sold-items?username=${username}`);
        const data = await response.json();
        
        const tableBody = document.getElementById("sold-items");
        tableBody.innerHTML = ""; // Clear previous data

        if (data.length === 0) {
            tableBody.innerHTML = "<tr><td colspan='5'>No items sold yet.</td></tr>";
            return;
        }

        data.forEach(item => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${item.product_name}</td>
                <td>${item.price} USD</td>
                <td>${item.quantity}</td>
                <td>${item.buyer}</td>
                <td>${item.sold_date ? new Date(item.sold_date).toLocaleDateString() : 'N/A'}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to load sold items.");
    }
});
