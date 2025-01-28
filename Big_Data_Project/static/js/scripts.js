const fetchChartData = async (endpoint, chartConfig) => {
    const response = await fetch(endpoint);
    const data = await response.json();
    const ctx = document.getElementById(chartConfig.id).getContext('2d');
    new Chart(ctx, {
        type: chartConfig.type,
        data: {
            labels: data.map(item => item[chartConfig.labelField]),
            datasets: [{
                label: chartConfig.datasetLabel,
                data: data.map(item => item[chartConfig.dataField]),
                backgroundColor: chartConfig.backgroundColor,
                borderColor: chartConfig.borderColor,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'top' },
                title: { display: true, text: chartConfig.title }
            }
        }
    });
};

const chartConfigs = [
    { id: 'annualTrendsChart', type: 'line', endpoint: '/api/annual_trends', labelField: 'Year', dataField: 'Total_Crimes', datasetLabel: 'Total Crimes', backgroundColor: 'rgba(75, 192, 192, 0.5)', borderColor: 'rgba(75, 192, 192, 1)', title: 'Annual Crime Trends' },
    { id: 'arrestRateCrimeChart', type: 'bar', endpoint: '/api/arrest_rate_crime', labelField: 'Crime_Type', dataField: 'Arrest_Rate', datasetLabel: 'Arrest Rate', backgroundColor: 'rgba(255, 99, 132, 0.5)', borderColor: 'rgba(255, 99, 132, 1)', title: 'Arrest Rates by Crime Type' },
    { id: 'hourlyCrimeChart', type: 'bar', endpoint: '/api/hourly_crime', labelField: 'Hour', dataField: 'Crime_Count', datasetLabel: 'Hourly Crimes', backgroundColor: 'rgba(153, 102, 255, 0.5)', borderColor: 'rgba(153, 102, 255, 1)', title: 'Hourly Crime Distribution' },
    { id: 'dayOfWeekChart', type: 'bar', endpoint: '/api/day_of_week', labelField: 'Day', dataField: 'Crime_Count', datasetLabel: 'Crimes by Day', backgroundColor: 'rgba(54, 162, 235, 0.5)', borderColor: 'rgba(54, 162, 235, 1)', title: 'Crime Trends by Day of Week' },
    { id: 'crimeTypeChart', type: 'pie', endpoint: '/api/crime_type', labelField: 'Crime_Type', dataField: 'Crime_Count', datasetLabel: 'Crime Types', backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'], borderColor: '#fff', title: 'Crime Type Distribution' },
    { id: 'crimeByMonthChart', type: 'line', endpoint: '/api/crime_by_month', labelField: 'Month', dataField: 'Crime_Count', datasetLabel: 'Monthly Crimes', backgroundColor: 'rgba(255, 206, 86, 0.5)', borderColor: 'rgba(255, 206, 86, 1)', title: 'Crime by Month' },
    { id: 'communityByCrimeChart', type: 'bar', endpoint: '/api/community_by_crime', labelField: 'Community', dataField: 'Crime_Count', datasetLabel: 'Community Crimes', backgroundColor: 'rgba(75, 192, 192, 0.5)', borderColor: 'rgba(75, 192, 192, 1)', title: 'Community by Crime' },
];

chartConfigs.forEach(config => fetchChartData(config.endpoint, config));
