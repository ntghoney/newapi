## 环境配置
```
make install
```
## 用例编写规则
1. 使用excel编写,放在cases文件夹下,用例文件格式以case_开头,后缀名为.xlsx
不支持.xls,如 case_user.xlsx
2. 接口编号 最好唯一
3. 接口路径  不要带域名
4. 数据准备,用例的前提数据,从sql和shell中获取,书写规则 sql:*** 
shell:***,sql和shell文件放在指定文件夹
5. 参数 josn格式
6. headers信息 键值对形式,等号连接,多个之间以换行符隔开；如 a=8 \n b=6
7. 请求方法,post,get
8. 关联接口,可写路径或接口编号或接口信息（json格式）如
    ```json
    {
        "apiHost":"/s5/reward.coin.claim.today",
        "method":"post",
        "apiParams":"",
        "apiHeaders":""
    }
    ```
9. 关联参数 返回结果中的字段,如果是多重json中的字段，用.连接如
    ```
        payload.uid 代表 {"payload":{"uid":""}}
    ```
10. 检查点,键值对形式,等号连接,多个之间以换行符隔开，间以.连接代表多重json
json数组检查，如id=(1,2,3,4,5,6)
    ```
       payload.uid=100 代表 {"payload":{"uid":100}}
    ```
11. sql语句 值对形式,：连接,多个之间以换行符隔开
    ```
        sql1:select * from t_user 
        sql2:select * from t_user
    ```
12. 数据库期望(sql检查点），与sql语句形式一样，键必须和sql语句的键一一对应,值可为数据库返回长度
len代表长度，数据库返回结果中的某个字段值，多个之间=连接
    ```
     sql1:len=1,id=2
     sql2:len=2,id=3
    ```
13. 是否执行 y,Y为执行，其他为不执行

## 运行
```
python main.py
```