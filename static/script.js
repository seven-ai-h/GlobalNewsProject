fetch("/api/data")
  .then(response => response.json())
  .then(data => {
    // SENTIMENT CHART
    const counts = { Positive: 0, Neutral: 0, Negative: 0 };
    data.forEach(d => {
      if (counts[d.sentiment]) counts[d.sentiment]++;
      else counts[d.sentiment] = 1;
    });

    const ctx = document.getElementById("sentimentChart").getContext("2d");
    new Chart(ctx, {
      type: "bar",
      data: {
        labels: Object.keys(counts),
        datasets: [{
          label: "Sentiment Count",
          data: Object.values(counts),
          backgroundColor: ["#4caf50", "#ffeb3b", "#f44336"]
        }]
      },
      options: {
        scales: { y: { beginAtZero: true } }
      }
    });

    // DATA TABLE
    const table = document.getElementById("dataTable");
    data.forEach(row => {
      table.innerHTML += `
        <tr class="hover:bg-gray-100">
          <td class="p-3">${row.text}</td>
          <td class="p-3">${row.language}</td>
          <td class="p-3">${row.sentiment}</td>
          <td class="p-3">${row.keywords}</td>
        </tr>`;
    });
  });
