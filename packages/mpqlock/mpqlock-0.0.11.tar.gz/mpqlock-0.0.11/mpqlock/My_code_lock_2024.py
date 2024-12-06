import sys
import datetime
year = (datetime.datetime.now().year)


def code_Lock():
    if year <= 2025:
        print('###################\n'
              '欢迎使用该程序！~~~~~~\n'
              '@auther: Peiqi Miao\n'
              '###################')
        # print('注意：有效期到%d'%year,'年底\n'
        #       '请联系管理员续费\n'
        #       '详情请咨询：15522342825')
    else:
        print('已到使用有效期！\n'
              '请联系管理员续费\n'
              '详情请咨询：15522342825')
        sys.exit(0)

if __name__ == "__main__":
    code_Lock()