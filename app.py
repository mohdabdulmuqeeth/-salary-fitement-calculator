from flask import Flask, render_template, request

app = Flask(__name__)

# Telangana districts classified
URBAN_DISTRICTS = [
    'Hyderabad', 'Warangal', 'Karimnagar', 'Khammam', 'Nizamabad',
    'Rangareddy', 'Medchal–Malkajgiri', 'Sangareddy'
]

ALL_DISTRICTS = [
    'Adilabad', 'Bhadradri Kothagudem', 'Hyderabad', 'Jagtial', 'Jangaon',
    'Jayashankar Bhupalpally', 'Jogulamba Gadwal', 'Kamareddy', 'Karimnagar',
    'Khammam', 'Komaram Bheem Asifabad', 'Mahabubabad', 'Mahabubnagar',
    'Mancherial', 'Medak', 'Medchal–Malkajgiri', 'Mulugu', 'Nagarkurnool',
    'Nalgonda', 'Nirmal', 'Nizamabad', 'Peddapalli', 'Rajanna Sircilla',
    'Rangareddy', 'Sangareddy', 'Siddipet', 'Suryapet', 'Vikarabad',
    'Wanaparthy', 'Warangal', 'Hanamkonda', 'Yadadri Bhuvanagiri'
]

class Employee:
    def __init__(self, basic_salary, district, department):
        self.basic_salary = basic_salary
        self.district = district
        self.department = department

class SalaryCalculator:
    def __init__(self, employee):
        self.employee = employee
        self.new_basic = self.calculate_new_basic()
        self.hra = self.calculate_hra()
        self.da = self.calculate_da()
        self.medical = 1000
        self.gross = self.new_basic + self.hra + self.da + self.medical
        self.tax = self.calculate_tax()
        self.net_salary = self.gross - self.tax
        self.salary_diff = self.new_basic - self.employee.basic_salary

    def calculate_new_basic(self):
        hike = 40/100 if self.employee.department == 'External Affairs' else 0.3
        return self.employee.basic_salary * (1 + hike)

    def calculate_hra(self):
        rate = 0.12 if self.employee.district in URBAN_DISTRICTS else 0.08
        return self.new_basic * rate

    def calculate_da(self):
        return self.new_basic * 0.25

    def calculate_tax(self):
        return self.gross * 0.05 if self.gross > 100000 else 0

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        basic_salary = float(request.form['salary'])
        district = request.form['district']
        department = request.form['department']
        emp = Employee(basic_salary, district, department)
        calc = SalaryCalculator(emp)
        result = {
            'New_Basic': round(calc.new_basic, 2),
            'hra': round(calc.hra, 2),
            'da': round(calc.da, 2),
            'medical': calc.medical,
            'gross': round(calc.gross, 2),
            'tax': round(calc.tax, 2),
            'net_salary': round(calc.net_salary, 2),
            'salary_diff': round(calc.salary_diff, 2)
        }
    return render_template('index.html', result=result, districts=ALL_DISTRICTS)

if __name__ == '__main__':
    app.run(debug=True)