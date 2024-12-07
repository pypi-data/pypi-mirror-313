import tempfile
import ctypes

from ctypes import c_char_p, c_bool

from contrast_agent_lib import lib_contrast


SUCCESS = 0


def test_init():
    with tempfile.TemporaryDirectory() as tmpdirname:
        log_level = b"TRACE"
        log_dir = bytes(tmpdirname, "utf8")

        assert (
            lib_contrast.init_with_options(
                c_bool(True), c_char_p(log_dir), c_char_p(log_level)
            )
            == SUCCESS
        )
