from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, BooleanAttribute
from core.config import settings


class InstitutionModel(Model):
    """PynamoDB model definition for the Institutions table"""

    class Meta:
        table_name = settings.TABLE_NAME
        region = settings.REGION_NAME
        billing_mode = settings.BILLING_MODE

    cnpj = UnicodeAttribute(hash_key=True, null=False)
    id = UnicodeAttribute(null=False)
    token = UnicodeAttribute(null=False)
    name = UnicodeAttribute(null=False)
    email = UnicodeAttribute(null=False)
    phone_number = UnicodeAttribute(null=False)
    cep = UnicodeAttribute(null=False)
    region = UnicodeAttribute(null=False)
    state = UnicodeAttribute(null=False)
    address = UnicodeAttribute(null=False)
    address_number = NumberAttribute(null=False)
    city = UnicodeAttribute(null=False)
    neighborhood = UnicodeAttribute(null=False)
    confirmation_audio = UnicodeAttribute(null=False)
    image = UnicodeAttribute(null=False)
    about = UnicodeAttribute(null=False)
    verified = BooleanAttribute(default=False, null=False)
    site = UnicodeAttribute(null=False)
