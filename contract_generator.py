"""
Legal Contract Generator System - WeasyPrint Version
====================================================
A professional OOP-based system for generating bilingual (Arabic-English) 
legal contracts from Excel data with biometric signature support.

✅ FIXED: Full Arabic support with proper RTL rendering
✅ FIXED: Beautiful UI with modern CSS
✅ Uses WeasyPrint (HTML/CSS to PDF)

Author: Contract Automation System
Version: 2.0.0 (WeasyPrint Edition)
License: Proprietary
"""

import pandas as pd
from weasyprint import HTML, CSS
from datetime import datetime
import hashlib
import secrets
import os
import qrcode
from io import BytesIO
import base64
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import json


@dataclass
class ContractData:
    """Data class for main contract information"""
    contract_id: str
    contract_date: str
    project_title: str
    dev_name: str
    dev_address: str
    dev_email: str
    client_name: str
    client_rep: str
    client_email: str
    client_telegram: str
    total_value: float
    currency: str
    payment_terms: str
    ip_ownership: str
    warranty_period: str
    revision_limit: int
    governing_law: str
    signing_link: str = ""
    verification_token: str = ""
    biometric_auth_status: str = "Pending"
    device_id: str = ""
    ip_log: str = ""
    digital_signature_hash: str = ""


@dataclass
class Milestone:
    """Data class for project milestones"""
    contract_id: str
    order: int
    title: str
    description: str
    price: float
    duration: int
    signature_status: str = "Pending"
    completion_percentage: int = 0


