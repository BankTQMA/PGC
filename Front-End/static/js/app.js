async function getValidToken() {
    let token = localStorage.getItem("access");
    const refresh = localStorage.getItem("refresh");

    if (!token) {
        window.location.href = "/login/";
        return null;
    }

    const res = await fetch("/api/gpa-tracking/", {
        headers: { "Authorization": "Bearer " + token },
    });

    if (res.status === 401 && refresh) {
        console.log("Access expired, trying refresh...");
        const refreshRes = await fetch("/api/auth/refresh/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh }),
        });

        const data = await refreshRes.json();
        if (refreshRes.ok && data.access) {
            localStorage.setItem("access", data.access);
            token = data.access;
        } else {
            console.log("Refresh token invalid. Redirecting...");
            localStorage.removeItem("access");
            localStorage.removeItem("refresh");
            window.location.href = "/login/";
            return null;
        }
    }

    return token;
}

document.addEventListener("DOMContentLoaded", () => {
    const yearSelect = document.getElementById("year-select");
    const currentYear = new Date().getFullYear();
    const startYear = 2020;
    for (let year = currentYear + 8; year >= startYear; year--) {
        const opt = document.createElement("option");
        opt.value = year;
        opt.text = year;
        if (year === currentYear) opt.selected = true;
        yearSelect.appendChild(opt);
    }

    const calcBtn = document.getElementById("calculate-gpa-btn");
    const addBtn = document.getElementById("add-subject-btn");
    const subjectListDiv = document.getElementById("dynamic-subject-list");
    const finalGpaDiv = document.getElementById("final-gpa");

    const addRow = () => {
        const div = document.createElement("div");
        div.className = "subject-row dynamic-row";
        div.innerHTML = `
            <div class="subject-info" style="display:flex; gap:10px; flex:1;">
                <input type="text" class="subject-name-input" placeholder="Subject Name"
                    style="width:60%; padding:10px; background:#f4f4f7; border:none; border-radius:8px;">
                <input type="number" class="credit-input" placeholder="Credits" min="0.5" max="6" step="0.5"
                    style="width:35%; padding:10px; background:#f4f4f7; border:none; border-radius:8px;">
            </div>
            <div class="subject-score">
                <input type="number" class="score-input" min="0" max="100" placeholder="Score"
                    style="width:100px; padding:10px; background:#f4f4f7; border:none; border-radius:8px;">
            </div>`;
        subjectListDiv.appendChild(div);
    };

    addBtn.addEventListener("click", addRow);
    addRow();
    calcBtn.addEventListener("click", async () => {
        const token = await getValidToken();
        if (!token) return;

        const subjectsList = [];
        const subjectRows = document.querySelectorAll(".dynamic-row");
        subjectRows.forEach(row => {
            const name = row.querySelector(".subject-name-input").value.trim();
            const credit = parseFloat(row.querySelector(".credit-input").value);
            const score = parseFloat(row.querySelector(".score-input").value);
            if (name && !isNaN(credit) && !isNaN(score)) {
                subjectsList.push({
                    subject_name: name,
                    credit: credit,
                    components: [{ component_name: "Total", score, weight: 100 }]
                });
            }
        });

        if (!subjectsList.length) {
            finalGpaDiv.textContent = "Please add at least one subject.";
            finalGpaDiv.style.color = "red";
            return;
        }

        const semester = document.getElementById("semester-select").value;
        const year = parseInt(document.getElementById("year-select").value);

        finalGpaDiv.textContent = "Calculating...";
        finalGpaDiv.style.color = "#777";

        try {
            const res = await fetch("/api/calculate/post/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    subjects: subjectsList,
                    semester,
                    year
                })
            });

            const data = await res.json();

            if (res.ok) {
                finalGpaDiv.innerHTML = `
                    <div style="text-align:center; color:#007bff; font-weight:600; font-size:1.2rem; margin-top:20px;">
                        GPA (4.0): ${data.GPA_4.toFixed(2)} |
                        Percent: ${data.GPA_percent} |
                        Grade: ${data.Grade}
                    </div>`;
            } else {
                finalGpaDiv.textContent = "Error: " + (data.detail || JSON.stringify(data));
                finalGpaDiv.style.color = "red";
            }
        } catch (err) {
            console.error("Network error:", err);
            finalGpaDiv.textContent = "Network error.";
            finalGpaDiv.style.color = "red";
        }
    });
});
