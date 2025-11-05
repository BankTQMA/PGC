async function getValidToken() {
  let token = localStorage.getItem("access");
  const refresh = localStorage.getItem("refresh");

  if (!token) {
    window.location.href = "/login/";
    return null;
  }

  const res = await fetch("/api/gpa-tracking/", {
    headers: { Authorization: "Bearer " + token },
  });

  if (res.status === 401 && refresh) {
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
      localStorage.clear();
      window.location.href = "/login/";
      return null;
    }
  }

  return token;
}

document.addEventListener("DOMContentLoaded", async () => {
  const dropdown = document.getElementById("recordDropdown");
  const targetInput = document.getElementById("targetGPA");
  const calcBtn = document.getElementById("calcBtn");
  const resultDiv = document.getElementById("resultArea");

  const token = await getValidToken();
  const res = await fetch("/api/my-history/", {
    headers: { Authorization: "Bearer " + token },
  });
  const data = await res.json();

  data.forEach((r) => {
    const opt = document.createElement("option");
    opt.value = r.id;
    opt.textContent = `ID ${r.id} — ${r.year}/${r.semester} (${r.grade_letter})`;
    dropdown.appendChild(opt);
  });

  calcBtn.addEventListener("click", async () => {
    console.log("Calculate clicked!");
    const id = dropdown.value;
    const target = parseFloat(targetInput.value);

    if (!id || isNaN(target)) {
      alert("Please select a record and enter target GPA.");
      return;
    }
    const selectedRecord = data.find((r) => r.id == id);
    if (!selectedRecord) {
      resultDiv.innerHTML = `<p style="color:red;">Record not found.</p>`;
      return;
    }

    const currentGPA = selectedRecord.gpa4;
    const currentPercent = selectedRecord.total_gpa; // ใช้จาก backend: percent (เช่น 67)

    if (currentGPA >= target) {
      resultDiv.innerHTML = `
        <p><strong>Target GPA:</strong> ${target.toFixed(2)}</p>
        <p style="color:green;font-weight:600;">You already hit the target! (Current GPA: ${currentGPA.toFixed(2)})</p>
      `;
      return;
    }

    const percentNeeded =
      currentPercent +
      ((target - currentGPA) / (4.0 - currentGPA)) * (100 - currentPercent);

    resultDiv.innerHTML = `
      <p><strong>Current GPA:</strong> ${currentGPA.toFixed(2)}</p>
      <p><strong>Target GPA:</strong> ${target.toFixed(2)}</p>
      <p><strong>Required Average Percent:</strong> ${percentNeeded.toFixed(
        2
      )}%</p>
      <p style="color:#007bff;font-weight:600;">
        You need to score around ${percentNeeded.toFixed(
          2
        )}% in average to reach ${target.toFixed(2)} GPA.
      </p>
    `;
  });
});
