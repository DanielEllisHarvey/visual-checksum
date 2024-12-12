from src import functions as vc

vc.pen_size = 5
vc.step = 25
vc.hmac_cycle("hello", "12345", "", "", 12345, filename="squiggly", hmac_pw="ww", hmac_salt="w3", straight_lines=False)

vc.pen_size = 2
vc.step = 5
vc.set_bg("#000000")
vc.hmac_single("hello", "12345", "", "", filename="straight", hmac_pw="ww", hmac_salt="w3", straight_lines=True)