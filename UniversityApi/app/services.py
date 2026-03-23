import xmlrpc.client
from flask import current_app

class UniversityService:
    @staticmethod
    def _get_odoo_proxy():
        url = current_app.config['ODOO_URL']
        db = current_app.config['ODOO_DB']
        username = current_app.config['ODOO_USER']
        password = current_app.config['ODOO_PASS']
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        if not uid:
            raise Exception(f"Auth failed")
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        return uid, models, password, db

    @staticmethod
    def create_course(data):
        uid, models, password, db = UniversityService._get_odoo_proxy()
        
        vals = {
            'name': data['name'],
            'max_capacity': data['capacity'], 
            'study_year': data['study_year'], 
            'study_plan_id': data['study_plan_id']
        }
        
        course_id = models.execute_kw(db, uid, password, 'university.subject', 'create', [vals])
        
        return {"id": course_id, "name": data['name']}

    @staticmethod
    def enroll_student(data):
        uid, models, password, db = UniversityService._get_odoo_proxy()
        
        course_id = data.get('course_id')
        req_plan_id = data.get('study_plan_id')

        course_data = models.execute_kw(db, uid, password, 'university.subject', 'read', 
                                        [course_id], {'fields': ['name', 'max_capacity', 'enrolled_count', 'study_plan_id']})
        
        if not course_data:
            return {"error": "Materia no encontrada"}, 404
        
        course = course_data[0]

        if not course['study_plan_id'] or course['study_plan_id'][0] != req_plan_id:
            return {
                "error": f"La materia '{course['name']}' no pertenece al Plan de Estudios (ID: {req_plan_id}) seleccionado."
            }, 400

        if course['enrolled_count'] >= course['max_capacity']:
            return {"error": "Cupo lleno"}, 400

        try:
            enroll_id = models.execute_kw(db, uid, password, 'university.enrollment', 'create', [{
                'student_id': data['student_id'],
                'career_id': data['career_id'],
                'study_plan_id': req_plan_id,
                'year': str(data['year']),
                'line_ids': [(0, 0, {'subject_id': course_id})]
            }])
            return {"id": enroll_id, "status": "Inscripción exitosa"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    @staticmethod
    def get_enrollments_by_student(student_id):
        uid, models, password, db = UniversityService._get_odoo_proxy()
        line_ids = models.execute_kw(db, uid, password, 'university.enrollment.line', 'search', [[
            ['enrollment_id.student_id', '=', student_id]
        ]])
        if not line_ids: return []
        lines = models.execute_kw(db, uid, password, 'university.enrollment.line', 'read', 
                                 [line_ids], {'fields': ['id', 'subject_id', 'enrollment_id']})
        return [{"materia": l['subject_id'][1], "id": l['id']} for l in lines]