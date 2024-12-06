import json

from odoo import http
from odoo.http import request


class WebCompanyLogoController(http.Controller):
    @http.route(
        ["/check_company_logo"],
        type="http",
        auth="public",
        methods=["GET"],
        website=True,
        sitemap=False,
    )
    def check_company_logo(self, company_id=0):
        has_logo = bool(request.env["res.company"].browse(int(company_id)).logo)

        return json.dumps(
            {
                "has_logo": has_logo,
            },
            ensure_ascii=False,
        )
