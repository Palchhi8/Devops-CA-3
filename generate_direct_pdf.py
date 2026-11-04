import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_PATH = r"C:\Users\jainp\OneDrive\Desktop\Devops-CA-3\OrderFlow_v2.3.0_Direct_GitHub_Report.pdf"

# Page dimensions for landscape letter: 11 x 8.5 inches = 792 x 612 pt
PAGE_WIDTH, PAGE_HEIGHT = landscape(letter)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header line
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(36, PAGE_HEIGHT - 38, PAGE_WIDTH - 36, PAGE_HEIGHT - 38)
        
        # Header text
        self.drawString(36, PAGE_HEIGHT - 32, "OrderFlow v2.3.0 - Direct GitHub Repository Screenshots & Verification")
        self.drawRightString(PAGE_WIDTH - 36, PAGE_HEIGHT - 32, "DevOps CA-3 | Palchhi8 / Devops-CA-3")
        
        # Footer line
        self.line(36, 36, PAGE_WIDTH - 36, 36)
        
        # Footer text
        self.drawString(36, 24, "GitHub: https://github.com/Palchhi8/Devops-CA-3  |  Branch: investigation/release-readiness")
        self.drawRightString(PAGE_WIDTH - 36, 24, f"Page {self._pageNumber} of {total_pages}")
        
        self.restoreState()

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=44
    )
    
    styles = getSampleStyleSheet()
    
    label_style = ParagraphStyle(
        'ScreenshotLabel',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1A202C"),
        spaceAfter=3,
        spaceBefore=0
    )
    
    meta_style = ParagraphStyle(
        'ScreenshotMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=6
    )
    
    caption_style = ParagraphStyle(
        'ScreenshotCaption',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1A365D"),
    )
    
    items = [
        {
            "num": 1,
            "label": "Screenshot 1 - Initial Deployment Investigation",
            "meta": "Direct Capture: https://github.com/Palchhi8/Devops-CA-3/actions/runs/41785812513 (Failed baseline run)",
            "file": "direct_screenshot1_failed_pipeline.png",
            "caption": "Caption: Investigation identified critical production risks: deployment executed prior to validation, artificial test failure, unversioned tags, missing approvals, and exposed plaintext credentials."
        },
        {
            "num": 2,
            "label": "Screenshot 2 - Deployment Pipeline Repairs",
            "meta": "Direct Capture: https://github.com/Palchhi8/Devops-CA-3/blob/investigation/release-readiness/.github/workflows/release.yml",
            "file": "direct_screenshot2_workflow_editor.png",
            "caption": "Caption: The updated deployment pipeline enforces strict pre-deployment validation, removes artificial failures, injects release version v2.3.0, and establishes production environment gates."
        },
        {
            "num": 3,
            "label": "Screenshot 3 - Secure Release Configuration",
            "meta": "Direct Capture: https://github.com/Palchhi8/Devops-CA-3/blob/investigation/release-readiness/deployment/kubernetes/deployment.yaml",
            "file": "direct_screenshot3_k8s_config.png",
            "caption": "Caption: Secured release configuration eradicates hardcoded secrets via Kubernetes SecretKeyRefs, formalizes multi-stakeholder sign-offs, and enforces v2.3.0 artifact traceability."
        },
        {
            "num": 4,
            "label": "Screenshot 4 - Successful Validation",
            "meta": "Direct Capture: https://github.com/Palchhi8/Devops-CA-3/actions/runs/41786994480 (Passing workflow run)",
            "file": "direct_screenshot4_successful_run.png",
            "caption": "Caption: Automated validation passed with 100% test success, verified secret hygiene, and executed production deployment with immutable release tag v2.3.0."
        },
        {
            "num": 5,
            "label": "Screenshot 5 - Final Release Readiness Pack",
            "meta": "Direct Capture: https://github.com/Palchhi8/Devops-CA-3/blob/investigation/release-readiness/release/RELEASE_DOCUMENTATION.md",
            "file": "direct_screenshot5_release_doc.png",
            "caption": "Caption: Comprehensive Release Readiness Pack establishes verifiable audit trails, zero-downtime rollback protocols, and verified operational procedures for OrderFlow v2.3.0."
        }
    ]
    
    story = []
    
    for i, item in enumerate(items):
        story.append(Paragraph(item["label"], label_style))
        story.append(Paragraph(item["meta"], meta_style))
        
        img = RLImage(item["file"], width=720, height=405)
        story.append(img)
        story.append(Spacer(1, 6))
        
        caption_p = Paragraph(item["caption"], caption_style)
        caption_table = Table([[caption_p]], colWidths=[720])
        caption_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3182CE")),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        story.append(caption_table)
        
        if i < len(items) - 1:
            story.append(PageBreak())
            
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Direct GitHub PDF build complete:", PDF_PATH)

if __name__ == "__main__":
    build_pdf()
