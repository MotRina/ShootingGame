from random import random, randint, randrange
import pyxel

WINDOW_H = 120
WINDOW_W = 160
PIC_H = 16
PIC_W = 16

class APP:
 def __init__(self):
    self.game_start = False
    self.game_over = False
    self.game_end = False
    self.boss = Boss()
    self.boss_enemys = []
    self.boss_flug = False
    self.boss_scr = 0
    self.boss_count = 1
    self.boss_color = 0
    self.score = 0
    self.shots = []
    self.enemys = []
    self.boss_hp = 20
    self.bombs = []
    self.p_ship = Ship()
    self.music_flug = False


    pyxel.init(WINDOW_W, WINDOW_H, title="ShootingGame_RinaMotoyama")
    pyxel.load("inve.pyxres")

    pyxel.mouse(False)


    pyxel.run(self.update, self.draw)

 def update(self):
    #BGM
    if self.music_flug == False:
        pyxel.playm(0, loop=True)
        self.music_flug = True

    #キーボード
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()
    if pyxel.btnp(pyxel.KEY_R):
        self.game_start = False
    if pyxel.btnp(pyxel.KEY_S):
        self.game_start = True
        self.retry()

    #自機の更新
    if self.game_over == False:
        self.ship_move()


    if self.game_end == False:
        self.hit_chk()
        self.ene_move()
        self.boss_move()

    self.bomb_del()
    #画面の爆発が3以上になったら古いものから消していく
    if len(self.bombs) > 3:
        del self.bombs[0]

 def draw(self):
    if self.boss_count == 6:
        pyxel.cls(15)
    else:
        pyxel.cls(15)

    #ゲームオーバー
    if self.game_over:
        if self.boss_count == 6:
            pyxel.cls(15)
            pyxel.text(100, 60, "GAME OVER!! ", 0)
            pyxel.text(100, 80, "R = RETRY ", 0)
            pyxel.text(100, 90, "Q = QUIT ", 0)
        else:
            pyxel.cls(15)
            pyxel.text(100, 60, "GAME OVER!! ", pyxel.frame_count % 16)
            pyxel.text(100, 80, "R = RETRY ", pyxel.frame_count % 16)
            pyxel.text(100, 90, "Q = QUIT ", pyxel.frame_count % 16)

    #得点描写：レベル５だけSCORE/LEVEL等の文字の色を変更＝＝ラストステージなので
    if self.boss_count == 5:
        pyxel.text(5, 2, "SCORE:" + str(self.score), 9)
        if self.boss_flug == True:
            pyxel.text(120, 2, "HP:" + str(self.boss.boss_h), 9)
        else:
            pyxel.text(120, 2, "LEVEL:" + str(self.boss_count), 9)
    else:
        pyxel.text(5, 2, "SCORE:" + str(self.score), 8)
        if self.boss_flug == True:
            pyxel.text(120, 2, "HP:" + str(self.boss.boss_h), 8)
        else:
            pyxel.text(120, 2, "LEVEL:" + str(self.boss_count), 8)

    #宇宙船の描画 ＝　レベル５の時宇宙船デザイン変更　・　ゲームオーバーの時宇宙船破壊
    if self.game_over == False:
        if self.boss_count == 5:
            pyxel.blt(self.p_ship.ship_x, self.p_ship.ship_y, 0, 144, 0,
                  -PIC_W, PIC_H, 6)
        else:
            pyxel.blt(self.p_ship.ship_x, self.p_ship.ship_y, 0, 96, 0,
                  -PIC_W, PIC_H, 6)
    else:
        pyxel.blt(self.p_ship.ship_x, self.p_ship.ship_y, 0, 112,
                            0,-PIC_W, PIC_H, 6)
        pyxel.play(1,8,loop=False)


    #弾の描画
    if self.boss_count == 6:
        for i in self.shots:
            if i.exists == True:
                pyxel.rect(i.pos_x+7, i.pos_y-3,
                           2, 2, 0)
    else:
        for i in self.shots:
            if i.exists == True:
                pyxel.rect(i.pos_x+7, i.pos_y-3,
                           2, 2, 12)

     #敵の描画 （敵一体につき、二通りのデザインに変わる）
    for i in self.enemys:
        if self.boss_flug == False:
            if self.boss_count == 6:
                if i.ene_f == 0:
                    pyxel.blt(i.ene_x, i.ene_y, 0, 0, i.ene_c * 32,
                                  -PIC_W, PIC_H, 6)
                else:
                    pyxel.blt(i.ene_x, i.ene_y, 0, 16, i.ene_c * 32,
                                  -PIC_W, PIC_H, 6)
            else:
                if i.ene_v == 1:
                    if i.ene_f == 0:
                        pyxel.blt(i.ene_x, i.ene_y, 0, 0, i.ene_c * 32,
                                  -PIC_W, PIC_H, 6)
                    else:
                        pyxel.blt(i.ene_x, i.ene_y, 0, 16, i.ene_c * 32,
                                  -PIC_W, PIC_H, 6)
                elif i.ene_v == 2:
                    if i.ene_f == 0:
                        pyxel.blt(i.ene_x, i.ene_y, 0, 32, i.ene_c * 32,
                                  -PIC_W, PIC_H, 6)
                    else:
                        pyxel.blt(i.ene_x, i.ene_y, 0, 48, i.ene_c * 32,
                                  -PIC_W, PIC_H, 6)
                else:
                    if i.ene_f == 0:
                        pyxel.blt(i.ene_x, i.ene_y, 0, 64, i.ene_c * 32,
                                  -PIC_W, PIC_H, 6)
                    else:
                        pyxel.blt(i.ene_x, i.ene_y, 0, 80, i.ene_c * 32,
                                  -PIC_W, PIC_H, 6)
        else:
            if self.boss_count == 7:
                if i.ene_f == 0:
                    pyxel.blt(i.ene_x, i.ene_y, 0, 0, i.ene_c * 32,
                                  -PIC_W, PIC_H, 6)
                else:
                    pyxel.blt(i.ene_x, i.ene_y, 0, 16, i.ene_c * 32,
                                  -PIC_W, PIC_H, 6)
            else:
                 pyxel.blt(i.ene_x, i.ene_y, 0, 48, 16 * self.boss_color,
                           16, 16, 6)

     #ボスの描画
    if self.boss_flug == True:
        if self.boss_count == 6:
            pyxel.blt(self.boss.boss_x, self.boss.boss_y,
                      0, 16, 128, 16, 16, 6)
        else:
            pyxel.blt(self.boss.boss_x, self.boss.boss_y,
                      0, 0, 16 * self.boss.boss_c, 48, 16, 6)

    #爆発の描写
    for i in self.bombs:
        if i.bomb_t < 30:
            pyxel.blt(i.bomb_x, i.bomb_y, 0, 128, 0,
                      -PIC_W, PIC_H, 6)
            pyxel.play(1,8,loop=False)


    #ゲームスタート画面
    if self.game_start == False:
         pyxel.cls(1)
         pyxel.text(40, 30, "--  SHOOTING GAME  --", 7)
         pyxel.text(55, 60, "ARE U READY? ", pyxel.frame_count % 16)
         pyxel.text(50, 70, "* ATTACK = SPACE ", pyxel.frame_count % 16)
         pyxel.text(50, 80, "* START = S ", pyxel.frame_count % 16)
         pyxel.text(50, 90, "* QUIT = Q ", pyxel.frame_count % 16)

    #ゲームクリア画面
    if self.game_end == True:
         pyxel.cls(0)
         pyxel.text(20, 30, "SHOOTING GAME", 10)
         pyxel.text(100, 60, "GAME CLEAR!", pyxel.frame_count % 16)

 def retry(self): #リトライ時のリセット関数
    self.game_over = False
    self.game_end = False
    self.boss_flug = False
    self.boss_count = 1
    self.boss_color = 0
    self.score = 0
    self.shots = []
    self.enemys = []
    self.boss_enemys = []
    self.boss_hp = 50
    self.bombs = []
    self.p_ship = Ship()

 def ship_move(self): #自機を動かす関数
    if pyxel.btn(pyxel.KEY_RIGHT):
        if self.p_ship.ship_x < 145:
            self.p_ship.update(self.p_ship.ship_x + 2, self.p_ship.ship_y)
    if pyxel.btn(pyxel.KEY_LEFT):
        if self.p_ship.ship_x > 0:
            self.p_ship.update(self.p_ship.ship_x - 2, self.p_ship.ship_y)
    #SPACEが押された際に発射する
    if pyxel.btnp(pyxel.KEY_SPACE, 5, 15):
        if len(self.shots) < 11:
            new_shot = Shot()
            new_shot.update(self.p_ship.ship_x, self.p_ship.ship_y, 8)
            self.shots.append(new_shot)
            pyxel.play(1,7,loop=False)

 def ene_move(self): #敵を動かす関数
    #通常時
    if self.boss_flug == False:
        if pyxel.frame_count % 30 == 0:
            if self.boss_count == 1:
                new_enemy = Enemy(1)
                new_enemy.ene_x = randrange(30, 65, 16)
                self.enemys.append(new_enemy)
                new_enemy = Enemy2(1)
                new_enemy.ene_x = randrange(70, 125, 16)
                self.enemys.append(new_enemy)
            elif self.boss_count == 2:
                enemy_v = randint(1, 2)
                new_enemy = Enemy(enemy_v)
                new_enemy.ene_x = randrange(30, 65, 16)
                self.enemys.append(new_enemy)
                enemy_v = randint(1, 2)
                new_enemy = Enemy2(enemy_v)
                new_enemy.ene_x = randrange(70, 125, 16)
                self.enemys.append(new_enemy)
            elif self.boss_count == 6:
                enemy_v = randint(1, 3)
                new_enemy = Enemy(enemy_v)
                new_enemy.ene_x = randrange(30, 65, 16)
                new_enemy.ene_c = 3.5
                self.enemys.append(new_enemy)
                enemy_v = randint(2, 3)
                new_enemy = Enemy2(enemy_v)
                new_enemy.ene_x = randrange(70, 125, 16)
                new_enemy.ene_c = 3.5
                self.enemys.append(new_enemy)
            else:
                enemy_v = randint(1, 3)
                new_enemy = Enemy(enemy_v)
                new_enemy.ene_x = randrange(30, 65, 16)
                self.enemys.append(new_enemy)
                enemy_v = randint(2, 3)
                new_enemy = Enemy2(enemy_v)
                new_enemy.ene_x = randrange(70, 125, 16)
                self.enemys.append(new_enemy)
    #ボス攻撃
    else:
        if self.boss_count != 6:
            if self.boss_count == 5:
                atk = 15
                if pyxel.frame_count % atk == 0:
                    new_enemy = Enemy(9)
                    if (self.boss.boss_x <= self.p_ship.ship_x + 8
                        <= self.boss.boss_x + 45):
                        new_enemy.ene_x = self.p_ship.ship_x + 5
                    else:
                        new_enemy.ene_x = randint(self.boss.boss_x + 5,
                                                  self.boss.boss_x + 40)
                    new_enemy.ene_y = self.boss.boss_y + 8
                    self.enemys.append(new_enemy)

            else:
                atk = 30 - (self.boss_count * 2)
                if pyxel.frame_count % atk == 0:
                    new_enemy = Enemy(9)
                    new_enemy.ene_x = self.boss.boss_x + 5
                    new_enemy.ene_y = self.boss.boss_y + 8
                    self.enemys.append(new_enemy)
                    new_enemy = Enemy(9)
                    new_enemy.ene_x = self.boss.boss_x + 45
                    new_enemy.ene_y = self.boss.boss_y + 8
                    self.enemys.append(new_enemy)

    enemy_count = len(self.enemys)
    for e in range (enemy_count):
        enemy_vec1 = randint(0, 7)
        enemy_vec2 = enemy_vec1 % 2
        if self.enemys[e].ene_y < 115:
            ene_chk =self.e_move_chk(e, self.enemys[e].ene_x,
                                         self.p_ship.ship_y)
            #敵のy座標
            if self.enemys[e].ene_v == 1:
                self.enemys[e].ene_y = self.enemys[e].ene_y + 1.0
            elif self.enemys[e].ene_v == 2:
                self.enemys[e].ene_y = self.enemys[e].ene_y + 1.2
                #2番の敵はここでx移動をさせる
                if ene_chk == 0:
                    if self.enemys[e].ene_x > self.p_ship.ship_x:
                        self.enemys[e].ene_x=self.enemys[e].ene_x - 0.25
                    else:
                        self.enemys[e].ene_x=self.enemys[e].ene_x + 0.25
            elif self.enemys[e].ene_v == 3:
                if self.enemys[e].ene_f == 0:
                    self.enemys[e].ene_y = self.enemys[e].ene_y + 1.4
                    if self.enemys[e].ene_y > self.p_ship.ship_y - 2:
                        self.enemys[e].ene_f = 1
                else:
                    self.enemys[e].ene_y = self.enemys[e].ene_y - 1.2
                    #3番の敵はここでx移動をさせる
                    if self.enemys[e].ene_x < self.p_ship.ship_x:
                        if ene_chk == 0:
                            self.enemys[e].ene_x=self.enemys[e].ene_x + 0.25
                    else:
                        if ene_chk == 0:
                            self.enemys[e].ene_x=self.enemys[e].ene_x - 0.25
                    if self.enemys[e].ene_y < self.p_ship.ship_y - 40:
                        if self.boss_count != 7 and self.boss_flug == False:
                            self.enemys[e].ene_f = 0
                        elif self.enemys[e].ene_y < 0:
                             del self.enemys[e]
                             break
            elif self.enemys[e].ene_v == 9:
                if self.boss_count == 5:
                    self.enemys[e].ene_y = (self.enemys[e].ene_y + 2.0)
                else:
                    self.enemys[e].ene_y = (self.enemys[e].ene_y + 1.0)

            if pyxel.frame_count % 50 == 0 and ene_chk == 0:
                if self.boss_flug == False or self.boss_count == 7:
                    #敵のx座標
                    if self.enemys[e].ene_v == 1:
                        if enemy_vec2 > 0:
                            self.enemys[e].ene_x = self.enemys[e].ene_x + 4
                            if self.enemys[e].ene_f == 0:
                                self.enemys[e].ene_f = 1
                            else:
                                self.enemys[e].ene_f = 0
                        else:
                            self.enemys[e].ene_x = self.enemys[e].ene_x - 4
                            if self.enemys[e].ene_f == 0:
                                self.enemys[e].ene_f = 1
                            else:
                                self.enemys[e].ene_f = 0
                    elif self.enemys[e].ene_v == 2:
                        if self.enemys[e].ene_x < self.p_ship.ship_x:
                            if self.enemys[e].ene_f == 0:
                                self.enemys[e].ene_f = 1
                            else:
                                self.enemys[e].ene_f = 0
                        else:
                            if self.enemys[e].ene_f == 0:
                                self.enemys[e].ene_f = 1
                            else:
                                self.enemys[e].ene_f = 0
                    else:
                        continue
                else:
                    continue
        else:
            del self.enemys[e]
            break

 def e_move_chk(self, me, x, y):
    enemy_hit = len(self.enemys)
    for e in range(enemy_hit):
        if e == me:
           break
        if ((self.enemys[e].ene_x - 8 <= x + 16) and
            (self.enemys[e].ene_x + 8 <= x -16 )and
            (self.enemys[e].ene_y - 8 <= y + 8)):
               result = 1
               return result
        else:
            result = 0
            return result

 def hit_chk(self): #当たり判定関数
    shot_count = len(self.shots)
    #上限を超えた弾を削除
    for j in range (shot_count):
        if self.shots[j].pos_y > 8:
            self.shots[j].pos_y = self.shots[j].pos_y - 3
        else:
            del self.shots[j]
            break
      #当たり判定
        #敵と弾
    shot_hit = len(self.shots)
    if self.boss_flug == False:
       for h in range (shot_hit):
            enemy_hit = len(self.enemys)
            for e in range (enemy_hit):
                if ((self.enemys[e].ene_x - 8 <= self.shots[h].pos_x
                     <= self.enemys[e].ene_x + 8)and
                     (self.enemys[e].ene_y - 7 <= self.shots[h].pos_y <=
                      self.enemys[e].ene_y + 15)and
                     (self.shots[h].exists == True)):
                    #敵に当たったらその座標に爆発を乗せる
                    new_bomb = Bomb(self.enemys[e].ene_x,
                                    self.enemys[e].ene_y)
                    self.bombs.append(new_bomb)
                    del self.enemys[e]
                    self.shots[h].shot_del()
                    if self.boss_flug == False:
                        self.score = self.score + 100
                        self.boss_scr = self.boss_scr + 1
                        break#敵に当たったらbreak
                else:
                    continue
                break

    #敵と自機
    enemy_atk = len(self.enemys)
    for e in range (enemy_atk):
        if self.boss_flug == False:
            #4か所で接触を検知
            #1
            if (((self.enemys[e].ene_x + 3 >= self.p_ship.ship_x + 2) and
                 (self.enemys[e].ene_x + 3 <= self.p_ship.ship_x + 14) and
                 (self.enemys[e].ene_y >= self.p_ship.ship_y) and
                 (self.enemys[e].ene_y <= self.p_ship.ship_y + 14))or
            #2
                 (self.enemys[e].ene_x + 12 >= self.p_ship.ship_x + 2) and
                 (self.enemys[e].ene_x + 12 <= self.p_ship.ship_x + 14) and
                 (self.enemys[e].ene_y >= self.p_ship.ship_y) and
                 (self.enemys[e].ene_y <= self.p_ship.ship_y + 14)or
            #3
                 (self.enemys[e].ene_x + 3 >= self.p_ship.ship_x + 2) and
                 (self.enemys[e].ene_x + 3 <= self.p_ship.ship_x + 14) and
                 (self.enemys[e].ene_y + 6 >= self.p_ship.ship_y) and
                 (self.enemys[e].ene_y + 6 <= self.p_ship.ship_y + 14)or
            #4
                 ((self.enemys[e].ene_x + 12 >= self.p_ship.ship_x + 2) and
                 (self.enemys[e].ene_x + 12 <= self.p_ship.ship_x + 14) and
                 (self.enemys[e].ene_y + 6 >= self.p_ship.ship_y) and
                 (self.enemys[e].ene_y + 6 <= self.p_ship.ship_y + 14))):
                  self.game_over = True
        else:
            #4か所で接触を検知
            #1
            if (((self.enemys[e].ene_x + 3 >= self.p_ship.ship_x + 2) and
                 (self.enemys[e].ene_x + 3 <= self.p_ship.ship_x + 14) and
                 (self.enemys[e].ene_y >= self.p_ship.ship_y) and
                 (self.enemys[e].ene_y <= self.p_ship.ship_y + 14))or
            #2
                 (self.enemys[e].ene_x + 12 >= self.p_ship.ship_x + 2) and
                 (self.enemys[e].ene_x + 12 <= self.p_ship.ship_x + 14) and
                 (self.enemys[e].ene_y >= self.p_ship.ship_y) and
                 (self.enemys[e].ene_y <= self.p_ship.ship_y + 14)or
            #3
                 (self.enemys[e].ene_x + 3 >= self.p_ship.ship_x + 2) and
                 (self.enemys[e].ene_x + 3 <= self.p_ship.ship_x + 14) and
                 (self.enemys[e].ene_y + 6 >= self.p_ship.ship_y) and
                 (self.enemys[e].ene_y + 6 <= self.p_ship.ship_y + 14)or
            #4
                 ((self.enemys[e].ene_x + 12 >= self.p_ship.ship_x + 2) and
                 (self.enemys[e].ene_x + 12 <= self.p_ship.ship_x + 14) and
                 (self.enemys[e].ene_y + 6 >= self.p_ship.ship_y) and
                 (self.enemys[e].ene_y + 6 <= self.p_ship.ship_y + 14))):
                  self.game_over = True

 def boss_move(self):
    #ボス出現フラグ
    if self.boss_flug == False: #ボス未出現の状態で
        if self.score != 0:     #ゲーム開始直後ではなく
            boss_chk = 15 * self.boss_count
            if boss_chk > 100:
                boss_chk = 100
            if self.boss_scr % boss_chk == 0: #ボススコアxxxx点に達したら
                if self.game_end == False: #ゲームクリアフラグがない場合にボス発生
                    if self.boss_count == 2:
                        self.boss_flug = True
                        self.enemys.clear()
                        self.boss_hp = 20 * self.boss_count
                        self.boss_color = 6
                        self.boss.update(50, 10, self.boss_hp,
                                         self.boss_color)
                        pyxel.playm(3, loop=True)

                    elif self.boss_count == 3:
                        self.boss_flug = True
                        self.enemys.clear()
                        self.boss_hp = 60
                        self.boss_color = randrange(1, 6, 2)
                        self.boss.update(70, 0, self.boss_hp,
                                         self.boss_color)


                    else:
                        self.boss_flug = True
                        self.enemys.clear()
                        self.boss_hp = 50
                        self.boss_color = randrange(1, 6, 2)
                        self.boss.update(50, 10, self.boss_hp,
                                         self.boss_color)



    #ボスの動き＆当たり判定
    if self.boss_flug == True:
        if self.boss_count == 4:
             if self.boss.boss_m == 0:
               if self.boss.boss_x > self.p_ship.ship_x - 8:
                   self.boss.move(self.boss.boss_x - 1, self.boss.boss_y)
               elif self.boss.boss_x == self.p_ship.ship_x - 8:
                   self.boss.boss_m = 1
               else:
                   self.boss.move(self.boss.boss_x + 1, self.boss.boss_y)
             elif self.boss.boss_m == 1:
               if self.boss.boss_y > self.p_ship.ship_y - 40:
                   self.boss.boss_m = 2
               else:
                   self.boss.move(self.boss.boss_x, self.boss.boss_y + 1)
             else:
                 self.boss.move(self.boss.boss_x, self.boss.boss_y - 1)
                 if self.boss.boss_y < 10:
                   self.boss.boss_m = 0
        elif self.boss_count == 5:
             if self.boss.boss_y < 150:
                 self.boss.move(self.boss.boss_x, self.boss.boss_y + 0.1)
                 if self.boss.boss_y > 100:
                     self.game_over == True
        else:
             if self.boss.boss_m == 0:
               if self.boss.boss_x > 0:
                   self.boss.move(self.boss.boss_x - 1, self.boss.boss_y)
               else:
                   self.boss.boss_m = 1
             else:
               if self.boss.boss_x < 115:
                   self.boss.move(self.boss.boss_x + 1, self.boss.boss_y)
               else:
                  self.boss.boss_m = 0
        shot_hit = len(self.shots)
        for h in range (shot_hit):
            if self.boss_count == 6 or self.boss_count == 7:
                hitbox_x = 15
                hitbox_y = 15
            else:
                hitbox_x = 40
                hitbox_y = 10
            if ((self.boss.boss_x - 8 <= self.shots[h].pos_x
                 <= self.boss.boss_x + hitbox_x) and
                (self.boss.boss_y <= self.shots[h].pos_y
                 <= self.boss.boss_y + hitbox_y)):
                self.shots[h].shot_del()
                self.boss.boss_h = self.boss.boss_h - 1
                new_bomb = Bomb(self.shots[h].pos_x, self.shots[h].pos_y)
                self.bombs.append(new_bomb)
    #ボス消滅
    if self.boss.boss_h <= 0:
        if self.boss_flug == True:
            self.score = self.score + 5000
            pyxel.cls(0)
            self.boss_flug = False
            self.enemys.clear()
            self.boss_count = self.boss_count + 1
            self.boss_scr = 1
            if self.boss_count == 6: #5体のボスを倒すとゲームクリア
                self.game_end = True

 def bomb_del(self): #爆発の寿命関数
    for b in self.bombs:
        b.bomb_t = b.bomb_t + 1

