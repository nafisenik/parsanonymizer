from parsanonymizer import Model

m = Model()

sent = "نفیسه +989133123121 و علی و @sdfafs مح a@s.com مد و sss زهرا  09222221133- محمدی ss.sawe_c@sdgm.c به شرکت گوگل و یاهو https://google.com رفتند و   1237651212 حسن جعفری و اکبری و hello.com محمدی sss@sss.com و امیری به آقای محمد حسینی سلام کردند."
# sent = 'کد ملی0924134127 است '
# sent = """
# +98-9133123121
# +989133123122
# 9133123123
# 09133123124
# 0098 9133123125
# 00989133123126
# 0913 312 31 27
# 0913-312-3128
# 00989133123129
# 09133123120
# +989133123120cls
# """


sent = """
علی احمدی در شهرستان اصفهان شهر فولادشهر به دنیا آمد. 
علی رضا و زهرا در کشور زیمباوه زندگی می‌کنند. 
زندگی در کشور france به نظر سخت است.
کشور به منطقه‌ای گفته می‌شود که مرز آن با سیاست تعیین شده است.
من در ۱۶ بهمن ۱۳۷۵ به دنیا آمدم.
در تاریخ ۱۶ فروردین به مکه رفتم و از شرکت داده پردازش نیز دیدن کردم.
کدملی من ۱۱۳۰۳۹۴۷۸۹ است.
۱۱۳۰۳۹۴۷۸۹ کد ملی من است.
سلام نام من جیسون محمدنژادپور است و در میامی  زندگی میکنم. شماره کارت اعتباری من 6104337958646987 است که از آن به حساب شما پول می‌ریزم. من سایت microsof.com رو مشاهده کردم و ایمیل کارمند مایکروسافت، akabr@micr.com، را برداشتم.
شماره شبای من  IR069600000001032420000011 است.
شماره IBAN من KW81CBKU0000000000001234560101 است.
ساعت ۸ صبح پرواز به مقصد روستای احمدآباد را دارم. 
من در اصفهان، کوشک، خیابان احمدی، کوچه شهید علی علیزاده پلاک ۱۴۳ زندگی میکنم.
این نشانی خیابان بهشتی است.
شماره تلفن من ۰۹۱۲۳۴۵۶۷۸۹ و شماره خانه‌ علیرضا ۰۲۱۳۳۴۴۵۵۶۶ است.
خیابان اهواز شهر اهواز بسیار تمیز است.
"""
#sent = '2071-7789-9070-7878 سلام DE12345678901234567890 , AE12345678901234567890, DE12345678901234567890'
# sent = 'علیپور علی‌پور رفت '
# sent = "https://google.com"
# sent = "this is my حات جطرو https://google.com/hi سلام hello"
#sent = "نفیسه +989133123121 و علی و @sdfafs مح a@s.com مد و sss زهرا  09222221133- محمدی ss.sawe_c@sdgm.c به شرکت گوگل و یاهو https://google.com رفتند و   1237651212 حسن جعفری و اکبری و hello.com محمدی sss@sss.com و امیری به آقای محمد حسینی سلام کردند."

spans = m.extract_span(sent)

with open('out.txt', 'w', encoding='utf-8-sig') as f:
    for key in spans.keys():
        f.write(f"\n{key}:\n")
        for span in spans[key]:
            start, end = span[0], span[1]
            f.write(f'{sent[start: end]}\n')

    for key in spans.keys():

        f.write(f"\n{key}:\n")

        for span in spans[key]:
            start, end = span[0], span[1]
            f.write(f'{sent[start: end]}\n')

keys_persian = {
    'personalname': 'نام شخصی',
    'date': 'تاریخ',
    'address': 'آدرس',
    'datetime': 'تاریخ و ساعت',
    'bankcard': 'شماره کارت',
    'companynames': 'اسم شرکت',
    'email': 'ایمیل',
    'melicode': 'کد ملی',
    'phonenumber': 'شماره تماس',
    'url': 'آدرس سایت',
    'time': 'زمان',
}


# hide_sent = list(sent)
# with open('out2.txt', 'w', encoding='utf-8-sig') as f:
#     for key in spans.keys():
#         for span in spans[key]:
#             start, end = span[0], span[1]
#             hide_sent[start:end+1] = f'-{keys_persian[key]}-'

#     sent = "".join(hide_sent)       
#     f.write(sent)


result = []
for key in spans.keys():
    for span in spans[key]:
        start, end = span[0], span[1]
        result.append({'span': (start, end), 'len': end-start, 'cat': key})

result.sort(key=lambda x: x['span'][0])

final_str = ''
last_index = 0
for span_info in result:
    span_start_index = span_info['span'][0]
    span_end_index = span_info['span'][1]
    final_str += sent[last_index:span_start_index]
    final_str += f" *{keys_persian[span_info['cat']]}* "   # sent[span_start_index:span_end_index+1]
    last_index = span_end_index+1

final_str += sent[last_index:]

with open('out2.txt', 'w', encoding='utf-8-sig') as f:
    f.write(final_str)

