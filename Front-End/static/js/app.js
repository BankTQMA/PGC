// Run code after the page loads
document.addEventListener("DOMContentLoaded", () => {
  // Year Dropdown
  const yearSelect = document.getElementById("year-select");
  const currentYear = new Date().getFullYear();
  const startYear = 2020;
  for (let year = currentYear + 8; year >= startYear; year--) {
    const option = document.createElement("option");
    option.value = year;
    option.text = year;
    if (year === currentYear) {
      option.selected = true;
    }
    yearSelect.appendChild(option);
  }

  const calcGpaBtn = document.getElementById("calculate-gpa-btn");
  const addSubjectBtn = document.getElementById("add-subject-btn");
  const subjectListDiv = document.getElementById("dynamic-subject-list");
  const finalGpaDiv = document.getElementById("final-gpa");
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

  // Function to add a new row
  const addSubjectRow = () => {
    const row = document.createElement("div");
    row.className = "subject-row dynamic-row";

    row.innerHTML = `
            <div class="subject-info" style="flex-grow: 1; display: flex; gap: 10px;">
                <input type="text" class="subject-name-input" placeholder="Subject Name" style="width: 60%; padding: 10px; border: none; background: #f4f4f7; border-radius: 8px; font-size: 1rem;">
                <input type="number" class="credit-input" placeholder="Credits" min="0.5" max="6" step="0.5" style="width: 35%; padding: 10px; border: none; background: #f4f4f7; border-radius: 8px; font-size: 1rem; text-align: center;">
            </div>
            <div class="subject-score">
                <input type="number" class="score-input" min="0" max="100" placeholder="Score" style="width: 100px; padding: 10px; border: none; background: #f4f4f7; border-radius: 8px; font-size: 1rem; text-align: center;">
            </div>
        `;
    subjectListDiv.appendChild(row);
  };

  // Listen for 'Add Subject' button click
  addSubjectBtn.addEventListener("click", addSubjectRow);

  // Add one row to start with
  addSubjectRow();

  // Main calculate button
  calcGpaBtn.addEventListener("click", async () => {
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
            {
              component_name: "Total",
              score: Number(score),
              weight: 100,
            },
          ],
        });
      }
    });

    if (subjectsList.length === 0) {
      finalGpaDiv.textContent = "Please add at least one valid subject.";
      finalGpaDiv.style.color = "red";
      return;
    }

    const semester = document.getElementById("semester-select").value;
    const year = parseInt(document.getElementById("year-select").value);

    const requestBody = { subjects: subjectsList, semester, year };

    console.log("Sending request:", requestBody);

    finalGpaDiv.textContent = "Calculating...";
    finalGpaDiv.style.color = "#666";

    try {
      const response = await fetch("/api/calculate/post/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();
      console.log("Response:", data);

      if (response.ok) {
        finalGpaDiv.innerHTML = `
                    <div style="
                        color: #007bff;
                        font-weight: 600;
                        font-size: 1.3rem;
                        text-align: center;
                        margin-top: 25px;
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
  });
});
