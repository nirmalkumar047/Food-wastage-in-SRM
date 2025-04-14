from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load and clean Excel data
df = pd.read_excel('data/wastage_data.xlsx')
df.columns = df.columns.str.strip()  # Remove any spaces in column names

@app.route('/')
def index():
    # Get list of hostel columns excluding 'Date', 'PARTICULARS', 'UOM', 'Total'
    hostels = [col for col in df.columns if col not in ['Date', 'PARTICULARS', 'UOM', 'Total']]
    return render_template('index.html', hostels=hostels)

@app.route('/check', methods=['POST'])
def check_wastage():
    hostel = request.form['hostel']
    date = request.form['date']
    meal = request.form['meal']

    try:
        formatted_date = pd.to_datetime(date).strftime('%d-%b-%y')  # e.g., '01-Feb-25'
        match = df[(df['Date'] == formatted_date) & (df['PARTICULARS'] == meal)]

        wastage = None
        if not match.empty and hostel in match.columns:
            wastage = match.iloc[0][hostel]
    except Exception as e:
        print("Error:", e)
        wastage = "Error retrieving data"

    return render_template('result.html', hostel=hostel, date=formatted_date, meal=meal, wastage=wastage)

if __name__ == '__main__':
    app.run(debug=True)
