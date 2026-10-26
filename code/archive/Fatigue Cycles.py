E = 77.6e+9 
coeff_thermal_expansion = 27e-6
twg = 273.15
twc = 300
dT = abs(twg - twc)


sigma_max = 40e+6
sigma_min = 10e+6

sigma_m   = 0.5*(sigma_max + sigma_min)
sigma_a   = 0.5*(sigma_max - sigma_min)
del_sigma = 2* sigma_a
R         = sigma_min/sigma_max


Kt = 3
Kf = 2.5

sigma_m_eff  = sigma_m*Kt
sigma_a_eff  = sigma_a*Kt
sigma_f      = 160e+6
sigma_y      = 12e+6
sigma_f_dash = sigma_f / Kf
sigma_a_allowable = sigma_f_dash*(1 - sigma_m_eff/sigma_y)

b    = -0.10
Nf   = (sigma_a_eff / sigma_f_dash)**(1/b)
N_req = 12  
SF = Nf/N_req