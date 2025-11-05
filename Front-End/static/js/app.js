async function getValidToken() {
  let token = localStorage.getItem("access");
  const refresh = localStorage.getItem("refresh");

  if (!token) {
    window.location.href = "/login/";
    return null;
  }

  // ตรวจว่า access token ยังใช้ได้อยู่ไหม
  const res = await fetch("/api/gpa-tracking/", {
    headers: { Authorization: "Bearer " + token },
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
  // ---------- Year Dropdown ----------
  const yearSelect = document.getElementById("year-select");
  const currentYear = new Date().getFullYear();
  const startYear = 2020;
  for (let year = currentYear + 8; year >= startYear; year--) {
    const option = document.createElement("option");
    option.value = year;
    option.text = year;
    if (year === currentYear) option.selected = true;
    yearSelect.appendChild(option);
  }

  const calcGpaBtn = document.getElementById("calculate-gpa-btn");
  const addSubjectBtn = document.getElementById("add-subject-btn");
  const subjectListDiv = document.getElementById("dynamic-subject-list");
  const finalGpaDiv = document.getElementById("final-gpa");
  const row = document.createElement("div");
  row.className = "subject-row dynamic-row";
  const card = document.querySelector(".semester-card");

  // ---------- Add Subject Row ----------
  const addSubjectRow = () => {
    row.innerHTML = `
      <div class="subject-info">
        <input type="text" class="subject-name-input" placeholder="Subject Name">
        <input type="number" class="credit-input" placeholder="Credits" min="0.5" max="6" step="0.5">
        <input type="number" class="score-input" min="0" max="100" placeholder="Score">
      </div>
    `;
    subjectListDiv.appendChild(row);
    requestAnimationFrame(() => row.classList.add("show"));
    card.style.maxHeight = card.scrollHeight + "px";
  };

  addSubjectBtn.addEventListener("click", addSubjectRow);
  addSubjectRow();

  // ---------- Calculate Button ----------
  calcGpaBtn.addEventListener("click", async () => {
    const token = await getValidToken();
    if (!token) return;

    const subjectsList = [];
    const subjectRows = document.querySelectorAll(".dynamic-row");

    subjectRows.forEach((row) => {
      const name = row.querySelector(".subject-name-input").value.trim();
      const credit = parseFloat(row.querySelector(".credit-input").value);
      const score = parseFloat(row.querySelector(".score-input").value);
      if (name && !isNaN(score) && !isNaN(credit) && credit > 0) {
        subjectsList.push({
          subject_name: name,
          credit: credit,
          components: [
            { component_name: "Total", score: Number(score), weight: 100 },
          ],
        });
      }
    });

    if (!subjectsList.length) {
      finalGpaDiv.textContent = "Please add at least one valid subject.";
      finalGpaDiv.style.color = "red";
      return;
    }

    const semester = document.getElementById("semester-select").value;
    const year = parseInt(document.getElementById("year-select").value);

    const requestBody = { subjects: subjectsList, semester, year };
    finalGpaDiv.textContent = "Calculating...";
    finalGpaDiv.style.color = "#666";

    try {
      const response = await fetch("/api/calculate/post/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();
      console.log("Response:", data);

      if (response.ok) {
        finalGpaDiv.innerHTML = `
          <div style="
              color:#007bff;
              font-weight:600;
              font-size:1.3rem;
              text-align:center;
              margin-top:25px;
          ">
              GPA (4.0): ${data.GPA_4.toFixed(2)} |
              Percent: ${data.GPA_percent} |
              Grade: ${data.Grade}
          </div>
        `;
      } else {
        let errorMsg = data.detail || JSON.stringify(data);
        if (data.subjects) errorMsg = "Check subject data.";
        finalGpaDiv.textContent = `Error: ${errorMsg}`;
        finalGpaDiv.style.color = "red";
      }
    } catch (error) {
      console.error("Network Error:", error);
      finalGpaDiv.textContent = "A network error occurred.";
      finalGpaDiv.style.color = "red";
    }

    requestAnimationFrame(() => card.classList.add("show"));
    card.style.maxHeight = card.scrollHeight + "px";
  });
});
