from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model Definition
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    father_occupation = db.Column(db.String(100), nullable=False)
    mother_occupation = db.Column(db.String(100), nullable=False)
    aadhar = db.Column(db.String(12), nullable=False, unique=True)
    phone = db.Column(db.String(15), nullable=False)

# Create Database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to handle student form submission
@app.route('/submit_student_form', methods=['POST'])
def submit_student_form():
    try:
        data = request.get_json()
        new_student = Student(
            name=data['name'],
            age=data['age'],
            address=data['address'],
            father_name=data['father_name'],
            mother_name=data['mother_name'],
            father_occupation=data['father_occupation'],
            mother_occupation=data['mother_occupation'],
            aadhar=data['aadhar'],
            phone=data['phone'],
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({"message": "Student data submitted successfully!"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Aadhar number must be unique!"}), 400
    except Exception as e:
        return jsonify({"message": f"Error submitting form: {str(e)}"}), 500

# Endpoint to search for students
@app.route('/search_student', methods=['GET'])
def search_student():
    name = request.args.get('name')
    if name:
        students = Student.query.filter(Student.name.ilike(f'%{name}%')).all()
        results = [{"name": student.name, "age": student.age, "address": student.address,
                    "father_name": student.father_name, "mother_name": student.mother_name,
                    "aadhar": student.aadhar, "phone": student.phone} for student in students]
        return jsonify(results)
    return jsonify([])  # Return an empty list if no name is provided

if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, render_template, request, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.exc import IntegrityError

# app = Flask(__name__)

# # Database Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# # Model Definition
# class Student(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     age = db.Column(db.Integer, nullable=False)
#     address = db.Column(db.String(200), nullable=False)
#     father_name = db.Column(db.String(100), nullable=False)
#     mother_name = db.Column(db.String(100), nullable=False)
#     father_occupation = db.Column(db.String(100), nullable=False)
#     mother_occupation = db.Column(db.String(100), nullable=False)
#     aadhar = db.Column(db.String(12), nullable=False, unique=True)
#     phone = db.Column(db.String(15), nullable=False)

# # Create Database
# with app.app_context():
#     db.create_all()

# @app.route('/')
# def index():
#     return render_template('index.html')

# # Endpoint to handle student form submission
# @app.route('/submit_student_form', methods=['POST'])
# def submit_student_form():
#     try:
#         data = request.get_json()
#         new_student = Student(
#             name=data['name'],
#             age=data['age'],
#             address=data['address'],
#             father_name=data['father_name'],
#             mother_name=data['mother_name'],
#             father_occupation=data['father_occupation'],
#             mother_occupation=data['mother_occupation'],
#             aadhar=data['aadhar'],
#             phone=data['phone']
#         )
#         db.session.add(new_student)
#         db.session.commit()
#         return jsonify({'message': 'Form submitted successfully!'}), 200
#     except IntegrityError:
#         db.session.rollback()
#         return jsonify({'error': 'Aadhar card number already exists!'}), 400
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# # Endpoint to search for students by name (for staff)
# @app.route('/search_student', methods=['GET'])
# def search_student():
#     name = request.args.get('name')
#     students = Student.query.filter(Student.name.ilike(f'%{name}%')).all()
#     if not students:
#         return jsonify([]), 200
#     student_list = [{
#         'name': student.name,
#         'age': student.age,
#         'address': student.address,
#         'father_name': student.father_name,
#         'mother_name': student.mother_name,
#         'aadhar_number':student.aadhar,
#         'phone': student.phone
#     } for student in students]
#     return jsonify(student_list), 200

# if __name__ == '__main__':
#     app.run(debug=True)
