from parsanonymizer import Model

m = Model()

sent = "نفیسه و علی و محمد و زهرا - محمدی و حسن جعفری و اکبری و محمدی و امیری به آقای محمد حسینی سلام کردند."
spans = m.extract_span(sent)

for key in spans.keys():
    print(f"{key}:")
    for span in spans[key]:
        start, end = span[0], span[1]
        print(sent[start: end])