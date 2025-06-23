from typing import List, Dict, Optional
import logging
import re
from utils.resume_standardizer import ResumeStandardizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResumeScorer:
    def __init__(self, domain: str = "general", criteria: Optional[Dict[str, int]] = None):
        self.domain = domain.lower()
        standardizer_helper = ResumeStandardizer(domain=self.domain)
        self.criteria = criteria if criteria else standardizer_helper.get_domain_specific_criteria()
        self.max_score = sum(self.criteria.values())
        self.domain_skills = standardizer_helper.domain_skills_mapping.get(
            self.domain.upper(),
            standardizer_helper.domain_skills_mapping["General"]
        )
       
        self.scoring_guide = {
            1: "Tidak memenuhi",
            2: "Tidak memenuhi",
            3: "Tidak memenuhi",
            4: "Memenuhi sebagian",
            5: "Memenuhi sebagian",
            6: "Memenuhi sebagian",
            7: "Memenuhi dengan baik",
            8: "Memenuhi dengan baik",
            9: "Melebihi ekspektasi",
            10: "Melebihi ekspektasi"
        }
       
        self.level_expectations = {
            "entry": {"min_score": 20, "max_score": 50},
            "mid": {"min_score": 40, "max_score": 70},
            "senior": {"min_score": 60, "max_score": 90},
            "expert": {"min_score": 80, "max_score": 100}
        }
   
    def extract_features_from_resume(self, standardized_resume: str, jd_text: Optional[str] = None) -> Dict:
        try:
            # Extract skills
            skills_match = re.search(r'SKILLS:(.+?)(?=\n[A-Z_]+:|$)', standardized_resume, re.DOTALL)
            if skills_match:
                skills_text = skills_match.group(1).strip()
                candidate_skills = [skill.strip().lower() for skill in skills_text.split(',')]
            else:
                candidate_skills = []
           
            # Calculate skill match score
            skill_match_score = 0
            if jd_text:
                jd_skills = []
                for skill in self.domain_skills:
                    if skill.lower() in jd_text.lower():
                        jd_skills.append(skill.lower())
               
                if jd_skills:
                    matched_skills = set(jd_skills) & set(candidate_skills)
                    skill_match_score = len(matched_skills) / len(jd_skills) if jd_skills else 0
                else:
                    skill_match_score = len(candidate_skills) / 10 if candidate_skills else 0
            else:
                skill_match_score = len(candidate_skills) / 10 if candidate_skills else 0
           
            # Extract experience years (PERBAIKAN)
            experience_match = re.search(r'EXPERIENCE_YEARS:(.+?)(?=\n[A-Z_]+:|$)', standardized_resume)
            if experience_match:
                experience_value = experience_match.group(1).strip()
                if experience_value.lower() in ['not specified', 'none', '']:
                    experience_years = 0
                else:
                    try:
                        experience_years = int(experience_value)
                    except ValueError:
                        experience_years = 0
            else:
                experience_years = 0
           
            # Extract education level
            education_match = re.search(r'EDUCATION:(.+?)(?=\n[A-Z_]+:|$)', standardized_resume, re.DOTALL)
            if education_match:
                education_text = education_match.group(1).strip().lower()
                if "phd" in education_text or "doctorate" in education_text:
                    education_level = 4
                elif "master" in education_text or "mba" in education_text:
                    education_level = 3
                elif "bachelor" in education_text or "bsc" in education_text:
                    education_level = 2
                else:
                    education_level = 1
            else:
                education_level = 0
           
            # Extract certifications
            cert_match = re.search(r'CERTIFICATIONS:(.+?)(?=\n[A-Z_]+:|$)', standardized_resume, re.DOTALL)
            if cert_match:
                cert_text = cert_match.group(1).strip()
                certifications_count = len(cert_text.split(',')) if cert_text != "None" else 0
            else:
                certifications_count = 0
           
            # Extract projects count (PERBAIKAN)
            projects_match = re.search(r'PROJECTS_COUNT:(.+?)(?=\n[A-Z_]+:|$)', standardized_resume)
            if projects_match:
                projects_value = projects_match.group(1).strip()
                if projects_value.lower() in ['not specified', 'none', '']:
                    projects_count = 0
                else:
                    try:
                        projects_count = int(projects_value)
                    except ValueError:
                        projects_count = 0
            else:
                projects_count = 0
           
            # Extract salary expectation
            salary_match = re.search(r'SALARY_EXPECTATION:(.+?)(?=\n[A-Z_]+:|$)', standardized_resume)
            if salary_match:
                salary_text = salary_match.group(1).strip()
                if salary_text != "Not specified":
                    salary_expectation = float(re.sub(r'[^\d.]', '', salary_text))
                else:
                    salary_expectation = 0.0
            else:
                salary_expectation = 0.0
           
            # Extract domain expertise
            expertise_match = re.search(r'DOMAIN_EXPERTISE:(.+?)(?=\n[A-Z_]+:|$)', standardized_resume)
            if expertise_match:
                expertise_text = expertise_match.group(1).strip().lower()
                expertise_score = 0.8 if "advanced" in expertise_text or "expert" in expertise_text else \
                                0.5 if "intermediate" in expertise_text else \
                                0.2 if "entry" in expertise_text else 0.0
            else:
                expertise_score = 0.0
           
            # Detect job role/level
            job_role_match = re.search(r'JOB_ROLE:(.+?)(?=\n[A-Z_]+:|$)', standardized_resume)
            if job_role_match:
                job_role = job_role_match.group(1).strip().lower()
                if "senior" in job_role or "lead" in job_role:
                    detected_role = 'senior'
                elif "junior" in job_role or "entry" in job_role:
                    detected_role = 'entry'
                else:
                    detected_role = 'mid'
            else:
                detected_role = 'mid'
           
            # Compute derived features
            salary_project_ratio = salary_expectation / (projects_count + 1e-6)
            exp_skill_interaction = experience_years * skill_match_score
           
            return {
                'Skill_Match': skill_match_score,
                'Experience (Years)': experience_years,
                'Education': education_level,
                'Certifications': certifications_count,
                'Projects Count': projects_count,
                'Job Role': detected_role,
                'Salary Expectation': salary_expectation,
                'Salary_Project_Ratio': salary_project_ratio,
                'Exp_Skill_Interaction': exp_skill_interaction,
                'Domain Expertise': expertise_score,
                'Combined_Text': standardized_resume[:2000],
                'resume_text': standardized_resume
            }
           
        except Exception as e:
            logger.error(f"Error extracting features: {str(e)}")
            return {
                'Skill_Match': 0,
                'Experience (Years)': 0,
                'Education': 0,
                'Certifications': 0,
                'Projects Count': 0,
                'Job Role': 'mid',
                'Salary Expectation': 0.0,
                'Salary_Project_Ratio': 0.0,
                'Exp_Skill_Interaction': 0.0,
                'Domain Expertise': 0.0,
                'Combined_Text': standardized_resume[:2000],
                'resume_text': standardized_resume[:1000] + "..."
            }
   
    def predict_score(self, features: Dict) -> float:
        try:
            score = 0
            score += features['Skill_Match'] * 25
            score += min(features['Experience (Years)'] / 10, 1.0) * 20
            score += (features['Education'] / 4) * 15
            score += min(features['Certifications'] / 5, 1.0) * 10
            score += min(features['Projects Count'] / 10, 1.0) * 10
            score += features['Domain Expertise'] * 15
            score += (1 if features['Job Role'] == 'senior' else 0.5 if features['Job Role'] == 'mid' else 0) * 5
            score = min(100, max(0, score))
            return score
        except Exception as e:
            logger.error(f"Error predicting score: {str(e)}")
            return 50.0
   
    def score_by_criteria(self, overall_score: float, features: Dict) -> Dict[str, float]:
        scores = {}
        base_score = overall_score / 10
       
        for criterion, weight in self.criteria.items():
            if "skill" in criterion.lower():
                factor = features['Skill_Match']
                criterion_score = base_score * 0.7 + factor * 3
            elif "experience" in criterion.lower():
                factor = min(features['Experience (Years)'] / 10, 1.0)
                criterion_score = base_score * 0.6 + factor * 4
            elif "education" in criterion.lower():
                factor = features['Education'] / 4
                criterion_score = base_score * 0.8 + factor * 2
            elif "certification" in criterion.lower():
                factor = min(features['Certifications'] / 5, 1.0)
                criterion_score = base_score * 0.8 + factor * 2
            elif "project" in criterion.lower():
                factor = min(features['Projects Count'] / 10, 1.0)
                criterion_score = base_score * 0.7 + factor * 3
            elif "expertise" in criterion.lower() or "leadership" in criterion.lower():
                factor = features['Domain Expertise']
                criterion_score = base_score * 0.7 + factor * 3
            else:
                criterion_score = base_score
           
            scores[criterion] = round(min(10, max(1, base_score)) * (weight / 10), 2)
        return scores
   
    def detect_experience_level(self, features: Dict) -> str:
        experience_years = features['Experience (Years)']
        job_role = features['Job Role']
        skill_match = features['Skill_Match']
        expertise = features['Domain Expertise']
       
        if experience_years >= 10 or expertise >= 0.8:
            return 'expert'
        elif experience_years >= 7 or (job_role == 'senior' and expertise >= 0.5):
            return 'senior'
        elif experience_years >= 3 or (job_role == 'mid' and skill_match >= 0.5):
            return 'mid'
        else:
            return 'entry'
   
    def score_resume(self, standardized_resume: str, jd_text: Optional[str] = None) -> Dict:
        try:
            features = self.extract_features_from_resume(standardized_resume, jd_text)
            ai_score = self.predict_score(features)
            criteria_scores = self.score_by_criteria(ai_score, features)
            total_score = sum(criteria_scores.values())
            percentage = (total_score / self.max_score) * 100
            level = self.detect_experience_level(features)
           
            return {
                "scores": criteria_scores,
                "total_score": round(total_score, 2),
                "percentage": round(percentage, 2),
                "ai_score": round(ai_score, 2),
                "level": level,
                "features": features,
                "standardized_resume": features['resume_text']
            }
           
        except Exception as e:
            logger.error(f"Error scoring resume: {str(e)}")
            return { "error": "Failed to score resume." }
   
    def compare_resumes(self, standardized_resume_texts: List[str], jd_text: Optional[str] = None) -> Dict:
        results = [self.score_resume(std_text, jd_text) for std_text in standardized_resume_texts]
        for i, result in enumerate(results):
            result["candidate_id"] = i + 1
        results.sort(key=lambda x: x.get("ai_score", 0), reverse=True)
        for i, result in enumerate(results):
            result["rank"] = i + 1
        return { "ranking": results, "criteria": self.criteria }