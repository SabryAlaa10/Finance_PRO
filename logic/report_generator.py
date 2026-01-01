"""
Report Generator Module
Generates professional PDF reports for weekly and monthly financial summaries.
"""
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server environments
import matplotlib.pyplot as plt
import numpy as np


def get_period_data(df: pd.DataFrame, period_type: str = "weekly"):
    """
    Filter data for the specified period (weekly or monthly).
    
    Args:
        df: Transaction dataframe
        period_type: "weekly" or "monthly"
        
    Returns:
        Filtered dataframe and period info (start_date, end_date)
    """
    today = datetime.now().date()  # Get date only, not timestamp
    
    if period_type == "weekly":
        # Last 7 days
        start_date = today - timedelta(days=7)
        period_name = "Weekly Report (Last 7 Days)"
    else:  # monthly
        # Current month from day 1 to today
        start_date = today.replace(day=1)
        period_name = f"Monthly Report ({datetime.now().strftime('%B %Y')})"
    
    end_date = today
    
    # Convert df Date to date only for comparison (remove time component)
    df_copy = df.copy()
    df_copy["Date"] = pd.to_datetime(df_copy["Date"]).dt.date
    
    # Filter dataframe
    filtered_df = df_copy[
        (df_copy["Date"] >= start_date) & 
        (df_copy["Date"] <= end_date)
    ].copy()
    
    # Convert back to datetime for charts compatibility
    filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])
    
    return filtered_df, start_date, end_date, period_name


def calculate_summary_stats(df: pd.DataFrame):
    """
    Calculate summary statistics for the report.
    
    Returns:
        Dictionary with summary stats
    """
    if df.empty:
        return {
            "total_income": 0,
            "total_expenses": 0,
            "total_investments": 0,
            "net_balance": 0,
            "num_transactions": 0
        }
    
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expenses = df[df["Type"] == "Expense"]["Amount"].sum()
    investments = df[df["Type"] == "Investment"]["Amount"].sum()
    
    return {
        "total_income": income,
        "total_expenses": expenses,
        "total_investments": investments,
        "net_balance": income - expenses,  # Net = Income - Expenses only
        "num_transactions": len(df)
    }


