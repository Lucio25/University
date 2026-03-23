from flask import Blueprint, request, jsonify
from .schema import StudentSchema, CourseSchema, EnrollmentSchema
from .services import UniversityService
from marshmallow import ValidationError

api_bp = Blueprint('api', __name__)

# Instanciamos los schemas
student_schema = StudentSchema()
course_schema = CourseSchema()
enrollment_schema = EnrollmentSchema()
enrollments_list_schema = EnrollmentSchema(many=True)

@api_bp.route('/students', methods=['POST'])
def create_student():
    json_data = request.get_json()
    try:
        # Validamos formato con Marshmallow
        data = student_schema.load(json_data)
        # El Service lo crea en Odoo 
        student_data = UniversityService.create_student(data)
        # Lo devolvemos formateado
        return student_schema.dump(student_data), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/courses', methods=['POST'])
def create_course():
    json_data = request.get_json()
    try:
        data = course_schema.load(json_data)
        course_data = UniversityService.create_course(data)
        return course_schema.dump(course_data), 201
    except ValidationError as err:
        return jsonify(err.messages), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/enrollments', methods=['POST'])
def enroll_student():
    json_data = request.get_json()
    try:
        # Validamos que vengan todos los IDs requeridos
        data = enrollment_schema.load(json_data)
        
        # Llamamos al service pasando el diccionario completo
        result, status_code = UniversityService.enroll_student(data)
        
        return jsonify(result), status_code
    except ValidationError as err:
        return jsonify(err.messages), 400   

@api_bp.route('/students/<int:id>/enrollments', methods=['GET'])
def get_student_enrollments(id):
    # Consultamos a Odoo a través del Service
    enrollments = UniversityService.get_enrollments_by_student(id)
    
    return jsonify(enrollments), 200