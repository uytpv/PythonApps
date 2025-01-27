import requests
import time

from openvpn_api import Openvnp_API

url = "https://vote.vars.vn/api.php"

headers = {
    "sec-ch-ua": "Google Chrome;v=113, Chromium;v=113, Not-A.Brand;v=24",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": "Windows",
    "Host": "vote.vars.vn"
}

payload = {
    "action": "vote_candidate",
    "email": "travinhnguyenminh@gmail.com",
    "myVote[0][company]": "Công ty TNHH MTV Sàn Giao Dịch BĐS Nam Long",
    "myVote[0][id]": "304",
    "myVote[0][name]": "CEO TRẦN VĨ THÀNH",
    "myVote[0][permalink]": "https://vote.vars.vn/ung-cu-vien/ceo-tran-vi-thanh/",
    "myVote[0][thumbnail]": "https://vote.vars.vn/storage/2023/05/Tran-Vi-Thanh-1.webp",
    "myVote[0][votes]": "2482",
    "nonce": "5f7978b61c",
    "phoneNumber": "0932062322",
    "token": "03AL8dmw8psuscFZFB12ewQGzQjgaQphA3DI3BHsXy2J4Xb8QZBHab0RAV6luHE6yUW_IkWX2FBoSoEoh4xSsJ1V3IexmND5TrmDmKc2AACQkvGW8BeBVC1812qGz4TBOFzDBvcxZvkPLGelHrS7kw2Iknk0qeha30dihTkNn5XbKNj9S3MpZhRyXKweXwM-Rbz3zVIH0N4LCIX8uYJzwDf4GXFL4pJM5ddh0plKDMjYfctGHY2ts9empHsW-of-FA_2WTehd_M-Bm86Af8R9RVox4Y3ECEqhtz8YHudJqhvl2b1x498za7gwnGHON8TpnRBkLvYxqUxXvFl9MLmffsLhx83m0MR5szX3TLP6RJSnY3af5MWUrBval2otOo6gPMsqCuhynK0nVKcfyaOpqWEEqNeR_7bbA4D3eDcAX1rqQoJYhAp5wnSZlwXni7Ov_AJq2PthV4fF8xYazxapNwBKJV9128lHnw_zVn-39Z8jAawTNasTXl4C5izs5wuIXHX_tHvwzLgv7gUWq-61CkH1bFO49dYb25YhzrFvycOLuVuAh8Wqqub9rNA0Qror_ONEkF3jMSm3y3nY8v4WBzoubEeguGoCo0iSPwNlfBtYSMZSBLTK-hPHS81W1Hch9V4JIpYmXRpurCml1piUdqo4kLxZ-5kmEg5lBCt0ehFGwnV7wUS3KFNFtxPRTo2gHdT5M9M5QhRXkfVrguHWQ8ADSAx77CRcmwfak5f89AhWk5_paxP5ySEEHVyGvx8E5T04RPs8-nDVQ8CSKedr6PlOOxI3f_t1PYMOY19Im-ip3B1MX1tKYEQ5d3S78JfeO3YYTU56o8t5QfD1PDRj8bpYHskIty60JoM_GyoPb_oT2neCyujt0oA4i5si5JoYS6iVNhoueyutMkYsmhVFi_t9p0rgjlzrKGoEmqVFsKnLmQ1uKNtFa0TfPeg3nqgwT5-zO127lRVjkeq-6QYqJx5ipSP9TdfSLbui8ZSRBTgYBDBSpnPE7lyLnT5B9eK0c1DecPdC_wr_YjWMceFaVqRr42lVfL-hOxPZtnLgYn8XTeOgEf0u4yG688-k7ubyCVFUzMv2NcB5GCgX2r5X1T0F-ENcj7irvEc9r3f5VBUw6UOaXvrNBV3YnYokxhgFqxUYcXJL_tmDIM_Vrf5iFvuNSZYvAXnQv1srb4pnAUsYb0YXu38q37PNmK2_uNC_YNSA3cHj3P1EeALkf8Dcrn2hp9AHHHWOkkF1NgAHsiSL-lTmNGI0_y3mhjCayQKkWILQJrMWzWeA73jjJJxRYGYiWGdVFj5Va6G20ugPLaPDqfIbOs9gtuZrcRDe-PQ_AbjiRziBVs5HWMu0EWfeShOfkzKmf9Gsz-QC17um3SBDBKGaVENHncwuEBzrXlQVGlEH9Af95vZ7It-mxZ5WsppH9B0pHh4Tm9tuFT2THMjUgnq4t9SW8TShsTJ83vn3h5fYlBRcIZHX_"
}


