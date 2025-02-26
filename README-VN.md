# Tập lệnh tự động hóa Monad Testnet

Kho lưu trữ này chứa một bộ sưu tập các tập lệnh Python được thiết kế để tự động hóa nhiều tác vụ trên Monad Testnet, bao gồm staking, hoán đổi, triển khai hợp đồng và gửi giao dịch. Các tập lệnh được tích hợp với một tệp `main.py` trung tâm để dễ dàng điều hướng và thực thi, hỗ trợ nhiều khóa riêng và giao diện CLI thân thiện với người dùng.

## Tổng quan về tính năng

### Tính năng chung
- **Hỗ trợ nhiều tài khoản**: Đọc khóa riêng từ `pvkey.txt` để thực hiện các hành động trên nhiều tài khoản.
- **CLI đầy màu sắc**: Sử dụng `colorama` để tạo đầu ra hấp dẫn với văn bản có màu và viền.
- **Thực thi bất đồng bộ**: Được xây dựng với `asyncio` để tương tác hiệu quả với blockchain (nếu áp dụng).
- **Xử lý lỗi**: Bắt lỗi toàn diện cho các giao dịch blockchain và các vấn đề RPC.

### 1. `main.py` - Menu chính
- **Mô tả**: Đóng vai trò là trung tâm để chọn và chạy các tập lệnh khác.
- **Tính năng**:
  - Menu tương tác với tùy chọn chọn ngôn ngữ (Tiếng Việt/Tiếng Anh).
  - Hỗ trợ chạy nhiều tập lệnh (`kitsu.py`, `bean.py`, `uniswap.py`, `deploy.py`, `sendtx.py`, `ambient.py`, `rubic.py`, `mono.py`, `apriori.py`, `bebop.py`, `izumi.py`, `magma.py`).
  - Giao diện console gọn gàng với các biểu ngữ và viền đầy màu sắc.
- **Cách dùng**: Chạy `python main.py` và chọn một tập lệnh từ menu.

### 2. `kitsu.py` - Staking Kitsu
- **Mô tả**: Tự động hóa staking và unstaking token MON trên hợp đồng Kitsu Staking.
- **Tính năng**:
  - Hỗ trợ nhiều khóa riêng từ `pvkey.txt`.
  - Số lượng staking ngẫu nhiên (0.01-0.05 MON).
  - Độ trễ ngẫu nhiên (1-3 phút) giữa các hành động.
  - Chu kỳ stake và unstake với nhật ký giao dịch chi tiết.
  - Đầu ra song ngữ (Tiếng Việt/Tiếng Anh).
- **Cách dùng**: Chọn từ menu `main.py`, nhập số chu kỳ.

### 3. `bean.py` - Hoán đổi Bean
- **Mô tả**: Tự động hóa hoán đổi giữa MON và các token (USDC, USDT, BEAN, JAI) trên Bean Swap.
- **Tính năng**:
  - Hỗ trợ nhiều khóa riêng từ `pvkey.txt`.
  - Hoán đổi ngẫu nhiên (MON → Token hoặc Token → MON).
  - Chu kỳ có thể cấu hình và độ trễ ngẫu nhiên (1-3 phút).
  - Kiểm tra số dư trước và sau khi hoán đổi.
  - Nhật ký giao dịch chi tiết với Tx Hash và liên kết explorer.
- **Cách dùng**: Chọn từ menu `main.py`, nhập số chu kỳ.

### 4. `uniswap.py` - Hoán đổi Uniswap
- **Mô tả**: Tự động hóa hoán đổi giữa MON và các token (DAC, USDT, WETH, MUK, USDC, CHOG) trên Uniswap V2.
- **Tính năng**:
  - Hỗ trợ nhiều khóa riêng từ `pvkey.txt`.
  - Hoán đổi ngẫu nhiên (MON → Token hoặc Token → MON).
  - Chu kỳ có thể cấu hình và độ trễ ngẫu nhiên (1-3 phút).
  - Kiểm tra số dư trước và sau khi hoán đổi.
  - Nhật ký giao dịch chi tiết với Tx Hash và liên kết explorer.
- **Cách dùng**: Chọn từ menu `main.py`, nhập số chu kỳ.

### 5. `deploy.py` - Triển khai hợp đồng
- **Mô tả**: Triển khai một hợp đồng Counter đơn giản lên Monad Testnet.
- **Tính năng**:
  - Hỗ trợ nhiều khóa riêng từ `pvkey.txt`.
  - Người dùng nhập tên và ký hiệu hợp đồng (ví dụ: "Thog Token", "THOG").
  - Chu kỳ triển khai có thể cấu hình với độ trễ ngẫu nhiên (4-6 giây).
  - Hiển thị địa chỉ hợp đồng và Tx Hash sau khi triển khai.
  - Đầu ra song ngữ (Tiếng Việt/Tiếng Anh).
- **Cách dùng**: Chọn từ menu `main.py`, nhập số chu kỳ, sau đó nhập tên và ký hiệu cho mỗi lần triển khai.

