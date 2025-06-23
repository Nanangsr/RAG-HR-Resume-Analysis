// src/pages/AnalysisPage.jsx (FINAL VERSION)

import React, { useState } from 'react';
import axios from 'axios';
import AnalysisForm from '../components/AnalysisForm.jsx';
import ResultsDisplay from '../components/ResultsDisplay.jsx';
import { FileCheck2 } from 'lucide-react';

const API_URL = 'http://127.0.0.1:5000';

const AnalysisPage = () => {
    const [analysisResult, setAnalysisResult] = useState(null);
    const [currentUseCase, setCurrentUseCase] = useState('score');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');

    const handleAnalysisSubmit = async (formData) => {
        setIsLoading(true);
        setError('');
        setAnalysisResult(null);
        setCurrentUseCase(formData.useCase);
        
        const data = new FormData();
        let endpoint = '';

        // Router Logika untuk setiap Use Case
        switch (formData.useCase) {
            case 'score':
                endpoint = '/api/score';
                data.append('domain', formData.domain);
                data.append('criteria', JSON.stringify(formData.criteria));
                data.append('jd_text', formData.jobDescription || '');
                if (formData.resumes) {
                    for (const file of formData.resumes) { data.append('resume_files', file); }
                }
                break;
            case 'compare':
                endpoint = '/api/compare';
                data.append('domain', formData.domain);
                data.append('jd_text', formData.jobDescription || '');
                if (formData.resumes) {
                    for (const file of formData.resumes) { data.append('resume_files', file); }
                }
                break;
            case 'qa':
                endpoint = '/api/qa';
                data.append('domain', formData.domain);
                data.append('question', formData.question);
                if (formData.resumes) { data.append('resume_file', formData.resumes[0]); }
                break;
            case 'search':
                endpoint = '/api/search';
                data.append('domain', formData.domain);
                if (formData.jobDescriptionFile) { data.append('jd_file', formData.jobDescriptionFile); }
                break;
            default:
                setError('Use case tidak valid.');
                setIsLoading(false);
                return;
        }

        try {
          const fullUrl = `${API_URL}${endpoint}`;
          const response = await axios.post(fullUrl, data, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });
          setAnalysisResult(response.data);
        } catch (err) {
          const errorMessage = err.response?.data?.error || 'Terjadi kesalahan pada server atau jaringan.';
          setError(errorMessage);
        } finally {
          setIsLoading(false);
        }
    };

    return (
        <div className="analysis-page-main">
            <div className="form-column">
                <AnalysisForm onFormSubmit={handleAnalysisSubmit} isLoading={isLoading} />
            </div>
            <div className="results-column">
                {isLoading && <div className="status-info">Menganalisis... Ini mungkin memakan waktu beberapa saat.</div>}
                {error && <div className="status-info error">Error: {error}</div>}
                
                {!isLoading && !error && !analysisResult && (
                    <div className="results-placeholder">
                        <FileCheck2 size={48} strokeWidth={1} />
                        <p>Hasil analisis Anda akan muncul di sini.</p>
                    </div>
                )}
                
                {analysisResult && !error && (
                    <ResultsDisplay results={analysisResult} useCase={currentUseCase} />
                )}
            </div>
        </div>
    );
};

export default AnalysisPage;
