A_li = []

# 模拟redis中获取的集合
set1 = {"123", "2345", "6789"}

# li = [["123", "anywhere"], ["1234", "anywhere"], ["345", "any"]]

li = {"title": ["A", "B"], "123": ["A", "B"], "45": ["", ""]}


a = {item for item in li.keys()} - set1
print(a)  # {'1234', '345'},这个就是新的数据，需要添加
li1 = [{i: li[i]} for i in a]
print(li1)
A_li.extend(li1)
print(A_li)