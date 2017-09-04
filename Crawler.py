import sys, os, time, sqlite3
import urllib, http.cookiejar
import re
from bs4 import BeautifulSoup
def verify(account, passwd):
    postData = {
        'user': account,
        'pass': passwd,
        'inputCode': '1234',
        'url': 'http://my.zust.edu.cn/login',
    }
    headers = {
        'Host': 'ez.zust.edu.cn',
        'Origin': 'https://ez.zust.edu.cn',
        'Referer': 'https://ez.zust.edu.cn/login?url=http://my.zust.edu.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    data = urllib.parse.urlencode(postData).encode(encoding='utf-8')
    request = urllib.request.Request('https://ez.zust.edu.cn/login', data, headers)
    response = opener.open(request)
    result = response.read().decode('utf-8', 'ignore')
    pattern1 = r'<DIV id="errmsg".*?>(.*?)</DIV>'
    pattern2 = r'<td><li>(.*?)</li></td>'
    match1 = re.search(pattern1, result)
    match2 = re.search(pattern2, result)
    if match1 or match2:
        if match1:
            return match1.group(1)
        else:
            return match2.group(1)
    return True
def login(info):
    postData = {
        'user': info['username'],
        'pass': info['password'],
        'inputCode': '1234',
        'url': 'http://my.zust.edu.cn/login',
    }
    headers = {
        'Host': 'ez.zust.edu.cn',
        'Origin': 'https://ez.zust.edu.cn',
        'Referer': 'https://ez.zust.edu.cn/login?url=http://my.zust.edu.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    data = urllib.parse.urlencode(postData).encode(encoding='utf-8')
    request = urllib.request.Request('https://ez.zust.edu.cn/login', data, headers)
    response = opener.open(request)
    result = response.read().decode('utf-8', 'ignore')
    pattern = r'<DIV id="errmsg".*?>(.*?)</DIV>'
    match = re.search(pattern, result)
    if match:
        print(match.group(1))
        return False
    return result
def loginZHFW(info):
    postData = {
        'Login.Token1': info['username'],
        'Login.Token2': info['password'],
        'captcha': '',
        'goto': 'http://my.zust.edu.cn.ez.zust.edu.cn/loginSuccess.portal',
        'gotoOnFail': 'http://my.zust.edu.cn.ez.zust.edu.cn/loginFailure.portal',
    }
    headers = {
        'Host': 'my.zust.edu.cn.ez.zust.edu.cn',
        'Origin': 'http://my.zust.edu.cn.ez.zust.edu.cn',
        'Referer': 'http://my.zust.edu.cn.ez.zust.edu.cn/login.portal',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    data = urllib.parse.urlencode(postData).encode(encoding='utf-8')
    request = urllib.request.Request('http://my.zust.edu.cn.ez.zust.edu.cn/userPasswordValidate.portal', data, headers)
    response = opener.open(request)
def loginJWXT():
    response = opener.open('http://jwxt.zust.edu.cn.ez.zust.edu.cn/default_zzjk.aspx')
    result = response.read().decode('utf-8')
    pattern_info = r'<span id="xhxm">\d*\s*(\w*?)\w\w</span>'
    match = re.search(pattern_info, result)
    return urllib.parse.quote(str(match.group(1)))
def getGradePage(urlName):
    url_cjcx = 'http://jwxt.zust.edu.cn.ez.zust.edu.cn/xscj_gc.aspx?xh=' + info[
        'username'] + '&xm=' + urlName + '&gnmkdm=N121616'
    headers = {
        'Host': 'jwxt.zust.edu.cn.ez.zust.edu.cn',
        'Referer': 'http://jwxt.zust.edu.cn.ez.zust.edu.cn/xs_main.aspx?xh=' + info['username'],
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    request = urllib.request.Request(url_cjcx, headers=headers)
    response = opener.open(request)
    result = response.read().decode()
    pattern_viewstate = r'<input type="hidden" name="__VIEWSTATE" value="(.*?)"'
    viewstate = re.search(pattern_viewstate, result).group(1)

    postData_cjcx = {
        '__VIEWSTATE': viewstate,
        'ddlXN': year,
        'ddlXQ': term,
        'Button1': '按学期查询',
    }
    headers_cjcx = {
        'Host': 'jwxt.zust.edu.cn.ez.zust.edu.cn',
        'Origin': 'http://jwxt.zust.edu.cn.ez.zust.edu.cn',
        'Referer': url_cjcx,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    data_cjcx = urllib.parse.urlencode(postData_cjcx).encode()
    request_cjcx = urllib.request.Request(url_cjcx, data_cjcx, headers_cjcx)
    response = opener.open(request_cjcx)
    return response.read().decode('utf-8')
def parseGradesPage(result_cjcx):
    pattern_table = r'<table class="datelist" cellspacing="0" cellpadding="3" border="0" id="Datagrid1" width="100%">(.*?)</table>'
    # pattern_tableHead = r'<tr class="datelisthead">(.*?)</tr>'
    pattern_subjectItem = r'(?:<tr>|<tr class="alt">)(.*?)</tr>'
    pattern_subjectInfo = r'<td>(.*?)</td>'

    table = re.search(pattern_table, result_cjcx, re.DOTALL).group()
    # tableHead = re.search(pattern_tableHead, table, re.DOTALL).group()
    subjectList = list()
    table = re.sub(r'&nbsp;', ' ', table)
    for item in re.findall(pattern_subjectItem, table, re.DOTALL):
        subjectList.append(re.findall(pattern_subjectInfo, item))
    return subjectList
def getGrade(urlName):
    gradePage = getGradePage(urlName)
    subjectList = parseGradesPage(gradePage)
    return subjectList
def getCardInfo():
    opener.open('http://ecard.zust.edu.cn.ez.zust.edu.cn/zghyportalHome.action', timeout=30)
    headers = {
        'Host': 'ecard.zust.edu.cn.ez.zust.edu.cn',
        'Referer': 'http://ecard.zust.edu.cn.ez.zust.edu.cn/accleftframe.action',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    request = urllib.request.Request('http://ecard.zust.edu.cn.ez.zust.edu.cn/accountcardUser.action', headers=headers)
    response = opener.open(request)
    result = response.read().decode('utf-8', 'ignore')
    pattern = r'余&nbsp;&nbsp;&nbsp;&nbsp;额.*?<td class="neiwen">(.*?)</td>'
    match = re.search(pattern, result, re.DOTALL)
    return match.group(1)
def getLibraryInfo():
    opener.open('http://my.lib.zust.edu.cn.ez.zust.edu.cn/idstar.aspx', timeout=30)
    headers = {
        'Host': 'my.lib.zust.edu.cn.ez.zust.edu.cn',
        'Referer': 'http://my.lib.zust.edu.cn.ez.zust.edu.cn/Borrowing.aspx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    request = urllib.request.Request('http://my.lib.zust.edu.cn.ez.zust.edu.cn/Borrowing.aspx', headers=headers)
    response = opener.open(request)
    result = response.read().decode('utf8')
    soup = BeautifulSoup(result, 'html.parser')
    table = str(soup.find('table', id="ctl00_ContentPlaceHolder1_GridView1"))
    pattern = r'<table.*?<a.*?>(.*?)<.*?借书时间.*?>(.*?)<.*?应还日期.*?>(.*?)<.*?续借次数.*?>(.*?)<.*?超期情况.*?>(.*?)<.*?</table>'
    match = re.findall(pattern, table, re.DOTALL)
    return match
def invoke(openid, account, passwd):
    db_path = 'info.db'
    conn = sqlite3.connect(db_path)
    conn.text_factory = str
    cursor = conn.cursor()
    info['username'] = account
    info['password'] = passwd
    login(info)
    loginZHFW(info)

    # '成绩':
    try:
        urlName = loginJWXT()
        subjectList = getGrade(urlName)
        cursor.execute('delete from grade where account=?',(account,))
        for subject in subjectList:
            cursor.execute('insert into grade values(?,?,?,?,?)',(account, subject[3], subject[6], subject[7], subject[8]))
    except:
        pass

    # '图书馆':
    bookList = getLibraryInfo()
    cursor.execute('delete from library where account=?', (account,))
    for book in bookList:
        cursor.execute('insert into library values(?,?,?,?,?,?)',(account, book[0], book[1], book[2], book[3], book[4]))

    # '一卡通':
    try:
        card = getCardInfo()
    except:
        card = '一卡通查询失败'
    cursor.execute('delete from user where openid=?', (openid,))
    cursor.execute('insert into user (openid,account,passwd,card,update_time,is_valid) values (?,?,?,?,?,?)',(openid, account, passwd, card,time.strftime('%Y-%m-%d-%H-%M',time.localtime(time.time())) ,'True'))
    cursor.close()
    conn.commit()
    conn.close()

cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
year = '2016-2017'
term = '2'
urlName = ''
info = dict()