# coding:utf-8
import time
import os


def main():
    ss = '''RELIABLE_SENDER_MESSAGE
T_APP_CONTAINER
T_APP_CONTA_HISTORY
T_CONTAINER_RULE
T_PATH_MATCH_RULE
T_SWIFT_BACKUP_DIFF_RECORD
T_SWIFT_BACKUP_ERROR_RECORD
T_SWIFT_BACKUP_RECORD
T_SWIFT_CIPHER_CFG
T_SWIFT_CIPHER_EXCEPTION
T_SWIFT_CIRCUIT_ROUTE
T_SWIFT_CIRCUIT_STRATEGY
T_SWIFT_CLUSTER
T_SWIFT_COMMON_RELEASE_HIS
T_SWIFT_COMMON_RULE
T_SWIFT_COMMON_RULE_APVL
T_SWIFT_COMMON_RULE_RELEASE
T_SWIFT_CONTAINER
T_SWIFT_DBRA_CFG
T_SWIFT_DOMAIN_MAPPING_RULE
T_SWIFT_NODE
T_SWIFT_ROUTE'''
    s = ''
    for line in ss.split('\n'):
        s = s + "" + line + ","
    print(s)


def get_fun_content(str_, fun_str):
    type_ = 0
    str2 = str_.split(fun_str + '(', 1)[1]
    for s in str2:
        if s == '(':
            type_ = 1
            break
        elif s == ')':
            type_ = 2
            break 
    if type_ == 2:
        rs = str2.split(')')[0]
    elif type_ == 1:
        r_num = str2.count('(') + 1
        rs = ''
        for i in str2.split(')')[0:r_num]:
            rs = rs + i + ')'
        rs = rs[0:-1]
    return rs


def get_pic_by_text(file_path, text, pic_size=(500, 500), color='white'):
    from PIL import Image
    img = Image.new('RGB', pic_size, color=color)
    img.save(file_path)
    img.close()


def locattime():
    """ 返回当前时间，格式%Y-%m-%d %H:%M:%S """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def locatdate():
    """ 返回当前日期，格式%Y-%m-%d """
    return time.strftime("%Y-%m-%d", time.localtime())

    
def cat(path, encoding='utf-8'):
    """ 同linux下的cat """
    import codecs
    file = codecs.open(path, encoding=encoding, errors='ignore')
    text = file.read()
    file.close()
    return text


def sql_remove_comments(text):
    """ sql中有--注释，直接带入可能会不识别，通过此方法去掉注释 """
    sql = ''
    for line in text.split('\n'):
        if '--' in line:
            sql_line = line.split('--')[0]
        else:
            sql_line = line
        sql = sql + ' ' + sql_line
    sql = merge_spaces(sql.replace('\n', ' '))
    return sql


def echo(text, path, mode='a', encoding='utf-8'): 
    """ 把text输出到指定路径文件，不存在会创建（包括文件夹），mode默认是a，表示追加写，设为w表示覆写 """
    try:
        mkdir(os.path.dirname(path))
    except:
        pass
    path = path.replace('\u202a', '')
    file = open(path, mode, encoding=encoding, errors='ignore')
    file.write(str(text) + '\n')
    file.close()

    
def mkdir(path):
    """ 不存在则创建文件夹，逐层创建 """
    if not os.path.exists(path):
        os.makedirs(path)

        
def rm(path):
    """ 同linux下的rm -rf """
    import shutil
    path = path.replace('\\', '/')
    if os.path.exists(path):
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def merge_spaces(s):
    """ 空格合并(\t会视为空格，\n不会)，直到不存在多个连续空格 """
    s2 = ''
    s = s.replace('\t', ' ')
    for line in s.split('\n'):
        s2 = s2 + ' '.join(line.split()) + '\n'
    return s2.strip()


def nvl(strVal, defaultVal):
    """ 同Oracle下的nvl """
    if strVal is None or strVal == '':
        return defaultVal
    else:
        return strVal

    
def round_(num, format_):
    """ round无异常 """
    import builtins
    try:
        return builtins.round(num, format_)
    except:
        return None


