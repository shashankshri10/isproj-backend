from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import io

class MyBorderedDocTemplate(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_num = 1  # Initialize page number

    def afterFlowable(self, flowable):
        # Increment page number after each flowable (content)
        if hasattr(flowable, 'split') and self.page_num > 0:
            self.page_num += 1

def create_plot():
    # Generate some sample data
    x = np.linspace(0, 10, 100)
    y1 = np.sin(x)
    y2 = np.cos(x)

    # Create the plot
    plt.figure(figsize=(6, 4.5))  # Adjusted the height of the plots

    # Plot the first graph
    plt.subplot(1, 2, 1)
    plt.plot(x, y1)
    plt.title('Current Value vs Time')
    plt.xlabel('Time')
    plt.ylabel('Current Value')

    # Plot the second graph and adjust its position
    plt.subplot(1, 2, 2)
    plt.subplots_adjust(wspace=0.5)  # Adjust the space between subplots
    plt.plot(x, y2)
    plt.title('Frequency Value vs Time')
    plt.xlabel('Time')
    plt.ylabel('Frequency Value')

    # Save the plot to a buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    return buffer

def create_pdf_with_plots(file_name, motor_condition, RUL_value, fault_type=None):
    doc = MyBorderedDocTemplate(file_name, pagesize=letter, leftMargin=0.5*inch, rightMargin=0.5*inch)
    styles = getSampleStyleSheet()

    # Define custom style for center-aligned paragraph
    centered_style = ParagraphStyle(name="Centered", alignment=1)

    # Define the header
    def header(canvas, doc):
        canvas.saveState()
        canvas.drawString(40, 750, f"Report Generated on {datetime.now().strftime('%d/%m/%Y')}")
        canvas.restoreState()

    doc.onFirstPage = lambda canvas, doc: header(canvas, doc)
    doc.onLaterPages = lambda canvas, doc: header(canvas, doc)

    # Add some content
    content = [
        Spacer(1, 0.005*inch),  # Adjusted the spacer size to reduce top margin
        Paragraph("<b>Motor Number:</b> M12345", styles['Heading2']),
        Paragraph("<b>Power Rating:</b> 5 HP", styles['Heading2']),
        Spacer(1, 0.1*inch),  # Adjusted the spacer size to reduce bottom margin
        Paragraph("<b>Operating Condition Summary for 1 Month:</b>", styles['Heading2'])
    ]
    
    if motor_condition == "Faulty" and fault_type:
        content.append(Paragraph(f"<b>Fault type:</b> {fault_type}", styles['Normal']))

    # Create the plots
    plot_buffer = create_plot()
    img = Image(plot_buffer)
    content.append(img)

    # Add new lines below the graphs and "Current Conditions of Motor" line
    content.extend([Spacer(1, 0.1*inch) for _ in range(2)])  # Adjust the number of new lines as needed
    content.append(Paragraph(f"<b>Current condition of motor:</b> {motor_condition}", styles['Heading2']))
    content.append(Paragraph(f"<b>Estimated Remaining Useful Life (RUL):</b> {RUL_value}", styles['Heading2']))

    # Center-aligned "Fault Table Summary" paragraph
    content.append(Paragraph("<b>Fault Table Summary</b>", centered_style))

    # Create table data
    table_data = [
        ["Fault Type", "Occurrence in Week", "", "Occurrence in Month", "", "Occurrence in Year", ""],
        ["", "Frequency", "Time", "Frequency", "Time", "Frequency", "Time"],
        ["Broken Rotar-Bar (BR)", "1", "1", "1", "1", "1", "1"],
        ["Broken End Ring", "1", "1", "1", "1", "1", "1"],
        ["Eccentricity", "1", "1", "1", "1", "1", "1"],
        ["Bearing", "1", "1", "1", "1", "1", "1"],
        ["Inter-turn Short Circuit", "1", "1", "1", "1", "1", "1"]


    ]

    # Create table
    content.extend([Spacer(1, 0.1*inch) for _ in range(2)])  # Adjust the number of new lines as needed
    fault_table = Table(table_data, colWidths=[150, 50, 75, 50, 75, 50, 75])
    fault_table.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
                                     ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                                     ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                     ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                                     ('BOTTOMPADDING', (0,0), (-1,0), 12),
                                     ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                                     ('SPAN', (1,0), (2,0)),  # Merge 2nd and 3rd cells
                                     ('SPAN', (3,0), (4,0)),  # Merge 4th and 5th cells
                                     ('SPAN', (5,0), (6,0)),  # Merge 6th and 7th cells
                                     ('GRID', (0,0), (-1,-1), 1, colors.black)]))

    content.append(fault_table)

    content.append(Paragraph("Suggestions Based On Current Situation: Normal", styles['Heading2']))

    doc.build(content)

if __name__ == "__main__":
    file_name = "output.pdf"
    create_pdf_with_plots(file_name, motor_condition="Healthy", RUL_value=0.82)
    print(f"PDF generated successfully: {file_name}")