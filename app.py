import streamlit as st
import streamlit.components.v1 as components

# 1. Configure the Streamlit page to be wide so the UI has room to breathe
st.set_page_config(
    page_title="Synthetic Data Studio",
    layout="wide",
    initial_sidebar_state="collapsed" # Hide the sidebar to make it look like a pure website
)

# 2. Hide Streamlit's default header and footer for a cleaner look
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Remove padding from the main block */
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Paste our complete HTML/CSS/JS frontend into a Python string
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --bg-gradient-1: #0f172a;
            --bg-gradient-2: #312e81;
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }

        body {
            margin: 0;
            padding: 2rem;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, var(--bg-gradient-1), var(--bg-gradient-2));
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .glass-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 16px;
            padding: 2rem;
            width: 100%;
            max-width: 1200px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
            margin-bottom: 2rem;
        }

        h1 {
            margin-top: 0;
            font-size: 2rem;
            font-weight: 600;
            background: linear-gradient(to right, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        h2 {
            font-size: 1.25rem;
            margin-bottom: 1rem;
            color: #e2e8f0;
            font-weight: 500;
        }

        .controls-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .input-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        label {
            font-size: 0.875rem;
            color: var(--text-muted);
        }

        input, select {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--glass-border);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            color: white;
            font-size: 1rem;
            outline: none;
            transition: border-color 0.2s;
        }

        input:focus, select:focus {
            border-color: var(--primary);
        }

        option {
            background: var(--bg-gradient-1);
            color: white;
        }

        #columns-container {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            margin-bottom: 1.5rem;
        }

        .column-row {
            display: flex;
            gap: 1rem;
            align-items: center;
            background: rgba(0, 0, 0, 0.1);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .column-row input, .column-row select {
            flex: 1;
        }

        button {
            cursor: pointer;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-size: 1rem;
            font-weight: 500;
            transition: all 0.2s;
        }

        .btn-primary {
            background: var(--primary);
            color: white;
            box-shadow: 0 4px 6px -1px rgba(99, 102, 241, 0.4);
        }

        .btn-primary:hover {
            background: var(--primary-hover);
            transform: translateY(-1px);
        }

        .btn-secondary {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid var(--glass-border);
        }

        .btn-secondary:hover {
            background: rgba(255, 255, 255, 0.15);
        }

        .btn-danger {
            background: rgba(239, 68, 68, 0.2);
            color: #fca5a5;
        }

        .actions {
            display: flex;
            gap: 1rem;
            margin-top: 1rem;
        }

        .table-container {
            overflow-x: auto;
            max-height: 500px;
            border-radius: 8px;
            border: 1px solid var(--glass-border);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            background: rgba(0,0,0,0.2);
        }

        th, td {
            padding: 1rem;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            white-space: nowrap;
        }

        th {
            background: rgba(0,0,0,0.4);
            position: sticky;
            top: 0;
            font-weight: 600;
            color: #cbd5e1;
            z-index: 10;
        }

        tr:hover {
            background: rgba(255,255,255,0.02);
        }
    </style>
</head>
<body>

    <div class="glass-panel">
        <h1>Advanced Data Synthesizer</h1>
        
        <div class="controls-grid">
            <div class="input-group">
                <label>Number of Rows</label>
                <input type="number" id="row-count" value="15" min="1" max="100000">
            </div>
        </div>

        <h2>Column Configuration</h2>
        <div id="columns-container"></div>

        <div class="actions">
            <button class="btn-secondary" onclick="addColumn()">+ Add Column</button>
            <button class="btn-primary" onclick="generateData()">Generate Dataset</button>
        </div>
    </div>

    <div class="glass-panel" id="results-panel" style="display: none;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <h2>Dataset Preview</h2>
            <button class="btn-primary" onclick="downloadCSV()">Download CSV</button>
        </div>
        
        <div class="table-container">
            <table id="data-table">
                <thead>
                    <tr id="table-header"></tr>
                </thead>
                <tbody id="table-body"></tbody>
            </table>
        </div>
    </div>

    <script>
        const FIRST_NAMES = ['John', 'Jane', 'Alex', 'Emily', 'Michael', 'Sarah', 'David', 'Jessica', 'James', 'Maria', 'Robert', 'Lisa'];
        const LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'];
        const DOMAINS = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'protonmail.com'];
        const COMPANIES = ['ApexCorp', 'VertexIndustries', 'NovaLogistics', 'QuantumTech', 'BlueSkyHolding', 'SummitMedia'];
        const CITIES = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego'];
        const STATES = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA', 'TX', 'CA'];
        
        const DATA_TYPES = ["Integers", "Floats", "Dates", "Full Name", "Email Address", "Company Name", "Phone Number", "City & State"];

        let currentColumns = [
            { id: 1, name: 'ID', type: 'Integers' },
            { id: 2, name: 'Full_Name', type: 'Full Name' },
            { id: 3, name: 'Contact_Email', type: 'Email Address' },
            { id: 4, name: 'Signup_Date', type: 'Dates' }
        ];
        let colCounter = 5;
        let generatedDataset = [];

        const randItem = (arr) => arr[Math.floor(Math.random() * arr.length)];
        const randInt = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

        function renderColumns() {
            const container = document.getElementById('columns-container');
            container.innerHTML = '';
            
            currentColumns.forEach(col => {
                const row = document.createElement('div');
                row.className = 'column-row';
                
                const typeOptions = DATA_TYPES.map(t => 
                    `<option value="${t}" ${col.type === t ? 'selected' : ''}>${t}</option>`
                ).join('');

                row.innerHTML = `
                    <input type="text" value="${col.name}" onchange="updateCol(${col.id}, 'name', this.value)" placeholder="Column Name">
                    <select onchange="updateCol(${col.id}, 'type', this.value)">
                        ${typeOptions}
                    </select>
                    <button class="btn-danger" onclick="removeColumn(${col.id})">✕</button>
                `;
                container.appendChild(row);
            });
        }

        function addColumn() {
            currentColumns.push({ id: colCounter++, name: `Field_${currentColumns.length + 1}`, type: 'Integers' });
            renderColumns();
        }

        function removeColumn(id) {
            currentColumns = currentColumns.filter(c => c.id !== id);
            renderColumns();
        }

        function updateCol(id, key, value) {
            const col = currentColumns.find(c => c.id === id);
            if(col) col[key] = value;
        }

        function synthesizeValue(type) {
            switch(type) {
                case "Integers": return randInt(-1000, 10000);
                case "Floats": return (Math.random() * 1000).toFixed(4);
                case "Dates": 
                    const past = Date.now() - randInt(0, 31536000000); 
                    return new Date(past).toISOString().split('T')[0];
                case "Full Name": return `${randItem(FIRST_NAMES)} ${randItem(LAST_NAMES)}`;
                case "Email Address": return `${randItem(FIRST_NAMES).toLowerCase()}.${randItem(LAST_NAMES).toLowerCase()}@${randItem(DOMAINS)}`;
                case "Company Name": return randItem(COMPANIES);
                case "Phone Number": return `+1 (${randInt(200,999)}) ${randInt(100,999)}-${randInt(1000,9999)}`;
                case "City & State": 
                    const idx = randInt(0, CITIES.length - 1);
                    return `${CITIES[idx]}, ${STATES[idx]}`;
                default: return "Unknown";
            }
        }

        function generateData() {
            const rowCount = parseInt(document.getElementById('row-count').value) || 15;
            generatedDataset = [];

            for(let i = 0; i < rowCount; i++) {
                const rowObj = {};
                currentColumns.forEach(col => {
                    let safeName = col.name;
                    while(rowObj[safeName] !== undefined) safeName += "_1";
                    rowObj[safeName] = synthesizeValue(col.type);
                });
                generatedDataset.push(rowObj);
            }

            renderTable();
        }

        function renderTable() {
            if(generatedDataset.length === 0) return;
            
            document.getElementById('results-panel').style.display = 'block';
            
            const headers = Object.keys(generatedDataset[0]);
            document.getElementById('table-header').innerHTML = headers.map(h => `<th>${h}</th>`).join('');
            
            const rowsHTML = generatedDataset.slice(0, 100).map(row => {
                return `<tr>${headers.map(h => `<td>${row[h]}</td>`).join('')}</tr>`;
            }).join('');
            
            document.getElementById('table-body').innerHTML = rowsHTML;
        }

        function downloadCSV() {
            if(generatedDataset.length === 0) return;
            
            const headers = Object.keys(generatedDataset[0]);
            const csvRows = [];
            csvRows.push(headers.join(','));
            
            generatedDataset.forEach(row => {
                const values = headers.map(header => {
                    const val = String(row[header]);
                    return val.includes(',') ? `"${val}"` : val;
                });
                csvRows.push(values.join(','));
            });
            
            const csvString = csvRows.join('\\n');
            const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement('a');
            
            link.href = URL.createObjectURL(blob);
            link.setAttribute('download', 'synthetic_data.csv');
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        renderColumns();
    </script>
</body>
</html>
"""

# 4. Render the HTML component in Streamlit
# Set a large height so the user doesn't have to scroll within an iframe
components.html(html_code, height=900, scrolling=True)
