document.addEventListener("DOMContentLoaded", function () {
    // Gráfico de torta
    fetch('/api/estadisticas/temas')
        .then(res => res.json())
        .then(datos => {
            const labels = Object.keys(datos);
            const valores = Object.values(datos);

            new Chart(document.getElementById('graficoTorta'), {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Actividades por tema',
                        data: valores
                    }]
                },
                options: { 
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        });

    // Gráfico de líneas
    fetch('/api/estadisticas/dias_semana')
        .then(res => res.json())
        .then(datos => {
            const labels = Object.keys(datos);
            const valores = Object.values(datos);

            new Chart(document.getElementById('graficoLinea'), {
                type: 'line', 
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Actividades por día de la semana',
                        data: valores,
                        fill: false,
                        borderColor: 'blue',
                        tension: 0.3
                    }]
                },
                options: { 
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
        });

    // Gráfico de barras por mes y tramo
    fetch('/api/estadisticas/Meses')
        .then(res => res.json())
        .then(datos => {
            const labels = Object.keys(datos); // Meses
            const tramos = ['Mañana', 'Mediodía', 'Tarde'];

            const datasets = tramos.map(tramo => {
                return {
                    label: tramo,
                    data: labels.map(mes => datos[mes][tramo]),
                    backgroundColor: tramo === 'Mañana' ? 'rgba(255, 99, 132, 0.5)' :
                                      tramo === 'Mediodía' ? 'rgba(54, 162, 235, 0.5)' :
                                      'rgba(75, 192, 192, 0.5)',
                    borderColor: 'rgba(0,0,0,0.2)',
                    borderWidth: 1
                };
            });

            new Chart(document.getElementById('graficoMeses'), {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            });
        }); 
}); 
