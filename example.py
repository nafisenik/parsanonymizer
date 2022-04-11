from parsanonymizer import Model

m = Model()

sent = "نفیسه و علی و محمد و زهرا - محمدی به شرکت گوگل و یاهو رفتند و حسن جعفری و اکبری و محمدی  و امیری به آقای محمد حسینی سلام کردند."
#sent = 'کد ملی0924134127 است '
sent = 'علیپور علی‌پور رفت '
spans = m.extract_span(sent)

with open('out.txt', 'w', encoding='utf-8-sig') as f:
    for key in spans.keys():
        f.write(f"{key}:\n\n")
        for span in spans[key]:
            start, end = span[0], span[1]
            f.write(f'{sent[start: end]}\n')
            