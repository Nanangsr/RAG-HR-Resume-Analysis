// src/components/DataVisualization.jsx

import React from 'react';
import { Bar, Radar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  RadialLinearScale,
  PointElement,
  LineElement,
  Filler,
} from 'chart.js';

ChartJS.register(
  CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend,
  RadialLinearScale, PointElement, LineElement, Filler
);

function DataVisualization({ ranking }) {
  if (!ranking || ranking.length === 0) {
    return <p>Data tidak cukup untuk visualisasi.</p>;
  }

  // Data untuk Bar Chart (Skor AI semua kandidat)
  const barChartData = {
    labels: ranking.map(c => c.name),
    datasets: [{
      label: 'Skor AI',
      data: ranking.map(c => c.ai_score),
      backgroundColor: 'rgba(124, 93, 250, 0.6)',
      borderColor: 'rgba(124, 93, 250, 1)',
      borderWidth: 1,
    }],
  };
  
  const barChartOptions = {
    responsive: true,
    plugins: {
      legend: { position: 'top' },
      title: { display: true, text: 'Perbandingan Skor AI Kandidat' },
    },
    scales: { y: { beginAtZero: true, max: 100 } },
  };

  // Data untuk Radar Chart (Top 3 kandidat)
  const top3 = ranking.slice(0, 3);
  const criteriaLabels = top3.length > 0 ? Object.keys(top3[0].scores) : [];
  const radarColors = [
    'rgba(124, 93, 250, 0.4)', // ungu
    'rgba(129, 199, 132, 0.4)', // hijau
    'rgba(255, 204, 128, 0.4)', // oranye
  ];
   const radarBorderColors = [
    'rgba(124, 93, 250, 1)',
    'rgba(129, 199, 132, 1)',
    'rgba(255, 204, 128, 1)',
  ];

  const radarChartData = {
    labels: criteriaLabels,
    datasets: top3.map((candidate, index) => ({
      label: candidate.name,
      data: criteriaLabels.map(label => candidate.scores[label]),
      backgroundColor: radarColors[index],
      borderColor: radarBorderColors[index],
      borderWidth: 2,
      pointBackgroundColor: radarBorderColors[index],
    })),
  };

  const radarChartOptions = {
    responsive: true,
    plugins: {
      title: { display: true, text: 'Perbandingan Kompetensi Top 3 Kandidat' },
    },
    scales: {
      r: {
        angleLines: { color: 'rgba(255, 255, 255, 0.2)' },
        grid: { color: 'rgba(255, 255, 255, 0.2)' },
        pointLabels: { font: { size: 12 } },
        ticks: { backdropColor: 'rgba(0,0,0,0.8)' },
        suggestedMin: 0,
        suggestedMax: 10
      }
    }
  };


  return (
    <div className="visualization-section">
      <h4>Visualisasi Data</h4>
      <div className="visualization-grid">
        <div className="chart-container">
            <Bar options={barChartOptions} data={barChartData} />
        </div>
        {top3.length >= 2 && (
             <div className="chart-container">
                <Radar data={radarChartData} options={radarChartOptions} />
            </div>
        )}
      </div>
    </div>
  );
}

export default DataVisualization;