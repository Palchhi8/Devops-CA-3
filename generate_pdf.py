import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

PDF_PATH = r"C:\Users\jainp\OneDrive\Desktop\Devops-CA-3\OrderFlow_v2.3.0_Release_Readiness_Report.pdf"
SCREENSHOTS_DIR = r"C:\Users\jainp\OneDrive\Desktop\Devops-CA-3\screenshots"

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
        
        # Header banner line
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.75)
        self.line(36, PAGE_HEIGHT - 38, PAGE_WIDTH - 36, PAGE_HEIGHT - 38)
        
        # Header text
        self.drawString(36, PAGE_HEIGHT - 32, "OrderFlow v2.3.0 - Production Release Readiness & Pipeline Verification")
        self.drawRightString(PAGE_WIDTH - 36, PAGE_HEIGHT - 32, "DevOps CA-3 | Palchhi8 / Devops-CA-3")
        
        # Footer banner line
        self.line(36, 36, PAGE_WIDTH - 36, 36)
        
        # Footer text
        self.drawString(36, 24, "Branch: investigation/release-readiness  |  Release Candidate: v2.3.0  |  Author: Palchhi")
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
            "meta": "Target: Repository and Pipeline before fixes  |  Artifact: Initial broken state with inverted deployment execution",
            "file": "Screenshot_1_Initial_Deployment_Investigation.png",
            "caption": "Caption: Investigation identified critical production risks: deployment executed prior to validation, artificial test failure, unversioned tags, missing approvals, and exposed plaintext credentials."
        },
        {
            "num": 2,
            "label": "Screenshot 2 - Deployment Pipeline Repairs",
            "meta": "Target: Updated deployment workflow (.github/workflows/release.yml)  |  Artifact: Corrected pipeline configuration in editor",
            "file": "Screenshot_2_Deployment_Pipeline_Repairs.png",
            "caption": "Caption: The updated deployment pipeline enforces strict pre-deployment validation, removes artificial failures, injects release version v2.3.0, and establishes production environment gates."
        },
        {
            "num": 3,
            "label": "Screenshot 3 - Secure Release Configuration",
            "meta": "Target: Hardened deployment configurations  |  Artifact: Kubernetes secretKeyRefs, approval sign-offs, and versioned manifests",
            "file": "Screenshot_3_Secure_Release_Configuration.png",
            "caption": "Caption: Secured release configuration eradicates hardcoded secrets via Kubernetes SecretKeyRefs, formalizes multi-stakeholder sign-offs, and enforces v2.3.0 artifact traceability."
        },
        {
            "num": 4,
            "label": "Screenshot 4 - Successful Validation",
            "meta": "Target: GitHub Actions Pipeline Execution (Run #2)  |  Artifact: Green validation and automated production deployment",
            "file": "Screenshot_4_Successful_Validation.png",
            "caption": "Caption: Automated validation passed with 100% test success, verified secret hygiene, and executed production deployment with immutable release tag v2.3.0."
        },
        {
            "num": 5,
            "label": "Screenshot 5 - Final Release Readiness Pack",
            "meta": "Target: Release documentation & final repository state  |  Artifact: Operational documentation, rollback plan, and approval matrix",
            "file": "Screenshot_5_Final_Release_Readiness_Pack.png",
            "caption": "Caption: Comprehensive Release Readiness Pack establishes verifiable audit trails, zero-downtime rollback protocols, and verified operational procedures for OrderFlow v2.3.0."
        }
    ]
    
    story = []
    
    for i, item in enumerate(items):
        story.append(Paragraph(item["label"], label_style))
        story.append(Paragraph(item["meta"], meta_style))
        
        img_full_path = os.path.join(SCREENSHOTS_DIR, item["file"])
        # Dimensions: width = 720 pt, height = 405 pt (16:9 ratio)
        img = RLImage(img_full_path, width=720, height=405)
        story.append(img)
        story.append(Spacer(1, 6))
        
        # Caption container box
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
    print("PDF build complete:", PDF_PATH)

if __name__ == "__main__":
    build_pdf()
