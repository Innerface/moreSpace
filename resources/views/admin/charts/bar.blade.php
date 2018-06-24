<canvas id="chartBar" width="400" height="400"></canvas>
<canvas id="chartLine" width="400" height="400"></canvas>
<canvas id="chartRadar" width="400" height="400"></canvas>
<canvas id="chartPolar" width="400" height="400"></canvas>
<canvas id="chartPie" width="400" height="400"></canvas>
<canvas id="chartDoughnut" width="400" height="400"></canvas>
<canvas id="chartBubble" width="400" height="400"></canvas>
<canvas id="chartScatter" width="400" height="400"></canvas>
<script>

    $(function () {
        var ctxBar = document.getElementById("chartBar").getContext('2d');
        var chartBar = new Chart(ctxBar, {
            type: 'bar',
            data: {
                labels: ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"],
                datasets: [{
                    label: '# of Votes',
                    data: [12, 19, 3, 5, 2, 3],
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255,99,132,1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

        var ctxLine = document.getElementById("chartLine").getContext('2d');
        var chartLine = new Chart(ctxLine, {
            type: 'line',
            data: {
                labels: ["January", "February", "March", "April", "May", "June", "July"],
                datasets: [
                    {
                        label: "My First dataset",
                        fillColor: "rgba(220,0,220,0.2)",
                        strokeColor: "rgba(220,0,220,1)",
                        pointColor: "rgba(220,0,220,1)",
                        pointStrokeColor: "#f7f",
                        pointHighlightFill: "#7ff",
                        pointHighlightStroke: "rgba(220,0,220,1)",
                        data: [65, 59, 80, 81, 56, 55, 40]
                    },
                    {
                        label: "My Second dataset",
                        fillColor: "rgba(1,187,205,0.2)",
                        strokeColor: "rgba(1,187,205,1)",
                        pointColor: "rgba(1,187,205,1)",
                        pointStrokeColor: "#ff7",
                        pointHighlightFill: "#7ff",
                        pointHighlightStroke: "rgba(1,187,205,1)",
                        data: [28, 48, 40, 19, 86, 27, 90]
                    }]
            },
            options: {
                responsive: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

        var ctxRadar = document.getElementById("chartRadar").getContext('2d');
        var chartRadar = new Chart(ctxRadar, {
            type: 'radar',
            data: {
                labels: ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"],
                datasets: [
                    {
                        label: "My First dataset",
                        fillColor: "rgba(220,0,0,0.2)",
                        strokeColor: "rgba(220,0,220,1)",
                        pointColor: "rgba(220,0,220,1)",
                        pointStrokeColor: "#f1f",
                        pointHighlightFill: "#f1f",
                        pointHighlightStroke: "rgba(220,0,220,1)",
                        data: [65, 59, 90, 81, 56, 55, 40]
                    },
                    {
                        label: "My Second dataset",
                        fillColor: "rgba(1,187,205,0.2)",
                        strokeColor: "rgba(1,187,205,1)",
                        pointColor: "rgba(1,187,205,1)",
                        pointStrokeColor: "#ff1",
                        pointHighlightFill: "#ff1",
                        pointHighlightStroke: "rgba(1,187,205,1)",
                        data: [28, 48, 40, 19, 96, 27, 100]
                    }]
            },
            options: {
                responsive: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

        var ctxPolar = document.getElementById("chartPolar").getContext('2d');
        var chartPolar = new Chart(ctxPolar, {
            type: 'polarArea',
            data: {
                datasets: [{
                    data: [10, 20, 30]
                }],

                // These labels appear in the legend and in the tooltips when hovering different arcs
                labels: [
                    'Red',
                    'Yellow',
                    'Blue'
                ]
            },
            options: {
                responsive: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

        var ctxPie = document.getElementById("chartPie").getContext('2d');
        var chartPie = new Chart(ctxPie, {
            type: 'pie',
            data: {
                datasets: [{
                    data: [10, 20, 30]
                }],

                // These labels appear in the legend and in the tooltips when hovering different arcs
                labels: [
                    'Red',
                    'Yellow',
                    'Blue'
                ]
            },
            options: {
                responsive: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

        var ctxDoughnut = document.getElementById("chartDoughnut").getContext('2d');
        var chartDoughnut = new Chart(ctxDoughnut, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [10, 20, 30]
                }],

                // These labels appear in the legend and in the tooltips when hovering different arcs
                labels: [
                    'Red',
                    'Yellow',
                    'Blue'
                ]
            },
            options: {
                responsive: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

        var ctxBubble = document.getElementById("chartBubble").getContext('2d');
        var chartBubble = new Chart(ctxBubble, {
            type: 'bubble',
            data: [{
                x:7,
                y:5,
                r:3
            },{
                x:2,
                y:4,
                r:1
            }
            ],
            options: {
                responsive: false,
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });

        var ctxScatter = document.getElementById("chartScatter").getContext('2d');
        var scatterChart = new Chart(ctxScatter, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Scatter Dataset',
                    data: [{
                        x: -10,
                        y: 0
                    }, {
                        x: 0,
                        y: 10
                    }, {
                        x: 10,
                        y: 5
                    }]
                }]
            },
            options: {
                responsive: false,
                scales: {
                    xAxes: [{
                        type: 'linear',
                        position: 'bottom'
                    }]
                }
            }
        });
    });
</script>