#オブジェクトのクラス


class Ship:
 def __init__(self):
    self.ship_x = 70
    self.ship_y = 105 #最初の場所
 def update(self, x, y):
    self.ship_x = x
    self.ship_y = y

class Shot:
 def __init__(self):
    self.pos_x = 0
    self.pos_y = 0
    self.color = 8
    self.exists = True
 def update(self, x, y, color):
    self.pos_x = x
    self.pos_y = y
    self.color = color
 def shot_del(self):
    self.exists = False

class Enemy:
 def __init__(self, v):
    self.ene_x = 0
    self.ene_y = 0
    self.ene_f = 0
    self.ene_c = randint(0, 2)
    self.ene_v = v
    self.ene_h = 4
 def update(self, x, y):
    self.ene_x = x
    self.ene_y = y
 def ene_del(self):
    self.exists = False

class Enemy2:
 def __init__(self, v):
    self.ene_x = randint(20, 125)
    self.ene_y = 10
    self.ene_f = 0
    self.ene_c = randint(0, 2)
    self.ene_v = v
 def update(self, x, y):
    self.ene_x = x
    self.ene_y = y

class Bomb:
 def __init__(self, x, y):
    self.bomb_x = x
    self.bomb_y = y
    self.bomb_t = 0

class Boss:
 def __init__(self):
    self.boss_x = 0
    self.boss_y = 0
    self.boss_h = 0
    self.boss_c = 0
    self.boss_m = 0
 def update(self, x, y, h, c):
    self.boss_x = x
    self.boss_y = y
    self.boss_h = h
    self.boss_c = c
 def move(self, x, y):
    self.boss_x = x
    self.boss_y = y

APP()
