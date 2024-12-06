odoo.define("web_company_logo.web_company_logo", function (require) {
    "use strict";

    const {registry} = require("@web/core/registry");
    const {Component} = owl;

    var session = require("web.session");

    class WebCompanyLogo extends Component {
        setup() {
            var url = window.location.origin;
            var companyId = session.company_id;
            $.ajax({
                type: "GET",
                data: {company_id: companyId},
                url: `${url}/check_company_logo`,
                success: function (result) {
                    var result = JSON.parse(result);
                    if (result.has_logo === true) {
                        $(
                            "#company-logo"
                        )[0].src = `${url}/web/image?model=res.company&id=${companyId}&field=logo`;
                    } else {
                        $("#company-logo-link")[0].remove();
                    }
                },
                error: function () {
                    console.log("Error encountered");
                },
            });
        }
    }
    WebCompanyLogo.template = "web_company_logo.WebCompanyLogo";
    registry
        .category("systray")
        .add("web_company_logo", {Component: WebCompanyLogo}, {sequence: 1000});
});