### 6. `sendtx.py` - Gửi giao dịch
- **Mô tả**: Gửi giao dịch MON đến các địa chỉ ngẫu nhiên hoặc từ một tệp.
- **Tính năng**:
  - Hỗ trợ nhiều khóa riêng từ `pvkey.txt`.
  - Hai chế độ:
    - Gửi đến địa chỉ ngẫu nhiên (số lượng giao dịch do người dùng định nghĩa).
    - Gửi đến địa chỉ từ `address.txt`.
  - Số lượng MON có thể cấu hình (mặc định 0.000001, tối đa 999).
  - Độ trễ ngẫu nhiên (1-3 giây) giữa các giao dịch.
  - Nhật ký chi tiết bao gồm người gửi, người nhận, số lượng, gas, khối và số dư.
- **Cách dùng**: Chọn từ menu `main.py`, nhập số lượng giao dịch, số lượng MON và chế độ.

### 7. `ambient.py` - Bot hoán đổi Ambient
- **Mô tả**: Tự động hóa hoán đổi token trên Ambient DEX.
- **Tính năng**:
  - Hoán đổi ngẫu nhiên: Thực hiện hoán đổi ngẫu nhiên giữa USDC, USDT và WETH với số lượng tùy chỉnh.
  - Hoán đổi thủ công: Cho phép người dùng chọn token nguồn/đích và nhập số lượng.
  - Kiểm tra số dư: Hiển thị số dư MON và token (USDC, USDT, WETH).
  - Cơ chế thử lại: Thử lại giao dịch thất bại tối đa 3 lần với độ trễ 5 giây cho lỗi RPC.
  - Thời hạn mở rộng: Giao dịch hoán đổi có thời hạn 1 giờ để tránh lỗi "Swap Deadline".
  - Menu tương tác: Cung cấp menu CLI để chọn giữa Hoán đổi ngẫu nhiên, Hoán đổi thủ công hoặc Thoát.
- **Cách dùng**: Chọn từ menu `main.py`, chọn chế độ Ngẫu nhiên/Thủ công và làm theo hướng dẫn.

### 8. `rubic.py` - Tập lệnh hoán đổi Rubic
- **Mô tả**: Tự động hóa hoán đổi MON sang USDT qua router Rubic.
- **Tính năng**:
  - Hỗ trợ nhiều khóa riêng từ `pvkey.txt`.
  - Chu kỳ hoán đổi có thể cấu hình với số lượng ngẫu nhiên (0.01 MON).
  - Độ trễ ngẫu nhiên (1-3 phút) giữa các chu kỳ và tài khoản.
  - Theo dõi giao dịch với Tx Hash và liên kết explorer.
- **Cách dùng**: Chọn từ menu `main.py`, nhập số chu kỳ.

### 9. `mono.py` - Tập lệnh giao dịch Monorail
- **Mô tả**: Gửi các giao dịch được xác định trước đến hợp đồng Monorail.
- **Tính năng**:
  - Hỗ trợ nhiều khóa riêng từ `pvkey.txt`.
  - Gửi giao dịch 0.1 MON với dữ liệu tùy chỉnh.
  - Ước lượng gas: Quay về 500,000 nếu ước lượng thất bại.
  - Liên kết Explorer: Cung cấp liên kết giao dịch để theo dõi.
  - Độ trễ ngẫu nhiên (1-3 phút) giữa các tài khoản.
- **Cách dùng**: Chọn từ menu `main.py`, chạy tự động cho tất cả tài khoản.

### 10. `apriori.py` - Staking Apriori
- **Mô tả**: Tự động hóa staking, unstaking và claiming MON trên hợp đồng Apriori Staking.
- **Tính năng**:
  - Hỗ trợ nhiều khóa riêng từ `pvkey.txt`.
  - Số lượng staking ngẫu nhiên (0.01-0.05 MON).
  - Chu kỳ có thể cấu hình với độ trễ ngẫu nhiên (1-3 phút) giữa các hành động.
  - Trình tự Stake → Unstake → Claim với kiểm tra trạng thái claimable qua API.
  - Nhật ký giao dịch chi tiết với Tx Hash và liên kết explorer.
  - Đầu ra song ngữ (Tiếng Việt/Tiếng Anh).
- **Cách dùng**: Chọn từ menu `main.py`, nhập số chu kỳ.

### 11. `bebop.py` - Tập lệnh Wrap/Unwrap Bebop (Đồng bộ)
- **Mô tả**: Wrap MON thành WMON và unwrap WMON về MON qua hợp đồng Bebop (phiên bản đồng bộ).
- **Tính năng**:
  - Hỗ trợ nhiều khóa riêng từ `pvkey.txt`.
  - Số lượng MON do người dùng định nghĩa (0.01-0.05) để wrap/unwrap.
  - Chu kỳ có thể cấu hình với độ trễ ngẫu nhiên (1-3 phút).
  - Theo dõi giao dịch với Tx Hash và liên kết explorer.
  - Đầu ra song ngữ (Tiếng Việt/Tiếng Anh).
