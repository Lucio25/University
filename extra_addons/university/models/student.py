from odoo import models, fields, api

class UniversityStudent(models.Model):
    _name = 'university.student'
    _description = 'Estudiante'

    name = fields.Char(string='Nombre Completo', required=True)
    email = fields.Char(string='Correo Electrónico')
    phone = fields.Char(string='Teléfono')
    registration_number = fields.Char(string='Número de Legajo', copy=False)

    # Inscripciones
    enrollment_ids = fields.One2many(
        'university.enrollment',
        'student_id',
        string='Inscripciones Académicas'
    )

    # Carrera
    career_id = fields.Many2one(
        'university.career',
        string='Carrera Principal',
        related='enrollment_ids.career_id',
        store=True,
        readonly=True
    )

    # Plan de estudio
    study_plan_id = fields.Many2one(
        'university.study_plan',
        string='Plan de Estudios',
        related='enrollment_ids.study_plan_id',
        store=True,
        readonly=True
    )

    # Año de cursado
    study_year = fields.Selection(
        related='enrollment_ids.year',
        string='Año actual',
        store=True,
        readonly=True
    )

    # Campos Computados
    career_ids = fields.Many2many(
        'university.career',
        string='Carreras',
        compute='_compute_related_academic_data',
    )

    subject_ids = fields.Many2many(
        'university.subject',
        string='Materias inscriptas',
        compute='_compute_related_academic_data',
    )

    career_duration_info = fields.Char(
        string='Duración de la Carrera',
        compute='_compute_career_duration',
    )

    @api.depends('enrollment_ids.career_id', 'enrollment_ids.line_ids.subject_id')
    def _compute_related_academic_data(self):
        for student in self:
            student.career_ids = student.enrollment_ids.mapped('career_id')
            student.subject_ids = student.enrollment_ids.mapped('line_ids.subject_id')

    @api.depends('career_ids.duration_years')
    def _compute_career_duration(self):
        for student in self:
            # Convertimos las duraciones a string y las unimos
            durations = student.career_ids.mapped(lambda c: str(c.duration_years))
            student.career_duration_info = ", ".join(durations) if durations else "N/A"