import requests

# 前期准备以及token的获取可参考：https://zhuanlan.zhihu.com/p/381527284
#                            https://www.zhihu.com/column/c_1389160991083692032
# 本页对应的数据库：https://www.notion.so/38a93f2a26284b19bc749cbf7464dabc?v=472018357e6a44b0865bd232fc099fa5
token = 'secret_feFoTGfTuwtdjxCzpsdutFWQtzW5stxZQkRucn1AUGC'
database_id = '38a93f2a26284b19bc749cbf7464dabc'
headers = {
    'Notion-Version': '2021-05-13',# 在新版中必须加入版本信息
    'Authorization': 'Bearer '+token,# 这一行也必须要有
}

# 查询数据库
url_notion = 'https://api.notion.com/v1/databases/'+database_id+'/query'
notion_response = requests.post(url_notion,headers=headers)
notion_data     = notion_response.json()['results']

# 查看返回数据，它们储存在'properties'中
notion_data[0]['properties']['标题']
notion_data[5]['properties']['小标题']['rich_text'][0]['text']['content']

# 构建上传数据的格式
body = {
    'parent': {'type': 'database_id', 'database_id': database_id},
}
body['properties'] = notion_data[0]['properties']
def update_properties(body_properties, date, title, content):
    body_properties['标题']['title'][0]['text']['content']=title
    body_properties['日期']['date']['start']=date
    body_properties['内容']['rich_text'][0]['text']['content']=content

update_properties(body['properties'], '2022-12-08', "第一条通过API创建的数据", "此条数据的内容")

# 上传数据
url_notion_additem = 'https://api.notion.com/v1/pages'
for i in range(30):
    notion_additem = requests.post(url_notion_additem,headers=headers,json=body)
    if notion_additem.status_code == 200:
        print('成功')
    elif notion_additem.status_code == 429:
        print('频率限制')
    elif notion_additem.status_code == 400:
        print('失败')

# 使用限制：https://developers.notion.com/reference/request-limits
# 官方文档：https://developers.notion.com/docs/working-with-page-content#reading-nested-blocks



