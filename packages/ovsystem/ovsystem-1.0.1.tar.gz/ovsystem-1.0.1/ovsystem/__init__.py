import socket, datetime, os, zlib, json
from firebase_admin import credentials, initialize_app, db
from dotenv import load_dotenv
from cryptography.fernet import Fernet
load_dotenv()

class OVSConnection():
    def __init__(self, encrypted_code, key):
        cipher = Fernet(key)
        decrypted_config = cipher.decrypt(encrypted_code).decode()
        self.encrypted_json_data = decrypted_config

        self.temp_file = "firebase_temp.json"
        self.create_temp_json_file()

    def create_temp_json_file(self):
        with open(self.temp_file, "w") as f: f.write(self.encrypted_json_data)

    def delete_temp_json_file(self):
        if os.path.exists(self.temp_file): os.remove(self.temp_file)

    def connect_to_firebase(self):
        try:
            self.create_temp_json_file()
            cred = credentials.Certificate(self.temp_file)
            initialize_app(cred, {'databaseURL': 'https://onlinevariablessystem-default-rtdb.europe-west1.firebasedatabase.app/'})
        except Exception as e: print(f"Hata: {e}")
        finally: self.delete_temp_json_file()

class OVS:
    def __init__(self, token):
        encrypted = b'gAAAAABnVBCwsb8SpkC3n2-5E_8E7gyVZK0554ywvPBDWUc47im-jxwiX_80G1bbVtN6TCYfdPvqZKSe_x9q4wce65LVo5vWkCwUC-ZUByegNyk2B-1eX0eNjZV_EEp_65SsEHY6CY_KdwVq_o290bfbO9AIIMAjgSFMOrQqBk-68U30EwNJHqUfY3lLEg_BaxsjG8_Xn1pA1dsL-clRVpWz7bLweREWJ-ueroWIcja9ZX6u_8f1BnD54ChdS40IvxrvYxKxnvQA_6n4zxq9NFaMqpQS1-pLHRuwY6sJEfdE219vhQDdBctmd83uEKZdEGUEJiDdZpyFRHFMa_V37fVsQpZHwKTCGMqvevo5vh-6ff4QYe54bOJb_Tg9_sIfa6QuAuUM5O4z9xVv_F9rH5eFpMij4w-3Sy463phWU-Abokc1BMYdWbVR60qE2y1MtpqGEhYC8lShKIsF-FQf4wOtDkgEd-VqQ-ZBlAqkiEOF46eOnGLPYl9Mi4zRM-sJokr9tqWp76wn21-ZQDtg7AgSvBC5BN7QLfd7y-Ate7llqXcaDvtDPApc829wqQ9O_-L50DElEswF6EPsjwa73QT-WNvrAcoU4egGXY9ZqVCsgZkSu5zCj_zLE2ejpMpNSgX6REzISWUlLP15snnh5ouLwq2glJqsF2jiMNam7-xZn3C-4UeJ67zl0tRT8pHSXLYjKOCH7YxYu-VtqGTARlssZ8FaEPZoPAQtpFbaTkOEkUUIciMWDQ8n0GqKJQzSbyrc59WlA-OlssVIYvJc5iR37-4tEiazUtU6_MM8Gnp5tVGblC7HKMp0_AQNB34q2r4jsaiTcFgbL-OYke0jYvjHdCIghNIZItGv95M4XwEGuvw9jI0Lj2Ra0VQARDE-CdsMejKjPkowOkLB15e7FNZKCczlAbZkzv216jp1kVtxY0yTH0JZcQq9sjnq-5xS5DcFnhwdjGwhusexaST1BWtYEJnrRAvr4mdWS1Z3sxZd7vrjTh1iouCWsSebUMqeuiFa9zRk1iAKgcnQFyJ32RQUt8aTYuciDTge27P4I5Up5rwIpJn7-BScWX3gkWbbKAXPDRZw8Xidpg7Mvryfs3m5uQrQRIjXSp3-4htLBmO6IEEDMQhIRk_ZrSzZs9XqzOEx6n-GqTLBFF2UjoHTmRnckMPKXWFuS9ZldvDhiA3xQxUu_VR7jSsbkBKtXyKTvnAumoxNydDxAfwXWgbxYNR5FZy5uxfvYWShpjgMssPk5YHR3MY-lhzUgt07Pc3qM_BLu0YBGGVxNObOtV0mBtj3J4es3ijOqWjW3eOQbWLN-uans_prlyhgi-fRR0RqL5UKOXb_DaekjX6tlfkHZtiYjj0NXxeMPgV8rwHlVNcn4roDE9FIC1avhK2PU76AKIOd_7eT3eUi6dijwHEYlX7c4xmKtlVQOtJwWAdff1bQALJX7wKfPiZIPaV8etm_ZasV9ur71GQyo_flZwekkkNGDOOS8E-BGQjbXOv2Fo6qoSxLw2QpdhYQTSYQtxRLR1T4W4CVp57Sw13lKOx2aFYufLpO_ekmHzqCepUJ6DbiKyouH8nPPNw2pZTJHHgoeQX5Y0UyWcG0PaCgyoTEAJs1TTlRKSqmTewyhnjNOH-aZrWIlFCGwb7YVXZaQulDnouvKTBdczCr_Bj8AJpxqPk1jgYMNks_IFepghEoKneYqaMn7WhnTE_sl4zh7eeEy4rhRwakHOdpAnRYzE0aLPVmtUxmmnrOVkOiW66eTfRYJLMeHhfNLfOm7ixnRkxI9uD2lRKhXWZbaipZ5qsxb3NQFiVrxVPtE2duB9WU3Wvl0dtlkhraKO9moqQn-_53US_dKDK3vG2Jf1YYK8pL5MbrEiqRV07mjQfDSINjGWCZ85fk-iDNsklXNxrtcPvzzjemwHso08K-J1QdyDn43jdYsPptUq1mXYwLxeOTLd8Aeq2TH33yYjqc4ap8wlOikHgFr0XqAnAspQ7NyRRzJxjdL3q5i7GU6BtXoCb328r9Ys7yEvG9KuZ7NhjC_7Sb_cxRtQ4J6wNZz5q4ufzMSCijn10UHL-oDKNAY-edjS3kqHPoHoamYXWApAGrfUa0t-O74oHMu6lVbTYRWAanXzJIZBW3azW_d8r_03wpAEqykcASYX9pvmH4acoCB8UQIqqPgRrhxPX-sRevgsG190bM2BTqTEtQFN3u0L69agz8KHiHFBNV4LRsE5wxeOA48sZdF41VyynDEIZt2AjCta5azt3XtGpAuOZsl60VbcVabnnViBaM12C7fPfhQiSSHQpS47mwye8JX41JhrlhzO0j1SCpwHUs_jXdRYuzABSL-fjoTKF_PoOAoggd9RxNKJzi0QwqSiOgLQ1L46CcPlDdCnoPChqNMJjl2MeuEmfbqdM61eOwfd5iHty5jFO5zXhnjmDzea5HvgdamfA7XHyz-JSpgnoOJY7R4ElTr7lm21wG2D377IV_NblNwLEgXIH-3bd21Nh0nD44SgK51940w0dFBQDpF5o30RPtPdgmshqTISJZcgK38XKrdveHljq_ZRYie5AwYBHpW_fqQL1xxdZisoOBrOjRB6MZhQdHOq_P8MvqACrM_EhBIxQ0v6WGpgYLhGhhg94kd1k4_FUUE6WMO9KiZzHHGpX9-WvUdIe7QHhfcifaA6bokClNRyhoX3bGpebw9RjiCa_kql-J2C-LoaQk3CCE9BEmEl0afmi82a7ydwe_ceymFF-RqSz6ZERWXfJyECxrT-1ixN-7CnPLbohWaFoqkyFZIwVUYJOK0a16hjRsKljikZL8nyUHZx6t1s21ltRObJy60CH_xYIvg7qHA6jJfkUvOQsHoJkxVYCfQ7tW2ft1wyxE_rbr5_PophCmUzvkTkOB_VjtHuLHyvC3ymr2iUz7NCFbG5DhDNfuEpB-4lVnlq4p1bNi8n6hKhkMtiNCieAIh6ua8mG8XDrVHNBJ4xsUMq_smVbeq36K47vGU9YYx36pJvZR57Yk0_CoCRnXOjoba2eVmeZ-As6wgnOmLtXqhBJ3HT5_CnzKz4SvfLpR7x62SJWxTBp5GDLDHP-NGkje_JCsBnFQbsY08vGGSXPruDvpa2dCaSoyIIH0bZDoaB6ZMCSVVAMT6TLgbNw9TIjtU0FvJ3h11fFPPa5fc0JAi6M41QpyuoMm7IGcU02DOG6mCE1_olnqqe27voeMybxy8ruGJOZlmNWKECngYZ6pLRzGRGJ3nxSHmoKyqv9QP05CQj04McYUxhukMDZMgqrqiZHxP8MlTciJEA=='
        key_ = b'F7a49gAS4oZ5AXlqB-PhYYlvTXuomYijzgRQeuAoUCY='
        self.connection = OVSConnection(encrypted_code=encrypted, key=key_)
        self.connection.connect_to_firebase()
        self.token = token

    def get(self, key):
        try: 
            for key, value in db.reference("tokens").get().items():
                if key == self.token:
                    self.tokens = db.reference("tokens").child(self.token)
                    self.vars = self.tokens.child("variables")
                    data = self.tokens.child("variables").child(key).child("value").get()
                    if data is not None: return data
                    else: raise ValueError(f"{key}, is not a variable.")
                else:
                    raise ValueError(f"{self.token}, is not a valid token.")
        except: ...
    def set(self, key, value):
        try: 
            for key, value in db.reference("tokens").get().items():
                if key == self.token:
                    self.tokens = db.reference("tokens").child(self.token)
                    self.vars = self.tokens.child("variables")
                    self.vars.update({key: {f"value": value, f"creationDate": datetime.datetime.now().strftime("%m/%d/%Y"), f"creationTime": datetime.datetime.now().strftime("%H:%M:%S"), "creator": socket.gethostname(), "creatorIP": socket.gethostbyname(socket.gethostname())}})
                else:
                    raise ValueError(f"{self.token}, is not a valid token.")
        except: ... 
    def getAll(self):
        try: 
            for key, value in db.reference("tokens").get().items():
                if key == self.token:
                    self.tokens = db.reference("tokens").child(self.token)
                    self.vars = self.tokens.child("variables")
                    return self.tokens.child("variables").get()
                else:
                    raise ValueError(f"{self.token}, is not a valid token.")
        except: ...

    def _generate_token(self):
        try:
            self.tokens = db.reference("tokens")
            self.tokens.update({self.token: {"creatorIP": socket.gethostbyname(socket.gethostname())}})
            return True
        except : return False

if __name__ == "__main__":
    ovs = OVS("yourToken")
    ovs.set("jack", "its jack name")
    print(ovs.get("jack"))