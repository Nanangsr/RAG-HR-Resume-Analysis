// src/pages/HomePage.jsx (FINAL Content & Layout)
import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';
import FeatureCard from '../components/FeatureCard.jsx';
import { GanttChartSquare, Rows, HelpCircle, SearchCheck } from 'lucide-react';
import heroImage from '../assets/hr-image.jpg';

// Fitur yang disesuaikan dengan 4 use case Anda
const features = [
  { icon: <GanttChartSquare />, title: "Skoring & Peringkat Otomatis", text: "Unggah beberapa CV untuk mendapatkan skor relevansi dan peringkat otomatis, mempercepat proses seleksi awal Anda." },
  { icon: <Rows />, title: "Analisis Perbandingan Kandidat", text: "Dapatkan analisis naratif komparatif yang mendalam untuk memahami kekuatan dan kelemahan relatif dari para kandidat top." },
  { icon: <HelpCircle />, title: "Tanya Jawab (QA) Interaktif", text: "Punya pertanyaan spesifik? 'Wawancarai' CV secara langsung dan dapatkan jawaban instan berbasis data dari dokumen." },
  { icon: <SearchCheck />, title: "Pencarian Berbasis Deskripsi", text: "Temukan kandidat paling relevan dari database Anda hanya dengan mengunggah deskripsi pekerjaan." },
];

const HomePage = () => {
    return (
        <div className="homepage">
            {/* Hero Section yang Disederhanakan dan Lebih Fokus */}
            <section className="hero-section">
                <div className="container">
                    <div className="hero-grid">
                        <div className="hero-content">
                            <div className="hero-badge">🚀 Platform Rekrutmen Cerdas</div>
                            <h1>Saring Talenta Terbaik, Bukan Sekadar CV</h1>
                            <p>Ubah tumpukan CV yang memakan waktu menjadi daftar kandidat yang terstruktur dan terukur. Hemat waktu, hilangkan bias, dan temukan talenta terbaik dengan kekuatan analisis AI.</p>
                            <div className="hero-buttons">
                                <Link to="/analysis" className="button button-primary">❤‍🔥 Mulai Analisis Sekarang</Link>
                            </div>
                        </div>
                        <div className="hero-image">
                        <img src={heroImage} alt="Seorang profesional HR sedang menganalisis resume" />
                    </div>
                    </div>
                </div>
            </section>

            {/* Features Section dengan 4 Kartu */}
            <section className="features-section section-padding">
                <div className="container">
                     <div className="section-header" style={{ textAlign: "center" }}>
                        <h2>Kekuatan AI untuk Rekrutmen Lebih Cerdas</h2>
                        <p>
                          Temukan fitur-fitur inovatif yang akan mengubah cara Anda menyeleksi kandidat lebih cepat, objektif, dan akurat. Jadikan setiap keputusan rekrutmen Anda didukung data dan insight terbaik!
                        </p>
                    </div>
                    <div className="features-grid">
                        {features.map((feature, index) => (
                            <FeatureCard key={index} icon={feature.icon} title={feature.title} text={feature.text} />
                        ))}
                    </div>
                </div>
            </section>
        </div>
    );
};

export default HomePage;