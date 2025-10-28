// Run code after the page loads
document.addEventListener("DOMContentLoaded", () => {

    const calcGpaBtn = document.getElementById("calculate-gpa-btn");
    const finalGpaDiv = document.getElementById("final-gpa");
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Listen for button click
    calcGpaBtn.addEventListener("click", async () => {

        let subjectsList = [];

        // Find every single ".subject-row" on the page
        const subjectRows = document.querySelectorAll('.subject-row');

        // Loop over each row
        subjectRows.forEach(row => {
            const name = row.dataset.name;
            const credit = parseFloat(row.dataset.credit);
            
            // Get the user score from the input box
            const score = parseFloat(row.querySelector('.score-input').value);

            if (!isNaN(score)) {
                subjectsList.push({
                    name: name,
                    score: score,
                    credit: credit
                });
            }
        });

        // Send the data to the API

        const requestBody = {
            subjects: subjectsList
        };

        finalGpaDiv.textContent = "Calculating...";
        finalGpaDiv.style.color = "#666";

        try {
            const response = await fetch('/api/calculate/post/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken // Send the security token
                },
                body: JSON.stringify(requestBody)
            });

            const data = await response.json();

            if (response.ok) {
                // Show the result
                finalGpaDiv.textContent = `Your GPA: ${data.GPA} (Grade: ${data.Grade})`;
                finalGpaDiv.style.color = "#007bff";
            } else {
                finalGpaDiv.textContent = "Error";
                finalGpaDiv.style.color = "red";
            }

        } catch (error) {
            console.error("Error:", error);
            finalGpaDiv.textContent = "A network error occurred.";
            finalGpaDiv.style.color = "red";
        }
    });
}); 