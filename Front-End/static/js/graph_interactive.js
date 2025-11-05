// ---- token helper ----
async function getValidToken() {
  let token = localStorage.getItem("access");
  const refresh = localStorage.getItem("refresh");
  if (!token) { window.location.href="/login/"; return null; }

  const res = await fetch("/api/gpa-tracking/", { headers:{Authorization:"Bearer "+token} });
  if (res.status===401 && refresh) {
    const refreshRes = await fetch("/api/auth/refresh/",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({refresh})
    });
    const data=await refreshRes.json();
    if(refreshRes.ok&&data.access){localStorage.setItem("access",data.access);token=data.access;}
    else{localStorage.clear();window.location.href="/login/";return null;}
  }
  return token;
}

document.addEventListener("DOMContentLoaded", async () => {
  const ctx = document.getElementById("gpaChart").getContext("2d");
  const addBtn = document.getElementById("addRecord");
  const resetBtn = document.getElementById("resetGraph");
  const dropdown = document.getElementById("recordDropdown");
  const statusEl = document.getElementById("chartStatus");

  let chart;
  let records = [];

  // render chart with GPA only
  function renderChart() {
    if (chart) chart.destroy();
    if (!records.length) { statusEl.textContent="No records selected."; return; }

    records.sort((a,b)=>new Date(a.created_at)-new Date(b.created_at));

    const labels = records.map(r=>{
      const d=new Date(r.created_at);
      return `${d.toLocaleDateString("en-GB",{day:"2-digit",month:"short"})} (${r.semester}/${r.year})`;
    });
    const gpaValues = records.map(r=>r.gpa4);

    chart = new Chart(ctx,{
      type:"line",
      data:{
        labels,
        datasets:[{
          label:"GPA (4.0)",
          data:gpaValues,
          borderColor:"#007bff",
          backgroundColor:"#007bff33",
          tension:0.3,
          borderWidth:3,
          pointRadius:5,
        }]
      },
      options:{
        layout:{padding:{top:20,bottom:10}},
        responsive:true,
        plugins:{
          legend:{position:"top"},
          tooltip:{
            callbacks:{
              title:(items)=>items[0].label,
              label:(item)=>{
                const r=records[item.dataIndex];
                return `GPA: ${r.gpa4} | Grade: ${r.grade_letter} | Year ${r.year} Sem ${r.semester}`;
              }
            }
          }
        },
        scales:{
          y:{beginAtZero:true,max:4,title:{display:true,text:"GPA (4.0)"}},
          x:{
            ticks:{autoSkip:false,maxRotation:45,minRotation:0},
            title:{display:true,text:"Date (Semester/Year)"}
          }
        }
      }
    });

    statusEl.textContent=`Loaded ${records.length} record(s).`;
  }

  // load dropdown list
  async function loadDropdown() {
    const token = await getValidToken();
    if(!token) return;
    const res = await fetch("/api/my-history/",{
      headers:{Authorization:"Bearer "+token}
    });
    const data = await res.json();
    dropdown.innerHTML='<option value="">Select record from history</option>';
    data.forEach(r=>{
      const opt=document.createElement("option");
      opt.value=r.id;
      opt.textContent=`ID ${r.id} — ${r.year}/${r.semester} (${r.grade_letter})`;
      dropdown.appendChild(opt);
    });
  }

  // add record
  addBtn.addEventListener("click",async()=>{
    const id=dropdown.value;
    if(!id){alert("Select a record first.");return;}
    const token=await getValidToken(); if(!token)return;
    const res=await fetch(`/api/record/${id}/`,{headers:{Authorization:"Bearer "+token}});
    const data=await res.json();
    if(!res.ok){alert(data.error||"Record not found.");return;}
    if(records.some(r=>r.id==data.id)){alert("Already added.");return;}
    records.push(data);
    renderChart();
  });

  resetBtn.addEventListener("click",()=>{
    records=[];
    if(chart)chart.destroy();
    statusEl.textContent="Graph cleared.";
  });

  await loadDropdown();
  renderChart();
});
