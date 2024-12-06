import pytest
from unittest.mock import patch, MagicMock
from endetail_utilities.Sendmail import SendMail  # Upravte podle názvu vašeho souboru

class TestSendMail:
    ...
    # @patch('smtplib.SMTP_SSL')
    # def test_send_email_with_ssl(self, mock_smtp_ssl):
    #     # Nastavení mock SMTP serveru
    #     mock_server = MagicMock()
    #     mock_smtp_ssl.return_value = mock_server
    #
    #     mailer = SendMail(smtp_server='smtp.example.com', port=465, username='test@example.com', password='password', use_ssl=True)
    #     mailer.send(
    #         to_email='recipient@example.com',
    #         subject='Test Subject',
    #         body='This is a test email.',
    #         reply_to='reply@example.com',
    #         from_email='custom_from@example.com'
    #     )
    #
    #     mock_server.login.assert_called_once_with('test@example.com', 'password')
    #     mock_server.sendmail.assert_called_once()
    #     assert mock_smtp_ssl.sendmail.call_args[0][0] == 'custom_from@example.com'
    #     assert mock_smtp_ssl.sendmail.call_args[0][1] == 'recipient@example.com'
    #
    # @patch('smtplib.SMTP')
    # def test_send_email_without_ssl(self, mock_smtp):
    #     # Nastavení mock SMTP serveru
    #     mock_server = MagicMock()
    #     mock_smtp.return_value = mock_server
    #
    #     mailer = SendMail(smtp_server='smtp.example.com', port=587, username='test@example.com', password='password', use_ssl=False)
    #     mailer.send(
    #         to_email='recipient@example.com',
    #         subject='Test Subject',
    #         body='This is a test email.',
    #         reply_to='reply@example.com',
    #         from_email='custom_from@example.com'
    #     )
    #
    #     # Ověření, že se přihlásilo a odeslalo zprávu
    #     mock_server.starttls.assert_called_once()
    #     mock_server.login.assert_called_once_with('test@example.com', 'password')
    #     mock_server.sendmail.assert_called_once()
    #     assert mock_server.sendmail.call_args[0][0] == 'custom_from@example.com'
    #     assert mock_server.sendmail.call_args[0][1] == 'recipient@example.com'

# Spusťte testy pomocí pytest
if __name__ == "__main__":
    pytest.main()
