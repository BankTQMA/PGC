async function getValidToken() {
  let token = localStorage.getItem("access");
  const refresh = localStorage.getItem("refresh");
  if (!token) { window.location.href = "/login/"; return null; }

  const res = await fetch("/api/gpa-tracking/", { headers:{ Authorization:"Bearer "+token } });
  if (res.status===401 && refresh) {
    const refreshRes = await fetch("/api/auth/refresh/", {
      method:"POST", headers:{ "Content-Type":"application/json" },
      body:JSON.stringify({ refresh })
    });
    const data = await refreshRes.json();
    if (refreshRes.ok && data.access) { localStorage.setItem("access", data.access); token=data.access; }
    else { localStorage.clear(); window.location.href="/login/"; return null; }
  }
  return token;
}

document.addEventListener("DOMContentLoaded", async () => {
  const dropdown = document.getElementById("recordDropdown");
  const targetInput = document.getElementById("targetGPA");
  const calcBtn = document.getElementById("calcBtn");
  const resultDiv = document.getElementById("resultArea");

  const token = await getValidToken();
  const res = await fetch("/api/my-history/", { headers:{ Authorization:"Bearer "+token } });
  const data = await res.json();

  data.forEach(r=>{
    const opt=document.createElement("option");
    opt.value=r.id;
    opt.textContent=`ID ${r.id} — ${r.year}/${r.semester} (${r.grade_letter})`;
    dropdown.appendChild(opt);
  });

    calcBtn.addEventListener("click", async () => {
    console.log("Calculate clicked!");
    const id = dropdown.value;
    const target = parseFloat(targetInput.value);
    if(!id || isNaN(target)) { alert("Please select record and enter target GPA."); return; }

    const response = await fetch("/api/what-if/", {
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        Authorization:"Bearer "+token
      },
      body:JSON.stringify({ target_gpa4: target })
    });

    const result = await response.json();
    if (response.ok) {
      resultDiv.innerHTML = `
        <p><strong>Target GPA:</strong> ${target.toFixed(2)}</p>
        <p><strong>Required Average Percent:</strong> ${result.required_avg_percent}%</p>
        <p style="color:#007bff;font-weight:600;">You need to score around ${result.required_avg_percent}% in average to reach ${target.toFixed(2)} GPA.</p>
      `;
    } else {
      resultDiv.innerHTML = `<p style="color:red;">Error: ${result.detail || "Cannot calculate"}</p>`;
    }
  });
});


