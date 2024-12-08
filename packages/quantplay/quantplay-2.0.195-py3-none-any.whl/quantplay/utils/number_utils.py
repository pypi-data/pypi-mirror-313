class NumberUtils:
    @staticmethod
    def split(x: int, n: int) -> list[int]:
        ans: list[float] = []

        if (x < n) or n <= 0:
            ans = [x]
        elif x % n == 0:
            ans = []
            for i in range(n):
                ans.append(x / n)
        else:
            zp = n - (x % n)
            pp = x // n
            for i in range(n):
                if i >= zp:
                    ans.append(pp + 1)
                else:
                    ans.append(pp)

        return [int(a) for a in ans]