def timeformat(timeStr, srcformat, dstformat):
    """ 自由的时间格式转换
    %y 两位数的年份表示（00-99）
    %Y 四位数的年份表示（000-9999）
    %m 月份（01-12）
    %d 月内中的一天（0-31）
    %H 24小时制小时数（0-23）
    %I 12小时制小时数（01-12）
    %M 分钟数（00-59）
    %S 秒（00-59）
    %a 本地简化星期名称
    %A 本地完整星期名称
    %b 本地简化的月份名称
    %B 本地完整的月份名称
    %c 本地相应的日期表示和时间表示
    %j 年内的一天（001-366）
    %p 本地A.M.或P.M.的等价符
    %U 一年中的星期数（00-53）星期天为星期的开始
    %w 星期（0-6），星期天为 0，星期一为 1，以此类推。
    %W 一年中的星期数（00-53）星期一为星期的开始
    %x 本地相应的日期表示
    %X 本地相应的时间表示
    %Z 当前时区的名称
    %% %号本身 """
    import datetime
    return datetime.datetime.strptime(timeStr, srcformat).strftime(dstformat)


def zip_folder(zip_folder_path, out_file_path):
    """ 压缩指定文件夹
    :param zip_folder_path: 目标文件夹路径
    :param out_file_path: 压缩文件保存路径+xxxx.zip
    :return: 无
    """
    import zipfile
    zip_ = zipfile.ZipFile(out_file_path, mode="w", compression=zipfile.ZIP_DEFLATED, allowZip64=True)
    for path, _, filenames in os.walk(zip_folder_path):
        # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
        fpath = path.replace(zip_folder_path, '')

        for filename in filenames:
            zip_.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip_.close()

    
def line_merge_align(str_1, str_2, iscompare=False):
    """ 两个字符串的同一行合并成新的一行，并且对齐（用于方便左右比较）
    iscompare为真时，左右不一致会在最右边提示*号 """
    str1s = str_1.split('\n')
    str2s = str_2.split('\n')
    strlennum = 0  # 最大字符长度
    for str_ in str1s:
        if strlennum < len(str_):
            strlennum = len(str_)
    for str_ in str2s:
        if strlennum < len(str_):
            strlennum = len(str_)
    linenum = len(str1s) if len(str1s) > len(str2s) else len(str2s)  # 最大行数
    str_ = ''
    for idx in range(0, linenum):
        try:
            str1 = str1s[idx]
        except:
            str1 = ''
        try:
            str2 = str2s[idx]
        except:
            str2 = ''
        if iscompare:
            if merge_spaces(str1.strip()) != merge_spaces(str2.strip()):
                str_ = str_ + str1 + ' ' * (strlennum - len(str1) + 1) + str2 + '\t*\n'
            else:
                str_ = str_ + str1 + ' ' * (strlennum - len(str1) + 1) + str2 + '\n'
        else:
            str_ = str_ + str1 + ' ' * (strlennum - len(str1) + 1) + str2 + '\n'
    return str_.strip()


def pictures_folder_2_pdf(source_path, target_pdf):
    from PIL import Image
    from PIL import ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    files = os.listdir(source_path)
    pic_files = []
    for file in files:
        if file.endswith('.jpg') or file.endswith('.png'):
            file = source_path + '/' + file
            pic_files.append(file)
    pic_files.sort()
    outFDF = Image.open(pic_files[0])
    pic_files.pop(0)
    sources = []
    for file in pic_files:
        png_file = Image.open(file)
        if png_file.mode != "RGB":
            png_file = png_file.convert("RGB")
        sources.append(png_file)    
        
    outFDF.save(target_pdf, "pdf", save_all=True, append_images=sources, optimize=True, progressive=True)
    sources.clear()


def repair_img(root_path):
    import cv2
    for fileName in os.listdir(root_path):
        file_path = os.path.join(root_path, fileName)
        img = cv2.imread(file_path)
        new_path = os.path.join(root_path, fileName)
        cv2.imwrite(new_path, img)


def remove_leading_space(str1):
    """ 每行去掉首尾的空格换行等字符后，再接回去 """
    str2 = ''
    for line in str1.split('\n'):
        str2 = str2 + line.strip() + '\n'
    return str2.strip('\n')


def analysis_hosts(host_conn):
    kv = {}
    hosts_str = host_conn.exec_command('cat /etc/hosts')
    for line in hosts_str.split('\n'):
        line = merge_spaces(line)
        strs = line.split(' ')
        if strs[0] != '::1' and strs[0] != '':
            for idx in range(1, len(strs)):
                kv[strs[idx]] = strs[0]
    return kv


def lstrip(ss, del_ss):
    if ss.find(del_ss) == 0:
        return ss[len(del_ss):len(ss)]
    else:
        return ss

    
def rstrip(ss, del_ss):
    if ss.rfind(del_ss) == len(ss) - len(del_ss):
        return ss[0:ss.rfind(del_ss)]
    else:
        return ss


def strip(ss, del_ss):
    return rstrip(lstrip(ss, del_ss), del_ss)


if __name__ == '__main__':
    main()
