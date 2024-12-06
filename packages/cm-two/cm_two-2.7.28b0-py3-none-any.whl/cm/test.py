a = open(r"C:\Users\faizi\OneDrive\Рабочий стол\out.txt", "r")
res = []
for l in a.readlines():
    r = l.split("|")[0]
    try:
        r = int(r)
        res.append(r)
    except:
        pass

print(tuple(res))

-kpp_cam_external
True
-kpp_cam_internal
True
-kpp_cam_internal_ip
localnet
-kpp_cam_internal_port
10101
-kpp_cam_external_ip
localnet
-kpp_cam_external_port
10102


-gross_cam
True
-gross_cam_ip
localnet
-gross_cam_port
10101
-auto_exit_cam
True
-gross_cam_ip
localnet
-gross_cam_port
10102
