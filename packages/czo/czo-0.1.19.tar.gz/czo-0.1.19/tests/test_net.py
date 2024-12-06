from czo import NetLib


def test_generate_ip_list_v4():
    l1 = ["1.0.0.1", "1.0.0.2", "1.0.0.3"]
    l2 = ["188.188.1.1", "188.188.1.2", "188.188.1.3"]
    assert NetLib.generate_ip_list(3) == l1
    assert NetLib.generate_ip_list(3, ip_str="188.188.1.1") == l2


def test_generate_ip_list_v6():
    l1 = [
        "2001:db8:0:42:0:8a2e:370:1",
        "2001:db8:0:42:0:8a2e:370:2",
        "2001:db8:0:42:0:8a2e:370:3",
    ]
    l2 = ["240e:c0a8:1:1:1:1:1:1", "240e:c0a8:1:1:1:1:1:2", "240e:c0a8:1:1:1:1:1:3"]
    assert NetLib.generate_ip_list(3, is_ipv6=True) == l1
    assert (
        NetLib.generate_ip_list(3, is_ipv6=True, ip_str="240e:c0a8:1:1:1:1:1:1") == l2
    )


def test_is_ip_in_range():
    q = "192.168.1.1"
    a = "192.168.1.0/24"
    z = "192.168.1.1 - 192.168.1.254"

    w = "2a00::110:1"
    s = "2a00::110:0/116"
    x = "2a00::110:1 - 2a00::110:fff"

    assert NetLib.is_ip_in_range(q, a) == True
    assert NetLib.is_ip_in_range(q, z) == True
    assert NetLib.is_ip_in_range(q, "172.17.0.0/24") == False
    assert NetLib.is_ip_in_range(q, "172.17.0.1-172.17.0.254") == False

    assert NetLib.is_ip_in_range(w, s) == True
    assert NetLib.is_ip_in_range(w, x) == True
    assert NetLib.is_ip_in_range(w, "fd00::110:0/124") == False
    assert NetLib.is_ip_in_range(w, "fd00::110:1-fd00::110:254") == False
