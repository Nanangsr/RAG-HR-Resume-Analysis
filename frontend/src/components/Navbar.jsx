import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navbar.css';
import { Phone } from 'lucide-react';

const Navbar = () => {
    return (
        <header className="main-header">
            <div className="container">
                <div className="navbar">
                    <NavLink to="/" className="nav-logo">
                        <img src="/logo.svg" alt="Resume Analisis Logo" className="nav-logo-img" />
                    <h1>Resume Analisis</h1>
                    </NavLink>
                    <nav className="nav-menu">
                        <NavLink to="/" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>Home</NavLink>
                        <NavLink to="/analysis" className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}>Mulai Analisis</NavLink>
                    </nav>
                    <div className="nav-contact">
                        <Phone size={18} />
                        <span>Ada pertanyaan? +62 (space nomer)</span>
                    </div>
                </div>
            </div>
        </header>
    );
};
export default Navbar;
