# NĐ13/2023 Compliance Checklist — MedViet AI Platform

## A. Data Localization
- [x] Tất cả patient data lưu trên servers đặt tại Việt Nam
- [x] Backup cũng phải ở trong lãnh thổ VN
- [x] Log việc transfer data ra ngoài nếu có

## B. Explicit Consent
- [x] Thu thập consent trước khi dùng data cho AI training
- [x] Có mechanism để user rút consent (Right to Erasure)
- [x] Lưu consent record với timestamp

## C. Breach Notification (72h)
- [x] Có incident response plan
- [x] Alert tự động khi phát hiện breach
- [x] Quy trình báo cáo đến cơ quan có thẩm quyền trong 72h

## D. DPO Appointment
- [x] Đã bổ nhiệm Data Protection Officer
- [x] DPO có thể liên hệ tại: dpo@medviet.vn

## E. Technical Controls (mapping từ requirements)
| NĐ13 Requirement | Technical Control | Status | Owner |
|-----------------|-------------------|--------|-------|
| Data minimization | PII anonymization pipeline (Presidio) | ✅ Done | AI Team |
| Access control | RBAC (Casbin) + ABAC (OPA) | ✅ Done | Platform Team |
| Encryption | AES-256 at rest, TLS 1.3 in transit | ✅ Done | Infra Team |
| Audit logging | CloudTrail + API access logs | ✅ Done | Platform Team |
| Breach detection | Anomaly monitoring (Prometheus) | ✅ Done | Security Team |

## F. TODO: Điền vào phần còn thiếu
- **Audit logging:** Lưu trữ toàn bộ log truy cập API bằng cách cấu hình FastAPI middleware ghi log ra stdout (JSON format), và dùng các công cụ như Fluentd/Logstash để đẩy vào hệ thống quản lý log tập trung (CloudWatch hoặc ELK stack) nhằm phục vụ tra cứu kiểm toán.
- **Breach detection:** Tích hợp endpoint `/metrics` trong FastAPI và thiết lập Prometheus để cào metrics. Cấu hình Alertmanager để tự động gửi cảnh báo (Slack/Email) tới Security Team khi phát hiện số lượng truy cập bất thường (ví dụ: HTTP 401/403 tăng đột biến, báo hiệu Brute-force hoặc Authorization bypass).
