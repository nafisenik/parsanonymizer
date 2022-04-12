from parsanonymizer import Model

m = Model()

sent = "نفیسه +989133123121 و علی و @sdfafs مح a@s.com مد و sss زهرا  09222221133- محمدی ss.sawe_c@sdgm.c به شرکت گوگل و یاهو https://google.com رفتند و   1237651212 حسن جعفری و اکبری و hello.com محمدی sss@sss.com و امیری به آقای محمد حسینی سلام کردند."
# sent = 'کد ملی0924134127 است '
sent = """
+98-9133123121
+989133123122
9133123123
09133123124
0098 9133123125
00989133123126
0913 312 31 27
0913-312-3128
00989133123129
09133123120
+989133123120cls
"""

sent = '2071-7789-9070-7878 سلام DE12345678901234567890 , AE12345678901234567890, DE12345678901234567890'
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
