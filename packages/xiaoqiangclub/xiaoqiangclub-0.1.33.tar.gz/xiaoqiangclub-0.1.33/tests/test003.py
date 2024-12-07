"""
公园购票规则:

- 身高大于1.2m 成人票
- 身高小于1.2m 儿童票
- 身高小于1m   免票
"""


# 整数、浮点数（小数）
def ticket(height: float):
    """
    购票规则
    :param height: 身高
    :return:
    """
    if height > 1.2:
        return "成人票"
    elif height < 1:
        return "免票"
    return "儿童票"


if __name__ == '__main__':
    while True:
        try:
            user_height = float(input("请输入身高："))
        except ValueError:
            print("输入身高不合法，请输入 0 - 3 之间的合法身高...")
            continue

        # 判断输入的身高合法
        if not user_height or user_height <= 0 or user_height > 3:
            print("输入身高不合法，请输入 0 - 3 之间的合法身高...")
            continue
        print(f'身高为 {user_height}，请购买：{ticket(user_height)}')
