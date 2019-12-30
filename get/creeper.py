# -*- coding: utf-8 -*-

import requests, math, os.path, re
from bs4 import BeautifulSoup
        
# 模拟登陆的方法
def login():
    # 登录的用户名
    username = '老潘家的潘老师'
    # 登录的密码
    password = 'divertingPan'
    # 登录所需的参数
    login_data = {
            'username': username,
            'password': password,
            'u': 'https://passport.baidu.com',
            'tpl': 'pp',
            'staticpage': 'https://passport.baidu.com/static/passpc-account/html/v3Jump.html',
            'isPhone': 'false',
            'charset': 'utf-8',
            'callback': 'parent.bd_pcbs_ra48vi'
            }
    # 构造所需的headers
    headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36"
            }
    # 登录的url
    baidu_loginurl = "https://passport.baidu.com/v2/api/?login"
    # 创建session
    session = requests.session()
    # 模拟登陆
    session.post(baidu_loginurl, login_data, headers=headers)
    # 创建session
    return session

# 获取总页数的方法
def get_total_page(url, session):
    # 获取网页内容
    res = session.get(url)
    # 解析出帖子总数
    soup = BeautifulSoup(res.text, 'html.parser')
    tiezi_total_num = soup.find('span', class_='red_text').text
    tiezi_total_num = int(tiezi_total_num.replace(',', ''))
    # 贴吧默认每页50条帖子
    page_size = 50
    # 计算出总页数
    total_page = math.ceil(tiezi_total_num / page_size)
    return total_page

# 获取帖子url列表的方法
def get_tiezi_url_list(total_page, url, session):
    #下面循环几次就是抓几页的帖子
    #是贴吧的翻页，不是帖子的翻页，帖子都会从一楼抓到最后楼
    all_tiezi_urls = []
    for i in range(0, 5):
        # 构造url
        tiezi_url = url + "&pn=" + str(i * 50)
        # 获取每一页的帖子url
        tiezis = get_tiezi_list(tiezi_url, session)
        # 将所有帖子url加入到all_tiezi_urls中
        all_tiezi_urls.extend(tiezis)
    return all_tiezi_urls

# 获取当前页所有帖子列表的方法
def get_tiezi_list(tiezi_url, session):
    # 获取某个帖子列表页面的网页内容
    res = session.get(tiezi_url)
    # 从中解析出每个帖子的链接
    soup = BeautifulSoup(res.text, 'html.parser')
    a_list= soup.find_all('a', class_='j_th_tit') #???
    # 拼接出真实的帖子链接
    static_tiezi_urls = []
    for each in a_list:
        static_tiezi_urls.append("http://tieba.baidu.com" + each.attrs['href'])
    return static_tiezi_urls

if __name__ == '__main__':

    session = login()
    keyword = input('请输入贴吧名称（例如：校花）：')
    # 构建贴吧主页url
    #index_url = 'https://tieba.baidu.com/f?kw={0}&tab=good'.format(keyword)
    index_url = 'https://tieba.baidu.com/f?kw={0}'.format(keyword)
    # 获取帖子总页数（经过测试发现 并不影响）
    total_page = get_total_page(index_url, session)
    # 获取每一页的帖子url 放在列表中
    all_tiezi_urls = get_tiezi_url_list(total_page, index_url, session)
    #以“关键字/数字序号.jpg”的形式保存爬取的图片
    #判断文件夹是否存在 如果不存在 则先创建文件夹
    img_dir = keyword
    if (not os.path.exists(img_dir)):
        os.mkdir(img_dir)
    i = 0
    for each in all_tiezi_urls:
        # 获取帖子的具体内容
        page = 1
        while(True):
            print('进入一个贴，第' + str(page) + '页')
            res = session.get(each)
            # 从中解析出图片url
            soup = BeautifulSoup(res.text, 'html.parser')
            img_urls = soup.find_all('img', class_='BDE_Image')
            for img in img_urls:
                i += 1                
                thumbnail = img.attrs['src']
                pic_id = ''.join(re.findall(r'(?<=/)(?![\w\W]*?/).*(?=.jpg)', thumbnail))
                tid = ''.join(list(re.findall(r'p/(.*)\?pn|p/(.*)$', each)[0]))
                print("正在下载第" + str(i) + "张图片" )
                high_img = 'http://tieba.baidu.com/photo/p?kw=' + keyword + '&flux=1&tid=' + tid + '&pic_id=' + pic_id
                res_img = session.get(high_img)
                soup_img = BeautifulSoup(res_img.text, 'html.parser')
                
                # baidu老狗又调皮了
                high_img_urls = ''.join(re.findall(r'(?<="waterurl":")(?![\w\W]*?"waterurl":").*(?="},"medium")', str(soup_img)))
                with open(img_dir + "/" + str(i) + '.jpg', 'wb') as f:
                    f.write(session.get(high_img_urls).content)
            
            if '>下一页</a>' in res.text:
                page += 1
                each = re.sub(r'\?pn(.*)?$', '', each)
                each = each + '?pn=' + str(page)
            else:
                break
    print("图片下载完毕！")
