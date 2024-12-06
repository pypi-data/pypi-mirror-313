import json
from . import schemas
from odoo.http import Response
from odoo.tools.translate import _
from odoo.addons.component.core import Component


class CrmLeadService(Component):
    _inherit = "base.rest.service"
    _name = "crm.lead.service"
    _usage = "crm-lead"
    _description = """
        Crm Lead Services
    """

    def create(self, params):
        create_dict = self._prepare_create(params)
        crm_lead = self.env["crm.lead"].create(create_dict)
        return Response(
            json.dumps({"message": _("Creation ok"), "id": crm_lead.id}),
            status=200,
            content_type="application/json",
        )

    def _validator_create(self):
        return schemas.S_CRM_LEAD_CREATE

    def _prepare_create(self, params):
        create_dict = {"type": "opportunity"}
        for key in params:
            create_dict[key] = params[key]
        return create_dict
