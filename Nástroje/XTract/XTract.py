import time
import xlwt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import hashlib 

website_url = input("Jmeno FB stranky pro scrappovani (priklad: https://www.facebook.com/Blesk.cz/): ")

# Nastavení chromu pro vypnutí upozornění požadavku na zasílání notifikací
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

# Spuštění prohlížeče
browser = webdriver.Chrome("C:/Users/[ADRESA ZDE]/chromedriver.exe",chrome_options=chrome_options)

browser.maximize_window()

print("Spuštění prohlížeče....")

# Otevření login stránky
browser.get('https://www.facebook.com/')
assert 'Facebook' in browser.title

time.sleep(3)

# Přihlášení
accept_button_cookies = browser.find_element_by_xpath('//*[@title="Přijmout vše"]').click()

print("Cookies přijaty...")
print("Přihlašování...")
# Username
userElem = browser.find_element_by_id("email")
userElem.send_keys('[PRIHLASOVACI JMENO ZDE]')
print("Uživatelský email.... OK")

# Password
passwordElem = browser.find_element_by_id("pass")
passwordElem.send_keys('[HESLO ZDE]')
print("Heslo.... OK")

# Login
loged_in = browser.find_element_by_xpath("//button[@class='_42ft _4jy0 _6lth _4jy6 _4jy1 selected _51sy']").click()

print("Úspěšně přihlášeno.... OK")

time.sleep(2)

# Otevření požadované stránky
browser.get(website_url)

time.sleep(3)

SCROLL_PAUSE_TIME = 3

# Navrátí aktuální výšku okna
last_height = browser.execute_script("return document.body.scrollHeight")


# O kolik obrazovek se má robot posunout na základě požadovaného počtu příspěvků (nastavitelný parametr)
for x in range(2):
    # Scrollnutí obrazovky na spodek s ohledem na aktuální velikost obrazovky
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Zastavení pohybu pro načtení načtení stránky (kvůli lazy-loading technice na novém FB layoutu)
    time.sleep(SCROLL_PAUSE_TIME)

    print("Načítám požadované množství příspěvků....")

    if x > 10:
        SCROLL_PAUSE_TIME = 5

    # Vytvoření nové výšky pro scroll a porovnání se starou výškou
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Vytvoření nového excel dokumentu a sheetu uvnitř něj
wb = xlwt.Workbook()
sheet1 = wb.add_sheet('Data')


# Vyscrollovaní zpět na hořejšek stránky (opět kvůli lazy-loadingu)
browser.execute_script("window.scrollTo(0, 0);")

# Rozbalení komentářů a posun okna do pozice komentáře
expand_comments = browser.find_elements_by_xpath("//span[@class='j83agx80 fv0vnmcu hpfvmrgz']")
i = 0
for expand in expand_comments:
    if expand.text == "":
        print("Prázdné")
        browser.execute_script("window.scrollBy(0, 1080);")
        time.sleep(3)
        if i < 3:
            print("Odkaz nenalezen, počet zbývajících obnovení existujících expanzí komentářů:")
            print(3-i)
            expand_comments = browser.find_elements_by_xpath("//span[@class='j83agx80 fv0vnmcu hpfvmrgz']")
            i += 1
    else:
        print("Lokace rozbalovacího tlačítka:")
        print(expand.location)
        print(expand.text)
        browser.execute_script("arguments[0].scrollIntoView();", expand)
        time.sleep(1)
        browser.execute_script("arguments[0].click();", expand)
        time.sleep(1)
        print("Komentáře rozbaleny....")
        time.sleep(1)

print("Zapisuji jména do souboru Data.xlsx")

browser.execute_script("window.scrollTo(0, 0);")
time.sleep(8)

# Zápis vizualně viditelných jmen do excel souboru a ošetření chyb, aby se program nezavřel
all_people = browser.find_elements_by_xpath("//div[@class='b3i9ofy5 e72ty7fz qlfml3jp inkptoze qmr60zad rq0escxv oo9gr5id q9uorilb kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x d2edcug0 jm1wdb64 l9j0dhe7 l3itjdph qv66sw1b']")
for names in all_people:
    if names.text == "":
        print("Nenalezeno jméno, přeskočeno")
    else:
        index = all_people.index(names)
        browser.execute_script("arguments[0].scrollIntoView();", names)

        names.get_attribute('innerHTML')
        
        print(names.text)
        commentator = all_people[index]
        comment = commentator.text

        time.sleep(0.1)

        name = names.text.splitlines( )
        #print(name)       tohle je cela bunka komentare vcetne jmena a komentu
        if "Přední fanoušek" in name[0]:
            name.remove('Přední fanoušek')
            sheet1.write(index, 3, "přední fanoušek")

        firstname = name[0].strip().split(' ')[0]
        lastname = ' '.join((name[0] + ' ').split(' ')[1:]).strip()

        hash_lastname = hashlib.md5(lastname.encode())
        hex_lastname = hash_lastname.hexdigest()

        comment_no_firstname = comment.replace(firstname, '')
        comment_no_lastname = comment_no_firstname.replace(lastname, '')
        comment_clean = comment_no_lastname.replace('Přední fanoušek', '')

        
        parent = names.find_element_by_xpath('./../../../../../../../../../../../../../../../../../../../../..')

        try:
            article_link = parent.find_element_by_xpath(".//a[@class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 datstx6m k4urcfbm']")
            titulek = article_link.find_element_by_xpath(".//img[@class='i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm bixrwtb6']")
        except NoSuchElementException:
            # Just append a None or ""
            print("chyba")
        

        if lastname.endswith(('ova', 'ová', 'á', 'a')):
            pohlavi = "žena"
        else:
            pohlavi = "muž"
        
        sheet1.write(index, 0, firstname)
        sheet1.write(index, 1, hex_lastname)
        sheet1.write(index, 4, comment_clean)
        sheet1.write(index, 5, len(comment_clean)-2)
        try:
            sheet1.write(index, 7, article_link.get_attribute("href"))
        except:
            sheet1.write(index, 7, "Stream")
        try:
            sheet1.write(index, 6, titulek.get_attribute("alt"))
        except:
            sheet1.write(index, 6, "Stream")
        sheet1.write(index, 2, pohlavi)

        #formula=f'IF(OR((RIGHT(TRIM(B{index+1}),1)="a"),(RIGHT(TRIM(B{index+1}),1)="á")),"žena","muž")' #=KDYŽ(NEBO((ZPRAVA(PROČISTIT(B2);1)="a");(ZPRAVA(PROČISTIT(B2);1)="á"));"žena";"muž")
        #sheet1.write(index, 2, xlwt.Formula(formula))

print("Ukládám výsledky")

# Uložení výsledků a terminace programu   
wb.save('NEWEST_DATA.xls')
time.sleep(5)
print("Uloženo, bye bye")
