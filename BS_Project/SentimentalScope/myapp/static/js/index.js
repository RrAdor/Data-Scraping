 // Initialize Sentiment Analysis Charts
        const ctx = document.getElementById('sentimentChart').getContext('2d');
        
        // Generate sample data
        const dates = Array.from({length: 7}, (_, i) => {
            const d = new Date();
            d.setDate(d.getDate() - (6 - i));
            return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
        });

        // Beautiful color palette
        const colors = {
            positive: '#00b4d8',
            neutral: '#90e0ef',
            negative: '#ff4d6d',
            positiveGradient: ['#00b4d8', '#90e0ef'],
            neutralGradient: ['#90e0ef', '#caf0f8'],
            negativeGradient: ['#ff4d6d', '#ffb3c1']
        };

        // Trend data
        const trendData = {
            positive: [65, 68, 72, 75, 70, 73, 78],
            neutral: [20, 18, 15, 14, 19, 16, 12],
            negative: [15, 14, 13, 11, 11, 11, 10]
        };

        // Create gradients
        const createGradient = (color1, color2) => {
            const gradient = ctx.createLinearGradient(0, 0, 0, 400);
            gradient.addColorStop(0, color1);
            gradient.addColorStop(1, color2);
            return gradient;
        };

        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'Positive Sentiment',
                        data: trendData.positive,
                        borderColor: colors.positive,
                        backgroundColor: createGradient(colors.positiveGradient[0] + '40', colors.positiveGradient[1] + '00'),
                        borderWidth: 3,
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: colors.positive,
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 6,
                        pointHoverRadius: 8
                    },
                    {
                        label: 'Neutral Sentiment',
                        data: trendData.neutral,
                        borderColor: colors.neutral,
                        backgroundColor: createGradient(colors.neutralGradient[0] + '40', colors.neutralGradient[1] + '00'),
                        borderWidth: 3,
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: colors.neutral,
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 6,
                        pointHoverRadius: 8
                    },
                    {
                        label: 'Negative Sentiment',
                        data: trendData.negative,
                        borderColor: colors.negative,
                        backgroundColor: createGradient(colors.negativeGradient[0] + '40', colors.negativeGradient[1] + '00'),
                        borderWidth: 3,
                        tension: 0.4,
                        fill: true,
                        pointBackgroundColor: colors.negative,
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 6,
                        pointHoverRadius: 8
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        labels: {
                            padding: 20,
                            boxWidth: 30,
                            color: 'rgba(255, 255, 255, 0.9)',
                            font: {
                                size: 13,
                                weight: '500'
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(255, 255, 255, 0.95)',
                        titleColor: '#000',
                        bodyColor: '#000',
                        bodyFont: {
                            size: 14
                        },
                        padding: 12,
                        boxWidth: 10,
                        usePointStyle: true,
                        borderColor: 'rgba(255, 255, 255, 0.2)',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.y + '%';
                            }
                        }
                    }
                },
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100,
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.8)',
                            padding: 10,
                            callback: function(value) {
                                return value + '%';
                            },
                            font: {
                                size: 12
                            }
                        }
                    },
                    x: {
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)',
                            drawBorder: false
                        },
                        ticks: {
                            color: 'rgba(255, 255, 255, 0.8)',
                            padding: 10,
                            font: {
                                size: 12
                            }
                        }
                    }
                },
                animation: {
                    duration: 2000,
                    easing: 'easeInOutQuart'
                },
                elements: {
                    line: {
                        borderWidth: 3
                    }
                }
            }
        });

        // Function to smoothly update chart data
        function updateChartData() {
            const newData = {
                positive: [],
                neutral: [],
                negative: []
            };

            // Generate smooth transitions for data
            chart.data.datasets.forEach((dataset, index) => {
                const dataKey = Object.keys(newData)[index];
                dataset.data.forEach(value => {
                    const change = Math.random() * 6 - 3; // Smaller range for smoother transitions
                    const newValue = Math.max(0, Math.min(100, value + change));
                    newData[dataKey].push(newValue);
                });
            });

            // Update datasets with new values
            chart.data.datasets[0].data = newData.positive;
            chart.data.datasets[1].data = newData.neutral;
            chart.data.datasets[2].data = newData.negative;

            // Smooth update animation
            chart.update('default');
        }

        // Update chart every 4 seconds for smoother visualization
        setInterval(updateChartData, 4000);

        // Reveal on scroll animation
        const observerOptions = {
            threshold: 0.2,
            rootMargin: '0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);

        document.querySelectorAll('.reveal-on-scroll').forEach(element => {
            observer.observe(element);
        });

        // Parallax effect for floating elements
        document.addEventListener('mousemove', (e) => {
            const floatItems = document.querySelectorAll('.float-item');
            const xAxis = (window.innerWidth / 2 - e.pageX) / 25;
            const yAxis = (window.innerHeight / 2 - e.pageY) / 25;
            
            floatItems.forEach((item) => {
                const speed = item.style.getPropertyValue('--delay').replace('s', '') || 1;
                item.style.transform = `translate(${xAxis * speed}px, ${yAxis * speed}px)`;
            });
        });

        // Image loading
        document.addEventListener('DOMContentLoaded', () => {
            const images = document.querySelectorAll('img');
            
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.addEventListener('load', () => img.classList.add('loaded'));
                        img.src = img.getAttribute('data-src') || img.src;
                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.01
            });

            images.forEach(img => {
                if (img.complete) {
                    img.classList.add('loaded');
                } else {
                    imageObserver.observe(img);
                }
            });

            // Smooth scrolling for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                });
            });

            // Add aria-expanded attribute to buttons when clicked
            const buttons = document.querySelectorAll('button');
            buttons.forEach(button => {
                button.addEventListener('click', () => {
                    const expanded = button.getAttribute('aria-expanded') === 'true';
                    button.setAttribute('aria-expanded', !expanded);
                });
            });
        });
    