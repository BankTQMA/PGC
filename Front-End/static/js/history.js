document.addEventListener("DOMContentLoaded", async () => {
    const tableBody = document.getElementById("history-body");

    try {
        const response = await fetch("/api/my-history/", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            tableBody.innerHTML = `
                <tr><td colspan="7" class="empty">Please login to view your history.</td></tr>
            `;
            return;
        }

        const data = await response.json();

        if (data.length === 0) {
            tableBody.innerHTML = `
                <tr><td colspan="7" class="empty">No records found yet.</td></tr>
            `;
            return;
        }

        tableBody.innerHTML = "";

        data.forEach(item => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${item.id}</td>
                <td>${item.semester || "-"}</td>
                <td>${item.year || "-"}</td>
                <td>${item.gpa4.toFixed(2)}</td>
                <td>${item.total_gpa.toFixed(2)}</td>
                <td>${item.grade_letter}</td>
                <td>${new Date(item.created_at).toLocaleString()}</td>
            `;
            tableBody.appendChild(row);
        });

    } catch (error) {
        console.error("Error loading history:", error);
        tableBody.innerHTML = `
            <tr><td colspan="7" class="empty">Error loading data.</td></tr>
        `;
    }
});
