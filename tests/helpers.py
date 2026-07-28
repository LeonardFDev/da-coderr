def status_code_with_message(self, response):
    with open("test_protocol.log", "a", encoding="utf-8") as f:
        f.write("\n")
        f.write("-" * 160 + "\n")
        f.write(f"Test: {self._testMethodName}\n")
        is_it_successful(self, response, f)
        f.write(f"Status: {response.status_code}\n")
        f.write(f"Response: {response.data}\n")
        f.write("-" * 160 + "\n")

def is_it_successful(self, response, f):
    method_name_number = self._testMethodName.split("_")[-1]
    code = int(method_name_number) if method_name_number.isdecimal() else None

    if code == None:
        f.write(f"Integer not found, or in the wrong position 🟠\n")

    elif code == response.status_code:
        f.write(f"Test successful: Yes 🟢\n")

    elif code != response.status_code and code != None:
        f.write(f"Test successful: No 🔴\n")