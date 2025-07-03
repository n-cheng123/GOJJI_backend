from flask import Blueprint, request, jsonify
from db import get_connection

summary_bp = Blueprint('summary', __name__)

@summary_bp.route('/summary', methods=['GET'])
def get_summary():
    clinic_id = request.args.get('clinic_id')
    provider_id = request.args.get('provider_id')
    start_date = request.args.get('start_date')  # e.g., "2025-05-01"
    end_date = request.args.get('end_date')      # e.g., "2025-05-31"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Dynamically build WHERE clause
    where = []
    params = []
    if clinic_id:
        where.append("p.clinicId = %s")
        params.append(clinic_id)
    if provider_id:
        where.append("p.providerId = %s")
        params.append(provider_id)
    if start_date:
        where.append("g.BGdate >= %s")
        params.append(start_date)
    if end_date:
        where.append("g.BGdate <= %s")
        params.append(end_date)
    where_clause = ("WHERE " + " AND ".join(where)) if where else ""
    
    # Example summary query (replace with your real logic)
    # Join patients to BG readings. You can aggregate as needed –
    # for example, AVG BGvalue, test counts, etc, using similar logic to the prior SQL.
    query = f"""
        SELECT
            CONCAT(p.firstName, ' ', p.lastName) AS patient_name,
            p.dob,
            ROUND(AVG(g.BGvalue), 0) AS avg_bg,
            COUNT(g.BGvalue) AS total_tests
        FROM patients p
        JOIN glucoses2 g ON p.patientID = g.patientID
        {where_clause}
        GROUP BY p.patientID, p.firstName, p.lastName, p.dob
        ORDER BY p.lastName, p.firstName
    """
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows), 200