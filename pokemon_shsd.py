import os
import cv2
import pytesseract
import re
#import gtuner
os.environ['KMP_DUPLICATE_LIB_OK']='True'

# Setup Attack order
Attack_1_Setup = 2
Attack_2_Setup = 4
Attack_3_Setup = 3
Attack_4_Setup = 1

# Flags
noFight = 0
inFight = 0
inPoke = 0
inBag = 0
inBag1 = 0
inEscape = 0
inAttack = 0
Attack_1 = 0
Attack_2 = 0
Attack_3 = 0
Attack_4 = 0
Attack_Selection = 0

# Datasets images
NOFIGHT_DATASET = 708.2083026906703
NOFIGHT1_DATASET = 17256.413416466356
FIGHT_DATASET = 899.4592820133661
FIGHT1_DATASET = 4156.635057351078
POKE_DATASET = 672.0111606216076
BAG_DATASET = 916.8969407736073
INBAG_DATASET = 626.0942421073684
ESCAPE_DATASET = 802.7602381782496
ATTACK_DATASET = 158.89619252832964
HP_SELF_DATASET = 1504.2439961655157
HP_SELF1_DATASET = 687.9680225126747
HP_SELF2_DATASET = 7.0710678118654755
HP_ENEMY_DATASET = 5.0
HP_ENEMY1_DATASET = 1272.7234577864901
HP_ENEMY2_DATASET = 1503.0219559274576


# GCV Data Offsets
FIGHT_OFFSET = 0
POKE_OFFSET = 1
BAG_OFFSET = 2
ESCAPE_OFFSET = 3
ATTACK_OFFSET = 4
HP_SELF_OFFSET = 5
HP_SELF1_OFFSET = 6
HP_SELF2_OFFSET = 7
HP_ENEMY_OFFSET = 8
HP_ENEMY1_OFFSET = 9
HP_ENEMY2_OFFSET = 10
ATTACK1_SE_OFFSET = 11
ATTACK1_EF_OFFSET = 12
ATTACK1_NE_OFFSET = 13
ATTACK2_SE_OFFSET = 14
ATTACK2_EF_OFFSET = 15
ATTACK2_NE_OFFSET = 16
ATTACK3_SE_OFFSET = 17
ATTACK3_EF_OFFSET = 18
ATTACK3_NE_OFFSET = 19
ATTACK4_SE_OFFSET = 20
ATTACK4_EF_OFFSET = 21
ATTACK4_NE_OFFSET = 22
NOFIGHT_OFFSET = 23

# OCR Data
ATTACK1_DATA_OCR = "unknown"
ATTACK2_DATA_OCR = "unknown"
ATTACK3_DATA_OCR = "unknown"
ATTACK4_DATA_OCR = "unknown"

#cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
class GCVWorker:
    def __init__(self, width, height):
        os.chdir(os.path.dirname(__file__))
        if int((width * 100) / height) != 177:
            print("WARNING: Select a video input with 16:9 aspect ratio, preferable 1920x1080")
        self.scale = width != 1920 or height != 1080
        #self.gcvdata = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        self.gcvdata = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                                  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                                  0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        self.noFight = True
        self.inFight = True
        self.inPoke = True
        self.inBag = True
        self.inBag1 = True
        self.inHpSelf = True
        self.inHpEnemy = True
        self.inEscape = True
        self.inAttack = True
        self.noFightOcvOn = True
        self.inFightOcvOn = True
        self.inPokeOcvOn = True
        self.inBagOcvOn = True
        self.inEscapeOcvOn = True
        self.inAttackOcvOn = True
        self.noFightImg = cv2.imread('img/no_fight_1.jpg')
        self.inFightImg = cv2.imread('img/fight.jpg')
        self.inPokeImg = cv2.imread('img/pokemon.jpg')
        self.inBagImg = cv2.imread('img/bag.jpg')
        self.inBag1Img = cv2.imread('img/inBag.jpg')
        self.inHpSelfImg = cv2.imread('img/hp_self.jpg')
        self.inHpEnemyImg = cv2.imread('img/hp_enemy.jpg')
        self.inEscapeImg = cv2.imread('img/escape.jpg')
        self.inAttackImg = cv2.imread('img/attack_mode.jpg')
        self.Attack1Img = cv2.imread('img/attack1/xy.jpg')

    def __del__(self):
        del self.scale
        del self.gcvdata
        del self.noFight
        del self.inFight
        del self.inPoke
        del self.inBag
        del self.inBag1
        del self.inHpSelf
        del self.inHpEnemy
        del self.inEscape
        del self.inAttack
        del self.noFightOcvOn
        del self.inFightOcvOn
        del self.inPokeOcvOn
        del self.inBagOcvOn
        del self.inEscapeOcvOn
        del self.inAttackOcvOn

    def process(self, frame):
        global ATTACK1_DATA_OCR
        global ATTACK2_DATA_OCR
        global ATTACK3_DATA_OCR
        global ATTACK4_DATA_OCR
        global noFight
        global inFight
        global inPoke
        global inBag
        global inBag1
        global inEscape
        global inAttack
        global NOFIGHT_DATASET
        global NOFIGHT1_DATASET
        global FIGHT_DATASET
        global FIGHT1_DATASET
        global POKE_DATASET
        global BAG_DATASET
        global BAG1_DATASET
        global ESCAPE_DATASET
        global ATTACK_DATASET
        global HP_SELF_DATASET
        global HP_SELF1_DATASET
        global HP_SELF2_DATASET
        global HP_ENEMY_DATASET
        global HP_ENEMY1_DATASET
        global HP_ENEMY2_DATASET
        global FIGHT_OFFSET
        global POKE_OFFSET
        global BAG_OFFSET
        global ESCAPE_OFFSET
        global ATTACK_OFFSET
        global Attack_1
        global Attack_2
        global Attack_3
        global Attack_4
        global Attack_Selection

        # If needed, scale frame to 1920x1080
        if self.scale:
            frame = cv2.resize(frame, (1920, 1080))

