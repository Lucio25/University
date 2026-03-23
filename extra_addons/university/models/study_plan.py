from odoo import models, fields


class UniversityStudyPlan(models.Model):
    _name = 'university.study_plan'
    _description = 'Plan de Estudios'

    name = fields.Char(
        string='Nombre del Plan',
        required=True,
        placeholder="Ej: Plan 2024")

    career_id = fields.Many2one(
        'university.career',
        string='Carrera',
        required=True)

    active = fields.Boolean(
        default=True,
        string='Plan Activo')

    # Relación inversa para ver las materias desde el plan
    subject_ids = fields.One2many(
        'university.subject',
        'study_plan_id',
        string='Materias del Plan')

    _sql_constraints = [
        ('unique_plan_name', 'unique(name, career_id)', 'Ya existe un plan con ese nombre para esta carrera.')
    ]