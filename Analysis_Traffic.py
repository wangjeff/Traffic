import csv
import os
import urllib
import operator


CAR = "31"
AN2MA = "01F3083N"  # 01F3083N:Anding -> Madou
TAIPEI2San = '01F0264S'
San2wugu = '01F0293S'
Young2Hukou = '01F0750S'
Debug_Trace = 0


def download(url, name):
    try:
        urllib.urlretrieve(url, name)
    except urllib.error.HTTPError:
        print('HTTPError')


def caclute_AvgSpeed(speed_dict):
    Hour = 0
    AvgSpeed_list = {}
    while Hour < 24:
        if Hour < 10:
            string_h = '0%s' % Hour
        else:
            string_h = '%s' % Hour
        AvgSpeed_list[string_h] = sum(
            speed_dict[string_h]) / len(speed_dict.get(string_h))
        Hour = Hour + 1
    return AvgSpeed_list


def Caclute_Day(Trip_type, Input_Day, data_Dir):
    speed_dict = {'00': [], '01': [], '02': [], '03': [], '04': [], '05': [],
                  '06': [], '07': [], '08': [], '09': [], '10': [], '11': [],
                  '12': [], '13': [], '14': [], '15': [], '16': [], '17': [],
                  '18': [], '19': [], '20': [], '21': [], '22': [], '23': []}
    AvgSpeed_list = {}
    for AllFiles in os.walk(data_Dir):
        # print AllFiles[2]
        for One_file in AllFiles[2]:
            currentfile = 'data/%s/%s' % (Input_Day, One_file)
            csvfile = open(currentfile, 'rb')
            for row in csv.reader(csvfile, delimiter=','):
                if Trip_type in row[1]:
                    if row[3] == CAR:
                        dict_name = '%s%s' % (One_file[19], One_file[20])
                        if row[4] != '0':
                            if dict_name in speed_dict:
                                speed_dict[dict_name].append(int(row[4]))
                                # print speed_dict
                            else:
                                speed_dict[dict_name] = int(row[4])

            csvfile.close()
    AvgSpeed_list = caclute_AvgSpeed(speed_dict)

    sorted_list = sorted(AvgSpeed_list.items(), key=operator.itemgetter(1))

    return AvgSpeed_list, sorted_list


def select_days():
    """
    select the days
    """


def main():
    """
    step1: download data if necessary
    """
    Input_Day = raw_input("Please enter date(ex:20160821): ")
    data_Dir = "\pratice_jeff\Traffic\data\%s" % Input_Day

    downloadfile(Input_Day)
    Trip_list = [TAIPEI2San, San2wugu, Young2Hukou]
    # Trip_list = [San2wugu]
    for Trip_type in Trip_list:
        if Debug_Trace:
            print Trip_type
        AvgSpeed_dict, sorted_list = Caclute_Day(
            Trip_type, Input_Day, data_Dir)
        # print sorted_list
        if Debug_Trace:
            print AvgSpeed_dict
        for data_time, data_speed in AvgSpeed_dict.iteritems():
            if data_speed < 70:
                print 'WARNING(Taipei to Hsinchu)!!!! Time:%s Speed is %s' \
                    % (data_time, data_speed)


def mkfolder(date):
    """
    Check the folder exist or not first.Then create the folder
    """
    Download_flag = 0
    mkdir_name = "data/%s" % date
    if not os.path.exists(mkdir_name):
        os.mkdir(mkdir_name)  # date folder
        Download_flag = 1

    return Download_flag


def downloadfile(date):
    """
    Need to create the data folder first
    All the M05A file will put in data folder
    """
    fix_history = "http://tisvcloud.freeway.gov.tw/history/TDCS/M05A"
    # "http://tisvcloud.freeway.gov.tw/history/TDCS/M05A/20160918/23/TDCS_M05A_20160918_235000.csv"
    Download_flag = mkfolder(date)
    Min = 0
    Hour = 0
    while (Hour < 24 and Download_flag == 1):
        # print Hour
        while Min < 56:
            if ((Hour < 10) and (Min < 10)):
                name = 'TDCS_M05A_%s_0%s0%s00.csv' % (date, Hour, Min)
            elif((Hour < 10) and (Min > 9)):
                name = 'TDCS_M05A_%s_0%s%s00.csv' % (date, Hour, Min)
            elif((Hour > 9) and (Min < 10)):
                name = 'TDCS_M05A_%s_%s0%s00.csv' % (date, Hour, Min)
            else:
                name = 'TDCS_M05A_%s_%s%s00.csv' % (date, Hour, Min)

            if (Hour < 10):
                url = "%s/%s/0%s/%s" % (fix_history, date, Hour, name)
            else:
                url = "%s/%s/%s/%s" % (fix_history, date, Hour, name)
            # print url
            # print name
            Min = Min + 5
            d_PathName = "data/%s/%s" % (date, name)
            download(url, d_PathName)
        Hour = Hour + 1
        Min = 0  # reset the Min and downlad the next one
    if Debug_Trace:
        if Download_flag:
            print 'download %s complete!! bye bye!!' % date
        else:
            print 'Aleardy download %s !! bye bye!!' % date


if __name__ == '__main__':
    main()
