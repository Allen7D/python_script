# _*_ coding: utf-8 _*_

from bs4 import BeautifulSoup as soup
import time
import requests
import webbrowser

'''
思路：
    1.模拟移动端获取指定课程的html代码
    2.解析出课程的所有章节，
    3.每次n分钟对比一次数据库的历史数据，一旦更新则发送邮件(包含课程链接)
    4.保存第一次获取的数据到数据库，或更新的数据库的数据

步骤：
    1.实现本地存储即可
'''

lesson_url = 'http://coding.m.imooc.com/classindex.html?cid=136'
headers = {
    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'
}
ORIGIN_SECTION_NUM = 142


def get_database(lesson_url, headers):
    web_data = requests.get(lesson_url, headers=headers)
    web_xml = soup(web_data.text, 'lxml')
    chapter_xml = web_xml.select('div.right > div.answer')
    chapter_list = []
    new_section_num = 0
    for chapter in chapter_xml:
        chapter_list.append({
            'chapter_title': chapter.select('p.p1')[0].get_text(),
            'section_num': len(chapter.select('p')[1:])
        })
        new_section_num += len(chapter.select('p')[1:])
    return chapter_list, new_section_num

def print_lesson_chapter(chapter_list):
    for chapter in chapter_list:
        print("{0}：{1}节".format(chapter['chapter_title'], chapter['section_num']))
    print('-----'*10)

def save_database(lesson_url):
    pass

if __name__ == '__main__':
    while True:
        chapter_list, new_section_num = get_database(lesson_url, headers)
        print_lesson_chapter(chapter_list)

        if ORIGIN_SECTION_NUM != new_section_num:
            webbrowser.open('http://coding.imooc.com/learn/list/136.html')
            print('更新了{}节内容'.format((new_section_num - ORIGIN_SECTION_NUM)))
        else:
            TOTAL_SECTION_NUM = new_section_num

        time.sleep(60)


