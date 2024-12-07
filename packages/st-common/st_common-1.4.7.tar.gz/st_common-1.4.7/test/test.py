from st_common.rpamodule import BaseBrowser

base = BaseBrowser(log_file='rpa_test.log')
base.logger.info("hello")
base.logger.error("hello")