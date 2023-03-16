# Shooting Game (Python/Pyxel)
##### Pyxel (ピクセル)を用いた、 シューティングゲームです。
##### Pyxel は Python 向けのレトロゲームエンジンで、[説明](https://github.com/kitao/pyxel/blob/main/docs/README.ja.md)を参考に作成しました。


# ゲーム構成
### ① スタート画面
##### プレイヤーは、スタート画面で大まかな使い方を把握することができます。 「Sキー」でスタート、「SPACEキー」で攻撃、「Qキー」でゲームをやめることができます。
<img width="325" alt="スタート画面" src="https://user-images.githubusercontent.com/127751292/225550213-b04875ee-7f15-4b05-bbb5-80b83166670e.png">


### ② 本編
##### 全部で5つのレベルが用意されています。 プレイヤー ・ 敵は、1度でも攻撃に当たってしまうと倒れる仕組みです。

+ スコアとレベルは上部に表記
+ 敵は上から下に落ちてくる
+ 敵を1体倒すと「SCORE+100」
+ ←/→で左右に移動
+ レベル3以上は一部の敵が下まで落ち切ると倒すまでその場で跳ね続けるようになる → 難易度が増す

<p>
<img width="326" alt="レベル1" src="https://user-images.githubusercontent.com/127751292/225553185-75ef5ab4-9a44-4da2-b053-0fcf4daa2c8f.png">　<img width="325" alt="倒れた画面" src="https://user-images.githubusercontent.com/127751292/225553192-623229b4-abc8-40d7-87e6-ffaf5e17704e.png">
 </p>

### ③ ボス
##### それぞれのレベルで一定得点を取得すると各レベルのボスが登場します。 ボスは1度攻撃を当てても倒れず、HPがなくなると倒れます。 各レベルのボスを倒すと、次のレベルに上がることができる仕組みです。

+ ボスを倒すと「SCORE+5000」
+ 1度でもボスの攻撃に当たるとゲームオーバー
+ レベルごとにボスのHPは異なる
+ レベル4以上はボスの動きにも変化あり → 難易度が増す
<img width="325" alt="ボス戦" src="https://user-images.githubusercontent.com/127751292/225553935-78af0657-74d5-45da-b7a2-7e2fbf7222f0.png">

# キャラクター
#####  Pyxel Editor を使って、使用するキャラクターの画像やサウンドを作成しました。 
##### Pyxel Editor は次のコマンドで起動します。
```
pyxel edit inve.pyxres   
```

<img width="325" alt="Pyxel Edit" src="https://user-images.githubusercontent.com/127751292/225558688-aeae6264-fa90-42e9-9f5f-b595aa6a34af.png"> 
<p>
<img width="499" alt="敵の種類" src="https://user-images.githubusercontent.com/127751292/225559947-6988e1cf-0d5d-4960-84de-e244a3ab9501.png"> 
<img width="507" alt="音の種類" src="https://user-images.githubusercontent.com/127751292/225560061-93575585-5783-4038-a4fe-1b8e92e8b5dc.png">
</p>

# デモ
https://user-images.githubusercontent.com/127751292/225552445-076d04c2-b4d7-4cfa-aaf2-98087f1e523d.mov



