import os
import shutil
import pathlib
import hashlib

from file.error import HashError


class File:
    """
    파일에 대한 기능을 제공하는 클래스입니다.
    """
    __path: str

    def __init__(self, path: str):
        self.__path = path

    @property
    def path(self) -> str:
        """
        파일 경로를 반환합니다.
        :return: 파일 경로 (str)
        """
        return self.__path

    @property
    def extension(self) -> str:
        """
        파일 확장자명을 반환합니다.

        Returns:
            str: 파일 확장자명
        """
        extensions = pathlib.Path(self.__path).suffixes
        extensions_len = len(extensions)

        if extensions_len == 0:
            return ""
        elif extensions_len == 1:
            return extensions.pop()[1:]
        else:
            ex = ""
            for extension in extensions:
                ex = ex + extension
            return ex[1:]

    @property
    def filename(self) -> str:
        """
        파일명을 반환합니다.

        Returns:
            str: 파일명
        """
        return os.path.basename(self.__path)

    @property
    def is_exist(self) -> bool:
        """
        파일 혹은 디렉터리가 존재하는지 여부를 반환함.

        Returns:
            bool: 파일 혹은 디렉터리 존재 여부
        """
        return os.path.exists(self.__path)

    @property
    def is_directory(self) -> bool:
        """
        디렉터리인지 여부를 반환함.

        Returns:
            bool: 디렉터리 여부
        """
        return os.path.isdir(self.__path)

    @property
    def is_file(self) -> bool:
        """
        파일인지 여부를 반환함.

        Returns:
            bool: 파일 여부
        """
        return os.path.isfile(self.__path)

    @property
    def can_read(self) -> bool:
        """
        파일을 읽을 수 있는지 여부를 반환함.

        Returns:
            bool: 파일 읽기 가능 여부
        """
        return os.access(self.__path, os.R_OK)

    @property
    def can_write(self) -> bool:
        """
        파일을 쓸 수 있는지 여부를 반환함.

        Returns:
            bool: 파일 쓰기 가능 여부
        """
        return os.access(self.__path, os.W_OK)

    @property
    def can_execute(self) -> bool:
        """
        파일을 실행할 수 있는지 여부를 반환함.

        Returns:
            bool: 파일 실행 가능 여부
        """
        return os.access(self.__path, os.X_OK)

    @property
    def size(self) -> int:
        """
        파일 크기를 반환함. (바이트 단위)

        Returns:
            int: 파일 크기 (byte)
        """
        return os.path.getsize(self.__path)

    def mkdir(self) -> None:
        """
        지정한 경로까지 재귀적으로 디렉터리를 생성.
        """
        os.makedirs(self.__path, exist_ok=True)

    def rm(self, recursive: bool = False) -> bool:
        """
        파일 또는 디렉터리를 삭제함.

        Args:
            recursive (bool): 디렉터리를 재귀적으로 삭제할지 여부 (기본 값: False)

        Returns:
            bool: 삭제 성공 여부
        """
        if self.is_directory:
            return self.__rm_directory(self.__path, recursive)
        else:
            return self.__rm_file(self.__path)

    def hash(self, algorithm: str = "sha256"):
        """
        파일의 해시값을 반환함.
        지원하는 알고리즘: 'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512',
                      'blake2b', 'blake2s',
                      'sha3_224', 'sha3_256', 'sha3_384', 'sha3_512',
                      'shake_128', 'shake_256'

        Args:
            algorithm (str): 해시 알고리즘 (기본 값: 'sha256')

        Raise:
            HashError: 해시값 생성 실패 시 예외 발생

        Returns:
            str: 파일 해시값 (폴더는 빈 문자열 반환)
        """
        if not self.is_file:
            return ""

        try:
            with open(self.__path, "rb") as f:
                hash_algorithm = hashlib.new(algorithm)
                while chunk := f.read(4096):
                    hash_algorithm.update(chunk)

                return hash_algorithm.hexdigest()
        except Exception:
            raise HashError

    def matches(self, file, algorithm: str = "sha256") -> bool:
        """
        두 파일의 해시 값을 비교하여 동일한 파일인지 여부를 반환함.

        Args:
            file (File): 비교할 파일
            algorithm (str): 해시 알고리즘 (기본 값: 'sha256')

        Returns:
            bool: 동일파일 여부
        """

        if type(file) is not File:
            return False

        return self.hash(algorithm) == file.hash(algorithm)

    def matches_deep(self, file) -> bool:
        """
        두 파일의 바이너리를 비교하여 동일한 파일인지 여부를 반환함.

        Args:
            file (File): 비교할 파일

        Returns:
            bool: 동일파일 여부
        """
        if type(file) is not File:
            return False

        with open(self.__path, "rb") as f:
            with open(file.path, "rb") as f2:
                return f.read() == f2.read()

    @staticmethod
    def __rm_directory(path: str, recursive: bool = False) -> bool:
        try:
            if recursive:
                # 디렉터리 내부 파일 및 디렉터리 삭제
                shutil.rmtree(path)
            else:
                # 빈 디렉터리 삭제 (디렉터리가 비어있지 않으면 삭제되지 않음)
                os.rmdir(path)
        except OSError:
            return False

        return True

    @staticmethod
    def __rm_file(path: str) -> bool:
        try:
            os.remove(path)
            return True
        except OSError:
            return False
