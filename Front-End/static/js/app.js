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
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // function to add a new row 
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

    calcGpaBtn.addEventListener("click", async () => {

        let subjectsList = [];

        // Find every .dynamic-row on the page
        const subjectRows = document.querySelectorAll('.dynamic-row');

        subjectRows.forEach(row => {
            const name = row.querySelector('.subject-name-input').value;
            const credit = parseFloat(row.querySelector('.credit-input').value);
            const score = parseFloat(row.querySelector('.score-input').value);

            if (name && !isNaN(score) && !isNaN(credit) && credit > 0) {
                subjectsList.push({
                    name: name,
                    score: score,
                    credit: credit
                });
            }
        });

        if (subjectsList.length === 0) {
            finalGpaDiv.textContent = "Please add at least one valid subject.";
            finalGpaDiv.style.color = "red";
            return;
        }

        const semester = document.getElementById('semester-select').value;
        const year = parseInt(document.getElementById('year-select').value);

        // Send the data to the API
        const requestBody = {
            subjects: subjectsList,
            semester: semester,
            year: year
        };

        finalGpaDiv.textContent = "Calculating...";
        finalGpaDiv.style.color = "#666";

        try {
            const response = await fetch('/api/calculate/post/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(requestBody)
            });

            const data = await response.json();

            if (response.ok) {
                finalGpaDiv.textContent = `GPA: ${data.GPA_percent} (Grade: ${data.Grade})`;
                finalGpaDiv.style.color = "#007bff";
            } else {
                let errorMsg = data.detail || "Error";
                if (data.subjects) errorMsg = "Check subject data.";
                finalGpaDiv.textContent = `Error: ${errorMsg}`;
                finalGpaDiv.style.color = "red";
            }

        } catch (error) {
            console.error("Error:", error);
            finalGpaDiv.textContent = "A network error occurred.";
            finalGpaDiv.style.color = "red";
        }
    });
});