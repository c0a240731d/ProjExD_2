import os
import random
import sys
import time
import pygame as pg

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

def gameover(screen: pg.Surface) -> None:
    bl_img = pg.Surface((WIDTH, HEIGHT))  # 空のSurface
    pg.draw.rect(bl_img, (0, 0, 0), (0, 0, 20, 20))  # 黒い四角を描画
    bl_img.set_alpha(200, 0)  # 透明度設定
    fonto = pg.font.Font(None, 80)  # フォントオブジェクト作成
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2)  # こうかとん画像拡大
    kk_rct = kk_img.get_rect()  # こうかとんRect
    kk_rct.center = 300, 300  # こうかとん座標
    bl_img.blit(kk_img, kk_rct)  # こうかとん描画
    bl_img.blit(kk_img, (kk_rct[0]+500,kk_rct[1]))  # こうかとん２体目描画
    txt = fonto.render("Game Over",True, (255, 255, 255))  # 文字描画
    bl_img.blit(txt, [400, 300])  # 文字描画位置
    screen.blit(bl_img, [0, 0])  # 画面に貼り付け
    pg.display.update()  # 画面更新
    time.sleep(5)  # 5秒間表示

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []  # 爆弾画像リスト
    bb_accs = []  # 爆弾速度リスト
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))  # 空のSurface
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)  # 赤い円を描画
        bb_img.set_colorkey((0, 0, 0))  # 黒色を透明色に設定
        bb_imgs.append(bb_img)
        bb_accs = [a for a in range(1, 11)]
    return bb_imgs, bb_accs

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 半径10の赤い円を描画
    bb_img.set_colorkey((0, 0, 0))  # 黒色を透明色に設定
    bb_rct = bb_img.get_rect()  # 爆弾Rect
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,HEIGHT)  # 爆弾座標
    vx,vy = +5, +5  # 爆弾の横速度,縦速度
    clock = pg.time.Clock()
    tmr = 0
    bb_imgs, bb_accs = init_bb_imgs()
    while True:
        
        avx = vx*bb_accs[min(tmr//500, 9)]  # 加速度を考慮した横速度
        avy = vy*bb_accs[min(tmr//500, 9)]  # 加速度を考慮した縦速度
        bb_img = bb_imgs[min(tmr//500, 9)]  # 加速度を考慮した爆弾画像
        
        for event in pg.event.get():  # イベント処理
            if event.type == pg.QUIT:  # 終了イベント
                return
        
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が衝突したら
            gameover(screen)
            print("ゲームオーバー")
            return
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
           # sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
           # sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
           # sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
           # sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]  # 横方向の移動量
                sum_mv[1] += mv[1]  # 縦方向の移動量

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):  # 画面外に出たら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 反転される
        screen.blit(kk_img, kk_rct)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出ていたら
            avx *= -1
        if not tate:  # 縦方向にはみ出ていたら
            avy *= -1
        bb_rct.move_ip(avx,avy)
        bb_rct.width = bb_img.get_rect().width
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
