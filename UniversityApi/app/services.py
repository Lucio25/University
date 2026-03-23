import xmlrpc.client
from fastapi import HTTPException, status
from .config import settings

class UniversityService:
    @staticmethod
    def _get_odoo_proxy():

        try:
            common = xmlrpc.client.ServerProxy(f'{settings.ODOO_URL}/xmlrpc/2/common')
            uid = common.authenticate(settings.ODOO_DB, settings.ODOO_USER, settings.ODOO_PASS, {})

            if not uid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Fallo de autenticación con Odoo. Verifique credenciales."
                )

            models = xmlrpc.client.ServerProxy(f'{settings.ODOO_URL}/xmlrpc/2/object')
            return uid, models, settings.ODOO_PASS, settings.ODOO_DB

        except Exception as e:
            if isinstance(e, HTTPException): raise e
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Error de conexión con el servidor Odoo: {str(e)}"
            )

    @staticmethod
    def create_student(data: dict):
        
        uid, models, password, db = UniversityService._get_odoo_proxy()
        
        vals = {
            'name': data['name'],
            'email': data.get('email'),
            'phone': data.get('phone'),
            'registration_number': data.get('registration_number'), 
        }
        
        try:
            student_id = models.execute_kw(db, uid, password, 'university.student', 'create', [vals])
            
            return {
                "id": student_id, 
                "name": data['name'], 
                "email": data.get('email'),
                "registration_number": data.get('registration_number')
            }
        except Exception as e:
            # Errores
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Error en Odoo: {str(e)}"
            )

    @staticmethod
    def create_course(data: dict):
        uid, models, password, db = UniversityService._get_odoo_proxy()

        vals = {
            'name': data['name'],
            'max_capacity': data['capacity'],
            'study_year': data['study_year'],
            'study_plan_id': data['study_plan_id']
        }

        try:
            course_id = models.execute_kw(db, uid, password, 'university.subject', 'create', [vals])
            return {"id": course_id, "name": data['name']}
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    def enroll_student(data: dict):
        """
        Versión ultra-simplificada para dejar que Odoo maneje la lógica 
        y evitar choques de tipos en el puente XML-RPC.
        """
        uid, models, password, db = UniversityService._get_odoo_proxy()
        
        try:
            student_id = int(data['student_id'])
            career_id = int(data['career_id'])
            study_plan_id = int(data['study_plan_id'])
            subject_id = int(data['course_id'])
            year = str(data['year'])

            existing_enrollment_ids = models.execute_kw(
                db,
                uid,
                password,
                'university.enrollment',
                'search',
                [[
                    ['student_id', '=', student_id],
                    ['career_id', '=', career_id],
                    ['study_plan_id', '=', study_plan_id]
                ]],
                {'limit': 1}
            )

            if existing_enrollment_ids:
                enrollment_id = existing_enrollment_ids[0]

                existing_subject_line_ids = models.execute_kw(
                    db,
                    uid,
                    password,
                    'university.enrollment.line',
                    'search',
                    [[
                        ['enrollment_id', '=', enrollment_id],
                        ['subject_id', '=', subject_id]
                    ]],
                    {'limit': 1}
                )

                if existing_subject_line_ids:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="La materia ya está agregada en esta inscripción."
                    )

                models.execute_kw(
                    db,
                    uid,
                    password,
                    'university.enrollment',
                    'write',
                    [[enrollment_id], {
                        'line_ids': [(0, 0, {'subject_id': subject_id})]
                    }]
                )

                return {
                    "id": enrollment_id,
                    "status": "updated",
                    "message": "Materia agregada a inscripción existente"
                }

            enroll_vals = {
                'student_id': student_id,
                'career_id': career_id,
                'study_plan_id': study_plan_id,
                'year': year,
                'line_ids': [(0, 0, {
                    'subject_id': subject_id
                })]
            }
            
            enroll_id = models.execute_kw(db, uid, password, 'university.enrollment', 'create', [enroll_vals])
            
            return {
                "id": enroll_id,
                "status": "created",
                "message": "Inscripción creada y materia agregada"
            }

        except HTTPException as e:
            raise e
        except Exception as e:
            error_msg = str(e)
            # Si el error viene de Odoo, lo mostramos limpio
            raise HTTPException(
                status_code=400, 
                detail=f"Error en Odoo (Revisá tipos de datos): {error_msg}"
            )
    
    @staticmethod
    def get_enrollments_by_student(student_id: int):
        uid, models, password, db = UniversityService._get_odoo_proxy()

        # Búsqueda de líneas de inscripción por ID de estudiante
        line_ids = models.execute_kw(db, uid, password, 'university.enrollment.line', 'search', [[
            ['enrollment_id.student_id', '=', student_id]
        ]])

        if not line_ids:
            return []

        lines = models.execute_kw(db, uid, password, 'university.enrollment.line', 'read',
                                  [line_ids], {'fields': ['id', 'subject_id', 'enrollment_id']})
        return [
            {
                "line_id": l['id'],
                "materia": l['subject_id'][1] if l.get('subject_id') else "",
                "materia_id": l['subject_id'][0] if l.get('subject_id') else 0,
                "inscripcion_id": l['enrollment_id'][0] if l.get('enrollment_id') else 0,
            }
            for l in lines
        ]