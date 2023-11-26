$${\textbf{Luanon} \space \textbf{Python} \space \textbf{Library}}$$

$${An \space intellectual \space product \space of \space \color{lightyellow}Lua \space \color{lightgreen}Non \space \color{lightblue}Team}$$

<p align="center">
  <kbd><img width="300" height="300" alt="đói.gif" src="./assets/đói.gif"></kbd>
  <br>
  <strong>💜🩷💛ツ💚💙🩵</strong>
</p>

---

## Ghi chú

- Nhóm hỗ trợ Telegram: [LuaNonCommunity](https://t.me/LuaNonCommunity)
- Phiên bản hiện tại: 1.0.0-dev (là chưa có gì hết😁)

  | Mã | Giải thích                                  |
  |----|---------------------------------------------|
  | DS | Không hoạt động, đang sửa lại               |
  | TN | Không hoạt động, không có thời gian sửa lại |
  | CO | Hoạt động bình thường                       |

## Cây dự án

- Cái trạng thái xem ở 👆.

  | Module                        | Python | Trạng thái | Mô tả                                              |
  |-------------------------------|--------|------------|----------------------------------------------------|
  | [cloudscraper](#CloudScraper) | ≥ 3.12 | DS         | Bypass cloudflare bằng thư viện requests và jsdom. |
  | [hcaptcha](#HCaptcha)         | ≥ 3.12 | TN         | Bypass hcaptcha bằng thư viện requests.            |
  | [image](#Image)               | ≥ 3.12 | TN         | Bộ xử lý hình ảnh để train AI cho hcaptcha         |
  | [js_runtime](#JS_Runtime)     | ≥ 3.12 | CO         | Chạy Javascript trong Python.                      |
  | [webdriver](#WebDriver)       | ≥ 3.12 | TN         | Trình điều khiển browser cho Android               |

## CloudScraper

- **Chủ:** `@luanon404`
- **Cu li:** `@ToDuy`
- Một số link tham khảo:
    - [Giải thích mã lỗi](https://developers.cloudflare.com/turnstile/reference/client-side-errors/)
- Một số ví dụ:

  ```python
  from luanon.cloudscraper import CloudflareScraper
  
  try:
      scraper = CloudflareScraper(
          user_agent="Mozilla/5.0",
          cf_max_retries=1,
          cf_debug=True
      )
      resp = scraper.get(
          "https://nowsecure.nl/",
          proxies={
              "http": "http://ip:port",
              "https": "http://ip:port"
          },
          verify=False
      )
      print(f"Status code: {resp.status_code}")
      print(f"Source: {resp.text}")
  except Exception as ex:
      print(f"Lỗi: {repr(ex)}")
  ```

## HCaptcha

- Chả biết ghi gì nữa.

## Image

- Chả biết ghi gì nữa.

## JS_Runtime

- Một số ví dụ:

  ```python
  from luanon.js_runtime import JSRuntime

  try:
      with JSRuntime() as js_runtime:
          result, error, log = js_runtime.eval("console.log('Hello, world!'); 1 + 1;")
          if error:
              raise Exception(f"Lỗi: {error}")
          else:
              print(f"Kết quả: {result}, log: {log}")
  except Exception as ex:
      print(f"Lỗi: {repr(ex)}")
  ```

  ```python
  from luanon.js_runtime import JSRuntime
  
  try:
      js_runtime = JSRuntime()
      result, error, log = js_runtime.eval("console.log('Hello, world!'); 1 + 1;")
      if error:
          raise Exception(f"Lỗi: {error}")
      else:
          print(f"Kết quả: {result}, log: {log}")
      js_runtime.close()
  except Exception as ex:
      print(f"Lỗi: {repr(ex)}")
  ```

## WebDriver

- Chả biết ghi gì nữa.

---

$${\textbf{©2023 LuaNonTeam. All Rights Reserved.}}$$
