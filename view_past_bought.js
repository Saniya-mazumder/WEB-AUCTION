document.addEventListener("DOMContentLoaded", async function () {
    const userId = localStorage.getItem("userId");  // Assuming user ID is stored on login
    if (!userId) {
        alert("User not logged in.");
        window.location.href = "auth.html";
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000/past-bought-items?user_id=${userId}`);
        const data = await response.json();
        
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
                <td>${new Date(item.purchase_date).toLocaleDateString()}</td>
            `;
            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("Error fetching data:", error);
        alert("Failed to load bought items.");
    }
});
