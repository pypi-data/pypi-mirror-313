from typing import Dict, Any
from datetime import datetime
from zoneinfo import ZoneInfo
from bson.objectid import ObjectId

from ....models.company.empresa import EmpresaModel
from ....models.users.user import User
from ....models.forms.company.auth0_company_registration_form import Auth0CompanyRegistrationForm

class EmpresaFactory:
    """
    Factory in charge of creating Empresa objects
    """
    @staticmethod
    def from_auth0_registration_form(auth0_registration_form:Dict[str, Any]):
        auht0_form = Auth0CompanyRegistrationForm(**auth0_registration_form)
        
        user = User(
            nombre = auht0_form.user_name,
            email = auht0_form.user_email,
            is_admin = True
        )
        return EmpresaModel(
            id = str(ObjectId()),
            created_at = datetime.now(ZoneInfo("UTC")),
            updated_at = datetime.now(ZoneInfo("UTC")),
            root_user = user,
            name = auht0_form.company_name,
            industry = auht0_form.industry,
            url = auht0_form.url,
            company_email = auht0_form.company_email,
            contributor_count = auht0_form.contributor_count,
            purpose_of_use_chatty = auht0_form.purpose_of_use_chatty,
            current_wpp_approach = auht0_form.current_wpp_approach,
            main_reason_to_use_chatty = auht0_form.main_reason_to_use_chatty,
            terms_of_service_agreement = auht0_form.terms_of_service_agreement,
            friendly_aliases = [auht0_form.alias],
            allowed_origins = [auht0_form.url],   
        )
        
