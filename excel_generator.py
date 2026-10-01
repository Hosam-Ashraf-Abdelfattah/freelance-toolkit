"""
Excel Template Generator for Contract System
=============================================
Creates a ready-to-use Excel file with sample data for testing
the contract generator system.
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def create_contracts_template():
    """Create Sheet 1: Main Contract Information"""
    
    # Sample data for 3 contracts
    contracts_data = {
        'Contract_ID': ['2026-001', '2026-002', '2026-003'],
        'Contract_Date': [
            '2026-01-15',
            '2026-01-10', 
            '2026-01-20'
        ],
        'Project_Title': [
            'نظام إدارة المخازن الذكي - Smart Warehouse Management System',
            'تطبيق التجارة الإلكترونية - E-Commerce Mobile App',
            'منصة التعليم عن بعد - Online Learning Platform'
        ],
        'Dev_Name': [
            'محمد أحمد علي',
            'محمد أحمد علي',
            'محمد أحمد علي'
        ],
        'Dev_Address': [
            '15 شارع الجمهورية، المنصورة، الدقهلية، مصر',
            '15 شارع الجمهورية، المنصورة، الدقهلية، مصر',
            '15 شارع الجمهورية، المنصورة، الدقهلية، مصر'
        ],
        'Dev_Email': [
            'mohamed.dev@techsolutions.com',
            'mohamed.dev@techsolutions.com',
            'mohamed.dev@techsolutions.com'
        ],
        'Client_Name': [
            'شركة النور للتجارة والتوزيع',
            'مؤسسة الأمل التجارية',
            'أكاديمية المستقبل للتدريب'
        ],
        'Client_Rep': [
            'أحمد محمود حسن',
            'سارة عبدالله إبراهيم',
            'خالد عمر السيد'
        ],
        'Client_Email': [
            'ahmed.mahmoud@alnoor-trade.com',
            'sara.abdullah@alamal.com',
            'khaled.omar@future-academy.edu'
        ],
        'Client_Telegram': [
            '@ahmed_alnoor',
            '@sara_alamal',
            '@khaled_future'
        ],
        'Total_Value': [
            85000.00,
            120000.00,
            95000.00
        ],
        'Currency': [
            'جنيه مصري - EGP',
            'جنيه مصري - EGP',
            'دولار أمريكي - USD'
        ],
        'Payment_Terms': [
            'الدفع المسبق 100% لكل مرحلة قبل البدء - 100% prepayment for each milestone before starting',
            'الدفع المسبق 100% لكل مرحلة قبل البدء - 100% prepayment for each milestone before starting',
            'الدفع المسبق 100% لكل مرحلة قبل البدء - 100% prepayment for each milestone before starting'
        ],
        'IP_Ownership': [
            'تنتقل الملكية الفكرية للعميل بعد سداد آخر دفعة فقط - IP transfers to client after final payment only',
            'تنتقل الملكية الفكرية للعميل بعد سداد آخر دفعة فقط - IP transfers to client after final payment only',
            'تنتقل الملكية الفكرية للعميل بعد سداد آخر دفعة فقط - IP transfers to client after final payment only'
        ],
        'Warranty_Period': [
            '90 يوماً من تاريخ التسليم النهائي - 90 days from final delivery',
            '60 يوماً من تاريخ التسليم النهائي - 60 days from final delivery',
            '120 يوماً من تاريخ التسليم النهائي - 120 days from final delivery'
        ],
        'Revision_Limit': [2, 3, 2],
        'Governing_Law': [
            'جمهورية مصر العربية - Arab Republic of Egypt',
            'جمهورية مصر العربية - Arab Republic of Egypt',
            'جمهورية مصر العربية - Arab Republic of Egypt'
        ],
        'Signing_Link': ['', '', ''],  # Will be auto-generated
        'Verification_Token': ['', '', ''],  # Will be auto-generated
        'Biometric_Auth_Status': ['Pending', 'Pending', 'Pending'],
        'Device_ID': ['', '', ''],  # Will be filled upon signing
        'IP_Log': ['', '', ''],  # Will be filled upon signing
        'Digital_Signature_Hash': ['', '', '']  # Will be generated
    }
    
    return pd.DataFrame(contracts_data)


def create_milestones_template():
    """Create Sheet 2: Project Milestones"""
    
    milestones_data = {
        'Contract_ID': [],
        'M_Order': [],
        'M_Title': [],
        'M_Description': [],
        'M_Price': [],
        'M_Duration': []
    }
    
    # Contract 2026-001: Warehouse Management System (5 milestones)
    contract_001_milestones = [
        {
            'order': 1,
            'title': 'تحليل المتطلبات وتصميم قاعدة البيانات - Requirements Analysis & Database Design',
            'description': 'دراسة احتياجات النظام، تصميم ERD، إنشاء جداول MySQL، تحديد العلاقات بين الكيانات، توثيق المواصفات الفنية الكاملة',
            'price': 15000.00,
            'duration': 10
        },
        {
            'order': 2,
            'title': 'برمجة لوحة التحكم الإدارية - Admin Dashboard Development',
            'description': 'بناء لوحة تحكم باستخدام React + Node.js، إدارة المخزون، تقارير الحركة، صلاحيات المستخدمين، واجهة عربية/إنجليزية',
            'price': 25000.00,
            'duration': 20
        },
        {
            'order': 3,
            'title': 'تطوير نظام الباركود والمسح الضوئي - Barcode & Scanner System',
            'description': 'تكامل قارئ الباركود، توليد QR codes للمنتجات، نظام إدخال وإخراج تلقائي، تتبع الحركة الفورية',
            'price': 18000.00,
            'duration': 15
        },
        {
            'order': 4,
            'title': 'نظام التقارير والتحليلات - Reports & Analytics System',
            'description': 'تقارير المخزون التفصيلية، تحليلات الحركة، رسوم بيانية تفاعلية، تصدير Excel/PDF، إشعارات النقص التلقائية',
            'price': 17000.00,
            'duration': 12
        },
        {
            'order': 5,
            'title': 'الاختبار والتسليم النهائي - Testing & Final Deployment',
            'description': 'اختبارات شاملة، تدريب الموظفين، نشر على السيرفر، توثيق المستخدم، دعم فني لمدة شهر',
            'price': 10000.00,
            'duration': 8
        }
    ]
    
    for m in contract_001_milestones:
        milestones_data['Contract_ID'].append('2026-001')
        milestones_data['M_Order'].append(m['order'])
        milestones_data['M_Title'].append(m['title'])
        milestones_data['M_Description'].append(m['description'])
        milestones_data['M_Price'].append(m['price'])
        milestones_data['M_Duration'].append(m['duration'])
    
    # Contract 2026-002: E-Commerce Mobile App (6 milestones)
    contract_002_milestones = [
        {
            'order': 1,
            'title': 'تصميم واجهات المستخدم - UI/UX Design',
            'description': 'تصميم شاشات التطبيق بالكامل، نماذج تفاعلية (Prototypes)، اختبارات تجربة المستخدم، دليل الألوان والخطوط',
            'price': 20000.00,
            'duration': 12
        },
        {
            'order': 2,
            'title': 'برمجة التطبيق (Android & iOS) - Mobile App Development',
            'description': 'بناء التطبيق باستخدام React Native، صفحات المنتجات، سلة المشتريات، نظام البحث والفلترة، التكامل مع API',
            'price': 35000.00,
            'duration': 25
        },
        {
            'order': 3,
            'title': 'تطوير لوحة إدارة التجار - Merchant Dashboard',
            'description': 'لوحة تحكم ويب للتجار، إضافة/تعديل المنتجات، إدارة الطلبات، تقارير المبيعات، نظام الإشعارات',
            'price': 22000.00,
            'duration': 18
        },
        {
            'order': 4,
            'title': 'تكامل بوابات الدفع - Payment Gateway Integration',
            'description': 'ربط Fawry، PayMob، Visa/Mastercard، Apple Pay، Google Pay، نظام استرجاع الأموال، سجل المعاملات الآمن',
            'price': 18000.00,
            'duration': 10
        },
        {
            'order': 5,
            'title': 'نظام الإشعارات والتتبع - Notifications & Tracking',
            'description': 'إشعارات Push للطلبات، تتبع الشحنات (GPS)، إشعارات SMS، تكامل مع شركات الشحن، تحديثات فورية',
            'price': 15000.00,
            'duration': 10
        },
        {
            'order': 6,
            'title': 'الاختبار والنشر - Testing & Deployment',
            'description': 'اختبارات شاملة (Unit/Integration)، نشر على App Store و Google Play، توثيق API، دعم فني شهرين',
            'price': 10000.00,
            'duration': 12
        }
    ]
    
    for m in contract_002_milestones:
        milestones_data['Contract_ID'].append('2026-002')
        milestones_data['M_Order'].append(m['order'])
        milestones_data['M_Title'].append(m['title'])
        milestones_data['M_Description'].append(m['description'])
        milestones_data['M_Price'].append(m['price'])
        milestones_data['M_Duration'].append(m['duration'])
    
    # Contract 2026-003: Online Learning Platform (4 milestones)
    contract_003_milestones = [
        {
            'order': 1,
            'title': 'تصميم المنصة وقاعدة البيانات - Platform Design & Database',
            'description': 'تصميم معماري كامل، ERD للمستخدمين/الكورسات/الاختبارات، تصميم واجهات الطلاب والمدرسين، دليل الهوية البصرية',
            'price': 18000.00,
            'duration': 14
        },
        {
            'order': 2,
            'title': 'برمجة نظام إدارة المحتوى - LMS Development',
            'description': 'نظام رفع الفيديوهات (AWS S3)، محرر الدروس، نظام الاختبارات التفاعلية، تتبع تقدم الطالب، شهادات إتمام آلية',
            'price': 35000.00,
            'duration': 28
        },
        {
            'order': 3,
            'title': 'نظام المحاضرات المباشرة - Live Streaming System',
            'description': 'تكامل Zoom/WebRTC، جدولة المحاضرات، تسجيل تلقائي، غرف نقاش، مشاركة الشاشة، whiteboard تفاعلي',
            'price': 28000.00,
            'duration': 20
        },
        {
            'order': 4,
            'title': 'نظام الدفع والشهادات - Payment & Certification',
            'description': 'بوابات الدفع المتعددة، نظام الاشتراكات الشهرية، شهادات PDF آلية، نظام التقييمات والمراجعات، الاختبار والتسليم',
            'price': 14000.00,
            'duration': 10
        }
    ]
    
    for m in contract_003_milestones:
        milestones_data['Contract_ID'].append('2026-003')
        milestones_data['M_Order'].append(m['order'])
        milestones_data['M_Title'].append(m['title'])
        milestones_data['M_Description'].append(m['description'])
        milestones_data['M_Price'].append(m['price'])
        milestones_data['M_Duration'].append(m['duration'])
    
    return pd.DataFrame(milestones_data)


def create_excel_file(filename='contracts_data.xlsx'):
    """
    Create complete Excel file with both sheets
    
    Args:
        filename: Output Excel filename
        
    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        # Create both sheets
        contracts_df = create_contracts_template()
        milestones_df = create_milestones_template()
        
        # Write to Excel with proper formatting
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Sheet 1: Contracts
            contracts_df.to_excel(writer, sheet_name='Contracts', index=False)
            
            # Sheet 2: Milestones
            milestones_df.to_excel(writer, sheet_name='Milestones', index=False)
            
            # Auto-adjust column widths
            for sheet_name in writer.sheets:
                worksheet = writer.sheets[sheet_name]
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
        
        # Print summary
        print(f"✅ Excel file created successfully: {filename}")
        print(f"\n📊 Summary:")
        print(f"  Sheet 1 (Contracts): {len(contracts_df)} contracts")
        print(f"  Sheet 2 (Milestones): {len(milestones_df)} milestones")
        print(f"\n📋 Contract Details:")
        
        for idx, row in contracts_df.iterrows():
            milestone_count = len(milestones_df[milestones_df['Contract_ID'] == row['Contract_ID']])
            total = milestones_df[milestones_df['Contract_ID'] == row['Contract_ID']]['M_Price'].sum()
            print(f"  • {row['Contract_ID']}: {row['Project_Title'][:50]}...")
            print(f"    Client: {row['Client_Name']}")
            print(f"    Value: {row['Total_Value']:,.2f} {row['Currency'].split('-')[0].strip()}")
            print(f"    Milestones: {milestone_count} (Total: {total:,.2f})")
            print()
        
        return True, f"Excel file created: {filename}"
        
    except Exception as e:
        return False, f"Error creating Excel: {str(e)}"


