from odoo import models, fields, api

class UniversityCareer(models.Model):
    _name = 'university.career'
    _description = 'Carrera'

    name = fields.Char(string='Nombre de la Carrera', required=True)
    code = fields.Char(string='Código')
    duration_years = fields.Integer(string='Duración en Años', required=True)

    subject_ids = fields.One2many('university.subject', 'career_id', string='Asignaturas')
    enrollment_ids = fields.One2many(
        'university.enrollment',
        'career_id',
        string='Inscripciones'
    )

    # Cantidad de inscriptos en tiempo real
    enrolled_count = fields.Integer(
        string='Total Inscriptos',
        compute='_compute_enrolled_count',
        store=True
    )

    #Plan de estudios
    study_plan_ids = fields.One2many(
        'university.study_plan',
        'career_id',
        string='Planes de Estudio'
    )

    @api.depends('enrollment_ids.student_id')
    def _compute_enrolled_count(self):
        for career in self:
            # Cuenta estudiantes unicos por carrera
            career.enrolled_count = len(set(career.enrollment_ids.mapped('student_id').ids))
