import sys
from datetime import date, timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist
from pytz import utc

from amr_dashboard.models import DeviceInfo, DeviceReading, UpdatedDeviceReading, InitialReading

####time date filter
up_from_date = date.today() - timedelta(days=17)
up_to_date = date.today() + timedelta(days=1)
from_date_range = (up_from_date, up_to_date)


####time date filter


def last_day_of_month(year, month):
    """ Work out the last day of the month """
    last_days = [31, 30, 29, 28, 27]
    for i in last_days:
        try:
            end = datetime(year, month, i)
        except ValueError:
            continue
        else:
            return end.date()
    return None


def first_day_of_month(year, month):
    """ Work out the last day of the month """
    first_day = [1]
    for i in first_day:
        try:
            first = datetime(year, month, i)
        except ValueError:
            continue
        else:
            return first.date()
    return None


def FirstCronTest():
    print("I am executed..!")
    # month = date.today().month
    #
    #
    #
    # from_month = first_day_of_month(2021,  12)
    # to_month = last_day_of_month(2021, 12 )
    # last_from_month = first_day_of_month(2021, 12 - 1)
    # last_to_month = last_day_of_month(2021, 12 - 1)
    # print(last_from_month, last_to_month)

    # foramt_date = date.today()
    foramt_date = datetime.strptime("2022-04-30", "%Y-%m-%d")


    curr_month = foramt_date.month
    curr_year = foramt_date.year
    print(curr_year,curr_month)

    from_month = first_day_of_month(curr_year, curr_month)
    to_month = last_day_of_month(curr_year, curr_month)
    if curr_month == 1:
        previous_from_month = first_day_of_month(curr_year-1, 12)
        previous_to_month = last_day_of_month(curr_year-1, 12)
    else:
        previous_from_month = first_day_of_month(curr_year, curr_month - 1)
        previous_to_month = last_day_of_month(curr_year, curr_month - 1)

    dev = DeviceInfo.objects.filter(is_active=1).values('id', 'consumer_account_no', 'consumer_contact_no',
                                                        'device_sim')
    a = []
    for x in dev:

        try:
            last_IN = InitialReading.objects.filter(date__range=(previous_from_month, previous_to_month), device_id=x['id'],device__is_active=1).latest('id')
        except ObjectDoesNotExist:
            last_IN = None
        if last_IN is not None:
            last_initial_reading = last_IN.initial_reading
        else:
            last_initial_reading = None
        try:
            latest_device = DeviceReading.objects.filter(date__range=(from_month, to_month), device_id=x['id'],
                                                         device__is_active=1).latest('id')
        except ObjectDoesNotExist:
            latest_device = None
        if (latest_device is not None):
            last_com = latest_device.reading
            last_date = latest_device.date
            last_time = latest_device.time
            last_create_date = latest_device.create_date
        else:
            last_com = None
            last_date = None
            last_time = None
            last_create_date = None

        if last_com is not None and last_initial_reading is not None:
            new_initial_id = x['id']
            new_initial_reading = float(last_com)
            new_initial_date = last_date
            new_initial_time = last_time
            new_initial_sim = x['device_sim']
            new_initial_create_date= last_create_date
        else:
            new_initial_id = x['id']
            new_initial_reading = 0
            new_initial_date = last_date
            new_initial_time = last_time
            new_initial_sim = x['device_sim']
            new_initial_create_date = last_create_date


        data = {
            "device_id": new_initial_id,
            "reading": new_initial_reading,
            "date": new_initial_date,
            "time": new_initial_time,
            "device_sim": new_initial_sim,
            "create_date":new_initial_create_date
        }

        try:
            InitialReading.objects.create(
                initial_reading=data['reading'],
                date=data['date'],
                time=data['time'],
                device_id=data['device_id'],
                device_sim=data['device_sim'],
                create_date=data['create_date']
            )
        except Exception as e:
            error = 'on line {}'.format(sys.exc_info()[-1].tb_lineno), e
            print(error)

        a.append(data)
        print(data)

    # print(a)




