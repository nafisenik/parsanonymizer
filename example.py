from parsanonymizer import Model

m = Model()

sent = "نفیسه و علی و @sdfafs مح a@s.com مد و sss زهرا - محمدی ss.sawe_c@sdgm.c به شرکت گوگل و یاهو رفتند و   1237651212 حسن جعفری و اکبری و محمدی sss@sss.com و امیری به آقای محمد حسینی سلام کردند."
# sent = 'کد ملی0924134127 است '
# sent = 'علیپور علی‌پور رفت '
spans = m.extract_span(sent)

with open('out.txt', 'w', encoding='utf-8-sig') as f:

    for key in spans.keys():

        f.write(f"\n{key}:\n")

        for span in spans[key]:
            start, end = span[0], span[1]
            f.write(f'{sent[start: end]}\n')
