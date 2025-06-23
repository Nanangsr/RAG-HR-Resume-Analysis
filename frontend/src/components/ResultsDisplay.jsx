// src/components/ResultsDisplay.jsx

import React, { useState } from 'react';
import DataVisualization from './DataVisualization.jsx';
import { exportToCSV, exportToJSON } from '../utils/export';
import { Download } from 'lucide-react';
import './ResultsDisplay.css';

const TabButton = ({ children, onClick, isActive }) => (
    <button className={`tab-button ${isActive ? 'active' : ''}`} onClick={onClick}>
        {children}
    </button>
);

function ResultsDisplay({ results, useCase }) {
  const [activeTab, setActiveTab] = useState('ranking');

  if (!results) return null;
  
  // Menangani hasil yang berbeda dari setiap use case
  if (useCase === 'qa' || useCase === 'search' || useCase === 'compare') {
      return (
        <div className="results-container">
            <div className="tab-content">
                <div className="narrative-section">
                    <h4>Hasil Analisis</h4>
                    {/* Hasil dari QA, search, compare biasanya berupa teks naratif panjang */}
                    {typeof results.answer === 'string' ? results.answer.split('\n').map((p, i) => <p key={i}>{p}</p>) :
                     typeof results.results === 'string' ? results.results.split('\n').map((p, i) => <p key={i}>{p}</p>) :
                     <pre>{JSON.stringify(results, null, 2)}</pre>
                    }
                </div>
            </div>
        </div>
      )
  }

  // Tampilan lengkap untuk use case 'score'
  if (useCase === 'score' && results.ranking) {
    const { ranking, narrative_analysis, criteria } = results;
    
    return (
        <div className="results-container">
            <div className="tabs-container">
                <TabButton isActive={activeTab === 'ranking'} onClick={() => setActiveTab('ranking')}>🏆 Peringkat</TabButton>
                <TabButton isActive={activeTab === 'viz'} onClick={() => setActiveTab('viz')}>📊 Visualisasi</TabButton>
                <TabButton isActive={activeTab === 'narrative'} onClick={() => setActiveTab('narrative')}>📝 Analisis AI</TabButton>
                <div className="export-buttons">
                    <button onClick={() => exportToCSV(results)} className="export-btn">
                        <Download size={16} /> CSV
                    </button>
                    <button onClick={() => exportToJSON(results)} className="export-btn">
                        <Download size={16} /> JSON
                    </button>
                </div>
            </div>
            <div className="tab-content">
                {activeTab === 'ranking' && (
                    <div className="ranking-section">
                        <h4>Tabel Peringkat Kandidat</h4>
                        <div className="table-wrapper">
                          <table>
                            <thead>
                                <tr>
                                    <th>Rank</th>
                                    <th>Nama</th>
                                    <th>Level</th>
                                    <th>Skor AI</th>
                                    {Object.keys(criteria).map(key => <th key={key}>{key}</th>)}
                                </tr>
                            </thead>
                            <tbody>
                                {ranking.map((candidate) => (
                                    <tr key={candidate.candidate_id}>
                                        <td className="rank-cell">{candidate.rank}</td>
                                        <td className="name-cell">{candidate.name}</td>
                                        <td className="level-cell">{candidate.level}</td>
                                        <td className="score-cell">{candidate.ai_score.toFixed(1)}</td>
                                        {Object.keys(criteria).map(criterion => (
                                            <td key={`${candidate.candidate_id}-${criterion}`}>
                                                {candidate.scores[criterion] ? candidate.scores[criterion].toFixed(1) : 'N/A'}
                                            </td>
                                        ))}
                                    </tr>
                                ))}
                            </tbody>
                          </table>
                        </div>
                    </div>
                )}
                {activeTab === 'viz' && <DataVisualization ranking={ranking} />}
                {activeTab === 'narrative' && (
                    <div className="narrative-section">
                        <h4>Analisis Naratif Mendalam</h4>
                        {narrative_analysis.split('\n').map((paragraph, index) => (
                            <p key={index}>{paragraph}</p>
                        ))}
                    </div>
                )}
            </div>
             <details className="raw-json-details">
                <summary>Lihat Data Mentah (JSON)</summary>
                <pre>{JSON.stringify(results, null, 2)}</pre>
            </details>
        </div>
    );
  }

  return null; // Fallback jika format data tidak sesuai
}

export default ResultsDisplay;