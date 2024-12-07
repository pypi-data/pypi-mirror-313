# MIT License
#
# Copyright (c) 2024 Gwyn Davies
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR,
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from montty.app.check.collect_base_check import CollectBaseCheck


class FakeCollectBaseCheck(CollectBaseCheck):
    def __init__(self, level_index=0):
        self._header_title = 'Test collection base check'
        super().__init__(self._header_title,  level_index)
        self._cpu_percent = None

    # @implement
    def _add_checks(self, checks) -> None:
        pass  # pragma: no cover

    # @implement
    def _run_checks(self) -> None:
        pass  # pragma: no cover


#########
# Tests #
#########


class TestCollectbaseCheck():
    # Ignore warning for accessing internal members
    # pylint: disable=W0212
    def test_ok(self):
        collection_check = FakeCollectBaseCheck(
            level_index=0)
        collection_check.run()

        string = str(collection_check.get_header())
        assert string.startswith('Test collection base check')
        assert '(NA)' in string
        assert string.endswith('\n')

        assert str(collection_check.get_body()) == ''
        assert collection_check.get_status().is_na()

        string = collection_check.get_output()
        assert string.startswith('Test collection base check')
        assert '(NA)' in string
        assert string.endswith('\n')

        assert collection_check.get_level().get_index() == 0
        assert str(collection_check.get_level()) == '     '


#########
# Level #
#########

    # Ignore warning for accessing internal members
    # pylint: disable=W0212


    def test_ok_has_level_1(self):
        collection_check = FakeCollectBaseCheck(level_index=1)
        collection_check.run()

        string = str(collection_check.get_header())
        assert string.startswith('Test collection base check')
        assert '(NA)' in string
        assert string.endswith('\n')

        assert str(collection_check.get_body()) == ''
        assert collection_check.get_status().is_na()

        string = collection_check.get_output()
        assert string.startswith('Test collection base check')
        assert '.(NA).' in string
        assert string.endswith('\n')

        assert collection_check.get_level().get_index() == 1
        assert str(collection_check.get_level()) == '    .'
