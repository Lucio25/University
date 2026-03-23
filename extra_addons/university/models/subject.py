from odoo import models, fields, api
from odoo.exceptions import ValidationError


class UniversitySubject(models.Model):
    _name = 'university.subject'
    _description = 'Asignatura'

    name = fields.Char(string='Nombre de la Materia', required=True)

    max_capacity = fields.Integer(string='Cupo Máximo', default=30)

    # Plan de estudios
    study_plan_id = fields.Many2one(
        'university.study_plan',
        string='Plan de Estudios',
        required=True,
        ondelete='cascade'
    )

    # Related significa que se llena solo, osea se selecciona la carrera al elegir el plan
    career_id = fields.Many2one(
        related='study_plan_id.career_id',
        string='Carrera',
        store=True,
        readonly=True
    )

    teacher_id = fields.Many2one('university.teacher', string='Profesor')

    study_year = fields.Selection([
        ('1', '1er Año'),
        ('2', '2do Año'),
        ('3', '3er Año'),
        ('4', '4to Año'),
        ('5', '5to Año'),
        ('6', '6to Año'),
    ], string='Año de Cursada', required=True, default='1')

    # Relaciones para el cálculo de alumnos
    enrollment_line_ids = fields.One2many(
        'university.enrollment.line',
        'subject_id',
        string='Líneas de Inscripción'
    )

    enrolled_count = fields.Integer(
        string='Alumnos Inscriptos',
        compute='_compute_enrolled_count',
        store=True
    )

    # Obtenemos la carrera desde el plan
    @api.constrains('study_year', 'study_plan_id')
    def _check_year_limit(self):
        for record in self:
            if record.study_plan_id and record.study_year:
                selected_year = int(record.study_year)
                # Obtenemos la duración de la carrera vinculada al plan
                max_years = record.study_plan_id.career_id.duration_years

                if selected_year > max_years:
                    raise ValidationError(
                        f"Error de consistencia: El plan '{record.study_plan_id.name}' "
                        f"pertenece a una carrera de {max_years} años. "
                        f"No podés asignar esta materia al año {selected_year}."
                    )

    @api.depends('enrollment_line_ids')
    def _compute_enrolled_count(self):
        for subject in self:
            subject.enrolled_count = len(subject.enrollment_line_ids)