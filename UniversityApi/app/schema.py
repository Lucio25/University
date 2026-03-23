from . import ma
from marshmallow import Schema, fields, validate
from .models import Student, Course

class StudentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Student
        load_instance = False
    name = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)

class CourseSchema(Schema):
    name = fields.Str(required=True)
    capacity = fields.Int(required=True)
    study_year = fields.Str(required=True) 
    study_plan_id = fields.Int(required=True)

class EnrollmentSchema(Schema):
    # Campos para el POST 
    student_id = fields.Int(load_only=True)
    course_id = fields.Int(load_only=True)
    career_id = fields.Int(load_only=True)
    study_plan_id = fields.Int(load_only=True)
    year = fields.Str(load_only=True)

    # Campos para el GET 
    line_id = fields.Int(dump_only=True)
    materia = fields.Str(dump_only=True)
    materia_id = fields.Int(dump_only=True)
    inscripcion_id = fields.Int(dump_only=True)

    class Meta:
        # Esto asegura que todos los campos sean visibles en el JSON
        fields = ("student_id", "course_id", "career_id", "study_plan_id", "year", 
                  "line_id", "materia", "materia_id", "inscripcion_id")