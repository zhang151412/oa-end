# pip install click
import click
from models.user import OAUser, OADepartment, OACrossDepartmentAssociation
from exts import db
# pip install faker
from faker import Faker
from pypinyin import lazy_pinyin
import random


def greet():
    click.echo("命令测试成功！")


@click.option("-e","--email",required=True)
@click.option("-p","--password",required=True)
@click.option("-r","--realname",required=True)
@click.option("-j","--jobnumber",required=True)
def create_user(email,password,realname,jobnumber):
    user = OAUser(email=email,password=password,realname=realname,jobnumber=jobnumber)
    db.session.add(user)
    db.session.commit()
    click.echo("恭喜！用户创建成功！")


# 创建部门
def create_department():
    # 1. 董事会
    board = OADepartment(name="董事会", intro="BOSS！")
    # 2. 运营部
    operator = OADepartment(name="运营部",intro="运营")
    # 3. 人事部
    ministry = OADepartment(name="人事部",intro="HR")
    # 4. 产品开发部
    developer = OADepartment(name="产品开发部",intro="项目开发")
    # 5. 市场部
    marketor = OADepartment(name="市场部",intro="开拓市场")
    # 6. 行政部
    xingzheng = OADepartment(name="行政部",intro="公司管理")

    # db.session.add/add_all：是把数据添加到缓存中
    db.session.add_all([board,operator,ministry,developer,marketor,xingzheng])
    # db.session.commit：才是把缓存中的数据同步到数据库中
    db.session.commit()
    click.echo("恭喜！部门数据添加成功！")


# 创建测试用户
def create_test_user():
    dongdong = OAUser(
        realname="东东",
        email="dongdong@qq.com",
        password="111111",
        jobnumber="001",
        department=OADepartment.query.filter_by(name="董事会").one(),
        is_leader=True
    )
    duoduo = OAUser(
        realname="多多",
        email="duoduo@qq.com",
        password="111111",
        jobnumber="002",
        department=OADepartment.query.filter_by(name="董事会").one(),
        is_leader=False
    )
    zhangsan = OAUser(
        realname="张三",
        email="zhangsan@qq.com",
        password="111111",
        jobnumber="003",
        department=OADepartment.query.filter_by(name="运营部").one(),
        is_leader=True
    )
    lisi = OAUser(
        realname="李四",
        email="lisi@qq.com",
        password="111111",
        jobnumber="004",
        department=OADepartment.query.filter_by(name="人事部").one(),
        is_leader=True
    )
    wangwu = OAUser(
        realname="王五",
        email="wangwu@qq.com",
        password="111111",
        jobnumber="005",
        department=OADepartment.query.filter_by(name="产品开发部").one(),
        is_leader=True
    )
    zhaoliu = OAUser(
        realname="赵六",
        email="zhaoliu@qq.com",
        password="111111",
        jobnumber="006",
        department=OADepartment.query.filter_by(name="市场部").one(),
        is_leader=True
    )
    sunqi = OAUser(
        realname="孙七",
        email="sunqi@qq.com",
        password="111111",
        jobnumber="007",
        department=OADepartment.query.filter_by(name="行政部").one(),
        is_leader=True
    )

    base_users = [dongdong,duoduo,zhangsan,lisi,wangwu,zhaoliu,sunqi]
    db.session.add_all(base_users)
    db.session.commit()

    fake = Faker("zh_CN")
    users = []
    emails = []
    for x in range(8,100):
        realname = fake.name()
        jobnumber = str(int(x)).zfill(3)
        email = "".join(lazy_pinyin(realname)) + "@qq.com"
        if email in emails:
            # 如果这个邮箱已经存在了，就直接过掉
            continue
        password = "111111"

        base_user = base_users[random.randint(0,6)]
        department = base_user.department

        user = OAUser(realname=realname,email=email,password=password,
                      jobnumber=jobnumber,department=department,is_leader=False)

        emails.append(email)
        users.append(user)

    db.session.add_all(users)
    db.session.commit()
    print("恭喜用户添加成功！")


# 创建跨部门关联
def create_association():
    # 2. 运营部
    operator = OADepartment.query.filter_by(name="运营部").one()
    # 3. 人事部
    ministry = OADepartment.query.filter_by(name="人事部").one()
    # 4. 产品开发部
    developer = OADepartment.query.filter_by(name="产品开发部").one()
    # 5. 市场部
    marketor = OADepartment.query.filter_by(name="市场部").one()
    # 6. 行政部
    xingzheng = OADepartment.query.filter_by(name="行政部").one()

    dongdong = OAUser.query.filter_by(realname="东东").one()
    duoduo = OAUser.query.filter_by(realname="多多").one()

    # "多多"是董事会的，管理运营部、人事部、产品开发部
    # "东东"也是董事会的，管理市场部、行政部
    a1 = OACrossDepartmentAssociation(manager=duoduo,department=operator)
    a2 = OACrossDepartmentAssociation(manager=duoduo,department=ministry)
    a3 = OACrossDepartmentAssociation(manager=duoduo, department=developer)
    a4 = OACrossDepartmentAssociation(manager=dongdong, department=marketor)
    a5 = OACrossDepartmentAssociation(manager=dongdong, department=xingzheng)

    db.session.add_all([a1,a2,a3,a4,a5])
    db.session.commit()
    click.echo("跨部门管理关联成功！")