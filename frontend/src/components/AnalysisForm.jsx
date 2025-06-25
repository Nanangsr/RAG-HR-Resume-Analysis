import React, { useState, useEffect } from 'react';
import './AnalysisForm.css';

const domainCriteriaConfig = {
    General: { "Professional Skills": 8, "Work Experience": 8, "Education": 7, "Leadership": 7, "Communication": 8, "Problem Solving": 7 },
    IT: { "Technical Skills": 9, "Problem Solving": 8, "Work Experience": 8, "Education": 6, "Certifications": 7, "Project Management": 6 },
    HR: { "People Management": 9, "Communication": 8, "Work Experience": 8, "Education": 7, "Certifications": 6, "Strategic Thinking": 7 },
    Finance: { "Analytical Skills": 9, "Attention to Detail": 8, "Work Experience": 8, "Education": 8, "Certifications": 9, "Compliance Knowledge": 7 },
    Marketing: { "Creativity": 8, "Digital Skills": 8, "Communication": 9, "Work Experience": 7, "Education": 6, "Data Analysis": 7 },
    Sales: { "Relationship Building": 9, "Communication": 9, "Achievement Record": 8, "Work Experience": 8, "Negotiation Skills": 7, "Industry Knowledge": 6 },
    Operations: { "Process Improvement": 8, "Leadership": 8, "Problem Solving": 8, "Work Experience": 8, "Education": 6, "Project Management": 9 },
};

const useCaseConfig = {
    score: { title: "Beri Skor & Ranking Kandidat", resumeLabel: "Unggah 2+ Resume", allowMultiple: true, needsJd: true, needsQuestion: false, needsCriteria: true },
    compare: { title: "Bandingkan Kandidat (Analisis Teks)", resumeLabel: "Unggah 2+ Resume", allowMultiple: true, needsJd: true, needsQuestion: false, needsCriteria: false },
    qa: { title: "Tanya Jawab (QA) per Resume", resumeLabel: "Unggah 1 Resume", allowMultiple: false, needsJd: false, needsQuestion: true, needsCriteria: false },
    search: { title: "Cari Kandidat via Job Desc", resumeLabel: "", allowMultiple: false, needsJd: true, needsQuestion: false, needsCriteria: false },
};

function AnalysisForm({ onFormSubmit, isLoading }) {
  const [useCase, setUseCase] = useState('score');
  const [domain, setDomain] = useState('General');
  const [criteria, setCriteria] = useState(domainCriteriaConfig.General);
  const [resumes, setResumes] = useState(null);
  const [jobDescriptionFile, setJobDescriptionFile] = useState(null);
  const [question, setQuestion] = useState('');

  useEffect(() => {
    setCriteria(domainCriteriaConfig[domain] || domainCriteriaConfig.General);
  }, [domain]);

  const handleCriteriaChange = (key, value) => {
    setCriteria(prev => ({ ...prev, [key]: parseInt(value, 10) }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onFormSubmit({ useCase, resumes, jobDescriptionFile, question, domain, criteria });
  };

  const currentConfig = useCaseConfig[useCase];

  return (
    <div className="form-container">
      <h3>Kontrol Analisis</h3>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="use-case-select">1. Pilih Use Case</label>
          <select id="use-case-select" value={useCase} onChange={(e) => setUseCase(e.target.value)} disabled={isLoading}>
            {Object.entries(useCaseConfig).map(([key, config]) => (
                <option key={key} value={key}>{config.title}</option>
            ))}
          </select>
        </div>
        
        <div className="form-group">
            <label htmlFor="domain-select">2. Pilih Domain Industri</label>
            <select id="domain-select" value={domain} onChange={(e) => setDomain(e.target.value)} disabled={isLoading}>
                {Object.keys(domainCriteriaConfig).map(domainName => (
                    <option key={domainName} value={domainName}>{domainName}</option>
                ))}
            </select>
        </div>

        {currentConfig.needsCriteria && (
            <details className="form-group criteria-expander">
                <summary>⚙️ Konfigurasi Kriteria Penilaian</summary>
                <div className="criteria-grid">
                    {Object.entries(criteria).map(([key, value]) => (
                        <div className="slider-group" key={key}>
                            <label htmlFor={key}><span>{key}</span> <span>{value}</span></label>
                            <input type="range" id={key} min="1" max="10" value={value} onChange={(e) => handleCriteriaChange(key, e.target.value)} disabled={isLoading}/>
                        </div>
                    ))}
                </div>
            </details>
        )}

        {currentConfig.needsJd && (
            <div className="form-group">
              <label htmlFor="jd-upload">3. Unggah Job Description</label>
              <input type="file" id="jd-upload" onChange={(e) => setJobDescriptionFile(e.target.files[0])} accept=".pdf,.docx" required={useCase === 'search'} disabled={isLoading}/>
            </div>
        )}

        {currentConfig.resumeLabel && (
            <div className="form-group">
              <label htmlFor="resume-upload">{currentConfig.needsJd ? '4' : '3'}. {currentConfig.resumeLabel}</label>
              <input type="file" id="resume-upload" multiple={currentConfig.allowMultiple} onChange={(e) => setResumes(e.target.files)} accept=".pdf,.docx" required disabled={isLoading}/>
            </div>
        )}
        
        {currentConfig.needsQuestion && (
          <div className="form-group">
            <label htmlFor="qa-question">4. Ajukan Pertanyaan Spesifik</label>
            <input type="text" id="qa-question" placeholder="Contoh: Apa saja pengalaman kandidat ini?" value={question} onChange={(e) => setQuestion(e.target.value)} required disabled={isLoading}/>
          </div>
        )}
        
        <div className="form-group">
          <button type="submit" className="submit-btn" disabled={isLoading}>{isLoading ? 'Menganalisis...' : 'Mulai Analisis'}</button>
        </div>
      </form>
    </div>
  );
}

export default AnalysisForm;
