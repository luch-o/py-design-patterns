from src.payment_service.models import ContactInfo
from src.payment_service.notifications import Notifier, EmailNotifier, SMSNotifier


class NotifierFactory:
    @staticmethod
    def create_notifier(contact_info: ContactInfo) -> Notifier:
        if contact_info.email:
            return EmailNotifier()
        if contact_info.phone:
            return SMSNotifier(gateway="MyGateway")
        
        raise ValueError(f"Invalid notifier type: {contact_info}")