from . import schemas
from odoo.addons.component.core import Component


class CrmLeadService(Component):
    _inherit = "crm.lead.service"
    _name = "crm.lead.service"

    def _validator_create(self):
        validator_schema = super()._validator_create().copy()
        validator_schema.update(schemas.S_CRM_LEAD_CREATE)
        return validator_schema

    def _prepare_create(self, params):
        create_dict = super()._prepare_create(params)
        form_metadatas = params.get('metadata', False)
        if form_metadatas:
            crm_metadata_lines_args = [
                line
                for line in form_metadatas
            ]
            crm_metadata_lines = self.env["crm.lead.metadata.line"].create(
                crm_metadata_lines_args)
            create_dict['metadata_line_ids'] = [
                (6, 0, [line.id for line in crm_metadata_lines])]
            create_dict.pop('metadata')
        return create_dict
