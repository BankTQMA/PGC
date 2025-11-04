document.addEventListener("DOMContentLoaded", async () => {
    const tbody = document.getElementById("history-body");
    const token = localStorage.getItem("access");

    // ถ้าไม่มี token ให้เด้งกลับ login
    if (!token) {
        tbody.innerHTML = `
            <tr><td colspan="8" style="padding:20px; color:red;">Please log in to view your history.</td></tr>
        `;
        setTimeout(() => (window.location.href = "/login/"), 1000);
        return;
    }

    try {
        console.log("Fetching history with token:", token.substring(0, 20) + "...");

        const res = await fetch("/api/my-history/", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });

        console.log("Response status:", res.status);

        if (res.status === 401) {
            console.warn("Access token expired → trying refresh token...");

            // ใช้ refresh token ถ้ามี
            const refresh = localStorage.getItem("refresh");
            if (refresh) {
                const refreshRes = await fetch("/api/auth/refresh/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ refresh }),
                });
                const refreshData = await refreshRes.json();

                if (refreshData.access) {
                    localStorage.setItem("access", refreshData.access);
                    console.log("Token refreshed, reloading page...");
                    location.reload();
                    return;
                } else {
                    console.error("Refresh failed", refreshData);
                    window.location.href = "/login/";
                    return;
                }
            } else {
                window.location.href = "/login/";
                return;
            }
        }

        const data = await res.json();

        tbody.innerHTML = "";

        if (!res.ok) {
            tbody.innerHTML = `<tr><td colspan="8" style="padding:20px; color:red;">Error: ${data.detail || "Failed to fetch history."
                }</td></tr>`;
            return;
        }

        if (!data.length) {
            tbody.innerHTML = `<tr><td colspan="8" style="padding:20px; color:#777;">No records found.</td></tr>`;
            return;
        }

        data.forEach((item) => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${item.id}</td>
                <td>${item.semester}</td>
                <td>${item.year}</td>
                <td>${item.gpa4.toFixed(2)}</td>
                <td>${item.total_gpa.toFixed(2)}</td>
                <td>${item.grade_letter}</td>
                <td>${new Date(item.created_at).toLocaleString()}</td>
                <td><button class="view-btn">View</button></td>
            `;
            tbody.appendChild(row);

            const detailRow = document.createElement("tr");
            detailRow.classList.add("details-row");
            detailRow.innerHTML = `
                <td colspan="8">
                    <div class="details-box" style="display:none;">
                        <strong>Subjects in this GPA calculation:</strong>
                        <table>
                            <thead>
                                <tr><th>Subject Name</th><th>Score (%)</th><th>Credit</th></tr>
                            </thead>
                            <tbody>
                                ${item.subjects
                    .map(
                        (s) =>
                            `<tr><td>${s.subject_name}</td><td>${s.score.toFixed(
                                2
                            )}</td><td>${s.credit}</td></tr>`
                    )
                    .join("")}
                            </tbody>
                        </table>
                    </div>
                </td>
            `;
            tbody.appendChild(detailRow);

            const btn = row.querySelector(".view-btn");
            const box = detailRow.querySelector(".details-box");
            btn.addEventListener("click", () => {
                const isHidden = box.style.display === "none";
                box.style.display = isHidden ? "block" : "none";
                btn.textContent = isHidden ? "Hide" : "View";
            });
        });
    } catch (err) {
        console.error("Error fetching history:", err);
        tbody.innerHTML = `<tr><td colspan="8" style="padding:20px; color:red;">Failed to load history.</td></tr>`;
    }
});