########################################################################################################################
# Output Layout
        if noFight == 1:
            cv2.putText(frame, "No Fight: " + str(self.noFightOcvOn), (5, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2,
                        cv2.LINE_AA)

        if inFight == 1:
            cv2.putText(frame, "Fight Button: " + str(self.inFightOcvOn), (5, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

        if inPoke == 1:
            cv2.putText(frame, "Poke Button: " + str(self.inPokeOcvOn), (5, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

        if inBag == 1:
            cv2.putText(frame, "Bag Button: " + str(self.inBagOcvOn), (5, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

        if inBag1 == 1:
            cv2.putText(frame, "Inside Bag: " + str(self.inBagOcvOn), (100, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2,
                        cv2.LINE_AA)

        if inEscape == 1:
            cv2.putText(frame, "Escape Button: " + str(self.inEscapeOcvOn), (5, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

        if inAttack == 1:
            cv2.putText(frame, "In Attack Mode: " + str(self.inAttackOcvOn), (5, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

            cv2.putText(frame, "Attack 1: " + str(ATTACK1_DATA_OCR), (5, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

            cv2.putText(frame, "Attack 2: " + str(ATTACK2_DATA_OCR), (5, 120),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

            cv2.putText(frame, "Attack 3: " + str(ATTACK3_DATA_OCR), (5, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

            cv2.putText(frame, "Attack 4: " + str(ATTACK4_DATA_OCR), (5, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2,
                        cv2.LINE_AA)

########################################################################################################################
# Main
        # noFight
        picture_noFight = frame[992:1075, 16:68]
        similar_noFight = cv2.norm(self.noFightImg, picture_noFight)
        if similar_noFight == NOFIGHT_DATASET and self.noFight:
            self.noFight = False
            noFight = 1
            print("Reset GPC Fight Data")
            self.gcvdata[NOFIGHT_OFFSET] = True
        elif similar_noFight == NOFIGHT1_DATASET and self.noFight:
            self.noFight = False
            noFight = 1
            print("Reset GPC Fight Data")
            self.gcvdata[NOFIGHT_OFFSET] = True
        elif similar_noFight == NOFIGHT_DATASET:
            pass
        elif similar_noFight == NOFIGHT1_DATASET:
            pass
        else:
            self.noFight = True
            self.gcvdata[NOFIGHT_OFFSET] = False
            noFight = 0

        # Fight
        picture_inFight = frame[625:697, 1773:1875]
        similar_inFight = cv2.norm(self.inFightImg, picture_inFight)
        if similar_inFight == FIGHT_DATASET and self.inFight:
            self.inFight = False
            inFight = 1
            self.gcvdata[FIGHT_OFFSET] = True
        elif similar_inFight == FIGHT1_DATASET and self.inFight:
            self.inFight = False
            inFight = 1
            self.gcvdata[FIGHT_OFFSET] = True
        elif similar_inFight == FIGHT_DATASET:
            pass
        elif similar_inFight == FIGHT1_DATASET:
            pass
        else:
            self.inFight = True
            self.inHpEnemy = True
            inFight = 0
            self.gcvdata[FIGHT_OFFSET] = False

        # hp enemy check
        if inFight == 1:
            picture_inEnemyHeal = frame[98:103, 1470:1475]
            similar_inEnemyHeal = cv2.norm(self.inHpEnemyImg, picture_inEnemyHeal)
            if similar_inEnemyHeal == HP_ENEMY_DATASET and self.inHpEnemy:
                self.inHpEnemy = False
                print("Enemy HP is high")
                self.gcvdata[HP_ENEMY_OFFSET] = True
            elif similar_inEnemyHeal == HP_ENEMY1_DATASET and self.inHpEnemy:
                self.inHpEnemy = False
                print("Enemy HP is low")
                self.gcvdata[HP_ENEMY2_OFFSET] = True
            elif similar_inEnemyHeal == HP_ENEMY2_DATASET and self.inHpEnemy:
                self.inHpEnemy = False
                print("Enemy HP is very low")
                self.gcvdata[HP_ENEMY2_OFFSET] = True
            elif similar_inEnemyHeal == HP_ENEMY_DATASET:
                pass
            elif similar_inEnemyHeal == HP_ENEMY1_DATASET:
                pass
            elif similar_inEnemyHeal == HP_ENEMY2_DATASET:
                pass
            else:
                self.inHpEnemy = True
                self.gcvdata[HP_ENEMY_OFFSET] = False
                self.gcvdata[HP_ENEMY1_OFFSET] = False
                self.gcvdata[HP_ENEMY2_OFFSET] = False

        # Poke
        picture_inPoke = frame[748:820, 1773:1875]
        similar_inPoke = cv2.norm(self.inPokeImg, picture_inPoke)
        if similar_inPoke == POKE_DATASET and self.inPoke:
            self.inPoke = False
            inPoke = 1
            print("Found Poke Button")
            self.gcvdata[POKE_OFFSET] = True
        elif similar_inPoke == POKE_DATASET:
            pass
        else:
            self.inPoke = True
            inPoke = 0
            self.gcvdata[POKE_OFFSET] = False

        # Bag Fight
        picture_inBag = frame[860:932, 1773:1875]
        similar_inBag = cv2.norm(self.inBagImg, picture_inBag)
        if similar_inBag == BAG_DATASET and self.inBag:
            self.inBag = False
            inBag = 1
            self.gcvdata[BAG_OFFSET] = True
            #hp self check
            picture_inSelfHeal = frame[985:990, 26:31]
            similar_inSelfHeal = cv2.norm(self.inHpSelfImg, picture_inSelfHeal)
            if similar_inSelfHeal == HP_SELF_DATASET and self.inHpSelf:
                self.inHpSelf = False
                print("Your HP is fine")
                self.gcvdata[HP_SELF_OFFSET] = True
            elif similar_inSelfHeal == HP_SELF1_DATASET and self.inHpSelf:
                self.inHpSelf = False
                print("Your HP is low")
                self.gcvdata[HP_SELF1_OFFSET] = True
            elif similar_inSelfHeal == HP_SELF2_DATASET and self.inHpSelf:
                self.inHpSelf = False
                print("Your HP is very low")
                self.gcvdata[HP_SELF2_OFFSET] = True

            elif similar_inSelfHeal == HP_SELF_DATASET:
                pass
            elif similar_inSelfHeal == HP_SELF1_DATASET:
                pass
            elif similar_inSelfHeal == HP_SELF2_DATASET:
                pass
            else:
                self.inHpSelf = True
                self.gcvdata[HP_SELF_OFFSET] = False
                self.gcvdata[HP_SELF1_OFFSET] = False
                self.gcvdata[HP_SELF2_OFFSET] = False

        elif similar_inBag == BAG_DATASET:
            pass
        else:
            self.inBag = True
            self.inHpSelf = True
            inBag = 0
            self.gcvdata[BAG_OFFSET] = False

        # Inside Bag
        picture_inBag1 = frame[13:60, 1502:1591]
        similar_inBag1 = cv2.norm(self.inBag1Img, picture_inBag1)

        if similar_inBag1 == INBAG_DATASET and self.inBag1:
            self.inBag1 = False
            inBag1 = 1
        elif similar_inBag1 == INBAG_DATASET:
            pass
        else:
            self.inBag1 = True
            inBag1 = 0

        # Escape
        picture_inEscape = frame[976:1048, 1773:1875]
        similar_inEscape = cv2.norm(self.inEscapeImg, picture_inEscape)
        if similar_inEscape == ESCAPE_DATASET and self.inEscape:
            self.inEscape = False
            inEscape = 1
            print("Found Escape Button")
            self.gcvdata[ESCAPE_OFFSET] = True
        elif similar_inEscape == ESCAPE_DATASET:
            pass
        else:
            self.inEscape = True
            inEscape = 0
            self.gcvdata[ESCAPE_OFFSET] = False

        # Attack
        picture_inAttack = frame[535:574, 1683:1910]
        similar_inAttack = cv2.norm(self.inAttackImg, picture_inAttack)
        if similar_inAttack == ATTACK_DATASET and self.inAttack:
            self.inAttack = False
            inAttack = 1
            print("Found Attack Mode")
            #ocr attack1
            picture_inAttack_1 = frame[705:735, 1382:1642]
            cv2.imwrite('img/attack1/temp_img.jpg', picture_inAttack_1)
            img_cv_attack1 = cv2.imread(r'img/attack1/temp_img.jpg')
            img_rgb_attack1 = cv2.cvtColor(img_cv_attack1, cv2.COLOR_BGR2RGB)
            custom_config = r'-c tessedit_char_blacklist=? --oem 3 --psm 6'
            ATTACK1_DATA = pytesseract.image_to_string(img_rgb_attack1, config=custom_config)
            #ocr attack2
            picture_inAttack_2 = frame[810:840, 1382:1642]
            cv2.imwrite('img/attack2/temp_img.jpg', picture_inAttack_2)
            img_cv_attack2 = cv2.imread(r'img/attack2/temp_img.jpg')
            img_rgb_attack2 = cv2.cvtColor(img_cv_attack2, cv2.COLOR_BGR2RGB)
            ATTACK2_DATA = pytesseract.image_to_string(img_rgb_attack2, config=custom_config)
            #ocr attack3
            picture_inAttack_3 = frame[913:943, 1382:1642]
            cv2.imwrite('img/attack3/temp_img.jpg', picture_inAttack_3)
            img_cv_attack3 = cv2.imread(r'img/attack3/temp_img.jpg')
            img_rgb_attack3 = cv2.cvtColor(img_cv_attack3, cv2.COLOR_BGR2RGB)
            ATTACK3_DATA = pytesseract.image_to_string(img_rgb_attack3, config=custom_config)
            #ocr attack4
            picture_inAttack_4 = frame[1018:1048, 1382:1642]
            cv2.imwrite('img/attack4/temp_img.jpg', picture_inAttack_4)
            img_cv_attack4 = cv2.imread(r'img/attack4/temp_img.jpg')
            img_rgb_attack4 = cv2.cvtColor(img_cv_attack4, cv2.COLOR_BGR2RGB)
            ATTACK4_DATA = pytesseract.image_to_string(img_rgb_attack4, config=custom_config)

            #check attack data
            def check_pattern1(s):
                global ATTACK1_DATA_OCR
                global Attack_1
                if re.match("Se[a-z]+", s):
                    print("Attack 1: Sehr Effektiv")
                    ATTACK1_DATA_OCR = "Sehr Effektiv"
                    Attack_1 = 4
                elif re.match("Ef[a-z]+", s):
                    print("Attack 1: Effektiv")
                    ATTACK1_DATA_OCR = "Effektiv"
                    Attack_1 = 3
                elif re.match("Ni[a-z]+", s):
                    print("Attack 1: Nicht Effektiv")
                    ATTACK1_DATA_OCR = "Nicht Effektiv"
                    Attack_1 = 2
                elif re.match("Wirkungslos+", s):
                    print("Attack 1: Wirkungslos")
                    ATTACK1_DATA_OCR = "Wirkungslos"
                else:
                    print("No Attack Data Found")
                    ATTACK1_DATA_OCR = "unknown"

            def check_pattern2(s):
                global ATTACK2_DATA_OCR
                global Attack_2
                if re.match("Se[a-z]+", s):
                    print("Attack 2: Sehr Effektiv")
                    ATTACK2_DATA_OCR = "Sehr Effektiv"
                    Attack_2 = 4
                elif re.match("Ef[a-z]+", s):
                    print("Attack 2: Effektiv")
                    ATTACK2_DATA_OCR = "Effektiv"
                    Attack_2 = 3
                elif re.match("Ni[a-z]+", s):
                    print("Attack 2: Nicht Effektiv")
                    ATTACK2_DATA_OCR = "Nicht Effektiv"
                    Attack_2 = 2
                elif re.match("Wirkungslos+", s):
                    print("Attack 2: Wirkungslos")
                    ATTACK2_DATA_OCR = "Wirkungslos"
                else:
                    print("No Attack Data Found")
                    ATTACK2_DATA_OCR = "unknown"

            def check_pattern3(s):
                global ATTACK3_DATA_OCR
                global Attack_3
                if re.match("Se[a-z]+", s):
                    print("Attack 3: Sehr Effektiv")
                    ATTACK3_DATA_OCR = "Sehr Effektiv"
                    Attack_3 = 4
                elif re.match("Ef[a-z]+", s):
                    print("Attack 3: Effektiv")
                    ATTACK3_DATA_OCR = "Effektiv"
                    Attack_3 = 3
                elif re.match("Ni[a-z]+", s):
                    print("Attack 3: Nicht Effektiv")
                    ATTACK3_DATA_OCR = "Nicht Effektiv"
                    Attack_3 = 2
                elif re.match("Wirkungslos+", s):
                    print("Attack 3: Wirkungslos")
                    ATTACK3_DATA_OCR = "Wirkungslos"
                else:
                    print("No Attack Data Found")
                    ATTACK3_DATA_OCR = "unknown"

            def check_pattern4(s):
                global ATTACK4_DATA_OCR
                global Attack_4
                if re.match("Se[a-z]+", s):
                    print("Attack 4: Sehr Effektiv")
                    ATTACK4_DATA_OCR = "Sehr Effektiv"
                    Attack_4 = 4
                elif re.match("Ef[a-z]+", s):
                    print("Attack 4: Effektiv")
                    ATTACK4_DATA_OCR = "Effektiv"
                    Attack_4 = 3
                elif re.match("Ni[a-z]+", s):
                    print("Attack 4: Nicht Effektiv")
                    ATTACK4_DATA_OCR = "Nicht Effektiv"
                    Attack_4 = 2
                elif re.match("Wirkungslos+", s):
                    print("Attack 4: Wirkungslos")
                    ATTACK4_DATA_OCR = "Wirkungslos"
                else:
                    print("No Attack Data Found")
                    ATTACK4_DATA_OCR = "unknown"

            check_pattern1(ATTACK1_DATA)
            check_pattern2(ATTACK2_DATA)
            check_pattern3(ATTACK3_DATA)
            check_pattern4(ATTACK4_DATA)
            self.gcvdata[ATTACK_OFFSET] = True

            if Attack_Selection == 0:
                if Attack_1 == 4 or Attack_2 == 4 or Attack_3 == 4 or Attack_4 == 4:
                    Attack_Selection = 4
                elif Attack_1 == 3 or Attack_2 == 3 or Attack_3 == 3 or Attack_4 == 3:
                    Attack_Selection = 3
                elif Attack_1 == 2 or Attack_2 == 2 or Attack_3 == 2 or Attack_4 == 2:
                    Attack_Selection = 2

            if Attack_1_Setup == 4 and Attack_Selection == 4:
                if Attack_1 == 4:
                    self.gcvdata[ATTACK1_SE_OFFSET] = True
                elif Attack_2_Setup == 3:
                    if Attack_2 == 4:
                        self.gcvdata[ATTACK2_SE_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 4:
                            self.gcvdata[ATTACK3_SE_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 4:
                                self.gcvdata[ATTACK4_SE_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 4:
                            self.gcvdata[ATTACK4_SE_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 4:
                                self.gcvdata[ATTACK3_SE_OFFSET] = True
                elif Attack_3_Setup == 3:
                    if Attack_3 == 4:
                        self.gcvdata[ATTACK3_SE_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 4:
                            self.gcvdata[ATTACK2_SE_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 4:
                                self.gcvdata[ATTACK4_SE_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 4:
                            self.gcvdata[ATTACK4_SE_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 4:
                                self.gcvdata[ATTACK2_SE_OFFSET] = True
                elif Attack_4_Setup == 3:
                    if Attack_4 == 4:
                        self.gcvdata[ATTACK4_SE_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 4:
                            self.gcvdata[ATTACK2_SE_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 4:
                                self.gcvdata[ATTACK3_SE_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 4:
                            self.gcvdata[ATTACK3_SE_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 4:
                                self.gcvdata[ATTACK2_SE_OFFSET] = True
            elif Attack_2_Setup == 4 and Attack_Selection == 4:
                if Attack_2 == 4:
                    self.gcvdata[ATTACK2_SE_OFFSET] = True
                elif Attack_1_Setup == 3:
                    if Attack_1 == 4:
                        self.gcvdata[ATTACK1_SE_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 4:
                            self.gcvdata[ATTACK3_SE_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 4:
                                self.gcvdata[ATTACK4_SE_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 4:
                            self.gcvdata[ATTACK4_SE_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 4:
                                self.gcvdata[ATTACK3_SE_OFFSET] = True
                elif Attack_3_Setup == 3:
                    if Attack_3 == 4:
                        self.gcvdata[ATTACK3_SE_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 4:
                            self.gcvdata[ATTACK1_SE_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 4:
                                self.gcvdata[ATTACK4_SE_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 4:
                            self.gcvdata[ATTACK4_SE_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 4:
                                self.gcvdata[ATTACK1_SE_OFFSET] = True
                elif Attack_4_Setup == 3:
                    if Attack_4 == 4:
                        self.gcvdata[ATTACK4_SE_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 4:
                            self.gcvdata[ATTACK1_SE_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 4:
                                self.gcvdata[ATTACK3_SE_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 4:
                            self.gcvdata[ATTACK3_SE_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 4:
                                self.gcvdata[ATTACK1_SE_OFFSET] = True
            elif Attack_3_Setup == 4 and Attack_Selection == 4:
                if Attack_3 == 4:
                    self.gcvdata[ATTACK3_SE_OFFSET] = True
                elif Attack_1_Setup == 3:
                    if Attack_1 == 4:
                        self.gcvdata[ATTACK1_SE_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 4:
                            self.gcvdata[ATTACK2_SE_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 4:
                                self.gcvdata[ATTACK4_SE_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 4:
                            self.gcvdata[ATTACK4_SE_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 4:
                                self.gcvdata[ATTACK2_SE_OFFSET] = True
                elif Attack_2_Setup == 3:
                    if Attack_2 == 4:
                        self.gcvdata[ATTACK2_SE_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 4:
                            self.gcvdata[ATTACK1_SE_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 4:
                                self.gcvdata[ATTACK4_SE_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 4:
                            self.gcvdata[ATTACK4_SE_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 4:
                                self.gcvdata[ATTACK1_SE_OFFSET] = True
                elif Attack_4_Setup == 3:
                    if Attack_4 == 4:
                        self.gcvdata[ATTACK4_SE_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 4:
                            self.gcvdata[ATTACK1_SE_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 4:
                                self.gcvdata[ATTACK2_SE_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 4:
                            self.gcvdata[ATTACK2_SE_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 4:
                                self.gcvdata[ATTACK1_SE_OFFSET] = True
            elif Attack_4_Setup == 4 and Attack_Selection == 4:
                if Attack_4 == 4:
                    self.gcvdata[ATTACK4_SE_OFFSET] = True
                elif Attack_1_Setup == 3:
                    if Attack_1 == 4:
                        self.gcvdata[ATTACK1_SE_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 4:
                            self.gcvdata[ATTACK2_SE_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 4:
                                self.gcvdata[ATTACK3_SE_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 4:
                            self.gcvdata[ATTACK3_SE_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 4:
                                self.gcvdata[ATTACK2_SE_OFFSET] = True
                elif Attack_2_Setup == 3:
                    if Attack_2 == 4:
                        self.gcvdata[ATTACK2_SE_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 4:
                            self.gcvdata[ATTACK1_SE_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 4:
                                self.gcvdata[ATTACK3_SE_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 4:
                            self.gcvdata[ATTACK3_SE_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 4:
                                self.gcvdata[ATTACK1_SE_OFFSET] = True
                elif Attack_3_Setup == 3:
                    if Attack_3 == 4:
                        self.gcvdata[ATTACK3_SE_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 4:
                            self.gcvdata[ATTACK1_SE_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 4:
                                self.gcvdata[ATTACK2_SE_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 4:
                            self.gcvdata[ATTACK2_SE_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 4:
                                self.gcvdata[ATTACK1_SE_OFFSET] = True
            #####
            if Attack_1_Setup == 4 and Attack_Selection == 3:
                if Attack_1 == 3:
                    self.gcvdata[ATTACK1_EF_OFFSET] = True
                elif Attack_2_Setup == 3:
                    if Attack_2 == 3:
                        self.gcvdata[ATTACK2_EF_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 3:
                            self.gcvdata[ATTACK3_EF_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 3:
                                self.gcvdata[ATTACK4_EF_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 3:
                            self.gcvdata[ATTACK4_EF_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 3:
                                self.gcvdata[ATTACK3_EF_OFFSET] = True
                elif Attack_3_Setup == 3:
                    if Attack_3 == 3:
                        self.gcvdata[ATTACK3_EF_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 3:
                            self.gcvdata[ATTACK2_EF_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 3:
                                self.gcvdata[ATTACK4_EF_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 3:
                            self.gcvdata[ATTACK4_EF_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 3:
                                self.gcvdata[ATTACK2_EF_OFFSET] = True
                elif Attack_4_Setup == 3:
                    if Attack_4 == 3:
                        self.gcvdata[ATTACK4_EF_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 3:
                            self.gcvdata[ATTACK2_EF_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 3:
                                self.gcvdata[ATTACK3_EF_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 3:
                            self.gcvdata[ATTACK3_EF_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 3:
                                self.gcvdata[ATTACK2_EF_OFFSET] = True
            elif Attack_2_Setup == 4 and Attack_Selection == 3:
                if Attack_2 == 3:
                    self.gcvdata[ATTACK2_EF_OFFSET] = True
                elif Attack_1_Setup == 3:
                    if Attack_1 == 3:
                        self.gcvdata[ATTACK1_EF_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 3:
                            self.gcvdata[ATTACK3_EF_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 3:
                                self.gcvdata[ATTACK4_EF_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 3:
                            self.gcvdata[ATTACK4_EF_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 3:
                                self.gcvdata[ATTACK3_EF_OFFSET] = True
                elif Attack_3_Setup == 3:
                    if Attack_3 == 3:
                        self.gcvdata[ATTACK3_EF_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 3:
                            self.gcvdata[ATTACK1_EF_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 3:
                                self.gcvdata[ATTACK4_EF_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 3:
                            self.gcvdata[ATTACK4_EF_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 3:
                                self.gcvdata[ATTACK1_EF_OFFSET] = True
                elif Attack_4_Setup == 3:
                    if Attack_4 == 3:
                        self.gcvdata[ATTACK4_EF_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 3:
                            self.gcvdata[ATTACK1_EF_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 3:
                                self.gcvdata[ATTACK3_EF_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 3:
                            self.gcvdata[ATTACK3_EF_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 3:
                                self.gcvdata[ATTACK1_EF_OFFSET] = True
            elif Attack_3_Setup == 4 and Attack_Selection == 3:
                if Attack_3 == 3:
                    self.gcvdata[ATTACK3_EF_OFFSET] = True
                elif Attack_1_Setup == 3:
                    if Attack_1 == 3:
                        self.gcvdata[ATTACK1_EF_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 3:
                            self.gcvdata[ATTACK2_EF_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 3:
                                self.gcvdata[ATTACK4_EF_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 3:
                            self.gcvdata[ATTACK4_EF_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 3:
                                self.gcvdata[ATTACK2_EF_OFFSET] = True
                elif Attack_2_Setup == 3:
                    if Attack_2 == 3:
                        self.gcvdata[ATTACK2_EF_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 3:
                            self.gcvdata[ATTACK1_EF_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 3:
                                self.gcvdata[ATTACK4_EF_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 3:
                            self.gcvdata[ATTACK4_EF_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 3:
                                self.gcvdata[ATTACK1_EF_OFFSET] = True
                elif Attack_4_Setup == 3:
                    if Attack_4 == 3:
                        self.gcvdata[ATTACK4_EF_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 3:
                            self.gcvdata[ATTACK1_EF_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 3:
                                self.gcvdata[ATTACK2_EF_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 3:
                            self.gcvdata[ATTACK2_EF_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 3:
                                self.gcvdata[ATTACK1_EF_OFFSET] = True
            elif Attack_4_Setup == 4 and Attack_Selection == 3:
                if Attack_4 == 3:
                    self.gcvdata[ATTACK4_EF_OFFSET] = True
                elif Attack_1_Setup == 3:
                    if Attack_1 == 3:
                        self.gcvdata[ATTACK1_EF_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 3:
                            self.gcvdata[ATTACK2_EF_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 3:
                                self.gcvdata[ATTACK3_EF_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 3:
                            self.gcvdata[ATTACK3_EF_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 3:
                                self.gcvdata[ATTACK2_EF_OFFSET] = True
                elif Attack_2_Setup == 3:
                    if Attack_2 == 3:
                        self.gcvdata[ATTACK2_EF_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 3:
                            self.gcvdata[ATTACK1_EF_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 3:
                                self.gcvdata[ATTACK3_EF_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 3:
                            self.gcvdata[ATTACK3_EF_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 3:
                                self.gcvdata[ATTACK1_EF_OFFSET] = True
                elif Attack_3_Setup == 3:
                    if Attack_3 == 3:
                        self.gcvdata[ATTACK3_EF_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 3:
                            self.gcvdata[ATTACK1_EF_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 3:
                                self.gcvdata[ATTACK2_EF_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 3:
                            self.gcvdata[ATTACK2_EF_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 3:
                                self.gcvdata[ATTACK1_EF_OFFSET] = True
            #####
            if Attack_1_Setup == 4 and Attack_Selection == 2:
                if Attack_1 == 2:
                    self.gcvdata[ATTACK1_NE_OFFSET] = True
                elif Attack_2_Setup == 3:
                    if Attack_2 == 2:
                        self.gcvdata[ATTACK2_NE_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 2:
                            self.gcvdata[ATTACK3_NE_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 2:
                                self.gcvdata[ATTACK4_NE_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 2:
                            self.gcvdata[ATTACK4_NE_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 2:
                                self.gcvdata[ATTACK3_NE_OFFSET] = True
                elif Attack_3_Setup == 3:
                    if Attack_3 == 2:
                        self.gcvdata[ATTACK3_NE_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 2:
                            self.gcvdata[ATTACK2_NE_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 2:
                                self.gcvdata[ATTACK4_NE_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 2:
                            self.gcvdata[ATTACK4_NE_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 2:
                                self.gcvdata[ATTACK2_NE_OFFSET] = True
                elif Attack_4_Setup == 3:
                    if Attack_4 == 2:
                        self.gcvdata[ATTACK4_NE_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 2:
                            self.gcvdata[ATTACK2_NE_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 2:
                                self.gcvdata[ATTACK3_NE_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 2:
                            self.gcvdata[ATTACK3_NE_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 2:
                                self.gcvdata[ATTACK2_NE_OFFSET] = True
            elif Attack_2_Setup == 4 and Attack_Selection == 2:
                if Attack_2 == 2:
                    self.gcvdata[ATTACK2_NE_OFFSET] = True
                elif Attack_1_Setup == 3:
                    if Attack_1 == 2:
                        self.gcvdata[ATTACK1_NE_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 2:
                            self.gcvdata[ATTACK3_NE_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 2:
                                self.gcvdata[ATTACK4_NE_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 2:
                            self.gcvdata[ATTACK4_NE_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 2:
                                self.gcvdata[ATTACK3_NE_OFFSET] = True
                elif Attack_3_Setup == 3:
                    if Attack_3 == 2:
                        self.gcvdata[ATTACK3_NE_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 2:
                            self.gcvdata[ATTACK1_NE_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 2:
                                self.gcvdata[ATTACK4_NE_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 2:
                            self.gcvdata[ATTACK4_NE_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 2:
                                self.gcvdata[ATTACK1_NE_OFFSET] = True
                elif Attack_4_Setup == 3:
                    if Attack_4 == 2:
                        self.gcvdata[ATTACK4_NE_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 2:
                            self.gcvdata[ATTACK1_NE_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 2:
                                self.gcvdata[ATTACK3_NE_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 2:
                            self.gcvdata[ATTACK3_NE_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 2:
                                self.gcvdata[ATTACK1_NE_OFFSET] = True
            elif Attack_3_Setup == 4 and Attack_Selection == 2:
                if Attack_3 == 2:
                    self.gcvdata[ATTACK3_NE_OFFSET] = True
                elif Attack_1_Setup == 3:
                    if Attack_1 == 2:
                        self.gcvdata[ATTACK1_NE_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 2:
                            self.gcvdata[ATTACK2_NE_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 2:
                                self.gcvdata[ATTACK4_NE_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 2:
                            self.gcvdata[ATTACK4_NE_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 2:
                                self.gcvdata[ATTACK2_NE_OFFSET] = True
                elif Attack_2_Setup == 3:
                    if Attack_2 == 2:
                        self.gcvdata[ATTACK2_NE_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 2:
                            self.gcvdata[ATTACK1_NE_OFFSET] = True
                        elif Attack_4_Setup == 1:
                            if Attack_4 == 2:
                                self.gcvdata[ATTACK4_NE_OFFSET] = True
                    elif Attack_4_Setup == 2:
                        if Attack_4 == 2:
                            self.gcvdata[ATTACK4_NE_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 2:
                                self.gcvdata[ATTACK1_NE_OFFSET] = True
                elif Attack_4_Setup == 3:
                    if Attack_4 == 2:
                        self.gcvdata[ATTACK4_NE_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 2:
                            self.gcvdata[ATTACK1_NE_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 2:
                                self.gcvdata[ATTACK2_NE_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 2:
                            self.gcvdata[ATTACK2_NE_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 2:
                                self.gcvdata[ATTACK1_NE_OFFSET] = True
            elif Attack_4_Setup == 4 and Attack_Selection == 2:
                if Attack_4 == 2:
                    self.gcvdata[ATTACK4_NE_OFFSET] = True
                elif Attack_1_Setup == 3:
                    if Attack_1 == 2:
                        self.gcvdata[ATTACK1_NE_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 2:
                            self.gcvdata[ATTACK2_NE_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 2:
                                self.gcvdata[ATTACK3_NE_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 2:
                            self.gcvdata[ATTACK3_NE_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 2:
                                self.gcvdata[ATTACK2_NE_OFFSET] = True
                elif Attack_2_Setup == 3:
                    if Attack_2 == 2:
                        self.gcvdata[ATTACK2_NE_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 2:
                            self.gcvdata[ATTACK1_NE_OFFSET] = True
                        elif Attack_3_Setup == 1:
                            if Attack_3 == 2:
                                self.gcvdata[ATTACK3_NE_OFFSET] = True
                    elif Attack_3_Setup == 2:
                        if Attack_3 == 2:
                            self.gcvdata[ATTACK3_NE_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 2:
                                self.gcvdata[ATTACK1_NE_OFFSET] = True
                elif Attack_3_Setup == 3:
                    if Attack_3 == 2:
                        self.gcvdata[ATTACK3_NE_OFFSET] = True
                    elif Attack_1_Setup == 2:
                        if Attack_1 == 2:
                            self.gcvdata[ATTACK1_NE_OFFSET] = True
                        elif Attack_2_Setup == 1:
                            if Attack_2 == 2:
                                self.gcvdata[ATTACK2_NE_OFFSET] = True
                    elif Attack_2_Setup == 2:
                        if Attack_2 == 2:
                            self.gcvdata[ATTACK2_NE_OFFSET] = True
                        elif Attack_1_Setup == 1:
                            if Attack_1 == 2:
                                self.gcvdata[ATTACK1_NE_OFFSET] = True

        elif similar_inAttack == ATTACK_DATASET:
            pass
        else:
            self.inAttack = True
            inAttack = 0
            self.gcvdata[ATTACK_OFFSET] = False
            Attack_1 = 0
            Attack_2 = 0
            Attack_3 = 0
            Attack_4 = 0
            Attack_Selection = 0
            self.gcvdata[ATTACK1_SE_OFFSET] = False
            self.gcvdata[ATTACK1_EF_OFFSET] = False
            self.gcvdata[ATTACK1_NE_OFFSET] = False
            self.gcvdata[ATTACK2_SE_OFFSET] = False
            self.gcvdata[ATTACK2_EF_OFFSET] = False
            self.gcvdata[ATTACK2_NE_OFFSET] = False
            self.gcvdata[ATTACK3_SE_OFFSET] = False
            self.gcvdata[ATTACK3_EF_OFFSET] = False
            self.gcvdata[ATTACK3_NE_OFFSET] = False
            self.gcvdata[ATTACK4_SE_OFFSET] = False
            self.gcvdata[ATTACK4_EF_OFFSET] = False
            self.gcvdata[ATTACK4_NE_OFFSET] = False

        return frame, self.gcvdata
