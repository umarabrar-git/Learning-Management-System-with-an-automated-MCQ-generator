from unittest.mock import patch

from django.test import SimpleTestCase

from app import mcq_generator


class MCQGeneratorTests(SimpleTestCase):
    def test_ensure_nltk_data_downloads_missing_resources(self):
        with patch.object(mcq_generator.nltk.data, 'find', side_effect=LookupError('missing')):
            with patch.object(mcq_generator.nltk, 'download', return_value='ok') as mock_download:
                result = mcq_generator.ensure_nltk_data()

        self.assertTrue(result)
        self.assertEqual(mock_download.call_count, 3)
        self.assertIn('punkt', [call.args[0] for call in mock_download.call_args_list])
        self.assertIn('stopwords', [call.args[0] for call in mock_download.call_args_list])
        self.assertIn('wordnet', [call.args[0] for call in mock_download.call_args_list])
