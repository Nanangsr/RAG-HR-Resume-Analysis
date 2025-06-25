import React from 'react';
import './Footer.css'; // Kita akan buat file CSS-nya
import dataInsLogo from '../assets/datains-logo.png'; // Impor logo
import { Linkedin } from 'lucide-react'; // Impor ikon LinkedIn

const Footer = () => {
  const yourName = "Nanang Safiu Ridho";
  const yourLinkedinUrl = "https://www.linkedin.com/in/nanang-safiu-ridho-804112248/";

  return (
    <footer className="main-footer">
      <div className="footer-content">
        <img src={dataInsLogo} alt="Global Data Inspirasi Logo" className="footer-logo" />
        <div className="footer-text">
          <p>© {new Date().getFullYear()} | Dibuat oleh {yourName}</p>
          <p className="role">Data Scientist Intern at Global Data Inspirasi</p>
        </div>
        <a href={yourLinkedinUrl} target="_blank" rel="noopener noreferrer" className="footer-social-link">
          <Linkedin size={24} />
        </a>
      </div>
    </footer>
  );
};

export default Footer;