def FlatReadingCronTest():
    month = date.today().month
    year = date.today().year
    from_month = first_day_of_month(year, month)
    to_month = last_day_of_month(year, month)

    # print(up_from_date,up_to_date)

    dev = DeviceInfo.objects.filter(is_active=1,has_billing=1).values('id', 'consumer_account_no', 'consumer_contact_no',
                                                        'device_sim')
    a = []
    b = []
    c = []
    d = []
    t=[]
    for x in dev:

        status = UpdatedDeviceReading.objects.filter(present_date__range=from_date_range, device_id=x['id'],
                                                     device__is_active=1).count()
        if status == 0:
            status_device = 'offline'
        else:
            status_device = "online"
            ##### lastest day S###

            try:
                device_reading = DeviceReading.objects.filter(date__range=(from_month, to_month), device_id=x['id'],
                                                              device__is_active=1).latest("id")
            except ObjectDoesNotExist:
                device_reading = None
            # print(device_reading[0].reading,device_reading[0].device_id,device_reading[0].date)

            if device_reading is not None:
                device_latest_date = device_reading.date
                device_latest_data = device_reading.reading
                device_l_id = device_reading.device_id
            else:
                device_latest_data = None
                device_latest_date = None
                device_l_id = x['id']

            # print(device_latest_date,device_latest_data,device_l_id,x['consumer_account_no'])
            ##### lastest day E###

            ##### 2nd last day S###
            if device_latest_data is not None:
                try:
                    device_reading2 = DeviceReading.objects.filter(
                        date__range=(from_month, device_latest_date - timedelta(days=1)), device_id=x['id'],
                        device__is_active=1).latest('id')
                except ObjectDoesNotExist:
                    device_reading2 = None
                if device_reading2 is not None:
                    device_latest_date2 = device_reading2.date
                    device_latest_data2 = device_reading2.reading
                    device_l_id = device_reading2.device_id
                else:
                    device_latest_date2 = None
                    device_latest_data2 = None
                    device_l_id = x['id']
            else:
                device_latest_date2 = None
                device_latest_data2 = None
                device_l_id = x['id']
            # print(device_latest_date2,device_latest_data2,device_l_id,x['consumer_account_no'])
            ##### 2nd last day E###

            ##### 3rd last day S###
            if device_latest_date2 is not None:
                try:
                    device_reading3 = DeviceReading.objects.filter(
                        date__range=(from_month, device_latest_date - timedelta(days=3)), device_id=x['id'],
                        device__is_active=1).latest('id')
                except ObjectDoesNotExist:
                    device_reading3 = None

                if device_reading3 is not None:
                    device_latest_date3 = device_reading3.date
                    device_latest_data3 = device_reading3.reading
                    device_l_id = device_reading3.device_id
                else:
                    device_latest_date3 = None
                    device_latest_data3 = None
                    device_l_id = x['id']
            else:
                device_latest_date3 = None
                device_latest_data3 = None
                device_l_id = x['id']
            # print(device_latest_date3,device_latest_data3,device_l_id,x['consumer_account_no'])
         ##### 3rd last day E###
    #
            if device_latest_data is not None and device_latest_data2 is not None and device_latest_data3 is not None:
                if float(device_latest_data) == float(device_latest_data3) and float(device_latest_data2) == float(device_latest_data3) and float(device_latest_data) == float(device_latest_data2):
                    # print(x['id'])
                    a.append(device_reading)

    for x in a:

        print(x.device.id)
                    # b.append(device_reading.device_id)
    # #
    #
    #
    #             x = float(device_latest_data) - float(device_latest_data2)
    #             if x>=0 and x<1:
    #                 a.append(device_reading.device.consumer_account_no)
    #
    #
    #             y = float(device_latest_data2) - float(device_latest_data3)
    #             if y>=0 and y<1:
    #                 b.append(device_reading.device.consumer_account_no)
    # #
    #
    #             z = float(device_latest_data) - float(device_latest_data3)
    #             if  z>=0 and z<1:
    #                 c.append(device_reading.device.consumer_account_no)
    #
    #
    #             if x==y :
    #                 d.append(device_reading.device.consumer_account_no)
    #
    #
    #
    #
    #
    # print(a)
    # print(len(a))
    #
    # print(b)
    # print(len(b))
    # #
    # # print(c)
    # # print(len(c))
    #
    # print(d)
    # print(len(d))

    # AllAbnormalDevice = list(set().union(a,b))
    # print(AllAbnormalDevice)
    # print(len(AllAbnormalDevice))

    # d = []
    # for y in a:
    #     # print(y.reading,y.device_id,y.device.consumer_account_no)
    #     d.append(y.device.consumer_account_no)
    # print(d)
    # print(len(d))


