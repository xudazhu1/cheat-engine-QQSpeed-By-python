# coding=utf-8




def shanghai(wuqi, wuqi2, wuqibaoshang,
             tougongji, toubaoshang, toubaoji):
    juese = 301
    # wuqi = 401
    # wuqi2 = 0.503
    # wuqibaoshang = 0
    # 圣遗物的攻击值
    shengyiwu1 = 430
    # 圣遗物的攻击百分比
    shengyiwu2 = 1.142 - 0.466 + tougongji

    #攻击力
    gongji = (juese + wuqi) * (1 + wuqi2 + shengyiwu2) + shengyiwu1

    # gongji = 2286.79
    # 元素伤害
    yaunsu = 0.616
    # 暴击率
    baoji = 0.40 + toubaoji
    #  暴击伤害
    baoshang = 1.184 + toubaoshang

    # 元素后伤害
    yuansuTemp = gongji * (1 + yaunsu)

    print("攻击力: \t\t\t\t\t" + str(gongji))
    print("暴击率: \t\t\t\t\t" + str(baoji))
    print("爆伤: \t\t\t\t\t" + str(baoshang + wuqibaoshang))
    print("元素伤害: \t\t\t\t" + str(yaunsu))

    # 总爆伤
    baoshangC = baoshang + wuqibaoshang

    # shanghai1 = yuansuTemp * (1 + baoshangC) * baoji + yuansuTemp * (1 - baoji)
    # shanghai1 = yuansuTemp * ((1 + baoshangC) * baoji + 1 - baoji)
    # shanghai1 = yuansuTemp * (baoji + baoshangC * baoji + 1 - baoji)
    shanghai1 = yuansuTemp * (baoshangC * baoji + 1)
    # 6758.243788032
    print("单次100%倍率期望伤害值: \t" + str(shanghai1 / 2))


# shanghai(401, 0.503, 0, 0.466, 0)
# shanghai(401, 0.503, 0, 0, 0.622)
# shanghai(497, 0, 0.335, 0, 0.622)
# shanghai(497, 0, 0.335, 0.466, 0)
shanghai(454, 0.551, 0, 0.466, 0, 0) # 武器1 攻击头
shanghai(454, 0.551, 0, 0, 0.622, 0.10) # 武器1 爆伤头
shanghai(454, 0.551, 0, 0, 0.13, 0.31) # 武器1 暴击头
# shanghai(565, 0, 0.368, 0, 0.622) # 武器2 爆伤头
# shanghai(565, 0, 0.368, 0.466, 0) # 武器2 攻击头