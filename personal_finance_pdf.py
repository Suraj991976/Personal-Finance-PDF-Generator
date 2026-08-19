from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

financial_data = {
    "name": "Suraj Baranwal",
    "month": "August 2026",
    "income": 50000,
    "expenses": {
        "Rent": 12000,
        "Food": 6000,
        "Transport": 3000,
        "Utilities": 2500,
        "Shopping": 4000,
        "Entertainment": 2000,
        "Other": 1500
    },
    "savings_goal": 15000
}

total_expenses = sum(financial_data["expenses"].values())
savings = financial_data["income"] - total_expenses
savings_percentage = (savings / financial_data["income"]) * 100

output_file = "personal_finance_report.pdf"

document = SimpleDocTemplate(
    output_file,
    pagesize=A4,
    rightMargin=40,
    leftMargin=40,
    topMargin=40,
    bottomMargin=40
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    fontSize=24,
    alignment=TA_CENTER,
    spaceAfter=15
)

subtitle_style = ParagraphStyle(
    "SubtitleStyle",
    parent=styles["Normal"],
    fontSize=11,
    alignment=TA_CENTER,
    textColor=colors.grey,
    spaceAfter=20
)

heading_style = ParagraphStyle(
    "HeadingStyle",
    parent=styles["Heading2"],
    fontSize=16,
    spaceBefore=15,
    spaceAfter=10
)

normal_style = ParagraphStyle(
    "NormalStyle",
    parent=styles["Normal"],
    fontSize=10,
    leading=15
)

tip_style = ParagraphStyle(
    "TipStyle",
    parent=styles["Normal"],
    fontSize=10,
    leading=15,
    leftIndent=10,
    rightIndent=10
)

def currency(amount):
    return f"₹{amount:,.2f}"

def add_header_footer(canvas, doc):
    canvas.saveState()

    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(
        40,
        A4[1] - 25,
        "PERSONAL FINANCE REPORT"
    )

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.grey)

    canvas.drawString(
        40,
        20,
        "Generated using Python & ReportLab"
    )

    canvas.drawRightString(
        A4[0] - 40,
        20,
        f"Page {doc.page}"
    )

    canvas.restoreState()
story = []
story.append(
    Paragraph(
        "Personal Finance Report",
        title_style
    )
)

story.append(
    Paragraph(
        f"{financial_data['name']} | {financial_data['month']}",
        subtitle_style
    )
)

story.append(Spacer(1, 10))
story.append(
    Paragraph(
        "Financial Summary",
        heading_style
    )
)

summary_data = [
    ["Category", "Amount"],
    ["Monthly Income", currency(financial_data["income"])],
    ["Total Expenses", currency(total_expenses)],
    ["Total Savings", currency(savings)],
    ["Savings Rate", f"{savings_percentage:.1f}%"]
]

summary_table = Table(
    summary_data,
    colWidths=[3.5 * inch, 2.2 * inch]
)

summary_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (1, -1), "RIGHT"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ])
)

story.append(summary_table)
story.append(Spacer(1, 20))
story.append(
    Paragraph(
        "Monthly Expense Breakdown",
        heading_style
    )
)

expense_table_data = [
    ["Expense Category", "Amount", "% of Expenses"]
]

for category, amount in financial_data["expenses"].items():
    percentage = (amount / total_expenses) * 100

    expense_table_data.append([
        category,
        currency(amount),
        f"{percentage:.1f}%"
    ])

expense_table_data.append([
    "TOTAL",
    currency(total_expenses),
    "100%"
])

expense_table = Table(
    expense_table_data,
    colWidths=[3 * inch, 1.5 * inch, 1.5 * inch]
)

expense_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),

        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),

        ("PADDING", (0, 0), (-1, -1), 7),
    ])
)

story.append(expense_table)
story.append(
    Paragraph(
        "Savings Goal",
        heading_style
    )
)

goal = financial_data["savings_goal"]

if savings >= goal:
    goal_status = "Goal Achieved"
else:
    goal_status = "Goal Not Achieved"

goal_data = [
    ["Savings Goal", currency(goal)],
    ["Actual Savings", currency(savings)],
    ["Status", goal_status]
]

goal_table = Table(
    goal_data,
    colWidths=[3.5 * inch, 2.5 * inch]
)

goal_table.setStyle(
    TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#D9EAF7")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 0), (1, -1), "RIGHT"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ])
)

story.append(goal_table)
story.append(
    Paragraph(
        "Personal Finance Tips",
        heading_style
    )
)

tips = [
    "Try to maintain an emergency fund covering 3–6 months of essential expenses.",
    "Review your monthly expenses and identify unnecessary spending.",
    "Set a fixed savings target before spending on non-essential items.",
    "Track your expenses regularly to understand your spending habits.",
    "Avoid taking unnecessary high-interest debt."
]

for tip in tips:
    story.append(
        Paragraph(
            f"• {tip}",
            tip_style
        )
    )
    story.append(Spacer(1, 5))

story.append(PageBreak())

story.append(
    Paragraph(
        "Personal Finance Basics",
        title_style
    )
)

education = [
    (
        "50/30/20 Rule",
        "A common budgeting approach is to allocate approximately "
        "50% of income to needs, 30% to wants, and 20% to savings "
        "or debt repayment."
    ),
    (
        "Emergency Fund",
        "An emergency fund provides financial protection against "
        "unexpected expenses such as medical costs, repairs, or "
        "temporary loss of income."
    ),
    (
        "Budgeting",
        "A budget helps you compare your income with your expenses "
        "and make informed financial decisions."
    ),
    (
        "Savings",
        "Consistent savings can help achieve short-term and long-term "
        "financial goals."
    )
]

for title, description in education:

    story.append(
        Paragraph(
            title,
            heading_style
        )
    )

    story.append(
        Paragraph(
            description,
            normal_style
        )
    )

    story.append(Spacer(1, 10))

document.build(
    story,
    onFirstPage=add_header_footer,
    onLaterPages=add_header_footer
)

print(f"PDF generated successfully: {output_file}")