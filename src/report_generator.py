"""
PDF Report Generator for Resume Analysis
"""
from fpdf import FPDF
from datetime import datetime
from typing import Dict, List
import os


class ResumeReportPDF(FPDF):
    """Custom PDF class for resume analysis reports"""
    
    def header(self):
        """PDF Header"""
        self.set_font('Arial', 'B', 16)
        self.set_text_color(33, 37, 41)
        self.cell(0, 10, 'AI Resume Analysis Report', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.set_text_color(108, 117, 125)
        self.cell(0, 5, f'Generated on {datetime.now().strftime("%B %d, %Y")}', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        """PDF Footer"""
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title: str, icon: str = ""):
        """Add a chapter title"""
        self.set_font('Arial', 'B', 14)
        self.set_text_color(13, 110, 253)
        self.cell(0, 10, f'{icon} {title}', 0, 1, 'L')
        self.ln(2)
    
    def section_text(self, text: str):
        """Add section text"""
        self.set_font('Arial', '', 11)
        self.set_text_color(33, 37, 41)
        self.multi_cell(0, 6, text)
        self.ln(3)
    
    def bullet_point(self, text: str):
        """Add a bullet point"""
        self.set_font('Arial', '', 10)
        self.set_text_color(52, 58, 64)
        self.cell(10, 6, chr(149), 0, 0)  # Bullet character
        self.multi_cell(0, 6, text)
    
    def score_box(self, label: str, score: int, max_score: int = 100):
        """Add a score box"""
        self.set_fill_color(233, 236, 239)
        self.set_draw_color(173, 181, 189)
        self.rect(self.get_x(), self.get_y(), 60, 15, 'DF')
        
        self.set_font('Arial', 'B', 12)
        self.set_text_color(33, 37, 41)
        self.cell(30, 7, label, 0, 0, 'L')
        
        # Score with color
        if score >= 80:
            self.set_text_color(25, 135, 84)  # Green
        elif score >= 60:
            self.set_text_color(255, 193, 7)  # Yellow
        else:
            self.set_text_color(220, 53, 69)  # Red
        
        self.set_font('Arial', 'B', 14)
        self.cell(30, 7, f'{score}/{max_score}', 0, 1, 'R')
        self.ln(5)


def generate_resume_report(
    summary: str,
    skills: Dict[str, List[str]],
    ats_score: Dict,
    gaps: str,
    roadmap: str,
    interview_tips: List[str],
    filename: str = "resume_analysis_report.pdf"
) -> str:
    """
    Generate comprehensive PDF report
    
    Args:
        summary: Resume summary
        skills: Extracted skills dictionary
        ats_score: ATS score dictionary
        gaps: Skill gaps analysis
        roadmap: Career roadmap
        interview_tips: List of interview tips
        filename: Output filename
        
    Returns:
        Path to generated PDF
    """
    pdf = ResumeReportPDF()
    pdf.add_page()
    
    # ATS Score Section
    pdf.chapter_title('ATS Compatibility Score', '📊')
    pdf.score_box('Overall Score', ats_score['total_score'], ats_score['max_score'])
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(33, 37, 41)
    pdf.cell(0, 8, f"Grade: {ats_score['grade']}", 0, 1)
    pdf.ln(3)
    
    # ATS Breakdown
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(0, 6, 'Score Breakdown:', 0, 1)
    for category, score in ats_score['breakdown'].items():
        category_name = category.replace('_', ' ').title()
        pdf.set_font('Arial', '', 10)
        pdf.cell(100, 6, f'  - {category_name}', 0, 0)
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(0, 6, f'{score} points', 0, 1)
    pdf.ln(5)
    
    # Resume Summary Section
    pdf.chapter_title('Resume Summary', '📄')
    pdf.section_text(summary[:500] + ('...' if len(summary) > 500 else ''))
    pdf.ln(3)
    
    # Skills Section
    pdf.chapter_title('Identified Skills', '💡')
    
    if skills['technical']:
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 6, 'Technical Skills:', 0, 1)
        pdf.set_font('Arial', '', 10)
        skills_text = ', '.join(skills['technical'][:15])
        pdf.multi_cell(0, 6, skills_text)
        pdf.ln(2)
    
    if skills['soft']:
        pdf.set_font('Arial', 'B', 11)
        pdf.cell(0, 6, 'Soft Skills:', 0, 1)
        pdf.set_font('Arial', '', 10)
        soft_skills_text = ', '.join(skills['soft'][:10])
        pdf.multi_cell(0, 6, soft_skills_text)
        pdf.ln(2)
    
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(108, 117, 125)
    pdf.cell(0, 6, f'Total Skills Identified: {skills["total_count"]}', 0, 1)
    pdf.ln(5)
    
    # Skill Gaps Section
    pdf.chapter_title('Skill Gaps & Areas for Improvement', '🎯')
    pdf.section_text(gaps[:600] + ('...' if len(gaps) > 600 else ''))
    pdf.ln(3)
    
    # Career Roadmap Section
    pdf.chapter_title('Career Roadmap', '🚀')
    pdf.section_text(roadmap[:600] + ('...' if len(roadmap) > 600 else ''))
    pdf.ln(3)
    
    # Interview Tips Section
    pdf.add_page()
    pdf.chapter_title('Interview Preparation Tips', '📚')
    for tip in interview_tips:
        pdf.bullet_point(tip)
        pdf.ln(1)
    
    # Recommendations
    pdf.ln(5)
    pdf.chapter_title('Key Recommendations', '✅')
    recommendations = [
        "Update your resume with quantifiable achievements",
        "Include action verbs in experience descriptions",
        "Add relevant certifications to boost credibility",
        "Tailor your resume for each job application",
        "Keep your LinkedIn profile synchronized with resume",
        "Practice mock interviews for targeted roles"
    ]
    
    for rec in recommendations:
        pdf.bullet_point(rec)
        pdf.ln(1)
    
    # Save PDF
    output_path = os.path.join(os.getcwd(), filename)
    pdf.output(output_path)
    
    return output_path
