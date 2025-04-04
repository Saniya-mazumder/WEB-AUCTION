document.addEventListener("DOMContentLoaded", async function () {
    const username = localStorage.getItem("username");  // Store username on login too
    if (!username) {
        alert("User not logged in.");
        window.location.href = "auth.html?type=buyer";
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/past-bought-items?username=${username}`);
        const data = await response.json();
        console.log(data);
        
        const tableBody = document.getElementById("bought-items");
        tableBody.innerHTML = ""; // Clear previous data

        if (data.length === 0) {
            tableBody.innerHTML = "<tr><td colspan='4'>No items bought yet.</td></tr>";
            return;
        }

        data.forEach(item => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${item.product_name}</td>
                <td>${item.price} USD</td>
                <td>${item.quantity}</td>
                <td>${item.purchase_date ? new Date(item.purchase_date).toLocaleDateString() : 'N/A'}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to load bought items.");
    }
});
