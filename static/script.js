document.getElementById("uploadForm").addEventListener("submit", async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file to upload.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/classify/", {
            method: "POST",
            body: formData,
        });

        if (!response.ok) {
            throw new Error("Failed to classify logs");
        }

        const data = await response.json();

        // Show results section
        document.getElementById("resultsSection").classList.remove("d-none");

        // Update summary
        document.getElementById("totalLogs").textContent = data.summary.total_logs;
        document.getElementById("labelDistribution").textContent = Object.entries(data.summary.label_distribution)
            .map(([label, count]) => `${label}: ${count}`)
            .join(", ");

        // Render pie chart
        const ctx = document.getElementById('pieChart').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: Object.keys(data.summary.label_distribution),
                datasets: [{
                    label: 'Log Distribution',
                    data: Object.values(data.summary.label_distribution),
                    backgroundColor: ['#ff6384', '#36a2eb', '#ffce56']
                }]
            }
        });

        // Populate table
        const tableBody = document.getElementById("logTableBody");
        tableBody.innerHTML = ""; // Clear previous data
        data.logs.forEach(log => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${log.source}</td>
                <td>${log.log_message}</td>
                <td><span class="badge bg-${log.target_label === 'Error' ? 'danger' : log.target_label === 'Warning' ? 'warning' : 'success'}">${log.target_label}</span></td>
            `;
            tableBody.appendChild(row);
        });

        // Download button
        document.getElementById("downloadBtn").addEventListener("click", () => {
            window.location.href = "/resources/output.csv";
        });
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while processing the file.");
    }
});