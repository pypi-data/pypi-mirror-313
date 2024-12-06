import pytest
from endetail_utilities.Logger import Logger  # Upravte podle názvu vašeho souboru


class TestLogger:
    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        self.log_file = tmp_path / "test_log.log"
        self.logger = Logger(log_file=str(self.log_file), when='S', interval=1, backup_count=7, log_level="DEBUG", logger_name='TestLogger')

    def test_logging_info(self):
        self.logger.info('Testovací info zpráva.')

        with open(self.log_file, 'r', encoding='utf-8') as f:
            logs = f.read()

        assert 'Testovací info zpráva.' in logs

    def test_logging_debug(self):
        self.logger.debug('Testovací debug zpráva.')

        with open(self.log_file, 'r', encoding='utf-8') as f:
            logs = f.read()

        assert 'Testovací debug zpráva.' in logs

    def test_logging_json(self):
        self.logger.info({'message': 'Testovací JSON zpráva.', 'data': 'data'})

        with open(self.log_file, 'r', encoding='utf-8') as f:
            logs = f.read()

        assert "{'message': 'Testovací JSON zpráva.', 'data': 'data'}" in logs