def print_column_reference():
    """Print column reference guide for users"""
    print("=" * 80)
    print("📚 EXCEL COLUMNS REFERENCE GUIDE")
    print("=" * 80)
    
    print("\n🔷 SHEET 1: Contracts (معلومات العقد الرئيسية)")
    print("-" * 80)
    
    sheet1_columns = {
        'Contract_ID': 'رقم العقد الفريد (مثل: 2026-001)',
        'Contract_Date': 'تاريخ العقد (YYYY-MM-DD)',
        'Project_Title': 'عنوان المشروع (عربي - English)',
        'Dev_Name': 'اسم المطور الكامل',
        'Dev_Address': 'عنوان المطور',
        'Dev_Email': 'بريد المطور الإلكتروني',
        'Client_Name': 'اسم العميل/الشركة',
        'Client_Rep': 'اسم ممثل العميل',
        'Client_Email': 'بريد العميل',
        'Client_Telegram': 'معرف تليجرام العميل (@username)',
        'Total_Value': 'القيمة الإجمالية (رقم)',
        'Currency': 'العملة (عربي - English)',
        'Payment_Terms': 'شروط الدفع',
        'IP_Ownership': 'حقوق الملكية الفكرية',
        'Warranty_Period': 'مدة الضمان',
        'Revision_Limit': 'عدد التعديلات المسموحة (رقم)',
        'Governing_Law': 'القانون الحاكم',
        'Signing_Link': 'رابط التوقيع (يُملأ تلقائياً)',
        'Verification_Token': 'رمز التحقق (يُملأ تلقائياً)',
        'Biometric_Auth_Status': 'حالة التوقيع البيومتري',
        'Device_ID': 'معرف الجهاز (يُملأ عند التوقيع)',
        'IP_Log': 'عنوان IP (يُملأ عند التوقيع)',
        'Digital_Signature_Hash': 'بصمة العقد الرقمية (SHA-256)'
    }
    
    for col, desc in sheet1_columns.items():
        print(f"  • {col:25s} : {desc}")
    
    print("\n🔷 SHEET 2: Milestones (مراحل المشروع)")
    print("-" * 80)
    
    sheet2_columns = {
        'Contract_ID': 'رقم العقد (يجب أن يطابق Sheet 1)',
        'M_Order': 'ترتيب المرحلة (1, 2, 3...)',
        'M_Title': 'اسم المرحلة (عربي - English)',
        'M_Description': 'وصف تفصيلي للمرحلة',
        'M_Price': 'سعر المرحلة (رقم)',
        'M_Duration': 'مدة التنفيذ بالأيام (رقم)'
    }
    
    for col, desc in sheet2_columns.items():
        print(f"  • {col:25s} : {desc}")
    
    print("\n" + "=" * 80)
    print("💡 TIPS:")
    print("  1. لا تحذف أي عمود حتى لو كان فارغاً")
    print("  2. Contract_ID في Sheet 2 يجب أن يطابق تماماً Sheet 1")
    print("  3. الأعمدة الأمنية (Signing_Link, Verification_Token, etc.) تُملأ تلقائياً")
    print("  4. استخدم التنسيق: 'عربي - English' في الحقول المهمة")
    print("=" * 80)


# Run the script
if __name__ == "__main__":
    # Print column reference
    print_column_reference()
    
    print("\n")
    input("Press Enter to create sample Excel file...")
    print("\n")
    
    # Create Excel file
    success, message = create_excel_file('contracts_data.xlsx')
    
    if success:
        print(f"\n🎉 {message}")
        print(f"\n📝 Next Steps:")
        print(f"  1. Open 'contracts_data.xlsx' to review the sample data")
        print(f"  2. Modify the data as needed for your contracts")
        print(f"  3. Run the ContractGenerator to create PDFs")
        print(f"\n💻 Example Code:")
        print(f"  from contract_generator import ContractGenerator")
        print(f"  gen = ContractGenerator('contracts_data.xlsx')")
        print(f"  success, msg, path = gen.generate_contract('2026-001')")
    else:
        print(f"\n❌ Error: {message}")