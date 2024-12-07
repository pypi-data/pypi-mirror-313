# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2024/11/11 11:21
# 文件名称： __init__.py.py
# 项目描述： 豆瓣平台相关接口
# 开发工具： PyCharm
if __name__ == '__main__':
    user_id = ['197964926', '283652746']  # 替换为实际的用户ID
    file_path = 'douban_wish.json'
    asyncio.run(get_douban_wish_details(user_id, print_results=True, save_to_file=True, file_path=file_path,
                                        skip_existing=True))