class SecurityManager:
    """Manages security tokens, hashing, and verification"""
    
    @staticmethod
    def generate_verification_token(length: int = 32) -> str:
        """Generate a secure random token for contract verification"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_contract_hash(contract_data: ContractData, milestones: List[Milestone]) -> str:
        """Generate SHA-256 hash of contract for integrity verification"""
        contract_string = json.dumps({
            'contract_id': contract_data.contract_id,
            'client_name': contract_data.client_name,
            'total_value': contract_data.total_value,
            'milestones': [
                {
                    'order': m.order,
                    'title': m.title,
                    'price': m.price
                } for m in milestones
            ]
        }, sort_keys=True)
        
        return hashlib.sha256(contract_string.encode('utf-8')).hexdigest()
    
    @staticmethod
    def generate_signing_link(contract_id: str, token: str, base_url: str = "https://contractsign.app") -> str:
        """Generate unique signing link with embedded token"""
        return f"{base_url}/sign/{contract_id}?token={token}"
    
    @staticmethod
    def generate_qr_code_base64(data: str, size: int = 10) -> str:
        """Generate QR code as base64 image"""
        qr = qrcode.QRCode(version=1, box_size=size, border=2)
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"


class LegalClausesEgypt:
    """Egyptian law-compliant legal clauses (Arabic & English)"""
    
    @staticmethod
    def get_termination_clause() -> Dict[str, str]:
        return {
            'ar': """
            <h3>البند الأول: سياسة الإلغاء والإنهاء</h3>
            <ol>
                <li>يحق لأي من الطرفين إنهاء هذا العقد بإشعار كتابي مدته ١٥ يوماً.</li>
                <li>في حالة الإنهاء من جانب العميل بعد بدء التنفيذ، تُستحق كامل قيمة المراحل المكتملة بالإضافة إلى ٣٠٪ من قيمة المرحلة الجارية كتعويض.</li>
                <li>في حالة الإخلال الجسيم بالالتزامات من أي طرف، يحق للطرف الآخر إنهاء العقد فوراً مع المطالبة بالتعويضات.</li>
                <li>تخضع جميع حالات الإنهاء لأحكام القانون المدني المصري رقم ١٣١ لسنة ١٩٤٨.</li>
            </ol>
            """,
            'en': """
            <h3>Article 1: Termination and Cancellation Policy</h3>
            <ol>
                <li>Either party may terminate this contract with 15 days written notice.</li>
                <li>If the Client terminates after execution begins, full value of completed milestones plus 30% of the current milestone is due as compensation.</li>
                <li>In case of material breach by either party, the other party may terminate immediately and claim damages.</li>
                <li>All termination cases are subject to Egyptian Civil Code No. 131 of 1948.</li>
            </ol>
            """
        }
    
    @staticmethod
    def get_confidentiality_clause() -> Dict[str, str]:
        return {
            'ar': """
            <h3>البند الثاني: السرية وحماية البيانات</h3>
            <ol>
                <li>يلتزم الطرفان بالحفاظ على سرية جميع المعلومات والبيانات المتبادلة أثناء تنفيذ المشروع.</li>
                <li>لا يجوز الإفصاح عن أي معلومات فنية أو تجارية لأطراف ثالثة دون موافقة كتابية مسبقة.</li>
                <li>تظل التزامات السرية سارية لمدة ٣ سنوات بعد انتهاء العقد.</li>
                <li>يخضع هذا البند لقانون حماية البيانات الشخصية المصري رقم ١٥١ لسنة ٢٠٢٠.</li>
            </ol>
            """,
            'en': """
            <h3>Article 2: Confidentiality and Data Protection</h3>
            <ol>
                <li>Both parties commit to maintaining confidentiality of all exchanged information during project execution.</li>
                <li>No technical or commercial information may be disclosed to third parties without prior written consent.</li>
                <li>Confidentiality obligations remain in effect for 3 years after contract termination.</li>
                <li>This clause is subject to Egyptian Personal Data Protection Law No. 151 of 2020.</li>
            </ol>
            """
        }
    
    @staticmethod
    def get_dispute_resolution_clause() -> Dict[str, str]:
        return {
            'ar': """
            <h3>البند الثالث: آلية حل النزاعات</h3>
            <ol>
                <li>في حالة نشوء أي خلاف، يلتزم الطرفان بمحاولة الحل الودي خلال ٣٠ يوماً.</li>
                <li>إذا تعذر الحل الودي، يتم اللجوء إلى التحكيم وفقاً لقانون التحكيم المصري رقم ٢٧ لسنة ١٩٩٤.</li>
                <li>يكون مقر التحكيم في القاهرة، جمهورية مصر العربية.</li>
                <li>تكون قرارات التحكيم نهائية وملزمة للطرفين.</li>
            </ol>
            """,
            'en': """
            <h3>Article 3: Dispute Resolution Mechanism</h3>
            <ol>
                <li>In case of any dispute, both parties commit to attempting amicable resolution within 30 days.</li>
                <li>If amicable resolution fails, arbitration shall be pursued under Egyptian Arbitration Law No. 27 of 1994.</li>
                <li>The arbitration venue shall be Cairo, Arab Republic of Egypt.</li>
                <li>Arbitration decisions are final and binding for both parties.</li>
            </ol>
            """
        }
    
    @staticmethod
    def get_force_majeure_clause() -> Dict[str, str]:
        return {
            'ar': """
            <h3>البند الرابع: القوة القاهرة</h3>
            <ol>
                <li>لا يُسأل أي من الطرفين عن التأخير أو عدم التنفيذ الناتج عن ظروف خارجة عن الإرادة (حروب، كوارث طبيعية، أوبئة، قرارات حكومية).</li>
                <li>يجب على الطرف المتأثر إخطار الطرف الآخر كتابياً خلال ٧ أيام من وقوع الحدث.</li>
                <li>يتم تعليق الالتزامات التعاقدية خلال فترة القوة القاهرة دون فسخ العقد.</li>
                <li>إذا استمرت القوة القاهرة لأكثر من ٩٠ يوماً، يحق لأي طرف إنهاء العقد دون تعويضات.</li>
            </ol>
            """,
            'en': """
            <h3>Article 4: Force Majeure</h3>
            <ol>
                <li>Neither party is liable for delays or non-performance resulting from circumstances beyond control (wars, natural disasters, epidemics, government decisions).</li>
                <li>The affected party must notify the other party in writing within 7 days of the event.</li>
                <li>Contractual obligations are suspended during force majeure without contract termination.</li>
                <li>If force majeure continues for more than 90 days, either party may terminate without compensation.</li>
            </ol>
            """
        }
    
    @staticmethod
    def get_digital_signature_clause() -> Dict[str, str]:
        return {
            'ar': """
            <h3>البند الخامس: التوقيع الإلكتروني والحجية القانونية</h3>
            <ol>
                <li>يُعتبر التوقيع الإلكتروني البيومتري (البصمة/الوجه) المُثبت عبر بروتوكول WebAuthn مُعادلاً للتوقيع الخطي التقليدي.</li>
                <li>يخضع التوقيع الإلكتروني لقانون تنظيم التوقيع الإلكتروني المصري رقم ١٥ لسنة ٢٠٠٤.</li>
                <li>يتم حفظ سجل رقمي يتضمن: (وقت التوقيع، معرف الجهاز، عنوان IP، البصمة الرقمية للعقد).</li>
                <li>لا يجوز للعميل إنكار التوقيع بعد التحقق البيومتري الناجح (مبدأ Non-Repudiation).</li>
                <li>يتم تشفير بيانات التوقيع بخوارزمية SHA-256 لضمان عدم التلاعب.</li>
            </ol>
            """,
            'en': """
            <h3>Article 5: Digital Signature and Legal Authority</h3>
            <ol>
                <li>Biometric digital signatures (fingerprint/face) verified via WebAuthn protocol are equivalent to traditional handwritten signatures.</li>
                <li>Digital signatures are subject to Egyptian Electronic Signature Regulation Law No. 15 of 2004.</li>
                <li>A digital log is maintained including: (signature time, device ID, IP address, contract digital fingerprint).</li>
                <li>The Client cannot deny the signature after successful biometric verification (Non-Repudiation principle).</li>
                <li>Signature data is encrypted with SHA-256 algorithm to ensure tamper-proof integrity.</li>
            </ol>
            """
        }


class HTMLContractBuilder:
    """Builds HTML contract with CSS styling"""
    
    def __init__(self):
        self.security_manager = SecurityManager()
        self.legal_clauses = LegalClausesEgypt()
    
    def get_css(self) -> str:
        """Get CSS styling for the contract"""
        return """
        @page {
            size: A4;
            margin: 2cm 1.5cm;
            @bottom-center {
                content: counter(page) " / " counter(pages);
                font-size: 9pt;
                color: #636e72;
            }
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            font-size: 10pt;
            line-height: 1.6;
            color: #2d3436;
        }
        
        .arabic {
            direction: rtl;
            text-align: right;
            font-family: 'Arial', 'Tahoma', sans-serif;
        }
        
        .english {
            direction: ltr;
            text-align: left;
        }
        
        .container {
            width: 100%;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #1a472a;
        }
        
        .main-title {
            font-size: 22pt;
            font-weight: bold;
            color: #1a472a;
            margin-bottom: 10px;
        }
        
        .section-title {
            font-size: 16pt;
            font-weight: bold;
            color: #1a472a;
            text-align: center;
            margin: 25px 0 15px 0;
            padding: 10px;
            background: linear-gradient(135deg, #1a472a 0%, #2c5f2d 100%);
            color: white;
            border-radius: 5px;
        }
        
        .two-column {
            display: table;
            width: 100%;
            margin-bottom: 20px;
        }
        
        .column {
            display: table-cell;
            width: 50%;
            padding: 15px;
            vertical-align: top;
            border: 1px solid #dfe6e9;
        }
        
        .column.arabic {
            border-right: 2px solid #1a472a;
        }
        
        .column.english {
            border-left: 2px solid #1a472a;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        
        th, td {
            padding: 12px;
            border: 1px solid #dfe6e9;
            text-align: left;
        }
        
        th {
            background: #1a472a;
            color: white;
            font-weight: bold;
        }
        
        tr:nth-child(even) {
            background: #f8f9fa;
        }
        
        .info-box {
            background: #f8f9fa;
            padding: 15px;
            border-left: 4px solid #1a472a;
            margin: 15px 0;
        }
        
        .party-header {
            background: #1a472a;
            color: white;
            padding: 10px;
            font-weight: bold;
            margin-top: 15px;
        }
        
        .qr-container {
            text-align: center;
            margin: 30px 0;
            padding: 20px;
            background: #f8f9fa;
            border: 2px dashed #1a472a;
            border-radius: 10px;
        }
        
        .qr-code {
            width: 200px;
            height: 200px;
            margin: 20px auto;
        }
        
        .signature-box {
            width: 45%;
            display: inline-block;
            margin: 20px 2%;
            padding: 20px;
            border: 2px solid #1a472a;
            text-align: center;
            vertical-align: top;
        }
        
        .signature-line {
            border-top: 2px solid #2d3436;
            margin: 60px 20px 10px 20px;
        }
        
        .page-break {
            page-break-after: always;
        }
        
        .milestone-table td {
            text-align: center;
        }
        
        .milestone-table td:nth-child(2),
        .milestone-table td:nth-child(3) {
            text-align: left;
        }
        
        .security-info {
            font-size: 8pt;
            background: #f8f9fa;
            padding: 8px;
            word-break: break-all;
        }
        
        h3 {
            color: #1a472a;
            margin: 15px 0 10px 0;
            font-size: 12pt;
        }
        
        ol {
            margin: 10px 0 10px 25px;
        }
        
        ol li {
            margin: 8px 0;
            line-height: 1.5;
        }
        
        .clause-box {
            background: white;
            padding: 20px;
            margin: 15px 0;
            border: 1px solid #dfe6e9;
            border-radius: 5px;
        }
        """
    
    def split_bilingual(self, text: str) -> Tuple[str, str]:
        """Split 'Arabic - English' text"""
        if ' - ' in text:
            parts = text.split(' - ', 1)
            return parts[0].strip(), parts[1].strip()
        return text, text
    
    def build_contract_html(self, contract_data: ContractData, milestones: List[Milestone]) -> str:
        """Build complete HTML contract"""
        
        # Split bilingual fields
        project_ar, project_en = self.split_bilingual(contract_data.project_title)
        currency_ar, currency_en = self.split_bilingual(contract_data.currency)
        payment_ar, payment_en = self.split_bilingual(contract_data.payment_terms)
        ip_ar, ip_en = self.split_bilingual(contract_data.ip_ownership)
        warranty_ar, warranty_en = self.split_bilingual(contract_data.warranty_period)
        law_ar, law_en = self.split_bilingual(contract_data.governing_law)
        
        # Generate QR code
        qr_code_base64 = self.security_manager.generate_qr_code_base64(contract_data.signing_link)
        
        # Build HTML
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Contract {contract_data.contract_id}</title>
        </head>
        <body>
            <div class="container">
                
                <!-- HEADER -->
                <div class="header">
                    <div class="main-title">
                        عقد تطوير برمجيات<br/>
                        SOFTWARE DEVELOPMENT CONTRACT
                    </div>
                </div>
                
                <!-- CONTRACT INFO -->
                <div class="two-column">
                    <div class="column arabic">
                        <strong>رقم العقد:</strong> {contract_data.contract_id}<br/>
                        <strong>التاريخ:</strong> {contract_data.contract_date}<br/>
                        <strong>المشروع:</strong> {project_ar}
                    </div>
                    <div class="column english">
                        <strong>Contract ID:</strong> {contract_data.contract_id}<br/>
                        <strong>Date:</strong> {contract_data.contract_date}<br/>
                        <strong>Project:</strong> {project_en}
                    </div>
                </div>
                
                <!-- PARTIES -->
                <div class="section-title">أطراف العقد / Contract Parties</div>
                
                <div class="two-column">
                    <div class="column arabic">
                        <div class="party-header">الطرف الأول (المطور)</div>
                        <p><strong>الاسم:</strong> {contract_data.dev_name}</p>
                        <p><strong>العنوان:</strong> {contract_data.dev_address}</p>
                        <p><strong>البريد الإلكتروني:</strong> {contract_data.dev_email}</p>
                        
                        <div class="party-header">الطرف الثاني (العميل)</div>
                        <p><strong>الشركة:</strong> {contract_data.client_name}</p>
                        <p><strong>الممثل:</strong> {contract_data.client_rep}</p>
                        <p><strong>البريد الإلكتروني:</strong> {contract_data.client_email}</p>
                        <p><strong>تليجرام:</strong> {contract_data.client_telegram}</p>
                    </div>
                    <div class="column english">
                        <div class="party-header">First Party (Developer)</div>
                        <p><strong>Name:</strong> {contract_data.dev_name}</p>
                        <p><strong>Address:</strong> {contract_data.dev_address}</p>
                        <p><strong>Email:</strong> {contract_data.dev_email}</p>
                        
                        <div class="party-header">Second Party (Client)</div>
                        <p><strong>Company:</strong> {contract_data.client_name}</p>
                        <p><strong>Representative:</strong> {contract_data.client_rep}</p>
                        <p><strong>Email:</strong> {contract_data.client_email}</p>
                        <p><strong>Telegram:</strong> {contract_data.client_telegram}</p>
                    </div>
                </div>
                
                <!-- FINANCIAL TERMS -->
                <div class="section-title">الشروط المالية / Financial Terms</div>
                
                <div class="two-column">
                    <div class="column arabic">
                        <p><strong>القيمة الإجمالية:</strong> {contract_data.total_value:,.2f} {currency_ar}</p>
                        <p><strong>شروط الدفع:</strong> {payment_ar}</p>
                        <p><strong>حقوق الملكية:</strong> {ip_ar}</p>
                        <p><strong>مدة الضمان:</strong> {warranty_ar}</p>
                        <p><strong>حد التعديلات:</strong> {contract_data.revision_limit} تعديلات لكل مرحلة</p>
                        <p><strong>القانون الحاكم:</strong> {law_ar}</p>
                    </div>
                    <div class="column english">
                        <p><strong>Total Value:</strong> {contract_data.total_value:,.2f} {currency_en}</p>
                        <p><strong>Payment Terms:</strong> {payment_en}</p>
                        <p><strong>IP Ownership:</strong> {ip_en}</p>
                        <p><strong>Warranty Period:</strong> {warranty_en}</p>
                        <p><strong>Revision Limit:</strong> {contract_data.revision_limit} revisions per milestone</p>
                        <p><strong>Governing Law:</strong> {law_en}</p>
                    </div>
                </div>
                
                <!-- MILESTONES -->
                <div class="section-title">مراحل المشروع / Project Milestones</div>
                
                <table class="milestone-table">
                    <thead>
                        <tr>
                            <th>#</th>
                            <th>Milestone / المرحلة</th>
                            <th>Description / التفاصيل</th>
                            <th>Price / السعر ({currency_en})</th>
                            <th>Duration / المدة (days)</th>
                            <th>Status / الحالة</th>
                        </tr>
                    </thead>
                    <tbody>
        """
        
        # Add milestones
        for m in milestones:
            m_title_ar, m_title_en = self.split_bilingual(m.title)
            html += f"""
                        <tr>
                            <td><strong>{m.order}</strong></td>
                            <td>{m_title_en}<br/><span class="arabic">{m_title_ar}</span></td>
                            <td style="text-align: justify; font-size: 9pt;">{m.description[:150]}...</td>
                            <td>{m.price:,.2f}</td>
                            <td>{m.duration}</td>
                            <td>☐ Pending</td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
                
                <!-- PAGE BREAK -->
                <div class="page-break"></div>
                
                <!-- LEGAL CLAUSES -->
                <div class="section-title">البنود القانونية / Legal Clauses</div>
        """
        
        # Add legal clauses
        clauses = [
            self.legal_clauses.get_termination_clause(),
            self.legal_clauses.get_confidentiality_clause(),
            self.legal_clauses.get_dispute_resolution_clause(),
            self.legal_clauses.get_force_majeure_clause(),
            self.legal_clauses.get_digital_signature_clause()
        ]
        
        for clause in clauses:
            html += f"""
                <div class="two-column clause-box">
                    <div class="column arabic">
                        {clause['ar']}
                    </div>
                    <div class="column english">
                        {clause['en']}
                    </div>
                </div>
            """
        
        html += f"""
                <!-- PAGE BREAK -->
                <div class="page-break"></div>
                
                <!-- DIGITAL SIGNATURE -->
                <div class="section-title">التوقيع الإلكتروني / Digital Signature</div>
                
                <div class="two-column">
                    <div class="column arabic">
                        <h3>كيفية التوقيع:</h3>
                        <ol>
                            <li>امسح رمز QR أدناه بهاتفك المحمول</li>
                            <li>تحقق من هويتك باستخدام البصمة أو التعرف على الوجه</li>
                            <li>سيتم تأمين توقيعك تشفيرياً</li>
                            <li>ستستلم نسخة موقعة عبر البريد الإلكتروني</li>
                        </ol>
                    </div>
                    <div class="column english">
                        <h3>How to Sign:</h3>
                        <ol>
                            <li>Scan the QR code below with your mobile device</li>
                            <li>Verify your identity using fingerprint or Face ID</li>
                            <li>Your signature will be cryptographically secured</li>
                            <li>You will receive a signed copy via email</li>
                        </ol>
                    </div>
                </div>
                
                <div class="qr-container">
                    <h3>Scan to Sign Contract / امسح للتوقيع على العقد</h3>
                    <img src="{qr_code_base64}" class="qr-code" alt="QR Code"/>
                </div>
                
                <!-- SECURITY INFO -->
                <div class="section-title">معلومات الأمان / Security Information</div>
                
                <table>
                    <tr>
                        <th>Security Feature / الميزة الأمنية</th>
                        <th>Value / القيمة</th>
                    </tr>
                    <tr>
                        <td>Verification Token / رمز التحقق</td>
                        <td class="security-info">{contract_data.verification_token[:24]}...</td>
                    </tr>
                    <tr>
                        <td>Contract Hash (SHA-256) / بصمة العقد</td>
                        <td class="security-info">{contract_data.digital_signature_hash[:24]}...</td>
                    </tr>
                    <tr>
                        <td>Biometric Status / المصادقة البيومترية</td>
                        <td>{contract_data.biometric_auth_status}</td>
                    </tr>
                    <tr>
                        <td>Signing Link / رابط التوقيع</td>
                        <td class="security-info">{contract_data.signing_link}</td>
                    </tr>
                </table>
                
                <!-- TRADITIONAL SIGNATURES -->
                <div class="section-title">التوقيعات التقليدية (اختياري) / Traditional Signatures (Optional)</div>
                
                <div class="signature-box">
                    <strong>First Party (Developer)</strong><br/>
                    <strong>الطرف الأول (المطور)</strong>
                    <div class="signature-line"></div>
                    Signature & Date / التوقيع والتاريخ
                </div>
                
                <div class="signature-box">
                    <strong>Second Party (Client)</strong><br/>
                    <strong>الطرف الثاني (العميل)</strong>
                    <div class="signature-line"></div>
                    Signature & Date / التوقيع والتاريخ
                </div>
                
            </div>
        </body>
        </html>
        """
        
        return html


class ContractGenerator:
    """Main contract generator class"""
    
    def __init__(self, excel_file_path: str, output_dir: str = "generated_contracts"):
        """
        Initialize the contract generator
        
        Args:
            excel_file_path: Path to Excel file with contract data
            output_dir: Directory to save generated PDFs
        """
        self.excel_file = excel_file_path
        self.output_dir = output_dir
        self.security_manager = SecurityManager()
        self.html_builder = HTMLContractBuilder()
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Load data
        self.contracts_df = None
        self.milestones_df = None
        self.load_excel_data()
    
    def load_excel_data(self) -> Tuple[bool, str]:
        """
        Load contract data from Excel file
        
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            self.contracts_df = pd.read_excel(self.excel_file, sheet_name=0)
            self.milestones_df = pd.read_excel(self.excel_file, sheet_name=1)
            
            # Validate required columns
            required_contract_cols = [
                'Contract_ID', 'Contract_Date', 'Project_Title', 'Dev_Name',
                'Client_Name', 'Total_Value', 'Currency'
            ]
            
            required_milestone_cols = [
                'Contract_ID', 'M_Order', 'M_Title', 'M_Price', 'M_Duration'
            ]
            
            missing_cols = [col for col in required_contract_cols if col not in self.contracts_df.columns]
            if missing_cols:
                return False, f"Missing contract columns: {', '.join(missing_cols)}"
            
            missing_milestone_cols = [col for col in required_milestone_cols if col not in self.milestones_df.columns]
            if missing_milestone_cols:
                return False, f"Missing milestone columns: {', '.join(missing_milestone_cols)}"
            
            return True, f"Successfully loaded {len(self.contracts_df)} contracts with milestones"
        
        except Exception as e:
            return False, f"Error loading Excel: {str(e)}"
    
    def get_contract_data(self, contract_id: str) -> Optional[ContractData]:
        """Extract contract data for specific contract ID"""
        try:
            row = self.contracts_df[self.contracts_df['Contract_ID'] == contract_id].iloc[0]
            
            # Generate security tokens
            verification_token = self.security_manager.generate_verification_token()
            signing_link = self.security_manager.generate_signing_link(contract_id, verification_token)
            
            return ContractData(
                contract_id=str(row['Contract_ID']),
                contract_date=str(row.get('Contract_Date', datetime.now().strftime('%Y-%m-%d'))),
                project_title=str(row['Project_Title']),
                dev_name=str(row['Dev_Name']),
                dev_address=str(row.get('Dev_Address', '')),
                dev_email=str(row.get('Dev_Email', '')),
                client_name=str(row['Client_Name']),
                client_rep=str(row.get('Client_Rep', '')),
                client_email=str(row.get('Client_Email', '')),
                client_telegram=str(row.get('Client_Telegram', '')),
                total_value=float(row['Total_Value']),
                currency=str(row['Currency']),
                payment_terms=str(row.get('Payment_Terms', 'الدفع المسبق 100% لكل مرحلة قبل البدء')),
                ip_ownership=str(row.get('IP_Ownership', 'تنتقل الملكية بعد سداد آخر دفعة فقط')),
                warranty_period=str(row.get('Warranty_Period', '90 يوماً')),
                revision_limit=int(row.get('Revision_Limit', 2)),
                governing_law=str(row.get('Governing_Law', 'جمهورية مصر العربية')),
                signing_link=signing_link,
                verification_token=verification_token
            )
        except Exception as e:
            print(f"Error extracting contract data: {e}")
            return None
    
    def get_milestones(self, contract_id: str) -> List[Milestone]:
        """Extract milestones for specific contract"""
        try:
            milestone_rows = self.milestones_df[self.milestones_df['Contract_ID'] == contract_id]
            milestones = []
            
            for _, row in milestone_rows.iterrows():
                milestones.append(Milestone(
                    contract_id=str(row['Contract_ID']),
                    order=int(row['M_Order']),
                    title=str(row['M_Title']),
                    description=str(row.get('M_Description', '')),
                    price=float(row['M_Price']),
                    duration=int(row['M_Duration'])
                ))
            
            return sorted(milestones, key=lambda x: x.order)
        except Exception as e:
            print(f"Error extracting milestones: {e}")
            return []
    
    def generate_contract(self, contract_id: str) -> Tuple[bool, str, Optional[str]]:
        """
        Generate PDF contract for specific contract ID
        
        Args:
            contract_id: The contract identifier
            
        Returns:
            Tuple of (success: bool, message: str, pdf_path: Optional[str])
        """
        try:
            # Get contract data
            contract_data = self.get_contract_data(contract_id)
            if not contract_data:
                return False, f"Contract {contract_id} not found", None
            
            # Get milestones
            milestones = self.get_milestones(contract_id)
            if not milestones:
                return False, f"No milestones found for contract {contract_id}", None
            
            # Generate contract hash
            contract_data.digital_signature_hash = self.security_manager.generate_contract_hash(
                contract_data, milestones
            )
            
            # Build HTML
            html_content = self.html_builder.build_contract_html(contract_data, milestones)
            css_content = self.html_builder.get_css()
            
            # Setup PDF
            pdf_filename = f"{contract_id}_{contract_data.client_name.replace(' ', '_')}.pdf"
            pdf_path = os.path.join(self.output_dir, pdf_filename)
            
            # Generate PDF from HTML
            HTML(string=html_content).write_pdf(
                pdf_path,
                stylesheets=[CSS(string=css_content)]
            )
            
            return True, f"Contract generated successfully: {pdf_filename}", pdf_path
            
        except Exception as e:
            return False, f"Error generating contract: {str(e)}", None
    
    def generate_all_contracts(self) -> Dict[str, Tuple[bool, str, Optional[str]]]:
        """
        Generate PDFs for all contracts in Excel file
        
        Returns:
            Dictionary mapping contract_id to (success, message, pdf_path)
        """
        results = {}
        
        for contract_id in self.contracts_df['Contract_ID'].unique():
            success, message, pdf_path = self.generate_contract(str(contract_id))
            results[str(contract_id)] = (success, message, pdf_path)
        
        return results
    
    def get_contract_metadata(self, contract_id: str) -> Optional[Dict]:
        """
        Get contract metadata for external use (e.g., email/telegram sending)
        
        Args:
            contract_id: The contract identifier
            
        Returns:
            Dictionary with contract metadata or None
        """
        try:
            contract_data = self.get_contract_data(contract_id)
            if not contract_data:
                return None
            
            milestones = self.get_milestones(contract_id)
            
            # Generate hash
            contract_data.digital_signature_hash = self.security_manager.generate_contract_hash(
                contract_data, milestones
            )
            
            return {
                'contract_id': contract_data.contract_id,
                'contract_date': contract_data.contract_date,
                'project_title': contract_data.project_title,
                'client_name': contract_data.client_name,
                'client_email': contract_data.client_email,
                'client_telegram': contract_data.client_telegram,
                'total_value': contract_data.total_value,
                'currency': contract_data.currency,
                'signing_link': contract_data.signing_link,
                'verification_token': contract_data.verification_token,
                'digital_hash': contract_data.digital_signature_hash,
                'milestone_count': len(milestones),
                'milestones': [
                    {
                        'order': m.order,
                        'title': m.title,
                        'price': m.price,
                        'duration': m.duration
                    } for m in milestones
                ]
            }
        except Exception as e:
            print(f"Error getting metadata: {e}")
            return None


# Example usage and testing
if __name__ == "__main__":
    """
    Example usage of the ContractGenerator class
    """
    
    print("=" * 70)
    print("CONTRACT GENERATOR - WeasyPrint Edition".center(70))
    print("=" * 70)
    print()
    
    # Initialize generator
    print("📂 Initializing Contract Generator...")
    generator = ContractGenerator(
        excel_file_path="contracts_data.xlsx",
        output_dir="generated_contracts"
    )
    
    # Load data
    success, message = generator.load_excel_data()
    print(f"📊 Data Loading: {message}")
    print()
    
    if success:
        # Generate single contract
        contract_id = "2026-001"
        print(f"📄 Generating Contract: {contract_id}")
        print("-" * 70)
        
        success, message, pdf_path = generator.generate_contract(contract_id)
        
        if success:
            print(f"✅ Status: Success")
            print(f"📝 Message: {message}")
            print(f"💾 File: {pdf_path}")
        else:
            print(f"❌ Status: Failed")
            print(f"⚠️  Error: {message}")
        
        print()
        
        # Get metadata for external use
        print(f"🔍 Fetching Contract Metadata...")
        print("-" * 70)
        
        metadata = generator.get_contract_metadata(contract_id)
        if metadata:
            print(f"📋 Contract ID: {metadata['contract_id']}")
            print(f"📧 Client Email: {metadata['client_email']}")
            print(f"💬 Telegram: {metadata['client_telegram']}")
            print(f"💰 Total Value: {metadata['total_value']:,.2f} {metadata['currency']}")
            print(f"🔗 Signing Link: {metadata['signing_link'][:50]}...")
            print(f"🔐 Verification Token: {metadata['verification_token'][:24]}...")
            print(f"#️⃣  Digital Hash: {metadata['digital_hash'][:24]}...")
            print(f"📊 Milestones: {metadata['milestone_count']}")
        
        print()
        print("=" * 70)
        
        # Generate all contracts
        print("🚀 Generating All Contracts...")
        print("=" * 70)
        print()
        
        all_results = generator.generate_all_contracts()
        
        success_count = sum(1 for s, _, _ in all_results.values() if s)
        fail_count = len(all_results) - success_count
        
        print(f"📊 Generation Summary:")
        print(f"   Total Contracts: {len(all_results)}")
        print(f"   ✅ Successful: {success_count}")
        print(f"   ❌ Failed: {fail_count}")
        print()
        
        print("📝 Detailed Results:")
        print("-" * 70)
        for cid, (success, msg, path) in all_results.items():
            status_icon = "✅" if success else "❌"
            print(f"{status_icon} {cid}: {msg}")
        
        print()
        print("=" * 70)
        print("🎉 Contract Generation Complete!".center(70))
        print("=" * 70)
    else:
        print(f"❌ Failed to load data. Please check your Excel file.")
        print(f"⚠️  Error: {message}")