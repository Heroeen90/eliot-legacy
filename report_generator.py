# -*- coding: utf-8 -*-
# نظام إنشاء التقارير

from datetime import datetime
import json

def generate_report_html(scan_type, target, findings, tools_used, duration):
    """توليد تقرير HTML احترافي"""
    
    risk_colors = {
        "critical": "#ff0000",
        "high": "#ff6600",
        "medium": "#ffcc00",
        "low": "#00cc00",
        "info": "#0099ff"
    }
    
    findings_html = ""
    for f in findings:
        color = risk_colors.get(f.get('risk', 'low'), '#00cc00')
        findings_html += f"""
        <tr>
            <td style="padding:10px;border:1px solid #333;color:{color};font-weight:700">{f.get('risk','N/A').upper()}</td>
            <td style="padding:10px;border:1px solid #333">{f.get('name','N/A')}</td>
            <td style="padding:10px;border:1px solid #333">{f.get('description','N/A')}</td>
            <td style="padding:10px;border:1px solid #333;color:#00ffcc">{f.get('fix','N/A')}</td>
        </tr>"""
    
    tools_html = ", ".join(tools_used) if tools_used else "N/A"
    
    html = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <title>تقرير إرث إليوت - {scan_type}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, sans-serif; background: #0a0a0f; color: #ccc; padding: 30px; }}
            h1 {{ color: #00ffcc; border-bottom: 2px solid #00ffcc33; padding-bottom: 10px; }}
            h2 {{ color: #ff6600; margin-top: 25px; }}
            .meta {{ background: #111; padding: 15px; border-radius: 8px; margin: 15px 0; }}
            .meta span {{ color: #00ffcc; }}
            table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
            th {{ background: #1a1a2e; padding: 12px; border: 1px solid #333; text-align: right; }}
            .footer {{ margin-top: 40px; padding-top: 15px; border-top: 1px solid #333; font-size: 0.8rem; color: #666; }}
        </style>
    </head>
    <body>
        <h1>💀 إرث إليوت — تقرير أمني</h1>
        
        <div class="meta">
            <p><span>📋 نوع الفحص:</span> {scan_type}</p>
            <p><span>🎯 الهدف:</span> {target}</p>
            <p><span>🔧 الأدوات المستخدمة:</span> {tools_html}</p>
            <p><span>⏱️ المدة:</span> {duration}</p>
            <p><span>📅 التاريخ:</span> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <h2>🚨 الثغرات المكتشفة</h2>
        <table>
            <thead>
                <tr>
                    <th>مستوى الخطورة</th>
                    <th>اسم الثغرة</th>
                    <th>الوصف</th>
                    <th>الحل</th>
                </tr>
            </thead>
            <tbody>
                {findings_html if findings_html else '<tr><td colspan="4" style="text-align:center;padding:20px">لم يتم اكتشاف ثغرات</td></tr>'}
            </tbody>
        </table>
        
        <h2>💡 توصيات</h2>
        <ul>
            <li>تحديث جميع الأنظمة والبرامج إلى آخر الإصدارات</li>
            <li>تغيير كلمات المرور الضعيفة</li>
            <li>تفعيل جدار الحماية</li>
            <li>إجراء فحوصات دورية</li>
        </ul>
        
        <div class="footer">
            <p>تم إنشاء هذا التقرير بواسطة <strong>إرث إليوت | Eliot's Legacy</strong></p>
            <p>🛡️ للأغراض التعليمية والأمنية فقط</p>
        </div>
    </body>
    </html>
    """
    
    return html

def generate_report_json(scan_type, target, findings, tools_used):
    """توليد تقرير JSON"""
    return {
        "report_type": scan_type,
        "target": target,
        "date": datetime.now().isoformat(),
        "tools_used": tools_used,
        "findings_count": len(findings),
        "findings": findings,
        "generated_by": "Eliot's Legacy Platform"
    }

def generate_summary(findings):
    """توليد ملخص تنفيذي"""
    critical = len([f for f in findings if f.get('risk') == 'critical'])
    high = len([f for f in findings if f.get('risk') == 'high'])
    medium = len([f for f in findings if f.get('risk') == 'medium'])
    low = len([f for f in findings if f.get('risk') == 'low'])
    
    total = len(findings)
    
    if total == 0:
        risk_level = "آمن"
        risk_color = "#00ff00"
    elif critical > 0:
        risk_level = "خطر جداً"
        risk_color = "#ff0000"
    elif high > 0:
        risk_level = "عالي الخطورة"
        risk_color = "#ff6600"
    elif medium > 0:
        risk_level = "متوسط الخطورة"
        risk_color = "#ffcc00"
    else:
        risk_level = "منخفض الخطورة"
        risk_color = "#00cc00"
    
    return {
        "total": total,
        "critical": critical,
        "high": high,
        "medium": medium,
        "low": low,
        "risk_level": risk_level,
        "risk_color": risk_color
    }