- **Cách dùng**: Chọn từ menu `main.py`, nhập số chu kỳ và số lượng MON.

### 12. `izumi.py` - Tập lệnh Wrap/Unwrap Izumi (Bất đồng bộ)
- **Mô tả**: Wrap MON thành WMON và unwrap WMON về MON qua hợp đồng Izumi (phiên bản bất đồng bộ).
- **Tính năng**:
  - Hỗ trợ nhiều khóa riêng từ `pvkey.txt`.
  - Số lượng wrap/unwrap ngẫu nhiên (0.01-0.05 MON).
  - Chu kỳ có thể cấu hình với độ trễ ngẫu nhiên (1-3 phút).
  - Theo dõi giao dịch với Tx Hash và liên kết explorer.
  - Đầu ra song ngữ (Tiếng Việt/Tiếng Anh).
- **Cách dùng**: Chọn từ menu `main.py`, nhập số chu kỳ.

### 13. `magma.py` - Staking Magma
- **Mô tả**: Tự động hóa staking MON và unstaking gMON trên hợp đồng Magma.
- **Tính năng**:
  - Hỗ trợ nhiều khóa riêng từ `pvkey.txt`.
  - Số lượng staking ngẫu nhiên (0.01-0.05 MON).
  - Chu kỳ có thể cấu hình với độ trễ ngẫu nhiên (1-3 phút) giữa stake/unstake.
  - Theo dõi giao dịch với Tx Hash và liên kết explorer.
  - Đầu ra song ngữ (Tiếng Việt/Tiếng Anh).
- **Cách dùng**: Chọn từ menu `main.py`, nhập số chu kỳ.

## Hướng dẫn cài đặt:

- **Phiên bản Python**: Python 3.7 trở lên (khuyến nghị 3.9 hoặc 3.10 do sử dụng `asyncio`).
- **Công cụ cài đặt**: `pip` (trình cài đặt gói Python).

## Cài đặt
1. **Sao chép kho lưu trữ**:
- Mở CMD hoặc Shell, sau đó chạy lệnh:
```sh
git clone https://github.com/thog9/Monad-testnet.git
```sh
cd Monad-testnet
```
2. **Cài đặt Module:**
- Mở cmd hoặc Shell, sau đó chạy lệnh:
```sh
pip install -r requirements.txt
```
3. **Prepare Input Files:**
- Mở `pvkey.txt`: Thêm khóa riêng của bạn (mỗi dòng một khóa) vào thư mục gốc.
```sh
nano pvkey.txt
```
- Mở `address.txt`(tùy chọn): Thêm địa chỉ người nhận (mỗi dòng một khóa) cho `sendtx.py`.
```sh
nano address.txt
```
4. **Chạy:**
- Mở cmd hoặc Shell, sau đó chạy lệnh:
```sh
python main.py
```
- Chọn ngôn ngữ (Tiếng Việt/Tiếng Anh).

## Khắc phục sự cố:

- **Connection Errors**: Ensure `pvkey.txt` exists and contains valid private keys. Check internet connectivity and RPC URL responsiveness (`https://testnet-rpc.monad.xyz/`).

- **Library Errors**: Verify all required libraries are installed (`pip list`).
  
- **Transaction Failures**: Check Tx Hash on Monad Testnet Explorer for detailed error messages (e.g., "Swap Deadline", insufficient balance).

- **API Errors in `apriori.py`**: Ensure the API endpoint `https://liquid-staking-backend-prod-b332fbe9ccfe.herokuapp.com/` is accessible.

## File Structure:
```
├── main.py           # Tập lệnh menu chính
├── scripts/          # Thư mục chứa tất cả các tập lệnh tự động hóa
│   ├── kitsu.py      # Tự động hóa staking Kitsu
│   ├── bean.py       # Tự động hóa hoán đổi Bean
│   ├── uniswap.py    # Tự động hóa hoán đổi Uniswap
│   ├── deploy.py     # Tự động hóa triển khai hợp đồng
│   ├── sendtx.py     # Tự động hóa gửi giao dịch
│   ├── ambient.py    # Tự động hóa hoán đổi Ambient
│   ├── rubic.py      # Tự động hóa hoán đổi Rubic
│   ├── mono.py       # Tự động hóa giao dịch Monorail
│   ├── apriori.py    # Tự động hóa staking Apriori
│   ├── bebop.py      # Tự động hóa wrap/unwrap Bebop (đồng bộ)
│   ├── izumi.py      # Tự động hóa wrap/unwrap Izumi (bất đồng bộ)
│   ├── magma.py      # Tự động hóa staking Magma
├── pvkey.txt         # Tệp chứa khóa riêng (tạo thủ công)
├── address.txt       # Tệp chứa địa chỉ người nhận (tùy chọn cho sendtx.py)
└── README.md         # +_-
```
