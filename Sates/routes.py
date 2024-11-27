from Sates import app, db
from flask import render_template,request, redirect, url_for, Response
from Sates.models import Satellite
from flask_sqlalchemy import SQLAlchemy
import os
from io import BytesIO
from reportlab.lib.pagesizes import LEDGER
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors



@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/Info')
def info_page():
    return render_template('info.html')

with app.app_context():
    if not os.path.exists("satellite.db"):
        db.create_all()

# update route       
@app.route("/Updates")
def sate_update():
    search_term = request.args.get("search", "").strip()
    if search_term:
        # Filter satellites where search term matches any field
            satellites = Satellite.query.filter(
                Satellite.name.ilike(f"%{search_term}%")|
                Satellite.satellite_type.ilike(f"%{search_term}%") |
                Satellite.manufacturer.ilike(f"%{search_term}%") |
                Satellite.continent.ilike(f"%{search_term}%") |
                Satellite.cost.ilike(f"%{search_term}%")
                ).all()
    else:
        # Show all satellites by default if no search term is provided
        satellites = Satellite.query.all()
        
    return render_template("Updates.html", satellites=satellites)

@app.route("/download", methods=["GET"])
def download_pdf():
    # Query all satellites
    satellites = Satellite.query.all()
    
    table_data = [["id", "Continent","Satellite Name", "Satellite Type","Manufacturer", "Cost (in million USD)", ]]  # Table header
    for satellite in satellites:
        table_data.append([
            satellite.id,
            satellite.continent,
            satellite.name,
            satellite.satellite_type,
            satellite.manufacturer,
            f"${satellite.cost:,.2f}", #.2f is to add 2 decimal places to the integer
            
        ])

    # Create a PDF in-memory
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=LEDGER)
    elements = []

    # Create a Table with styles
    column_widths = [20, 120, 250, 250, 250, 100] #setting a column widths for the table
    table = Table(table_data, colWidths=column_widths)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # add Header for background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # add Header for text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center align all cells
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Header font bold
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # Reduce font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Header bottom padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Alternate row background
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
    ])
    table.setStyle(table_style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=LEDGER,
        leftMargin=20,
        topMargin=20,
        bottomMargin=20
    )
    pdf.build(elements)

    # Prepare the response
    buffer.seek(0)
    response = Response(buffer.getvalue(), mimetype="application/pdf")
    response.headers["Content-Disposition"] = "attachment; filename=satellites.pdf"

    return response


    


