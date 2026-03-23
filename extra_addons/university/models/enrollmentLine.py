from odoo import models, fields, api

class EnrollmentLine(models.Model):
    _name = 'university.enrollment.line'
    _description = 'Detalle de Inscripción Académica'
    _rec_name = 'subject_id'

    # Conexión con la cabecera
    enrollment_id = fields.Many2one('university.enrollment', string='Inscripción', ondelete='cascade')

    # Traemos el Plan desde la cabecera
    study_plan_id = fields.Many2one(
        related='enrollment_id.study_plan_id',
        string='Plan de Estudios',
        store=True,
        readonly=True
    )

    # Conexión con la materia (solo del plan elegido)
    subject_id = fields.Many2one(
        'university.subject',
        string='Materia',
        required=True,
        domain="[('study_plan_id', '=', parent.study_plan_id)]"
    )

    # Datos relacionados
    career_id = fields.Many2one(
        related='enrollment_id.career_id',
        string='Carrera',
        store=True,
        readonly=True
    )

    teacher_id = fields.Many2one(
        related='subject_id.teacher_id',
        string='Profesor',
        readonly=True,
        store=True
    )

    student_id = fields.Many2one(
        related='enrollment_id.student_id',
        string='Alumno',
        store=True,
        readonly=True
    )

    enrollment_year = fields.Selection(
        related='enrollment_id.year',
        string='Año Académico',
        store=True
    )

    subject_year = fields.Selection(
        related='subject_id.study_year',
        string='Año Materia',
        readonly=True,
        store=True
    )

    note = fields.Float(string='Nota final de la materia')