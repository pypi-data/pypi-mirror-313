import os
import platform
import pytest

from file import File, HashError
from pathlib import Path

class TestFile:
    __resource_abs_dir = os.path.join(

          # test_file.py가 존재하는 디렉터리 경로
          os.path.dirname(os.path.realpath(__file__))

          # 부모 디렉터리로 이동
        , os.pardir

          # resources 디렉터리로 이동
        , "resources"
    )
    __file1 = File(os.path.join(__resource_abs_dir + os.sep + "test.txt"))
    __file2 = File(__resource_abs_dir + os.sep + "test.tar.gz")
    __directory1 = File(__resource_abs_dir + os.sep + "test")

    def test_get_path(self):
        assert self.__file1.path == self.__resource_abs_dir + os.sep + "test.txt"
        assert self.__file2.path == self.__resource_abs_dir + os.sep + "test.tar.gz"
        assert self.__directory1.path == self.__resource_abs_dir + os.sep + "test"

    def test_get_extension(self):
        assert self.__file1.extension == "txt"
        assert self.__file2.extension == "tar.gz"
        assert self.__directory1.extension == ""

    def test_get_filename(self):
        assert self.__file1.filename == "test.txt"
        assert self.__file2.filename == "test.tar.gz"
        assert self.__directory1.filename == "test"

    def test_is_exist(self):
        assert True == self.__file1.is_exist
        assert True == self.__file2.is_exist
        assert True == self.__directory1.is_exist

    def test_is_directory(self):
        assert False == self.__file1.is_directory
        assert False == self.__file2.is_directory
        assert True == self.__directory1.is_directory

    def test_is_file(self):
        assert True == self.__file1.is_file
        assert True == self.__file2.is_file
        assert False == self.__directory1.is_file

    def test_can_read(self):
        assert True == self.__file1.can_read
        assert True == self.__file2.can_read
        assert True == self.__directory1.can_read

    def test_can_write(self):
        assert True == self.__file1.can_write
        assert True == self.__file2.can_write
        assert True == self.__directory1.can_write

    @pytest.mark.skipif(platform.uname().system == "Windows", reason="Windows에서는 실행 권한을 체크할 수 없습니다.")
    def test_can_execute(self):
        assert False == self.__file1.can_execute
        assert False == self.__file2.can_execute
        assert True == self.__directory1.can_execute

    def test_size(self):
        assert self.__file1.size == 23
        assert self.__file2.size == 380
        assert self.__directory1.size == 0 or self.__directory1.size == 96 or self.__directory1.size == 4096

    def test_mkdir_and_rm(self):

        # "resources/testdir/innerdir" 디렉터리 생성
        f = File(os.path.join(self.__resource_abs_dir, "testdir/innerdir"))
        f.mkdir()

        # "resources/testdir/innerdir/test.txt" 파일 생성
        Path(os.path.join(self.__resource_abs_dir, "testdir/innerdir/test.txt")).touch()

        file = File(os.path.join(self.__resource_abs_dir, "testdir/innerdir/test.txt"))
        assert file.is_exist

        directory = File(os.path.join(self.__resource_abs_dir, "testdir"))
        assert directory.is_exist

        inner_directory = File(os.path.join(self.__resource_abs_dir, "testdir/innerdir"))
        assert inner_directory.is_exist

        result = directory.rm()
        assert not result
        assert directory.is_exist

        file.rm()
        assert not file.is_exist

        inner_directory.rm()
        assert not inner_directory.is_exist

        directory.rm()
        assert not directory.is_exist

        # "resources/testdir/innerdir" 디렉터리 생성
        f = File(os.path.join(self.__resource_abs_dir, "testdir/innerdir"))
        f.mkdir()

        # "resources/testdir/innerdir/test.txt" 파일 생성
        Path(os.path.join(self.__resource_abs_dir, "testdir/innerdir/test.txt")).touch()

        f = File(os.path.join(self.__resource_abs_dir, "testdir"))
        f.rm(True)

    def test_hash(self):
        assert self.__directory1.hash() == ""

        assert self.__file1.hash() == "c4262018183408ce4bf05652ab8d2f599b7d6040cb319ed71794bd98a030b55c"
        assert self.__file1.hash("sha256") == "c4262018183408ce4bf05652ab8d2f599b7d6040cb319ed71794bd98a030b55c"

        try:
            File(os.path.join(self.__resource_abs_dir, "testdir/innerdir/null.txt")).hash()
        except HashError as ex:
            assert str(ex) == "해시값을 생성할 수 없습니다."

    def test_match(self):
        assert self.__file1.matches(self.__file1)
        assert not self.__file1.matches(self.__file2)

    def test_match_deep(self):
        assert self.__file1.matches_deep(self.__file1)
        assert not self.__file1.matches_deep(self.__file2)