import unittest

suite = unittest.TestSuite()
# suite.addTest(TestIEMSLogin('test_right_login_01'))
dir = 'IemsTestcase'
suite.addTests(unittest.TestLoader().discover(start_dir=dir, pattern='test*.py'))
# unittest.main()
runner = unittest.TextTestRunner(verbosity=2)
runner.run(suite)
