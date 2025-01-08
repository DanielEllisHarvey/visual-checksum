from src import functions as vc

# vc.pen_size = 5
# vc.step = 25
# vc.hmac_cycle_expand("hello", "12345", "", "", 3, filename="squiggly", hmac_pw="ww", hmac_salt="w3", straight_lines=False)

vc.pen_size = 2
vc.step = 5
vc.set_bg("#ddeeff")
vc.hmac_cycle_expand("hello", "123456", "", "", iters=128, max_bits=512, filename="straight", hmac_pw="ww", hmac_salt="w3", straight_lines=True)