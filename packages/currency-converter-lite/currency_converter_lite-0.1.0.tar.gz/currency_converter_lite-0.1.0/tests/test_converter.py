import unittest
from unittest.mock import patch
from currency_converter.converter import (
    CurrencyConverter,
    get_cached_rate,
    cache_rate,
    load_cache,
    save_cache,
)


class TestCurrencyConverter(unittest.TestCase):
    @patch("currency_converter.converter.get_exchange_rate_yahoo")
    @patch("currency_converter.converter.get_exchange_rate_google")
    def test_get_rate_yahoo(self, mock_google, mock_yahoo):
        # Mock Yahoo Finance
        mock_yahoo.return_value = 1.1
        mock_google.return_value = 1.5  # To ensure only Yahoo's value is used

        converter = CurrencyConverter(use_yahoo=True)
        rate = converter.get_rate("USD", "EUR")
        self.assertEqual(rate, 1.1)

    @patch("currency_converter.converter.get_exchange_rate_google")
    def test_get_rate_google(self, mock_google):
        # Mock Google Finance
        mock_google.return_value = 1.2

        converter = CurrencyConverter(use_yahoo=False)
        rate = converter.get_rate("USD", "EUR")
        self.assertEqual(rate, 1.2)

    @patch("currency_converter.converter.get_exchange_rate_yahoo")
    @patch("currency_converter.converter.get_exchange_rate_google")
    def test_caching_mechanism(self, mock_google, mock_yahoo):
        # Mock both services
        mock_yahoo.return_value = 1.3
        mock_google.return_value = 1.4

        converter = CurrencyConverter(use_yahoo=True)

        # First fetch should call the Yahoo API
        rate_1 = converter.get_rate("USD", "EUR")
        self.assertEqual(rate_1, 1.3)

        # Second fetch should use the cached value, not call the Yahoo API
        rate_2 = converter.get_rate("USD", "EUR")
        self.assertEqual(rate_2, 1.3)

        # Ensure the mock was called only once
        mock_yahoo.assert_called_once()
        mock_google.assert_not_called()


    @patch("currency_converter.converter.get_exchange_rate_yahoo")
    def test_convert(self, mock_yahoo):
        # Mock Yahoo Finance
        mock_yahoo.return_value = 1.5

        converter = CurrencyConverter(use_yahoo=True)
        converted_amount = converter.convert(100, "USD", "EUR")
        self.assertEqual(converted_amount, 150.0)

    def test_cache_rate(self):
        cache_rate("USD", "EUR", 1.5)
        rate = get_cached_rate("USD", "EUR")
        self.assertEqual(rate, 1.5)

    def test_load_save_cache(self):
        # Test saving and loading cache
        data = {"test_key": "test_value"}
        save_cache(data)
        loaded_data = load_cache()
        self.assertEqual(loaded_data, data)


if __name__ == "__main__":
    unittest.main()