def send_vote_request():
    data = {
        "action": "vote_candidate",
        "email": "travinhnguyenminh@gmail.com",
        "myVote[0][company]": "Công ty TNHH MTV Sàn Giao Dịch BĐS Nam Long",
        "myVote[0][id]": "304",
        "myVote[0][name]": "CEO TRẦN VĨ THÀNH",
        "myVote[0][permalink]": "https://vote.vars.vn/ung-cu-vien/ceo-tran-vi-thanh/",
        "myVote[0][thumbnail]": "https://vote.vars.vn/storage/2023/05/Tran-Vi-Thanh-1.webp",
        "myVote[0][votes]": "2482",
        "nonce": "5f7978b61c",
        "phoneNumber": "0932062322",
        "token": "03AL8dmw8psuscFZFB12ewQGzQjgaQphA3DI3BHsXy2J4Xb8QZBHab0RAV6luHE6yUW_IkWX2FBoSoEoh4xSsJ1V3IexmND5TrmDmKc2AACQkvGW8BeBVC1812qGz4TBOFzDBvcxZvkPLGelHrS7kw2Iknk0qeha30dihTkNn5XbKNj9S3MpZhRyXKweXwM-Rbz3zVIH0N4LCIX8uYJzwDf4GXFL4pJM5ddh0plKDMjYfctGHY2ts9empHsW-of-FA_2WTehd_M-Bm86Af8R9RVox4Y3ECEqhtz8YHudJqhvl2b1x498za7gwnGHON8TpnRBkLvYxqUxXvFl9MLmffsLhx83m0MR5szX3TLP6RJSnY3af5MWUrBval2otOo6gPMsqCuhynK0nVKcfyaOpqWEEqNeR_7bbA4D3eDcAX1rqQoJYhAp5wnSZlwXni7Ov_AJq2PthV4fF8xYazxapNwBKJV9128lHnw_zVn-39Z8jAawTNasTXl4C5izs5wuIXHX_tHvwzLgv7gUWq-61CkH1bFO49dYb25YhzrFvycOLuVuAh8Wqqub9rNA0Qror_ONEkF3jMSm3y3nY8v4WBzoubEeguGoCo0iSPwNlfBtYSMZSBLTK-hPHS81W1Hch9V4JIpYmXRpurCml1piUdqo4kLxZ-5kmEg5lBCt0ehFGwnV7wUS3KFNFtxPRTo2gHdT5M9M5QhRXkfVrguHWQ8ADSAx77CRcmwfak5f89AhWk5_paxP5ySEEHVyGvx8E5T04RPs8-nDVQ8CSKedr6PlOOxI3f_t1PYMOY19Im-ip3B1MX1tKYEQ5d3S78JfeO3YYTU56o8t5QfD1PDRj8bpYHskIty60JoM_GyoPb_oT2neCyujt0oA4i5si5JoYS6iVNhoueyutMkYsmhVFi_t9p0rgjlzrKGoEmqVFsKnLmQ1uKNtFa0TfPeg3nqgwT5-zO127lRVjkeq-6QYqJx5ipSP9TdfSLbui8ZSRBTgYBDBSpnPE7lyLnT5B9eK0c1DecPdC_wr_YjWMceFaVqRr42lVfL-hOxPZtnLgYn8XTeOgEf0u4yG688-k7ubyCVFUzMv2NcB5GCgX2r5X1T0F-ENcj7irvEc9r3f5VBUw6UOaXvrNBV3YnYokxhgFqxUYcXJL_tmDIM_Vrf5iFvuNSZYvAXnQv1srb4pnAUsYb0YXu38q37PNmK2_uNC_YNSA3cHj3P1EeALkf8Dcrn2hp9AHHHWOkkF1NgAHsiSL-lTmNGI0_y3mhjCayQKkWILQJrMWzWeA73jjJJxRYGYiWGdVFj5Va6G20ugPLaPDqfIbOs9gtuZrcRDe-PQ_AbjiRziBVs5HWMu0EWfeShOfkzKmf9Gsz-QC17um3SBDBKGaVENHncwuEBzrXlQVGlEH9Af95vZ7It-mxZ5WsppH9B0pHh4Tm9tuFT2THMjUgnq4t9SW8TShsTJ83vn3",
    }

    response = requests.post(url, headers=headers, data=data)
    print(response.ok)


while True:
    # Tạo đối tượng OpenvpnAPI và kết nối đến OpenVPN
    api = Openvnp_API()
    api.connect('http://localhost:7505')
    # Lấy thông tin về kết nối OpenVPN
    print(api.get_status())
    send_vote_request()
    time.sleep(10)
    # Ngắt kết nối OpenVPN
    api.disconnect()