def create_chart_image(df: pd.DataFrame, chart_type: str = "summary"):
    """
    Create chart using matplotlib and return as image bytes.
    
    Args:
        df: Transaction dataframe
        chart_type: "summary", "category_breakdown", "daily_trend", "income_sources"
        
    Returns:
        Image bytes
    """
    try:
        buf = BytesIO()
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 5), dpi=150)
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')
        
        if df.empty:
            # Create empty placeholder
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', fontsize=16, color='#94a3b8',
                   transform=ax.transAxes)
            ax.axis('off')
        
        elif chart_type == "summary":
            # Financial Summary bar chart
            income = df[df["Type"] == "Income"]["Amount"].sum()
            expenses = df[df["Type"] == "Expense"]["Amount"].sum()
            investments = df[df["Type"] == "Investment"]["Amount"].sum()
            
            categories = ['Income', 'Expenses', 'Investments']
            values = [income, expenses, investments]
            colors_list = ['#22c55e', '#ef4444', '#a855f7']
            
            bars = ax.bar(categories, values, color=colors_list, edgecolor='#1e293b', linewidth=2.5, width=0.6)
            ax.set_ylabel('Amount (EGP)', fontsize=13, fontweight='bold', color='#1e293b')
            ax.set_title('Financial Summary', fontsize=17, fontweight='bold', pad=20, color='#1e293b')
            ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.8)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#cbd5e1')
            ax.spines['bottom'].set_color('#cbd5e1')
            
            # Add value labels on bars
            for bar, val in zip(bars, values):
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'{val:,.0f} EGP', ha='center', va='bottom', 
                           fontweight='bold', fontsize=11, color='#1e293b')
        
        elif chart_type == "income_sources":
            # Income breakdown by category
            income_df = df[df["Type"] == "Income"]
            if not income_df.empty:
                income_summary = income_df.groupby("Category")["Amount"].sum().sort_values().reset_index()
                
                bars = ax.barh(income_summary["Category"], income_summary["Amount"], 
                       color='#22c55e', edgecolor='#059669', linewidth=2)
                ax.set_xlabel('Amount (EGP)', fontsize=13, fontweight='bold', color='#1e293b')
                ax.set_title('Income by Source', fontsize=17, fontweight='bold', pad=20, color='#1e293b')
                ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.8)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color('#cbd5e1')
                ax.spines['bottom'].set_color('#cbd5e1')
                
                # Add value labels
                for i, val in enumerate(income_summary["Amount"]):
                    ax.text(val, i, f' {val:,.0f} EGP', va='center', 
                           fontweight='bold', fontsize=10, color='#1e293b')
            else:
                ax.text(0.5, 0.5, 'No income data', 
                       ha='center', va='center', fontsize=16, color='#94a3b8',
                       transform=ax.transAxes)
                ax.axis('off')
        
        elif chart_type == "category_breakdown":
            # Expenses by category
            expenses_df = df[df["Type"] == "Expense"]
            if not expenses_df.empty:
                cat_summary = expenses_df.groupby("Category")["Amount"].sum().sort_values().reset_index()
                
                bars = ax.barh(cat_summary["Category"], cat_summary["Amount"],
                       color='#ef4444', edgecolor='#b91c1c', linewidth=2)
                ax.set_xlabel('Amount (EGP)', fontsize=13, fontweight='bold', color='#1e293b')
                ax.set_title('Expense Breakdown', fontsize=17, fontweight='bold', pad=20, color='#1e293b')
                ax.grid(axis='x', alpha=0.3, linestyle='--', linewidth=0.8)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_color('#cbd5e1')
                ax.spines['bottom'].set_color('#cbd5e1')
                
                # Add value labels
                for i, val in enumerate(cat_summary["Amount"]):
                    ax.text(val, i, f' {val:,.0f} EGP', va='center', 
                           fontweight='bold', fontsize=10, color='#1e293b')
            else:
                ax.text(0.5, 0.5, 'No expense data', 
                       ha='center', va='center', fontsize=16, color='#94a3b8',
                       transform=ax.transAxes)
                ax.axis('off')
        
        elif chart_type == "daily_trend":
            # Daily transaction trend
            if not df.empty:
                daily = df.groupby([df["Date"].dt.date, "Type"])["Amount"].sum().reset_index()
                
                # Plot each transaction type
                has_data = False
                for txn_type, color, marker in [("Income", "#22c55e", "o"), 
                                                 ("Expense", "#ef4444", "s"), 
                                                 ("Investment", "#a855f7", "^")]:
                    type_data = daily[daily["Type"] == txn_type]
                    if not type_data.empty:
                        ax.plot(type_data["Date"], type_data["Amount"], 
                               marker=marker, linewidth=2.5, markersize=8,
                               color=color, label=txn_type, markeredgecolor='white',
                               markeredgewidth=1.5)
                        has_data = True
                
                if has_data:
                    ax.set_xlabel('Date', fontsize=13, fontweight='bold', color='#1e293b')
                    ax.set_ylabel('Amount (EGP)', fontsize=13, fontweight='bold', color='#1e293b')
                    ax.set_title('Daily Transaction Trend', fontsize=17, fontweight='bold', 
                                pad=20, color='#1e293b')
                    ax.legend(loc='upper left', framealpha=0.95, edgecolor='#cbd5e1')
                    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.spines['left'].set_color('#cbd5e1')
                    ax.spines['bottom'].set_color('#cbd5e1')
                    plt.xticks(rotation=45, ha='right')
                else:
                    ax.text(0.5, 0.5, 'No transaction data', 
                           ha='center', va='center', fontsize=16, color='#94a3b8',
                           transform=ax.transAxes)
                    ax.axis('off')
            else:
                ax.text(0.5, 0.5, 'No transaction data', 
                       ha='center', va='center', fontsize=16, color='#94a3b8',
                       transform=ax.transAxes)
                ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        
        buf.seek(0)
        return buf.getvalue()
        
    except Exception as e:
        print(f"Chart generation error: {e}")
        # Return error placeholder image
        try:
            fig_empty, ax_empty = plt.subplots(figsize=(10, 5), dpi=100)
            ax_empty.text(0.5, 0.5, f'Chart generation failed\n{str(e)}', 
                         ha='center', va='center', fontsize=12, color='#ef4444',
                         transform=ax_empty.transAxes)
            ax_empty.axis('off')
            buf_empty = BytesIO()
            plt.savefig(buf_empty, format='png', dpi=100, bbox_inches='tight', facecolor='white')
            plt.close(fig_empty)
            buf_empty.seek(0)
            return buf_empty.getvalue()
        except:
            # Last resort: return minimal image
            return b''


