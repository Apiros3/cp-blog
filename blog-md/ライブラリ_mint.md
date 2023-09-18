# mint (modint)ライブラリ

## 目標：
long longでやることと同じ操作をする際に、勝手にmodを取って欲しい

## 実装：

### 初期化：

```
long long mintmod = 998244353;
```

としておく。また、`class mint`を定義しておく。
また、privateの中に

```
long long x;
```

を定義しておく。

classが呼ばれた時の初期化は：

```
mint(long long x = 0) : x((x%mintmod + mintmod)%mintmod) {}
```

負の数でも$0 \leq i < mod$となるようにしっかり処理を行う。

### Helper Functions

$a^b mod M$を高速に求めてくれる関数、modpow_sを用意する。modの値が大きくなる可能性があるので、積の結果が64bitを超えてもmodを取るとoverflowなどのバグが発生しない関数を使います。

```
long long modmul(unsigned long long a, unsigned long long b, unsigned long long M) {
    long long ret = a * b - M * (unsigned long long)(1.L / M * a * b);
    return ret + M * (ret < 0) - M * (ret >= (unsigned long long)M);
}
long long modpow_s(long long btmn, long long topn, long long modn) {
    long long ret_num = 1;
    btmn%=modn;
    for(; topn; topn/=2, btmn=modmul(btmn,btmn,modn))
        if (topn & 1ll) ret_num=modmul(ret_num,btmn,modn);
    return ret_num%modn;
} 
```

Overflow等でバグが発生しない[証明](https://github.com/kth-competitive-programming/kactl/blob/main/doc/modmul-proof.md)です。

### 負の数を返す関数

```
mint operator-() const {
    return mint(-x);
}
```

### 足し算・引き算・掛け算

```
mint& operator+=(const mint& a) {
    if ((x += a.x) >= mintmod) x -= mintmod;
    return *this;
}
mint& operator-=(const mint& a) {
    if ((x += mintmod - a.x) >= mintmod) x -= mintmod;
    return *this;
}
mint& operator*=(const mint& a) {
    x = modmul(x, a.x, mintmod);
    return *this;
}
mint operator+(const mint& a) const {
    mint res(*this);
    return res += a;
}
mint operator-(const mint& a) const {
    mint res(*this);
    return res -= a;
}
mint operator*(const mint& a) const {
    mint res(*this);
    return res *= a;
}
```

掛け算にはしっかり上記で定義したmodmul関数を使います。他の人との実装はここが異なっているかもしれません<s>一般的には素数mod且つ32bit以内に収まるものを使うことを想定するだけでよいので充分という話はある</s>

### 冪数・逆元

```
template<typename T>
mint pow(T t) const {
    if (!t) return 1;
    mint a = pow(t >> 1);
    a *= a;
    if (t & 1) a *= *this;
    return a;
}
mint inv() const {
    return pow(mintmod-2);
}
```

### 割り算

定義された逆元を使って割り算を行います

```
mint& operator/=(const mint& a) {
    return (*this) *= a.inv();
}
mint operator/(const mint& a) const {
    mint res(*this);
    return res/=a;
}
```

### 同値確認

同じmint、またはlong longなどの整数型と値を比べれるようにします（$== 0$ などをしたいかもしれないので）

```
mint operator==(const mint& a) {
    return (*this).x == a.x;
}
template <typename T>
mint operator==(const T &a) {
    return (*this).x == a;
}
```

### 出力

```
friend std::ostream& operator<<(std::ostream& os, const mint& m) {
    os << m.x;
    return os;
}
```

## 全体コード：

あとはmain関数内でmintmodを書き直したりすれば、`mint x = 3;`などで定義できます。

```
long long mintmod = 998244353;
class mint {
private:
    long long x;
    long long modmul(unsigned long long a, unsigned long long b, unsigned long long M) {
        long long ret = a * b - M * (unsigned long long)(1.L / M * a * b);
        return ret + M * (ret < 0) - M * (ret >= (unsigned long long)M);
    }
    long long modpow_s(long long btmn, long long topn, long long modn) {
        long long ret_num = 1;
        btmn%=modn;
        for(; topn; topn/=2, btmn=modmul(btmn,btmn,modn))
            if (topn & 1ll) ret_num=modmul(ret_num,btmn,modn);
        return ret_num%modn;
    } 
public:
    mint(long long x = 0) : x((x%mintmod + mintmod)%mintmod) {}
    mint operator-() const {
        return mint(-x);
    }
    mint& operator+=(const mint& a) {
        if ((x += a.x) >= mintmod) x -= mintmod;
        return *this;
    }
    mint& operator-=(const mint& a) {
        if ((x += mintmod - a.x) >= mintmod) x -= mintmod;
        return *this;
    }
    mint& operator*=(const mint& a) {
        x = modmul(x, a.x, mintmod);
        return *this;
    }
    mint operator+(const mint& a) const {
        mint res(*this);
        return res += a;
    }
    mint operator-(const mint& a) const {
        mint res(*this);
        return res -= a;
    }
    mint operator*(const mint& a) const {
        mint res(*this);
        return res *= a;
    }
    template<typename T>
    mint pow(T t) const {
        if (!t) return 1;
        mint a = pow(t >> 1);
        a *= a;
        if (t & 1) a *= *this;
        return a;
    }
    mint inv() const {
        return pow(mintmod-2);
    }
    mint& operator/=(const mint& a) {
        return (*this) *= a.inv();
    }
    mint operator/(const mint& a) const {
        mint res(*this);
        return res/=a;
    }

    mint operator==(const mint& a) {
        return (*this).x == a.x;
    }
    template <typename T>
    mint operator==(const T &a) {
        return (*this).x == a;
    }

    friend std::ostream& operator<<(std::ostream& os, const mint& m) {
        os << m.x;
        return os;
    }
};
```