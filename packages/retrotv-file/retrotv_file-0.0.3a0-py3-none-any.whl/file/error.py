class HashError(Exception):
    def __str__(self):
        return "해시값을 생성할 수 없습니다."