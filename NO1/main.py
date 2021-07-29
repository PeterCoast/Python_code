import requests
import re
import threading


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) "}

# 循环获取 URL
def get_image(base_url):

    res = requests.get(url=base_url, headers=headers)

    if res is not None:
        html = res.text
		# 正则表达式提取数据
        pattern = re.compile(
            '<img lazysrc="(.*?)" lazysrc2x=".*?" width="221" height="362" alt=".*?" title="(.*?)"')
        match_list = pattern.findall(html)
        for url, title in match_list:
        	# url 字符串进行处理，去除缩略图部分
            save_image(url[:url.find('jpg')+3], title)

        print(match_list)
def save_image(url, title):
    try:
        print(f"{title} - {url}")
        res = requests.get(url=url, headers=headers)

        if res is not None:
            html = res.content

            with open(f"images/{title}.jpg", "wb+") as f:
                f.write(res.content)
    except Exception as e:
        print(e)
if __name__ == '__main__':
    num = 0
    # 最多开启5个线程
    semaphore = threading.BoundedSemaphore(5)
    for index in range(189):
        t = threading.Thread(target=get_image, args=(
            f"https://www.3gbizhi.com/sjbz/index_{index}.html",))
        t.start()
    while threading.active_count() != 1:
        pass
    else:
        print('所有线程运行完毕')

