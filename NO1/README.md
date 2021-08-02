# 用Python爬取5000张手机高清壁纸
## 数据源分析
### 爬取目标
图片首页地址为：`https://www.3gbizhi.com/sjbz/index_1.html`，该网站壁纸质量不错，清晰度也非常好，重点是对爬虫也非常友善，试了几次，爬取速度都可以，因此大家应该把该网站用于学习目的。  
[插图1.png](https://img13.360buyimg.com/ddimg/jfs/t1/196629/23/15483/1547096/6102da0fEeeeda363/0823fa3b11b6a0c0.png)  
### 使用的 Python 模块
  
本次使用 `requests`，`re`，`threading`。  
  
`threading` 模块将在本案例中，进行分页多线程抓取。  
  
### 重点学习内容
  
爬虫基本套路  
  
多线程图片爬虫  
  
通过小图获取大图  
  
### 列表页分析
  
分析列表的时候发现，该网站可以直接通过，修改列表页图片地址获取高清地址，有这样的技巧存在，就能大幅度减少爬虫代码编写量，具体如下  
  
通过浏览器检查图片标签，获得如下图所示图片地址，即 `https://pic.3gbizhi.com/2020/1214/20201214112632727.jpg.476.780.jpg`  
  
在浏览器中打开该地址，得到一张图片预览地址，去除 `.476.780` 相关内容，直接获取到大图地址，即 `https://pic.3gbizhi.com/2020/1214/20201214112632727.jpg`  
[插图2.png](https://img10.360buyimg.com/ddimg/jfs/t1/186213/36/16377/524589/6102daf9E2bad3a16/19571f9b71630b3a.png)  
既然可以通过列表页直接获取大图地址，那针对该网站的爬取，直接通过列表页即可实现。下面就可以针对分析进行需求的整理工作  
## 整理需求如下
1. 爬取目标网站列表页；
2. 分析图片大图链接；
3. 请求图片，保存图片。  
## 编码时间
在上文针对列表页面进行了数据上的分析，接下来就可以对其进行代码编写了。  
  
编写图片地址提取代码，该代码的重点在于，需要将图片地址后面的缩放进行处理，即下述代码 `url[:url.find('jpg')+3]` 部分内容，下文中的正则表达式部分需要特别注意，在网站上右键查看的源码与服务器返回的代码存在差异，测试时需针对服务器返回进行匹配。  
  
下文代码中 `save_image` 在后文涉及。  
```python
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

```
此时获取到的就是图片的真实地址，调用 `save_image` 函数，对远程图片进行存储。其中 `title` 为图片存储地址。  
```pythpn
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

```
最后使用多线程进行爬取，开启 5 个线程，当所有线程结束运行时，停止整体代码。  
```python
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
```
运行我们的爬虫程序，会看到图片批量的存储到了本地。  
  
# 抓取结果展示时间
抓取到非常多优质的手机壁纸，换到手机不能用，都用不完了  
[插图3.png](https://img13.360buyimg.com/ddimg/jfs/t1/189566/25/15688/1072233/6102db53E7c61ed39/620382d373de4e2d.png)  
## 完整代码下载地址：[main.py](./main.py)  
  
代码编写过程中，顺手爬取了一堆图片，可以提前预览一波，看看图，在决定是否运行这段代码。
## 下载链接：
* [3k张壁纸](https://ws28.cn/f/60sdbzsqqp1) 密码：1188