def NotSetToZero():
    month = date.today().month
    year = date.today().year
    from_month = first_day_of_month(year, month)
    to_month = last_day_of_month(year, month)
    dev = DeviceInfo.objects.filter(is_active=1).values('id', 'consumer_account_no', 'consumer_contact_no',
                                                        'device_sim')
    b = []
    for x in dev:

        status = UpdatedDeviceReading.objects.filter(present_date__range=from_date_range, device_id=x['id'],
                                                     device__is_active=1).count()

        if status == 0:
            status_device = 'offline'
        else:
            status_device = "online"

            firstday = first_day_of_month(year, month)

            seconday = firstday + timedelta(days=1)
            # print(firstday,seconday)

            try:
                device_reading = DeviceReading.objects.filter(date__range=(firstday, seconday), device_id=x['id'],
                                                              device__is_active=1).latest("id")
            except ObjectDoesNotExist:
                device_reading = None

            if device_reading is not None:
                if device_reading.reading >= 100:
                    # print(device_reading.device.consumer_account_no)
                    b.append(device_reading.device.consumer_account_no)

    # print(b)
    # print(len(b))


def AbnormalDeviceReading():

    dev = DeviceInfo.objects.filter(is_active=1,has_billing=1).values('id', 'consumer_account_no', 'consumer_contact_no','device_sim','average_meter_consumption_per_day')
    curr_month = date.today().month
    curr_year = date.today().year
    from_month = first_day_of_month(curr_year,  curr_month)
    to_month = last_day_of_month(curr_year, curr_month )
    a=[]
    b = []
    c = []
    d = []
    for x in dev:
        try:
            device_reading_info = DeviceReading.objects.filter(date__range=(from_month, to_month), device_id=x['id'],
                                                          device__is_active=1).latest("id")
        except ObjectDoesNotExist:
            device_reading_info = None

        if device_reading_info is not None:
            device_last_rading_date = datetime.strptime(str(device_reading_info.date), "%Y-%m-%d")
            device_last_rading_days =datetime.strptime(str(device_reading_info.date), "%Y-%m-%d").day
            device_last_reading= device_reading_info.reading
            meter_avg_per_day = (x["average_meter_consumption_per_day"])/1000
            device_id = x['id']
        else:
            device_last_rading_date = None
            device_last_rading_days = None
            device_last_reading = None
            meter_avg_per_day = (x["average_meter_consumption_per_day"])/1000
            device_id = x['id']




        # print(device_last_rading_days)



        if device_reading_info is not None :
            device_avg_per_day = float(device_last_reading) / float(device_last_rading_days)
            meter_avg_per_day_max = meter_avg_per_day+(((float(meter_avg_per_day))*50)/100)
            meter_avg_per_day_min = meter_avg_per_day-(((float(meter_avg_per_day))*50)/100)

            if device_avg_per_day <= meter_avg_per_day_max and device_avg_per_day >=meter_avg_per_day_min:
                # print('NOT Abnormmal',device_reading_info.device.consumer_account_no,device_avg_per_day,meter_avg_per_day_max,meter_avg_per_day_min,x['id'])
                b.append(device_reading_info.device.consumer_account_no)

            else:
                if device_avg_per_day > meter_avg_per_day_max:
                    c.append(device_reading_info.device.consumer_account_no)
                elif device_avg_per_day < meter_avg_per_day_min:
                    d.append(device_reading_info.device.consumer_account_no)
                # print(device_reading_info.device.consumer_account_no,device_avg_per_day,meter_avg_per_day_max,meter_avg_per_day_min,x['id'])
                a.append(device_reading_info.device.consumer_account_no)

    # print(c)
    # print(len(c))
    # print(d)
    # print(len(d))


def Hello():
    print("hello from cron job")






