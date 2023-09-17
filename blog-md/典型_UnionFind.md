# UnionFind典型

UnionFindの良典型問題集：

## [ABC183F](https://atcoder.jp/contests/abc183/tasks/abc183_f) 

> $N, Q \leq 10^5$

始めに、$\forall s \in [1,N], f(s) = \{s\}$ <br>
また、$g : [1:N] \rightarrow [1:N]$が渡される 

2種類のクエリを処理する問題

* クエリ1: $s_1, s_2 \in [1:N]$が与えられるので、$f(s_1)とf(s_2)をf(s_1) \cup f(s_2)$の値に置き換える(再定義する)
* クエリ2: $s, k$が与えらえるので、#$\{u \in f(s) : g(u) = k\}$を出力

クエリ1の処理は通常のUnionFindと同様 <br>
また、クエリ2を処理することを考えると、$h(s,k) = \#\{u \in f(s) : g(u) = k\}$とした時、集合のマージ時：

* $root(s_1) = root(s_2)$ : 
    * $ h(s,k)_{new} = h(s,k)_{old} $
* $root(s_1) \neq root(s_2)$ :
    * $h(s,k)_{new} = h(s,k)_{old} : s \neq s_1,s_2$
    * $h(s,k)_{new} = h(s_1,k)_{old}+h(s_2,k)_{old} : s = s_1,s_2$

$h(s,k)$の中で値が0でない$k$は高々$|f(s)|$なので、vector\<map\>などで$h$を保持すると、処理が簡単です。また、merge時、小さい方の集合を大きい方に足すことで処理を高速化できます（ここが典型ポイント）

これでクエリ2を高速に処理できます(各クエリ$O(logN)$です)