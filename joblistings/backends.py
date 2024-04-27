from django.core.mail.backends.smtp import EmailBackend
import smtplib
from ssl import create_default_context, CERT_NONE

class NoVerifyEmailBackend(EmailBackend):
    def open(self):
        if self.connection:
            return False  # Don't need to set up a new connection
        try:
            connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
            if self.use_tls:
                context = create_default_context()
                context.check_hostname = False
                context.verify_mode = CERT_NONE
                connection.starttls(context=context)
            if self.username and self.password:
                connection.login(self.username, self.password)
            self.connection = connection
            return True
        except (smtplib.SMTPException, OSError):
            if not self.fail_silently:
                raise
            return False
