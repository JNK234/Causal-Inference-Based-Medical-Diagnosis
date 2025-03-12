"""
Report generator module for creating PDF reports of medical diagnosis and treatment plans.
"""
import os
import tempfile
import base64
from datetime import datetime
import logging
from jinja2 import Template
import pdfkit
import re

class ReportGenerator:
    """
    Creates PDF reports of medical diagnosis and treatment plans.
    """
    
    def __init__(self):
        """Initialize the report generator."""
        pass
    
    def generate_pdf_report(self, diagnosis_results):
        """
        Generate a PDF report of the diagnosis and treatment plan.
        
        Args:
            diagnosis_results (dict): Dictionary containing all diagnosis results
            
        Returns:
            str: Path to the generated PDF file
        """
        try:
            # Create HTML content using a template
            html_content = self._create_html_report(diagnosis_results)
            
            # Create a temporary file for the HTML
            with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as html_file:
                html_file.write(html_content.encode('utf-8'))
                html_file_path = html_file.name
            
            # Define the output PDF path
            pdf_file_path = html_file_path.replace('.html', '.pdf')
            
            # Convert HTML to PDF
            try:
                pdfkit.from_file(html_file_path, pdf_file_path)
                logging.info(f"PDF report generated at {pdf_file_path}")
            except Exception as e:
                logging.error(f"Error generating PDF: {str(e)}")
                # If PDF generation fails, return the HTML file path instead
                return html_file_path
            
            # Clean up the HTML file
            os.unlink(html_file_path)
            
            return pdf_file_path
        
        except Exception as e:
            logging.error(f"Error in generate_pdf_report: {str(e)}")
            return None
    
    def _create_html_report(self, diagnosis_results):
        """
        Create HTML content for the report.
        
        Args:
            diagnosis_results (dict): Dictionary containing all diagnosis results
            
        Returns:
            str: HTML content for the report
        """
        # HTML template for the report
        template_str = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Medical Diagnosis Report</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    line-height: 1.6;
                    color: #333;
                }
                h1 {
                    color: #2C3E50;
                    border-bottom: 2px solid #3498DB;
                    padding-bottom: 10px;
                }
                h2 {
                    color: #3498DB;
                    margin-top: 30px;
                    border-bottom: 1px solid #ddd;
                    padding-bottom: 5px;
                }
                .section {
                    margin-bottom: 30px;
                }
                .highlight {
                    background-color: #F8F9F9;
                    padding: 15px;
                    border-left: 5px solid #3498DB;
                    margin: 20px 0;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }
                th, td {
                    padding: 12px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }
                th {
                    background-color: #f2f2f2;
                }
                .footer {
                    margin-top: 50px;
                    text-align: center;
                    font-size: 12px;
                    color: #777;
                }
                .arrow {
                    color: #3498DB;
                    font-weight: bold;
                }
                .causal {
                    color: #4CAF50;
                    font-weight: bold;
                }
                .preventative {
                    color: #2196F3;
                    font-weight: bold;
                }
                .symptomatic {
                    color: #FFC107;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <h1>Medical Diagnosis and Treatment Plan</h1>
            <p>Generated on: {{ date }}</p>
            
            <div class="section">
                <h2>Patient Case</h2>
                <p>{{ case_text }}</p>
            </div>
            
            <div class="section">
                <h2>Medical Factors</h2>
                {{ extracted_factors }}
            </div>
            
            <div class="section">
                <h2>Causal Analysis</h2>
                {{ causal_links }}
            </div>
            
            <div class="section">
                <h2>Diagnosis</h2>
                <div class="highlight">{{ diagnosis }}</div>
            </div>
            
            <div class="section">
                <h2>Treatment Plan</h2>
                {{ treatment_plan }}
            </div>
            
            <div class="section">
                <h2>Patient-Specific Considerations</h2>
                {{ patient_specific_plan }}
            </div>
            
            <div class="section">
                <h2>Final Treatment Recommendation</h2>
                <div class="highlight">{{ final_treatment_plan }}</div>
            </div>
            
            <div class="footer">
                <p>This report was generated using causal inference with LLMs. It is intended for informational purposes only and should be reviewed by a qualified medical professional.</p>
            </div>
        </body>
        </html>
        """
        
        # Create a Jinja2 template
        template = Template(template_str)
        
        # Extract data from diagnosis results
        data = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'case_text': diagnosis_results.get('initial', {}).get('case_text', 'No case text provided'),
            'extracted_factors': self._format_html_content(diagnosis_results.get('extraction', {}).get('extracted_factors', 'No extracted factors available')),
            'causal_links': self._format_html_content(diagnosis_results.get('causal_analysis', {}).get('causal_links', 'No causal links available')),
            'diagnosis': self._format_html_content(diagnosis_results.get('diagnosis', {}).get('diagnosis', 'No diagnosis available')),
            'treatment_plan': self._format_html_content(diagnosis_results.get('treatment_planning', {}).get('treatment_plan', 'No treatment plan available')),
            'patient_specific_plan': self._format_html_content(diagnosis_results.get('patient_specific', {}).get('patient_specific_plan', 'No patient-specific plan available')),
            'final_treatment_plan': self._format_html_content(diagnosis_results.get('final_plan', {}).get('final_treatment_plan', 'No final treatment plan available'))
        }
        
        # Render the template with the data
        html_content = template.render(**data)
        
        return html_content
    
    def _format_html_content(self, content):
        """
        Format content for HTML display.
        
        Args:
            content (str): The content to format
            
        Returns:
            str: Formatted HTML content
        """
        if not content:
            return "<p>No information available</p>"
        
        # Replace newlines with <br> tags
        formatted_content = content.replace('\n', '<br>')
        
        # Format causal arrows
        formatted_content = re.sub(r'→', r'<span class="arrow">→</span>', formatted_content)
        
        # Format treatment categories
        formatted_content = re.sub(r'✅\s*Causal Treatment', r'<span class="causal">✅ Causal Treatment</span>', formatted_content)
        formatted_content = re.sub(r'✅\s*Preventative Treatment', r'<span class="preventative">✅ Preventative Treatment</span>', formatted_content)
        formatted_content = re.sub(r'❌\s*Symptomatic Treatment', r'<span class="symptomatic">❌ Symptomatic Treatment</span>', formatted_content)
        
        return formatted_content
    
    def get_pdf_download_link(self, pdf_path, link_text="Download PDF Report"):
        """
        Create a download link for the PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            link_text (str): Text for the download link
            
        Returns:
            str: HTML for the download link
        """
        try:
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            
            b64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            # Add a direct download attribute and styling to make the button more prominent
            href = f'''
            <div style="margin: 20px 0;">
                <a href="data:application/pdf;base64,{b64_pdf}" 
                   download="diagnosis_report.pdf" 
                   style="background-color: #4CAF50; color: white; padding: 12px 20px; 
                          text-align: center; text-decoration: none; display: inline-block; 
                          font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 4px;">
                    {link_text}
                </a>
                <p style="font-size: 12px; color: #666; margin-top: 8px;">
                    Click the button above to download. If download doesn't start automatically, 
                    right-click the button and select "Save link as..."
                </p>
            </div>
            '''
            return href
        except Exception as e:
            logging.error(f"Error creating PDF download link: {str(e)}")
            return f"<p>Error creating download link: {str(e)}</p>"