def generate_pdf_report(df: pd.DataFrame, period_type: str = "weekly"):
    """
    Generate a professional PDF report.
    
    Args:
        df: Full transaction dataframe
        period_type: "weekly" or "monthly"
        
    Returns:
        BytesIO object containing the PDF
    """
    # Get period data
    filtered_df, start_date, end_date, period_name = get_period_data(df, period_type)
    
    # Calculate statistics
    stats = calculate_summary_stats(filtered_df)
    
    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch,
        leftMargin=0.75*inch,
        rightMargin=0.75*inch
    )
    
    # Container for PDF elements
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    
    # Custom styles matching app colors
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor("#64748b"),
        spaceAfter=20,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )
    
    # Header Section
    story.append(Paragraph(f"💎 Finance PRO - {period_name}", title_style))
    
    # Add helpful note for monthly reports
    if period_type == "monthly":
        period_note = f"Period: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')} (Current Month to Date)"
    else:
        period_note = f"Period: {start_date.strftime('%B %d, %Y')} - {end_date.strftime('%B %d, %Y')} (Last 7 Days)"
    
    story.append(Paragraph(period_note, subtitle_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Summary Statistics Section
    story.append(Paragraph("📊 Financial Summary", heading_style))
    
    # Create summary table with app colors
    summary_data = [
        ["Metric", "Amount (EGP)", "Status"],
        ["Total Income", f"{stats['total_income']:,.0f}", "✓"],
        ["Total Expenses", f"{stats['total_expenses']:,.0f}", "✓"],
        ["Total Investments", f"{stats['total_investments']:,.0f}", "✓"],
        ["Net Balance", f"{stats['net_balance']:,.0f}", 
         "🟢 Positive" if stats['net_balance'] >= 0 else "🔴 Negative"],
        ["Total Transactions", f"{stats['num_transactions']}", "✓"]
    ]
    
    summary_table = Table(summary_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
    summary_table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Data rows
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#f8fafc")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#1e293b")),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        
        # Grid
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Charts Section
    if not filtered_df.empty:
        # Summary Chart
        story.append(Paragraph("📈 Visual Analysis", heading_style))
        try:
            summary_chart = create_chart_image(filtered_df, "summary")
            img = Image(BytesIO(summary_chart), width=6*inch, height=3*inch)
            story.append(img)
            story.append(Spacer(1, 0.2*inch))
        except Exception as e:
            story.append(Paragraph(f"Chart generation error: {str(e)}", styles['Normal']))
        
        # Income Sources Chart
        if len(filtered_df[filtered_df["Type"] == "Income"]) > 0:
            story.append(Paragraph("💰 Income by Source", heading_style))
            try:
                income_chart = create_chart_image(filtered_df, "income_sources")
                img_income = Image(BytesIO(income_chart), width=6*inch, height=3*inch)
                story.append(img_income)
                story.append(Spacer(1, 0.2*inch))
            except Exception as e:
                story.append(Paragraph(f"Chart generation error: {str(e)}", styles['Normal']))
        
        # Expense Category Breakdown
        if len(filtered_df[filtered_df["Type"] == "Expense"]) > 0:
            story.append(Paragraph("🎯 Expense Breakdown", heading_style))
            try:
                category_chart = create_chart_image(filtered_df, "category_breakdown")
                img2 = Image(BytesIO(category_chart), width=6*inch, height=3*inch)
                story.append(img2)
                story.append(Spacer(1, 0.2*inch))
            except Exception as e:
                story.append(Paragraph(f"Chart generation error: {str(e)}", styles['Normal']))
        
        # Daily Trend Chart
        story.append(Paragraph("📊 Daily Transaction Trend", heading_style))
        try:
            trend_chart = create_chart_image(filtered_df, "daily_trend")
            img3 = Image(BytesIO(trend_chart), width=6*inch, height=3*inch)
            story.append(img3)
            story.append(Spacer(1, 0.2*inch))
        except Exception as e:
            story.append(Paragraph(f"Chart generation error: {str(e)}", styles['Normal']))
        
        # Transaction Details
        story.append(PageBreak())
        story.append(Paragraph("📝 Transaction Details", heading_style))
        
        # Create transactions table
        txn_data = [["Date", "Type", "Category", "Amount (EGP)", "Source"]]
        
        for _, row in filtered_df.sort_values("Date", ascending=False).iterrows():
            txn_data.append([
                row["Date"].strftime("%Y-%m-%d"),
                row["Type"],
                row["Category"][:20] if pd.notna(row["Category"]) else "N/A",
                f"{row['Amount']:,.0f}",
                row["Source"][:15] if pd.notna(row["Source"]) else "N/A"
            ])
        
        txn_table = Table(txn_data, colWidths=[1.2*inch, 1*inch, 1.5*inch, 1.2*inch, 1.1*inch])
        txn_table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            
            # Data
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor("#1e293b")),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ALIGN', (3, 1), (3, -1), 'RIGHT'),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        
        story.append(txn_table)
    else:
        story.append(Paragraph("No transactions found in this period.", styles['Normal']))
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor("#94a3b8"),
        alignment=TA_CENTER
    )
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | Finance PRO Dashboard",
        footer_style
    ))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
