import io
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import app


class PaymentSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.patches = [patch.object(app, 'DB_PATH', Path(self.temp.name) / 'test.db'),
                        patch.object(app, 'PRODUCTION', True),
                        patch.object(app, 'PUBLIC_BASE_URL', 'https://honigautomat.at'),
                        patch.object(app, 'ORDER_TOKEN_SECRET', 'test-secret-' * 5)]
        for p in self.patches:
            p.start()
        app.init_db()
        self.order = {'order_id': 'order123', 'payment_id': 'tr_test', 'total_eur': 120.0}
        self.payment = {'id': 'tr_test', 'mode': 'live', 'status': 'paid',
                        'amount': {'currency': 'EUR', 'value': '120.00'},
                        'metadata': {'order_id': 'order123'}}

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        self.temp.cleanup()

    def request(self, path, body=None, headers=None):
        handler = object.__new__(app.HonigautomatRequestHandler)
        handler.path = path
        handler.headers = headers or {}
        result = {}
        handler._send_json = lambda data, status=200: result.update(data=data, status=status)
        if body is None:
            handler.do_GET()
        else:
            handler._read_body_json = lambda: body
            handler.do_POST()
        return result

    def test_blocked_management_and_simulator(self):
        for path in ['/api/orders', '/api/mollie/settings', '/mollie-checkout/tr_sim_123', '/api/configurator/code']:
            self.assertEqual(self.request(path)['status'], 404)
        self.assertEqual(self.request('/api/mollie/settings', {'api_key': 'live_fake'})['status'], 404)

    def test_order_requires_token(self):
        self.assertEqual(self.request('/api/orders/order123')['status'], 404)
        self.assertNotEqual(app.order_token('order123'), app.order_token('other'))

    def test_payment_must_match_order(self):
        with patch.object(app.mollie_service, 'fetch_payment_status', return_value=self.payment):
            self.assertEqual(app.verified_payment_status(self.order), 'paid')
        for field, value in [('mode', 'test'), ('id', 'tr_other'), ('metadata', {'order_id': 'other'}),
                             ('amount', {'currency': 'EUR', 'value': '1.00'}),
                             ('amount', {'currency': 'USD', 'value': '120.00'})]:
            with patch.object(app.mollie_service, 'fetch_payment_status', return_value={**self.payment, field: value}):
                with self.assertRaises(ValueError):
                    app.verified_payment_status(self.order)

    def test_checkout_fails_closed_without_live_key(self):
        with patch.object(app.mollie_service, 'get_mode_info', return_value={'mode': 'sandbox_simulator'}):
            self.assertEqual(self.request('/api/orders/checkout', {'items': []})['status'], 503)

    def test_redirect_cannot_use_host_header(self):
        handler = object.__new__(app.HonigautomatRequestHandler)
        handler.headers = {'Host': 'attacker.invalid', 'X-Forwarded-Proto': 'http'}
        self.assertEqual(handler._base_url(), 'https://honigautomat.at')

    def test_forged_webhook_status_is_ignored(self):
        with sqlite3.connect(app.DB_PATH) as conn:
            conn.execute('INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                         ('order123', 'BL-TEST', '{}', '[]', 100, 0, 120, 20, 'eps', 'tr_test', 'open', 'mollie_api_v2', '', '', ''))
        pending = {**self.payment, 'status': 'open'}
        with patch.object(app.mollie_service, 'is_live_or_test_key_configured', return_value=True), patch.object(app.mollie_service, 'fetch_payment_status', return_value=pending):
            self.assertEqual(self.request('/api/mollie/webhook', {'id': 'tr_test', 'status': 'paid'})['status'], 200)
        with sqlite3.connect(app.DB_PATH) as conn:
            self.assertEqual(conn.execute('SELECT payment_status FROM orders').fetchone()[0], 'open')

    def test_failed_webhook_verification_retries(self):
        with sqlite3.connect(app.DB_PATH) as conn:
            conn.execute('INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                         ('order123', 'BL-TEST', '{}', '[]', 100, 0, 120, 20, 'eps', 'tr_test', 'open', 'mollie_api_v2', '', '', ''))
        with patch.object(app.mollie_service, 'is_live_or_test_key_configured', return_value=True), patch.object(app.mollie_service, 'fetch_payment_status', side_effect=RuntimeError('unavailable')):
            self.assertEqual(self.request('/api/mollie/webhook', {'id': 'tr_test'})['status'], 503)


if __name__ == '__main__':
    unittest.main()
