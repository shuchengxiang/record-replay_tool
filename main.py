from record import record_
from replay import replay_
import os

if __name__ == '__main__':

    while True:
        newest_file = 'records/' + os.listdir('records')[-1]
        op = input('请输入操作对应的数字并回车执行:1--录制(录制结束需按esc键)，2--回放，3--退出\n')
        if op == '1':
            record_()
        elif op == '2':
            replay_(newest_file)
        elif op == '3':
            break
        else:
            print('请选择支持的操作~')
